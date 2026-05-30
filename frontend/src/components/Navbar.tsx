import { Link, useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "@/store";
import { clearToken } from "@/store/fieldSlice";

export default function Navbar() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const token = useAppSelector((s) => s.field.token);

  function handleLogout() {
    dispatch(clearToken());
    navigate("/login");
  }

  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.brand}>
        🌱 TerraIQ
      </Link>
      {token && (
        <div style={styles.actions}>
          <Link to="/" style={styles.link}>Dashboard</Link>
          <button onClick={handleLogout} style={styles.logout}>
            Logout
          </button>
        </div>
      )}
    </nav>
  );
}

const styles: Record<string, React.CSSProperties> = {
  nav: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 2rem",
    height: "60px",
    background: "#0f4c2a",
    color: "#fff",
    position: "sticky",
    top: 0,
    zIndex: 100,
  },
  brand: {
    color: "#fff",
    textDecoration: "none",
    fontWeight: 700,
    fontSize: "1.2rem",
    letterSpacing: "0.5px",
  },
  actions: { display: "flex", alignItems: "center", gap: "1.5rem" },
  link: { color: "#a8d5b5", textDecoration: "none", fontSize: "0.95rem" },
  logout: {
    background: "transparent",
    border: "1px solid #a8d5b5",
    color: "#a8d5b5",
    padding: "6px 16px",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "0.9rem",
  },
};
