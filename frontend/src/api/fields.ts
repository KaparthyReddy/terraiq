import client from "./client";
import type { Field } from "@/store/fieldSlice";

export const fieldsApi = {
  list: async (): Promise<Field[]> => {
    const { data } = await client.get("/fields/");
    return data;
  },
  get: async (id: string): Promise<Field> => {
    const { data } = await client.get(`/fields/${id}`);
    return data;
  },
  create: async (payload: Partial<Field>): Promise<Field> => {
    const { data } = await client.post("/fields/", payload);
    return data;
  },
  update: async (id: string, payload: Partial<Field>): Promise<Field> => {
    const { data } = await client.patch(`/fields/${id}`, payload);
    return data;
  },
  delete: async (id: string): Promise<void> => {
    await client.delete(`/fields/${id}`);
  },
};
