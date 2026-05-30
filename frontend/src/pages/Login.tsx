import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAppDispatch } from "@/store";
import { setToken } from "@/store/fieldSlice";
import client from "@/api/client";

export default function Login() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const payload =
        mode === "login"
          ? { email, password }
          : { email, password, full_name: fullName };

      const { data } = await client.post(
        mode === "login" ? "/auth/login" : "/auth/register",
        payload
      );
      dispatch(setToken(data.access_token));
      navigate("/");
    } catch (err: any) {
      setError(err.response?.data?.detail ?? "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.wrap}>
      <div style={styles.card}>
        <div style={styles.logo}>🌱 TerraIQ</div>
        <h2 style={styles.heading}>
          {mode === "login" ? "Sign in" : "Create account"}
        </h2>

        <form onSubmit={handleSubmit} style={styles.form}>
          {mode === "register" && (
            <input
              style={styles.input}
              type="text"
              placeholder="Full name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
          )}
          <input
            style={styles.input}
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            style={styles.input}
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <div style={styles.error}>{error}</div>}
          <button style={styles.btn} type="submit" disabled={loading}>
            {loading ? "Please wait…" : mode === "login" ? "Sign in" : "Register"}
          </button>
        </form>

        <p style={styles.toggle}>
          {mode === "login" ? "No account? " : "Already registered? "}
          <button
            style={styles.toggleBtn}
            onClick={() => setMode(mode === "login" ? "register" : "login")}
          >
            {mode === "login" ? "Register" : "Sign in"}
          </button>
        </p>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrap: {
    minHeight: "calc(100vh - 60px)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f4f6f4",
  },
  card: {
    background: "#fff",
    borderRadius: "16px",
    padding: "2.5rem 2rem",
    width: "100%",
    maxWidth: "400px",
    boxShadow: "0 4px 24px rgba(0,0,0,0.07)",
  },
  logo: { fontSize: "1.5rem", fontWeight: 800, color: "#0f4c2a", marginBottom: "0.5rem" },
  heading: { margin: "0 0 1.5rem", fontSize: "1.2rem", fontWeight: 600, color: "#1a1a1a" },
  form: { display: "flex", flexDirection: "column", gap: "0.75rem" },
  input: {
    padding: "10px 14px",
    borderRadius: "8px",
    border: "1px solid #ddd",
    fontSize: "0.95rem",
    outline: "none",
  },
  error: { color: "#c0392b", fontSize: "0.85rem" },
  btn: {
    padding: "11px",
    background: "#0f4c2a",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontWeight: 600,
    fontSize: "1rem",
    cursor: "pointer",
    marginTop: "0.25rem",
  },
  toggle: { textAlign: "center", marginTop: "1.2rem", fontSize: "0.88rem", color: "#666" },
  toggleBtn: {
    background: "none",
    border: "none",
    color: "#0f4c2a",
    fontWeight: 600,
    cursor: "pointer",
    fontSize: "0.88rem",
  },
};
