import { useState } from "react";
import { MapPin, Search } from "lucide-react";

interface Props {
  onSearch: (query: string, city: string) => void;
}

export default function SearchBar({ onSearch }: Props) {
  const [query, setQuery] = useState("");
  const [city, setCity] = useState("Chennai");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSearch(query.trim(), city);
  };

  return (
    <form onSubmit={handleSubmit} className="search-panel">
      <label className="search-field">
        <Search size={21} aria-hidden="true" />
        <span className="sr-only">Dish or cuisine</span>
        <input
          value={query}
          placeholder="Biryani, dosa, something spicy..."
          onChange={(e) => setQuery(e.target.value)}
          autoComplete="off"
        />
      </label>
      <label className="location-field">
        <MapPin size={19} aria-hidden="true" />
        <span className="sr-only">City</span>
        <select value={city} onChange={(e) => setCity(e.target.value)}>
          <option value="Chennai">Chennai</option>
          <option value="Madurai">Madurai</option>
          <option value="Coimbatore">Coimbatore</option>
          <option value="Trichy">Trichy</option>
          <option value="Salem">Salem</option>
        </select>
      </label>
      <button type="submit" className="search-button" disabled={!query.trim()}>
        Find my food <Search size={18} aria-hidden="true" />
      </button>
    </form>
  );
}
