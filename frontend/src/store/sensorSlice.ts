import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { sensorsApi } from "@/api/sensors";

export interface SensorReading {
  id: string;
  field_id: string;
  sensor_id: string;
  ph: number | null;
  moisture_pct: number | null;
  temperature_c: number | null;
  nitrogen_ppm: number | null;
  phosphorus_ppm: number | null;
  potassium_ppm: number | null;
  organic_matter_pct: number | null;
  recorded_at: string;
}

interface SensorState {
  latest: SensorReading | null;
  history: SensorReading[];
  loading: boolean;
}

const initialState: SensorState = {
  latest: null,
  history: [],
  loading: false,
};

export const fetchLatest = createAsyncThunk(
  "sensor/fetchLatest",
  async (fieldId: string) => sensorsApi.latest(fieldId)
);

export const fetchHistory = createAsyncThunk(
  "sensor/fetchHistory",
  async (fieldId: string) => sensorsApi.history(fieldId)
);

const sensorSlice = createSlice({
  name: "sensor",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchLatest.pending, (state) => { state.loading = true; })
      .addCase(fetchLatest.fulfilled, (state, action) => {
        state.loading = false;
        state.latest = action.payload;
      })
      .addCase(fetchHistory.fulfilled, (state, action) => {
        state.history = action.payload;
      });
  },
});

export default sensorSlice.reducer;
