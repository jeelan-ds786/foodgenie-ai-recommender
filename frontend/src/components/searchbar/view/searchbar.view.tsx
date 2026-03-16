import { useState } from "react";

interface Props {
  onSearch: (query: string, city: string) => void;
}

export default function SearchBar({ onSearch }: Props) {
  const [query, setQuery] = useState("");
  const [city, setCity] = useState("Chennai");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;
    onSearch(query, city);
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{ display: "flex", gap: "10px", marginTop: "20px" }}
    >
      <input
        value={query}
        placeholder="Search food... (e.g., biryani, parotta)"
        onChange={(e) => setQuery(e.target.value)}
        style={{
          flex: 1,
          padding: "10px",
          fontSize: "16px",
          borderRadius: "5px",
          border: "1px solid #ccc",
        }}
      />

      <select
        value={city}
        onChange={(e) => setCity(e.target.value)}
        style={{
          padding: "10px",
          fontSize: "16px",
          borderRadius: "5px",
          border: "1px solid #ccc",
        }}
      >
        <option value="Chennai">Chennai</option>
        <option value="Madurai">Madurai</option>
        <option value="Coimbatore">Coimbatore</option>
        <option value="Trichy">Trichy</option>
        <option value="Salem">Salem</option>
      </select>

      <button
        type="submit"
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Search 🔍
      </button>
    </form>
  );
}
