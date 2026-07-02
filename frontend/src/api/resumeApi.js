import { apiClient } from "./client"

export async function parseResume(file) {

    const formData = new FormData()
    formData.append("file", file);

    const response = await apiClient.post("/resume/parse",formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

    console.log(response);
    return response.data; 
}