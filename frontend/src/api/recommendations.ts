import client from "./client";

export interface Recommendation {
  id: string;
  field_id: string;
  trigger: string;
  microbiome_health_score: number | null;
  predicted_yield_impact_pct: number | null;
  actions: ActionItem[];
  summary: string;
  ndvi_value: number | null;
  confidence: number | null;
  status: string;
  created_at: string;
}

export interface ActionItem {
  type: string;
  input: string;
  quantity_kg_ha: number | null;
  timing: string | null;
  priority: string;
}

export const recommendationsApi = {
  list: async (fieldId: string): Promise<Recommendation[]> => {
    const { data } = await client.get(`/recommendations/${fieldId}`);
    return data;
  },
  updateStatus: async (
    id: string,
    status: "applied" | "dismissed"
  ): Promise<Recommendation> => {
    const { data } = await client.patch(`/recommendations/${id}/status`, { status });
    return data;
  },
};
