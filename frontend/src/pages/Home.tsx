import { useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchBar from "../components/searchbar/view/searchbar.view";
import { resultsgrid as ResultsGrid } from "../components/resultsgrid";
import { fetchRecommendations } from "../api/recommendApi";
import { removeToken } from "../api/authApi";
import type { FoodRecommendation } from "../api/types";

export default function Home() {
  const navigate = useNavigate();
  const [foods, setFoods] = useState<FoodRecommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string, city: string) => {
    setLoading(true);
    setError(null);

    try {
      console.log("Searching for:", query, "in", city);
      const results = await fetchRecommendations(query, city);
      console.log("Got results:", results);
      setFoods(results);
    } catch (err: any) {
      console.error("Search error:", err);
      if (err.response?.status === 401) {
        setError("Session expired. Please login again.");
        removeToken();
        navigate("/login");
      } else {
        setError(
          "Failed to fetch recommendations. Make sure the backend is running.",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    removeToken();
    navigate("/login");
  };

  return (
    <div style={{ padding: "40px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1>FoodGenie 🍜</h1>
        <button
          onClick={handleLogout}
          style={{
            padding: "10px 20px",
            fontSize: "14px",
            backgroundColor: "#f44336",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </div>

      <SearchBar onSearch={handleSearch} />

      {loading && <p>Loading recommendations...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && foods.length === 0 && (
        <p style={{ marginTop: "20px", color: "#666" }}>
          Search for food to get recommendations!
        </p>
      )}

      <ResultsGrid foods={foods} />
    </div>
  );
}
