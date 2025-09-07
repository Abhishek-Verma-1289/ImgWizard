// API helper functions
function callApi(endpoint, formData) {
    return fetch(window.appConfig.apiBaseUrl + endpoint, {
        method: 'POST',
        body: formData
    });
}

// Export functions
window.api = {
    removeBg: (formData) => callApi(window.appConfig.endpoints.removeBg, formData),
    enhance: (formData) => callApi(window.appConfig.endpoints.enhance, formData),
    addColorBg: (formData) => callApi(window.appConfig.endpoints.addColorBg, formData)
};
