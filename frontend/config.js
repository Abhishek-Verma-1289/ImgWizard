// Configuration for the application
const config = {
    // API endpoints
    apiBaseUrl: 'https://imgwizard-backend.onrender.com',
    endpoints: {
        removeBg: '/remove-bg',
        enhance: '/enhance-bg-removed',
        addColorBg: '/add-color-background'
    },
    
    // UI Configuration
    maxImageSize: 10 * 1024 * 1024, // 10MB
    supportedFormats: ['image/jpeg', 'image/png', 'image/webp'],
    
    // Feature flags
    enableEnhancement: true,
    enableBackgroundRemoval: true,
    enableColorBackground: true
};

// Export configuration
window.appConfig = config;
