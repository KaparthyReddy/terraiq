import client from "./client";
import type { SensorReading } from "@/store/sensorSlice";

export const sensorsApi = {
  latest: async (fieldId: string): Promise<SensorReading> => {
    const { data } = await client.get(`/sensors/${fieldId}/latest`);
    return data;
  },
  history: async (fieldId: string, limit = 100): Promise<SensorReading[]> => {
    const { data } = await client.get(`/sensors/${fieldId}/history`, {
      params: { limit },
    });
    return data;
  },
  ingest: async (payload: Partial<SensorReading>): Promise<SensorReading> => {
    const { data } = await client.post("/sensors/ingest", payload);
    return data;
  },
};
