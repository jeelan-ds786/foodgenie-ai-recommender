import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowRight,
  AtSign,
  Eye,
  EyeOff,
  Heart,
  LockKeyhole,
  Salad,
  Sparkles,
  UserRound,
  UtensilsCrossed,
} from "lucide-react";
import { register } from "../api/authApi";

export default function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    full_name: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await register(formData);
      alert("Registration successful! Please login.");
      navigate("/login");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="register-page">
      <section className="register-welcome" aria-label="FoodGenie welcome">
        <Link className="register-brand" to="/">
          <span aria-hidden="true">FG</span>
          FoodGenie
        </Link>

        <div className="register-welcome-copy">
          <span className="register-kicker">
            <Sparkles size={15} aria-hidden="true" /> Your table is ready
          </span>
          <h1>Good food gets even better when it knows you.</h1>
          <p>
            Create your taste profile and make every recommendation feel a
            little more personal.
          </p>
        </div>

        <div className="register-perks" aria-hidden="true">
          <span>
            <Salad size={19} /> Pick your cravings
          </span>
          <span>
            <Heart size={19} /> Save what you love
          </span>
          <span>
            <UtensilsCrossed size={19} /> Discover your next order
          </span>
        </div>
      </section>

      <section className="register-form-side">
        <div className="register-form-wrap">
          <div className="register-heading">
            <span className="register-mobile-mark" aria-hidden="true">
              <UtensilsCrossed size={20} />
            </span>
            <p>Join FoodGenie</p>
            <h2>Create your account</h2>
            <span>Four quick details, then the tasty part begins.</span>
          </div>

          <form className="register-form" onSubmit={handleSubmit}>
            <label className="register-field">
              <span>Username</span>
              <span className="register-input">
                <UserRound size={18} aria-hidden="true" />
                <input
                  type="text"
                  value={formData.username}
                  onChange={(event) =>
                    setFormData({ ...formData, username: event.target.value })
                  }
                  placeholder="your foodie name"
                  autoComplete="username"
                  required
                />
              </span>
            </label>

            <label className="register-field">
              <span>Email</span>
              <span className="register-input">
                <AtSign size={18} aria-hidden="true" />
                <input
                  type="email"
                  value={formData.email}
                  onChange={(event) =>
                    setFormData({ ...formData, email: event.target.value })
                  }
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                />
              </span>
            </label>

            <label className="register-field">
              <span>
                Full name <small>Optional</small>
              </span>
              <span className="register-input">
                <Sparkles size={18} aria-hidden="true" />
                <input
                  type="text"
                  value={formData.full_name}
                  onChange={(event) =>
                    setFormData({ ...formData, full_name: event.target.value })
                  }
                  placeholder="What should we call you?"
                  autoComplete="name"
                />
              </span>
            </label>

            <label className="register-field">
              <span>Password</span>
              <span className="register-input">
                <LockKeyhole size={18} aria-hidden="true" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={formData.password}
                  onChange={(event) =>
                    setFormData({ ...formData, password: event.target.value })
                  }
                  placeholder="Create a password"
                  autoComplete="new-password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((visible) => !visible)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  title={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </span>
            </label>

            {error && (
              <p className="register-error" role="alert">
                {error}
              </p>
            )}

            <button
              className="register-submit"
              type="submit"
              disabled={loading}
            >
              {loading ? "Creating your account..." : "Create account"}
              {!loading && <ArrowRight size={18} aria-hidden="true" />}
            </button>
          </form>

          <p className="register-login">
            Already have an account? <Link to="/login">Log in</Link>
          </p>
        </div>
      </section>
    </main>
  );
}
