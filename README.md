# ImgWizard

ImgWizard is a powerful web-based image processing tool that provides background removal, image enhancement, and background color customization features.

## Features

- 🎨 Background Removal
- ✨ Image Enhancement
- 🖌️ Custom Background Colors
- 📱 Responsive Design
- ⚡ Fast Processing
- 🔒 Secure File Handling

## Tech Stack

- Frontend: HTML5, CSS3, JavaScript (Vanilla)
- Backend: Python, Flask
- Image Processing: rembg, OpenCV, Pillow
- Deployment: Render (Backend), GitHub Pages (Frontend)

## Setup Instructions

### Backend Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Configure the API endpoint:
   - Open `frontend/config.js`
   - Update `apiBaseUrl` to match your backend URL

2. Serve the frontend:
   - For development:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
   - For production, deploy to GitHub Pages or any static hosting service

## Development

1. Backend development:
   - The backend uses Flask and provides RESTful endpoints
   - Image processing is optimized with caching and size optimization
   - GPU acceleration is available if CUDA is installed

2. Frontend development:
   - Modular JavaScript with separate files for API, auth, and core functionality
   - Responsive design with CSS Grid and Flexbox
   - Client-side image validation and optimization

## API Endpoints

- `POST /remove-bg`: Remove image background
- `POST /enhance-bg-removed`: Enhance image with background removed
- `POST /enhance-only`: Enhance original image
- `POST /add-color-background`: Add custom background color

## Error Handling

- Client-side validation for file types and sizes
- Server-side error handling with detailed error messages
- Automatic retry for failed API calls
- Graceful fallback for unsupported features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details
