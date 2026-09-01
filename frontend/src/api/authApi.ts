import axios from "axios";

const API_URL = "http://localhost:8000/v1/auth";

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

function getAuthError(error: unknown, fallback: string): Error {
  if (!axios.isAxiosError(error)) {
    return new Error(fallback);
  }

  const detail = error.response?.data?.detail;
  if (typeof detail === "string") {
    return new Error(detail);
  }

  if (!error.response) {
    return new Error("Cannot reach the FoodGenie backend. Make sure it is running on port 8000.");
  }

  return new Error(fallback);
}

export async function register(data: RegisterData): Promise<void> {
  try {
    await axios.post(`${API_URL}/register`, data);
  } catch (error: unknown) {
    throw getAuthError(error, "Registration failed");
  }
}

export async function login(data: LoginData): Promise<AuthResponse> {
  try {
    const response = await axios.post(`${API_URL}/login-json`, data);
    return response.data;
  } catch (error: unknown) {
    throw getAuthError(error, "Login failed");
  }
}

export function saveToken(token: string): void {
  localStorage.setItem("foodgenie_token", token);
}

export function getToken(): string | null {
  return localStorage.getItem("foodgenie_token");
}

export function removeToken(): void {
  localStorage.removeItem("foodgenie_token");
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}
