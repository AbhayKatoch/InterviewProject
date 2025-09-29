import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import uiReducer from "./uiSlice";
import { configureStore } from '@reduxjs/toolkit';
import candidateReducer from './candidateSlice';
import dashboardReducer from './dashboardSlice';
import sessionReducer from './sessionSlice';

export const store = configureStore({
  reducer: {
    candidate: candidateReducer,
    session: sessionReducer,
    dashboard: dashboardReducer,
    ui: uiReducer,
  },
});


export const fetchCandidates = createAsyncThunk("dashboard/fetchCandidates", async () => {
  const res = await axios.get("/api/candidates/");
  return res.data;
});

export const fetchCandidateDetail = createAsyncThunk(
  "dashboard/fetchCandidateDetail",
  async (id) => {
    const res = await axios.get(`/api/candidates/${id}/`);
    return res.data;
  }
);

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState: {
    list: [],
    selected: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(fetchCandidates.fulfilled, (state, action) => {
      state.list = action.payload;
    });
    builder.addCase(fetchCandidateDetail.fulfilled, (state, action) => {
      state.selected = action.payload;
    });
  },
});

export default dashboardSlice.reducer;
