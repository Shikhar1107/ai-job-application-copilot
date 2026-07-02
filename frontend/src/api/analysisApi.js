import { apiClient } from "./client";

export async function analyzeResumeJob(payload) {
    console.log("/analysis/analyze");
    const response = await apiClient.post("/analysis/analyze", payload);
    console.log(response);

    return response.data;
}
export async function generateResumeBullets(payload) {
    console.log("/analysis/rewrite-bullets");
    const response = await apiClient.post("/analysis/rewrite-bullets", payload);
    console.log(response);
    return response.data;
}
export async function generateCoverLetter(payload) {
    console.log("/analysis/cover-letter")
    const response = await apiClient.post("/analysis/cover-letter", payload);
    console.log(response);

    return response.data;
}
export async function generateInterviewQuestions(payload) {

    console.log("/analysis/interview-questions");
    const response = await apiClient.post("/analysis/interview-questions", payload);
    console.log(response);

    return response.data;
}