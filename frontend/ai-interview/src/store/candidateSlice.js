import {createslice, createAsyncThunk} from '@reduxjs/toolkit';
import axios from 'axios';

export const UploadResume = createAsyncThunk(
  'candidate/uploadResume',
  async (file, thunkAPI) => {
    const formData = new FormData();
    formData.append("resume",file);
    const res = await axios.post("/api/upload_resume/",formData,{
        headers: {'Content-Type': 'multipart/form-data'}
    });
    return res.data;
    });

const candidateSlice = createSlice({
    name: 'candidate',
    initialState: {
        data:null,
        status: 'idle',
    },
    reducers:{},
    extraReducers: (builder) => {
        builder
        .addCase(UploadResume.pending, (state) => {
            state.status = 'loading';
        })
        .addCase(UploadResume.fulfilled, (state, action) => {
            state.status = 'succeeded';
            state.data = action.payload;
        })
        .addCase(UploadResume.rejected, (state, action) => {
            state.status = 'failed';
            state.error = action.payload;
        });
    }
});
export default candidateSlice.reducer;