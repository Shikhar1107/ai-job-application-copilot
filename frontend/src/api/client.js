import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_BACKEND_API_URL;

export const apiClient = axios.create({
    baseURL: `${API_BASE_URL}/api/v1`,
    headers: {
        "Content-Type": "application/json"
    },
    timeout: 500000,
});

apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        const message = 
        error.response?.data?.detail ||
        error.response?.data?.message ||
        error.message ||
        "Something went wrong";
        return Promise.reject(new Error(message));
    }
);
