import { useParams, useNavigate } from "react-router-dom";
import { useField } from "@/hooks/useField";
import { useLatestReading, useSensorHistory } from "@/hooks/useSensor";
import FieldMap from "@/components/FieldMap";
import SoilGauge from "@/components/SoilGauge";
import SensorChart from "@/components/SensorChart";

const GAUGES = [
  { key: "ph",            label: "pH",          min: 3,   max: 10,  optimal: [5.5, 7.5] as [number,number], unit: "" },
  { key: "moisture_pct",  label: "Moisture",     min: 0,   max: 100, optimal: [25, 65]   as [number,number], unit: "%" },
  { key: "nitrogen_ppm",  label: "Nitrogen",     min: 0,   max: 400, optimal: [20, 200]  as [number,number], unit: " ppm" },
  { key: "phosphorus_ppm",label: "Phosphorus",   min: 0,   max: 200, optimal: [15, 100]  as [number,number], unit: " ppm" },
  { key: "potassium_ppm", label: "Potassium",    min: 0,   max: 500, optimal: [80, 300]  as [number,number], unit: " ppm" },
  { key: "temperature_c", label: "Temperature",  min: -5,  max: 50,  optimal: [10, 30]   as [number,number], unit: "°C" },
];

export default function FieldDetail() {
  const { fieldId } = useParams<{ fieldId: string }>();
  const navigate = useNavigate();
  const field = useField(fieldId!);
  const { latest } = useLatestReading(fieldId!);
  const history = useSensorHistory(fieldId!);

  if (!field) return <div style={styles.center}>Loading field…</div>;

  return (
    <div style={styles.wrap}>
      <div style={styles.topBar}>
        <button onClick={() => navigate("/")} style={styles.back}>← Back</button>
        <h1 style={styles.h1}>{field.name}</h1>
        <button
          style={styles.recBtn}
          onClick={() => navigate(`/fields/${fieldId}/recommendations`)}
        >
          View recommendations
        </button>
      </div>

      <FieldMap field={field as any} height="300px" />

      <h2 style={styles.h2}>Live Soil Readings</h2>
      <div style={styles.gaugeGrid}>
        {GAUGES.map((g) => (
          <SoilGauge
            key={g.key}
            label={g.label}
            value={latest ? (latest as any)[g.key] : null}
            min={g.min}
            max={g.max}
            optimal={g.optimal}
            unit={g.unit}
          />
        ))}
      </div>

      <SensorChart history={history} />
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrap: { padding: "2rem", maxWidth: "1100px", margin: "0 auto" },
  topBar: { display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1.5rem" },
  h1: { margin: 0, flex: 1, fontSize: "1.5rem", fontWeight: 700, color: "#1a1a1a" },
  h2: { margin: "2rem 0 1rem", fontSize: "1.1rem", fontWeight: 600, color: "#333" },
  back: {
    background: "none", border: "1px solid #ddd", borderRadius: "8px",
    padding: "6px 14px", cursor: "pointer", fontSize: "0.88rem", color: "#555",
  },
  recBtn: {
    background: "#0f4c2a", color: "#fff", border: "none",
    borderRadius: "8px", padding: "8px 18px", cursor: "pointer",
    fontWeight: 600, fontSize: "0.88rem",
  },
  gaugeGrid: {
    display: "flex", flexWrap: "wrap", gap: "1rem",
  },
  center: { textAlign: "center", padding: "4rem", color: "#888" },
};
