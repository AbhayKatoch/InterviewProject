import { configureStore } from '@reduxjs/toolkit';
import candidateReducer from '../store/candidateSlice';
import dashboardReducer from '../store/dashboardSlice';
import sessionReducer from '../store/sessionSlice';
import uiReducer from '../store/uiSlice';

export const store = configureStore({
  reducer: {
    candidate: candidateReducer,
    dashboard: dashboardReducer,
    session: sessionReducer,
    ui: uiReducer,
  },
});

export default store;