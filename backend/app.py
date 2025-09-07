from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove, new_session
from PIL import Image, ImageEnhance
import io
import cv2
import numpy as np
import os
import functools

app = Flask(__name__)
CORS(app)

# Initialize rembg session once
session = new_session()

# Cache for processed images
cache = {}

def optimize_image_size(image_data, max_size=1500):
    """Optimize image size before processing"""
    image = Image.open(io.BytesIO(image_data))
    
    # Calculate new size while maintaining aspect ratio
    ratio = min(max_size / max(image.size[0], image.size[1]), 1.0)
    if ratio < 1.0:
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert back to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format or 'PNG')
        return img_byte_arr.getvalue()
    
    return image_data

@functools.lru_cache(maxsize=20)
def remove_background(image_hash):
    """Cached background removal"""
    if image_hash in cache:
        return cache[image_hash]
    return None

@app.route('/')
def home():
    """Health check and API information endpoint"""
    return jsonify({
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'remove_bg': '/remove-bg',
            'enhance': '/enhance-bg-removed',
            'enhance_original': '/enhance-only',
            'add_color_bg': '/add-color-background'
        }
    })

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f'Server error: {str(e)}')
    return jsonify({
        'error': 'Internal server error',
        'message': str(e)
    }), 500

@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        'error': 'Bad request',
        'message': str(e)
    }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def enhance_image(pil_image):
    """Simple image enhancement using OpenCV and PIL - preserves transparency"""
    # Check if image has transparency
    has_transparency = pil_image.mode in ('RGBA', 'LA') or 'transparency' in pil_image.info
    
    if has_transparency:
        # Handle RGBA images (with transparency)
        rgba_array = np.array(pil_image)
        rgb_array = rgba_array[:, :, :3]  # RGB channels
        alpha_array = rgba_array[:, :, 3]  # Alpha channel
        
        # Convert RGB to OpenCV format
        opencv_image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
        
        # Resize image (2x upscaling)
        height, width = opencv_image.shape[:2]
        upscaled = cv2.resize(opencv_image, (width*2, height*2), interpolation=cv2.INTER_CUBIC)
        upscaled_alpha = cv2.resize(alpha_array, (width*2, height*2), interpolation=cv2.INTER_CUBIC)
        
        # Apply sharpening filter only to RGB channels
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(upscaled, -1, kernel)
        
        # Convert back to PIL with alpha
        enhanced_rgb = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
        enhanced_rgba = np.dstack((enhanced_rgb, upscaled_alpha))
        enhanced_pil = Image.fromarray(enhanced_rgba, 'RGBA')
        
        # Enhance contrast and sharpness (PIL preserves alpha)
        enhancer = ImageEnhance.Contrast(enhanced_pil)
        enhanced_pil = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Sharpness(enhanced_pil)
        enhanced_pil = enhancer.enhance(1.1)
        
        return enhanced_pil
    
    else:
        # Handle regular RGB images (no transparency)
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Resize image (2x upscaling)
        height, width = opencv_image.shape[:2]
        upscaled = cv2.resize(opencv_image, (width*2, height*2), interpolation=cv2.INTER_CUBIC)
        
        # Apply sharpening filter
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(upscaled, -1, kernel)
        
        # Convert back to PIL
        enhanced_pil = Image.fromarray(cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB))
        
        # Enhance contrast and sharpness
        enhancer = ImageEnhance.Contrast(enhanced_pil)
        enhanced_pil = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Sharpness(enhanced_pil)
        enhanced_pil = enhancer.enhance(1.1)
        
        return enhanced_pil

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            app.logger.error('No image file in request')
            return 'No image uploaded', 400

        file = request.files['image']
        app.logger.info(f'Processing image: {file.filename}')
        
        # Read and optimize input image
        input_data = file.read()
        optimized_data = optimize_image_size(input_data)
        app.logger.info('Image optimized successfully')
        
        # Generate a hash of the image data for caching
        image_hash = hash(optimized_data)
        
        # Check cache first
        cached_result = remove_background(image_hash)
        if cached_result:
            app.logger.info('Using cached result')
            return send_file(io.BytesIO(cached_result), mimetype='image/png', 
                           as_attachment=False, download_name='no-bg.png')
        
        # Process the image with the global session
        output_data = remove(optimized_data, session=session)
        app.logger.info('Background removal completed')
        
        # Cache the result
        cache[image_hash] = output_data
        
        return send_file(io.BytesIO(output_data), mimetype='image/png', 
                        as_attachment=False, download_name='no-bg.png')
    except Exception as e:
        app.logger.error(f'Error in background removal: {str(e)}')
        return f'Error processing image: {str(e)}', 500

@app.route('/remove-and-upscale', methods=['POST'])
def remove_and_upscale():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    input_data = file.read()

    # Step 1: Remove background
    no_bg_data = remove(input_data)
    no_bg_image = Image.open(io.BytesIO(no_bg_data)).convert("RGBA")

    # Step 2: Enhance image using our custom function
    enhanced_image = enhance_image(no_bg_image)

    # Step 3: Return the image
    output_io = io.BytesIO()
    enhanced_image.save(output_io, format='PNG')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/png', as_attachment=False, download_name='enhanced.png')

@app.route('/enhance-only', methods=['POST'])
def enhance_only():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    input_data = file.read()

    # Step 1: Open the original image (no background removal)
    original_image = Image.open(io.BytesIO(input_data)).convert("RGB")

    # Step 2: Enhance image using our custom function
    enhanced_image = enhance_image(original_image)

    # Step 3: Return the image
    output_io = io.BytesIO()
    enhanced_image.save(output_io, format='PNG')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/png', as_attachment=False, download_name='enhanced.png')

@app.route('/enhance-bg-removed', methods=['POST'])
def enhance_bg_removed():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    input_data = file.read()

    # Step 1: Open the background-removed image (already processed)
    bg_removed_image = Image.open(io.BytesIO(input_data)).convert("RGBA")

    # Step 2: Enhance the background-removed image
    enhanced_image = enhance_image(bg_removed_image)

    # Step 3: Return the enhanced image
    output_io = io.BytesIO()
    enhanced_image.save(output_io, format='PNG')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/png', as_attachment=False, download_name='enhanced-no-bg.png')

@app.route('/add-color-background', methods=['POST'])
def add_color_background():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    input_data = file.read()
    
    # Get the color from the form data
    color = request.form.get('color', '#ffffff')  # Default to white if no color provided
    
    # Convert hex color to RGB
    color = color.lstrip('#')
    rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    # Step 1: Open the background-removed image
    bg_removed_image = Image.open(io.BytesIO(input_data)).convert("RGBA")
    
    # Step 2: Create a new image with the selected background color
    width, height = bg_removed_image.size
    colored_bg = Image.new('RGBA', (width, height), rgb_color + (255,))
    
    # Step 3: Composite the images (background-removed image on top of colored background)
    final_image = Image.alpha_composite(colored_bg, bg_removed_image)
    
    # Convert to RGB for final output (removes alpha channel)
    final_image = final_image.convert('RGB')

    # Step 4: Return the image
    output_io = io.BytesIO()
    final_image.save(output_io, format='PNG')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/png', as_attachment=False, download_name='colored-bg.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    
