import { useEffect, useState } from "react";
import { LocateFixed, MapPin, MapPinOff, Search } from "lucide-react";
import { fetchCities, fetchNearestCity } from "../../../api/restaurantApi";
import type { LocationResult } from "../../../api/restaurantApi";

interface Props {
  onSearch: (query: string, city: string) => void;
}

export default function SearchBar({ onSearch }: Props) {
  const [query, setQuery] = useState("");
  const [city, setCity] = useState("");
  const [cities, setCities] = useState<string[]>([]);
  const [citiesError, setCitiesError] = useState(false);
  const [isDetecting, setIsDetecting] = useState(false);
  const [locationMessage, setLocationMessage] = useState("");
  const [unavailableLocation, setUnavailableLocation] =
    useState<LocationResult | null>(null);
  const [isGlowing, setIsGlowing] = useState(false);

  useEffect(() => {
    let isActive = true;

    fetchCities()
      .then((availableCities) => {
        if (!isActive) return;
        setCities(availableCities);
        setCity(availableCities[0] ?? "");
      })
      .catch(() => {
        if (isActive) setCitiesError(true);
      });

    return () => {
      isActive = false;
    };
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || !city) return;
    setIsGlowing(true);
    window.setTimeout(() => setIsGlowing(false), 900);
    onSearch(query.trim(), city);
  };

  const handleDetectLocation = () => {
    if (!navigator.geolocation) {
      setLocationMessage(
        "Location detection is not supported by this browser.",
      );
      return;
    }

    setIsDetecting(true);
    setUnavailableLocation(null);
    setLocationMessage("Detecting your location...");
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => {
        fetchNearestCity(coords.latitude, coords.longitude)
          .then((result) => {
            if (result.available) {
              setCity(result.city);
              setLocationMessage(
                `Location detected: ${result.city.replaceAll("_", " ")}.`,
              );
              return;
            }

            setLocationMessage("");
            setUnavailableLocation(result);
          })
          .catch(() =>
            setLocationMessage(
              "Could not match your location to an available city.",
            ),
          )
          .finally(() => setIsDetecting(false));
      },
      () => {
        setIsDetecting(false);
        setLocationMessage(
          "Location access was unavailable. Choose a city from the list.",
        );
      },
      { enableHighAccuracy: false, timeout: 10000, maximumAge: 300000 },
    );
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
        <select
          value={city}
          onChange={(e) => setCity(e.target.value)}
          disabled={cities.length === 0}
        >
          {cities.length === 0 && (
            <option value="">
              {citiesError ? "Cities unavailable" : "Loading cities..."}
            </option>
          )}
          {cities.map((availableCity) => (
            <option key={availableCity} value={availableCity}>
              {availableCity.replaceAll("_", " ")}
            </option>
          ))}
        </select>
        <button
          type="button"
          className="location-button"
          onClick={handleDetectLocation}
          disabled={isDetecting || cities.length === 0}
          title="Detect current location"
          aria-label="Detect current location"
        >
          <LocateFixed size={18} aria-hidden="true" />
        </button>
      </label>
      <button
        type="submit"
        className={`search-button${isGlowing ? " is-glowing" : ""}`}
        disabled={!query.trim() || !city}
      >
        Find my food <Search size={18} aria-hidden="true" />
      </button>
      {locationMessage && (
        <p className="location-message" role="status">
          {locationMessage}
        </p>
      )}
      {unavailableLocation && (
        <div className="location-unavailable" role="status">
          <span className="location-unavailable-icon" aria-hidden="true">
            <MapPinOff size={23} />
          </span>
          <div>
            <strong>Sorry, we’re not in your city yet</strong>
            <p>
              FoodGenie is currently unavailable in{" "}
              {unavailableLocation.detected_city}. The nearest available city is{" "}
              {unavailableLocation.city.replaceAll("_", " ")}.
            </p>
          </div>
          <button
            type="button"
            onClick={() => {
              setCity(unavailableLocation.city);
              setUnavailableLocation(null);
              setLocationMessage(
                `Showing recommendations for ${unavailableLocation.city.replaceAll("_", " ")}.`,
              );
            }}
          >
            Explore {unavailableLocation.city.replaceAll("_", " ")}
          </button>
        </div>
      )}
    </form>
  );
}
