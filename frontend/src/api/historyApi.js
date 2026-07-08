import { apiClient } from "./client";

export async function getAnalysisHistory() {
  console.log("/history");
  const response = await apiClient.get("/history");
  console.log(response);
  return response.data;
}

export async function getAnalysisById(id) {
  console.log("/history/{id}")
  const response = await apiClient.get(`/history/${id}`);
  console.log(response);
  return response.data;
}

export async function deleteAnalysisById(id) {
  const response = await apiClient.delete(`/history/${id}`);
  return response.data;
};