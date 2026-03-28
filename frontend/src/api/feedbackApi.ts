import axios from "axios";

const API_BASE_URL = "http://localhost:8000/v1/feedback";

export interface FeedbackResponse {
  status: string;
  action: string;
  food_id: string;
  reward?: number;
  is_active?: boolean;
  removed?: boolean;
}

export async function likeFoodItem(foodId: string, userId?: string): Promise<FeedbackResponse> {
  try {
    const response = await axios.post(`${API_BASE_URL}/like`, {
      food_id: foodId,
      user_id: userId,
    });
    return response.data;
  } catch (error) {
    console.error("Failed to record like:", error);
    throw error;
  }
}

export async function unlikeFoodItem(foodId: string, userId?: string): Promise<FeedbackResponse> {
  try {
    const response = await axios.delete(`${API_BASE_URL}/like`, {
      data: {
        food_id: foodId,
        user_id: userId,
      }
    });
    return response.data;
  } catch (error) {
    console.error("Failed to remove like:", error);
    throw error;
  }
}

export async function skipFoodItem(foodId: string, userId?: string): Promise<FeedbackResponse> {
  try {
    const response = await axios.post(`${API_BASE_URL}/skip`, {
      food_id: foodId,
      user_id: userId,
    });
    return response.data;
  } catch (error) {
    console.error("Failed to record skip:", error);
    throw error;
  }
}

export async function unskipFoodItem(foodId: string, userId?: string): Promise<FeedbackResponse> {
  try {
    const response = await axios.delete(`${API_BASE_URL}/skip`, {
      data: {
        food_id: foodId,
        user_id: userId,
      }
    });
    return response.data;
  } catch (error) {
    console.error("Failed to remove skip:", error);
    throw error;
  }
}

export async function orderFoodItem(foodId: string, userId?: string): Promise<FeedbackResponse> {
  try {
    const response = await axios.post(`${API_BASE_URL}/order`, {
      food_id: foodId,
      user_id: userId,
    });
    return response.data;
  } catch (error) {
    console.error("Failed to record order:", error);
    throw error;
  }
}

export async function unorderFoodItem(foodId: string, userId?: string): Promise<FeedbackResponse> {
  try {
    const response = await axios.delete(`${API_BASE_URL}/order`, {
      data: {
        food_id: foodId,
        user_id: userId,
      }
    });
    return response.data;
  } catch (error) {
    console.error("Failed to remove order:", error);
    throw error;
  }
}
