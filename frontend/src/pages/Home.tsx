import { useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchBar from "../components/searchbar/view/searchbar.view";
import { resultsgrid as ResultsGrid } from "../components/resultsgrid";
import { fetchRecommendations } from "../api/recommendApi";
import { removeToken } from "../api/authApi";
import type { FoodRecommendation } from "../api/types";
import { LogOut, Sparkles } from "lucide-react";
import axios from "axios";

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
    } catch (err: unknown) {
      console.error("Search error:", err);
      if (axios.isAxiosError(err) && err.response?.status === 401) {
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
    <main className="home-shell">
      <header className="site-header">
        <a className="brand" href="/" aria-label="FoodGenie home">
          <span className="brand-mark" aria-hidden="true">
            FG
          </span>
          <span>FoodGenie</span>
        </a>
        <button
          className="icon-button"
          onClick={handleLogout}
          title="Log out"
          aria-label="Log out"
        >
          <LogOut size={19} aria-hidden="true" />
        </button>
      </header>

      <section className="discovery" aria-labelledby="discovery-title">
        <div className="eyebrow">
          <Sparkles size={16} aria-hidden="true" /> Personal taste, smarter
          picks
        </div>
        <h1 id="discovery-title">What are you craving?</h1>
        <p className="discovery-copy">
          Tell us what sounds good. FoodGenie learns from every choice and finds
          dishes matched to your taste.
        </p>
        <SearchBar onSearch={handleSearch} />
        <div className="quick-picks" aria-label="Popular searches">
          <span>Try</span>
          <button onClick={() => handleSearch("biryani", "Chennai")}>
            Biryani
          </button>
          <button onClick={() => handleSearch("dosa", "Chennai")}>Dosa</button>
          <button onClick={() => handleSearch("parotta", "Chennai")}>
            Parotta
          </button>
        </div>
      </section>

      <section
        className="results-section"
        aria-live="polite"
        aria-busy={loading}
      >
        {loading && (
          <div className="status-message">
            <span className="loader" aria-hidden="true" />
            <strong>Finding your best matches</strong>
            <span>Balancing taste, location, and your preferences...</span>
          </div>
        )}
        {error && (
          <div className="status-message error-message" role="alert">
            {error}
          </div>
        )}
        {!loading && !error && foods.length === 0 && (
          <div className="empty-state">
            <span className="empty-mark" aria-hidden="true">
              01
            </span>
            <div>
              <strong>Your next favorite dish starts here.</strong>
              <p>Search above to get personalized recommendations near you.</p>
            </div>
          </div>
        )}
        {!loading && !error && foods.length > 0 && (
          <div className="results-heading">
            <div>
              <span className="section-kicker">Curated for you</span>
              <h2>Top recommendations</h2>
            </div>
            <span>{foods.length} matches</span>
          </div>
        )}
        {!loading && !error && <ResultsGrid foods={foods} />}
      </section>
    </main>
  );
}
