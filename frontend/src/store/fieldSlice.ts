import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import { fieldsApi } from "@/api/fields";

export interface Field {
  id: string;
  name: string;
  area_hectares: number;
  centroid_lat: number;
  centroid_lon: number;
  crop_type: string | null;
  soil_type: string | null;
  created_at: string;
}

interface FieldState {
  token: string | null;
  fields: Field[];
  selected: Field | null;
  loading: boolean;
  error: string | null;
}

const initialState: FieldState = {
  token: localStorage.getItem("terraiq_token"),
  fields: [],
  selected: null,
  loading: false,
  error: null,
};

export const fetchFields = createAsyncThunk("field/fetchAll", async () => {
  return fieldsApi.list();
});

export const fetchField = createAsyncThunk(
  "field/fetchOne",
  async (id: string) => fieldsApi.get(id)
);

const fieldSlice = createSlice({
  name: "field",
  initialState,
  reducers: {
    setToken(state, action: PayloadAction<string>) {
      state.token = action.payload;
      localStorage.setItem("terraiq_token", action.payload);
    },
    clearToken(state) {
      state.token = null;
      localStorage.removeItem("terraiq_token");
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchFields.pending, (state) => { state.loading = true; })
      .addCase(fetchFields.fulfilled, (state, action) => {
        state.loading = false;
        state.fields = action.payload;
      })
      .addCase(fetchFields.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Failed to load fields";
      })
      .addCase(fetchField.fulfilled, (state, action) => {
        state.selected = action.payload;
      });
  },
});

export const { setToken, clearToken } = fieldSlice.actions;
export default fieldSlice.reducer;
