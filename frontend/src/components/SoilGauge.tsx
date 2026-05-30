interface Props {
  label: string;
  value: number | null;
  min: number;
  max: number;
  optimal: [number, number];
  unit: string;
}

export default function SoilGauge({ label, value, min, max, optimal, unit }: Props) {
  if (value === null) return <GaugeShell label={label} unit={unit} empty />;

  const pct = ((value - min) / (max - min)) * 100;
  const optLow = ((optimal[0] - min) / (max - min)) * 100;
  const optHigh = ((optimal[1] - min) / (max - min)) * 100;
  const inRange = value >= optimal[0] && value <= optimal[1];

  return (
    <div style={styles.card}>
      <div style={styles.label}>{label}</div>
      <div style={styles.value}>
        <span style={{ color: inRange ? "#1a7a3f" : "#c0392b" }}>
          {value.toFixed(1)}
        </span>
        <span style={styles.unit}>{unit}</span>
      </div>

      <div style={styles.track}>
        {/* Optimal zone highlight */}
        <div
          style={{
            ...styles.optZone,
            left: `${optLow}%`,
            width: `${optHigh - optLow}%`,
          }}
        />
        {/* Fill bar */}
        <div
          style={{
            ...styles.fill,
            width: `${Math.min(pct, 100)}%`,
            background: inRange ? "#1a7a3f" : "#c0392b",
          }}
        />
        {/* Needle */}
        <div style={{ ...styles.needle, left: `${Math.min(pct, 100)}%` }} />
      </div>

      <div style={styles.range}>
        <span>{min}{unit}</span>
        <span style={styles.optLabel}>optimal {optimal[0]}–{optimal[1]}</span>
        <span>{max}{unit}</span>
      </div>
    </div>
  );
}

function GaugeShell({ label, unit, empty }: { label: string; unit: string; empty?: boolean }) {
  return (
    <div style={{ ...styles.card, opacity: 0.45 }}>
      <div style={styles.label}>{label}</div>
      <div style={styles.value}>— <span style={styles.unit}>{unit}</span></div>
      <div style={styles.track} />
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  card: {
    background: "#fff",
    border: "1px solid #e0e0e0",
    borderRadius: "12px",
    padding: "1rem 1.2rem",
    minWidth: "160px",
    flex: "1 1 160px",
  },
  label: { fontSize: "0.78rem", color: "#666", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.5px" },
  value: { fontSize: "1.6rem", fontWeight: 700, marginBottom: "10px" },
  unit: { fontSize: "0.9rem", color: "#888", marginLeft: "4px" },
  track: {
    position: "relative",
    height: "8px",
    background: "#f0f0f0",
    borderRadius: "4px",
    overflow: "visible",
    marginBottom: "6px",
  },
  optZone: {
    position: "absolute",
    height: "100%",
    background: "rgba(26,122,63,0.15)",
    borderRadius: "4px",
  },
  fill: {
    position: "absolute",
    height: "100%",
    borderRadius: "4px",
    transition: "width 0.6s ease",
    opacity: 0.7,
  },
  needle: {
    position: "absolute",
    top: "-3px",
    width: "3px",
    height: "14px",
    background: "#333",
    borderRadius: "2px",
    transform: "translateX(-50%)",
    transition: "left 0.6s ease",
  },
  range: {
    display: "flex",
    justifyContent: "space-between",
    fontSize: "0.7rem",
    color: "#999",
  },
  optLabel: { color: "#1a7a3f", fontWeight: 500 },
};
