import { createSlice } from "@reduxjs/toolkit";

const uiSlice = createSlice({
  name: "ui",
  initialState: {
    showWelcomeBack: false,
  },
  reducers: {
    setShowWelcomeBack(state, action) {
      state.showWelcomeBack = action.payload;
    },
  },
});

export const { setShowWelcomeBack } = uiSlice.actions;
export default uiSlice.reducer;
