// API helper functions
async function callApi(endpoint, formData) {
    try {
        const response = await fetch(window.appConfig.apiBaseUrl + endpoint, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return response;
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Export functions
window.api = {
    removeBg: async (formData) => {
        return await callApi(window.appConfig.endpoints.removeBg, formData);
    },
    enhance: async (formData, isBackgroundRemoved = true) => {
        const endpoint = isBackgroundRemoved ? 
            window.appConfig.endpoints.enhance : 
            window.appConfig.endpoints.enhanceOriginal;
        return await callApi(endpoint, formData);
    },
    addColorBg: async (formData) => {
        return await callApi(window.appConfig.endpoints.addColorBg, formData);
    }
};
