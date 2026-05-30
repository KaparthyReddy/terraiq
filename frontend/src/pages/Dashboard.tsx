import { useNavigate } from "react-router-dom";
import { useFields } from "@/hooks/useField";
import type { Field } from "@/store/fieldSlice";

export default function Dashboard() {
  const { fields, loading } = useFields();
  const navigate = useNavigate();

  if (loading) return <div style={styles.center}>Loading fields…</div>;

  return (
    <div style={styles.wrap}>
      <div style={styles.header}>
        <h1 style={styles.h1}>Your Fields</h1>
        <span style={styles.count}>{fields.length} field{fields.length !== 1 ? "s" : ""}</span>
      </div>

      {fields.length === 0 && (
        <div style={styles.empty}>
          No fields yet. Add your first field via the API or mobile app.
        </div>
      )}

      <div style={styles.grid}>
        {fields.map((f) => (
          <FieldCard key={f.id} field={f} onClick={() => navigate(`/fields/${f.id}`)} />
        ))}
      </div>
    </div>
  );
}

function FieldCard({ field, onClick }: { field: Field; onClick: () => void }) {
  return (
    <div style={styles.card} onClick={onClick}>
      <div style={styles.cardTop}>
        <span style={styles.fieldName}>{field.name}</span>
        <span style={styles.area}>{field.area_hectares} ha</span>
      </div>
      <div style={styles.meta}>
        {field.crop_type && <Tag label={field.crop_type} color="#1a7a3f" />}
        {field.soil_type && <Tag label={field.soil_type} color="#7a5c1a" />}
      </div>
      <div style={styles.coords}>
        {field.centroid_lat.toFixed(4)}°N, {field.centroid_lon.toFixed(4)}°E
      </div>
    </div>
  );
}

function Tag({ label, color }: { label: string; color: string }) {
  return (
    <span style={{ ...styles.tag, background: color + "18", color }}>
      {label}
    </span>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrap: { padding: "2rem", maxWidth: "1100px", margin: "0 auto" },
  header: { display: "flex", alignItems: "baseline", gap: "1rem", marginBottom: "1.5rem" },
  h1: { margin: 0, fontSize: "1.6rem", fontWeight: 700, color: "#1a1a1a" },
  count: { fontSize: "0.9rem", color: "#888" },
  empty: { textAlign: "center", color: "#aaa", padding: "4rem 0" },
  center: { textAlign: "center", padding: "4rem", color: "#888" },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
    gap: "1.25rem",
  },
  card: {
    background: "#fff",
    border: "1px solid #e8e8e8",
    borderRadius: "14px",
    padding: "1.25rem 1.4rem",
    cursor: "pointer",
    transition: "box-shadow 0.2s, transform 0.15s",
    boxShadow: "0 2px 8px rgba(0,0,0,0.04)",
  },
  cardTop: { display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "0.6rem" },
  fieldName: { fontWeight: 700, fontSize: "1.05rem", color: "#1a1a1a" },
  area: { fontSize: "0.85rem", color: "#888" },
  meta: { display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "0.75rem" },
  tag: { fontSize: "0.75rem", fontWeight: 600, padding: "2px 10px", borderRadius: "20px" },
  coords: { fontSize: "0.75rem", color: "#bbb", fontFamily: "monospace" },
};
