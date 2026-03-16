import axios from "axios";
import type { FoodRecommendation } from "./types";
import { getToken } from "./authApi";

const API_URL = "http://localhost:8000/v1/recommend";

export async function fetchRecommendations(
  query: string,
  city: string = "Chennai",
  topK: number = 10
): Promise<FoodRecommendation[]> {
  try {
    const token = getToken();
    
    if (!token) {
      throw new Error("Not authenticated");
    }
    
    const res = await axios.post(
      API_URL,
      {
        query,
        city,
        top_k: topK,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return res.data.recommendations || [];
  } catch (error) {
    console.error("Failed to fetch recommendations:", error);
    throw error;
  }
}