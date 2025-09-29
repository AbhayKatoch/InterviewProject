import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const uploadResume = createAsyncThunk(
  'candidate/uploadResume',
  async (file, { rejectWithValue }) => {
    try {
      const form = new FormData();
      form.append('resume', file);
      const res = await fetch('/api/candidates/upload_resume/', {
        method: 'POST',
        body: form,
      });
      if (!res.ok) {
        const text = await res.text();
        return rejectWithValue(text || 'Upload failed');
      }
      return await res.json();
    } catch (err) {
      return rejectWithValue(err.message || 'Network error');
    }
  }
);

const initialState = {
  list: [],
  uploadStatus: 'idle',
  uploadError: null,
  current: null,
};

const candidateSlice = createSlice({
  name: 'candidate',
  initialState,
  reducers: {
    setCurrentCandidate(state, action) {
      state.current = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(uploadResume.pending, (state) => {
        state.uploadStatus = 'loading';
        state.uploadError = null;
      })
      .addCase(uploadResume.fulfilled, (state, action) => {
        state.uploadStatus = 'succeeded';
        state.list.push(action.payload);
      })
      .addCase(uploadResume.rejected, (state, action) => {
        state.uploadStatus = 'failed';
        state.uploadError = action.payload || action.error.message;
      });
  },
});

export const { setCurrentCandidate } = candidateSlice.actions;
export default candidateSlice.reducer;