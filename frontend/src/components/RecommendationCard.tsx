import type { Recommendation } from "@/api/recommendations";
import { recommendationsApi } from "@/api/recommendations";
import { useState } from "react";

const PRIORITY_COLOR: Record<string, string> = {
  high: "#c0392b",
  medium: "#e67e22",
  low: "#27ae60",
};

const TYPE_ICON: Record<string, string> = {
  fertilize: "🌿",
  irrigate: "💧",
  apply_amendment: "🪨",
  till: "🚜",
};

interface Props {
  rec: Recommendation;
  onStatusChange?: (updated: Recommendation) => void;
}

export default function RecommendationCard({ rec, onStatusChange }: Props) {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(rec.status);

  async function handleAction(s: "applied" | "dismissed") {
    setLoading(true);
    try {
      const updated = await recommendationsApi.updateStatus(rec.id, s);
      setStatus(updated.status);
      onStatusChange?.(updated);
    } finally {
      setLoading(false);
    }
  }

  const isPending = status === "pending";

  return (
    <div style={{ ...styles.card, opacity: isPending ? 1 : 0.65 }}>
      <div style={styles.header}>
        <div>
          <span style={styles.trigger}>{rec.trigger.toUpperCase()}</span>
          <span style={{ ...styles.statusBadge, background: isPending ? "#fff3cd" : "#e8f5e9" }}>
            {status}
          </span>
        </div>
        <span style={styles.date}>
          {new Date(rec.created_at).toLocaleDateString()}
        </span>
      </div>

      <p style={styles.summary}>{rec.summary}</p>

      <div style={styles.metrics}>
        {rec.microbiome_health_score !== null && (
          <Metric label="Microbiome health" value={`${(rec.microbiome_health_score * 100).toFixed(0)}%`} />
        )}
        {rec.ndvi_value !== null && (
          <Metric label="NDVI" value={rec.ndvi_value?.toFixed(3) ?? "—"} />
        )}
        {rec.confidence !== null && (
          <Metric label="Confidence" value={`${(rec.confidence! * 100).toFixed(0)}%`} />
        )}
      </div>

      {rec.actions.length > 0 && (
        <div style={styles.actions}>
          {rec.actions.map((a, i) => (
            <div key={i} style={styles.action}>
              <span>{TYPE_ICON[a.type] ?? "⚙️"}</span>
              <div>
                <div style={styles.actionTitle}>
                  {a.input}
                  {a.quantity_kg_ha && (
                    <span style={styles.qty}> · {a.quantity_kg_ha} kg/ha</span>
                  )}
                  <span style={{ ...styles.priority, color: PRIORITY_COLOR[a.priority] }}>
                    {a.priority}
                  </span>
                </div>
                {a.timing && <div style={styles.timing}>{a.timing}</div>}
              </div>
            </div>
          ))}
        </div>
      )}

      {isPending && (
        <div style={styles.buttons}>
          <button
            style={{ ...styles.btn, background: "#1a7a3f", color: "#fff" }}
            onClick={() => handleAction("applied")}
            disabled={loading}
          >
            ✓ Mark applied
          </button>
          <button
            style={{ ...styles.btn, background: "#f5f5f5", color: "#666" }}
            onClick={() => handleAction("dismissed")}
            disabled={loading}
          >
            Dismiss
          </button>
        </div>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ fontSize: "1.1rem", fontWeight: 700 }}>{value}</div>
      <div style={{ fontSize: "0.72rem", color: "#888" }}>{label}</div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  card: {
    background: "#fff",
    border: "1px solid #e0e0e0",
    borderRadius: "12px",
    padding: "1.2rem 1.5rem",
    marginBottom: "1rem",
  },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.6rem" },
  trigger: { fontSize: "0.7rem", fontWeight: 700, color: "#888", letterSpacing: "1px", marginRight: "8px" },
  statusBadge: { fontSize: "0.72rem", padding: "2px 8px", borderRadius: "20px", fontWeight: 500 },
  date: { fontSize: "0.78rem", color: "#aaa" },
  summary: { fontSize: "0.92rem", color: "#333", margin: "0 0 1rem", lineHeight: 1.5 },
  metrics: { display: "flex", gap: "2rem", marginBottom: "1rem" },
  actions: { display: "flex", flexDirection: "column", gap: "0.6rem", marginBottom: "1rem" },
  action: { display: "flex", gap: "0.75rem", alignItems: "flex-start", fontSize: "0.88rem" },
  actionTitle: { fontWeight: 500, color: "#222" },
  qty: { color: "#666", fontWeight: 400 },
  priority: { fontSize: "0.72rem", fontWeight: 700, marginLeft: "8px", textTransform: "uppercase" },
  timing: { fontSize: "0.78rem", color: "#888", marginTop: "2px" },
  buttons: { display: "flex", gap: "0.75rem" },
  btn: {
    padding: "8px 20px",
    borderRadius: "8px",
    border: "none",
    cursor: "pointer",
    fontWeight: 500,
    fontSize: "0.88rem",
  },
};
