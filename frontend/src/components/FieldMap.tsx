import { MapContainer, TileLayer, GeoJSON, Marker, Popup } from "react-leaflet";
import type { Field } from "@/store/fieldSlice";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix default marker icons in Vite
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

interface Props {
  field: Field & { boundary?: object };
  height?: string;
}

export default function FieldMap({ field, height = "320px" }: Props) {
  const center: [number, number] = [field.centroid_lat, field.centroid_lon];

  return (
    <div style={{ height, borderRadius: "12px", overflow: "hidden", border: "1px solid #e0e0e0" }}>
      <MapContainer
        center={center}
        zoom={14}
        style={{ height: "100%", width: "100%" }}
        scrollWheelZoom={false}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='© <a href="https://openstreetmap.org">OpenStreetMap</a>'
        />
        {field.boundary && (
          <GeoJSON
            data={field.boundary as any}
            style={{ color: "#1a7a3f", weight: 2, fillOpacity: 0.15 }}
          />
        )}
        <Marker position={center}>
          <Popup>
            <strong>{field.name}</strong><br />
            {field.area_hectares} ha · {field.crop_type ?? "crop unknown"}
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}
