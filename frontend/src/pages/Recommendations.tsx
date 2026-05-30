import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { recommendationsApi, type Recommendation } from "@/api/recommendations";
import RecommendationCard from "@/components/RecommendationCard";

export default function Recommendations() {
  const { fieldId } = useParams<{ fieldId: string }>();
  const navigate = useNavigate();
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!fieldId) return;
    recommendationsApi.list(fieldId).then((data) => {
      setRecs(data);
      setLoading(false);
    });
  }, [fieldId]);

  function handleStatusChange(updated: Recommendation) {
    setRecs((prev) => prev.map((r) => (r.id === updated.id ? updated : r)));
  }

  const pending  = recs.filter((r) => r.status === "pending");
  const resolved = recs.filter((r) => r.status !== "pending");

  return (
    <div style={styles.wrap}>
      <div style={styles.topBar}>
        <button onClick={() => navigate(`/fields/${fieldId}`)} style={styles.back}>
          ← Field detail
        </button>
        <h1 style={styles.h1}>Recommendations</h1>
      </div>

      {loading && <div style={styles.center}>Loading…</div>}

      {!loading && recs.length === 0 && (
        <div style={styles.empty}>
          No recommendations yet. Readings with anomalies will generate them automatically.
        </div>
      )}

      {pending.length > 0 && (
        <>
          <h2 style={styles.h2}>Pending ({pending.length})</h2>
          {pending.map((r) => (
            <RecommendationCard key={r.id} rec={r} onStatusChange={handleStatusChange} />
          ))}
        </>
      )}

      {resolved.length > 0 && (
        <>
          <h2 style={{ ...styles.h2, marginTop: "2rem" }}>Resolved ({resolved.length})</h2>
          {resolved.map((r) => (
            <RecommendationCard key={r.id} rec={r} onStatusChange={handleStatusChange} />
          ))}
        </>
      )}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrap: { padding: "2rem", maxWidth: "860px", margin: "0 auto" },
  topBar: { display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1.5rem" },
  h1: { margin: 0, fontSize: "1.5rem", fontWeight: 700, color: "#1a1a1a" },
  h2: { margin: "0 0 1rem", fontSize: "1rem", fontWeight: 600, color: "#555" },
  back: {
    background: "none", border: "1px solid #ddd", borderRadius: "8px",
    padding: "6px 14px", cursor: "pointer", fontSize: "0.88rem", color: "#555",
  },
  empty: { textAlign: "center", color: "#aaa", padding: "4rem 0" },
  center: { textAlign: "center", padding: "4rem", color: "#888" },
};
