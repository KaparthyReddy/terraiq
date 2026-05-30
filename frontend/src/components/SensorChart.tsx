import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { format } from "date-fns";
import type { SensorReading } from "@/store/sensorSlice";

interface Props {
  history: SensorReading[];
}

const METRICS = [
  { key: "ph",            color: "#1a7a3f", label: "pH" },
  { key: "moisture_pct",  color: "#2980b9", label: "Moisture %" },
  { key: "nitrogen_ppm",  color: "#8e44ad", label: "N (ppm)" },
];

export default function SensorChart({ history }: Props) {
  const data = [...history]
    .sort((a, b) => new Date(a.recorded_at).getTime() - new Date(b.recorded_at).getTime())
    .map((r) => ({
      time: format(new Date(r.recorded_at), "MMM d HH:mm"),
      ph: r.ph,
      moisture_pct: r.moisture_pct,
      nitrogen_ppm: r.nitrogen_ppm,
    }));

  if (data.length === 0) {
    return (
      <div style={styles.empty}>No historical readings yet.</div>
    );
  }

  return (
    <div style={styles.wrap}>
      <h3 style={styles.title}>Sensor History</h3>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data} margin={{ top: 8, right: 24, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis dataKey="time" tick={{ fontSize: 11 }} tickLine={false} />
          <YAxis tick={{ fontSize: 11 }} tickLine={false} axisLine={false} />
          <Tooltip
            contentStyle={{ borderRadius: "8px", fontSize: "0.85rem" }}
          />
          <Legend wrapperStyle={{ fontSize: "0.82rem" }} />
          {METRICS.map((m) => (
            <Line
              key={m.key}
              type="monotone"
              dataKey={m.key}
              name={m.label}
              stroke={m.color}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  wrap: {
    background: "#fff",
    border: "1px solid #e0e0e0",
    borderRadius: "12px",
    padding: "1.2rem 1.5rem",
    marginTop: "1.5rem",
  },
  title: { margin: "0 0 1rem", fontSize: "1rem", fontWeight: 600, color: "#1a1a1a" },
  empty: { textAlign: "center", color: "#aaa", padding: "2rem" },
};
