import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import axios from "axios";

export const startInterview = createAsyncThunk(
    'session/startInterview',
    async (candidateId) => {
        const res = await axios.post('/api/start_interview/', {candidate_id: candidateId});
        return res.data;
    }
);

export const submitAnswer = createAsyncThunk(
    'session/submitAnswer',
    async({sessionId, index, answer})=>{
        const res = await axios.post('/api/submit_answer/', {session_id: sessionId, index, answer});
        return res.data;
    }
);

const sessionSlice = createSlice({
    name: 'session',
    initialState: {
        session:null,
        currentQuestion:null,
        timeRemaining: null,
        status: 'idle',
    },
    reducers: {
        setCurrentQuestion(state, action) {
        state.currentQuestion = action.payload;
        state.timeRemaining = action.payload.time_limit;
        },
        tick(state) {
        if (state.timeRemaining > 0) state.timeRemaining -= 1;
        },
        resetTimer(state) {
        if (state.currentQuestion) state.timeRemaining = state.currentQuestion.time_limit;
        },
    },
    extraReducers: (builder) => {
    builder
      .addCase(startInterview.fulfilled, (state, action) => {
        state.session = action.payload;
        state.currentQuestion = action.payload.questions_meta[0];
        state.timeRemaining = action.payload.questions_meta[0].time_limit;
      })
      .addCase(submitAnswer.fulfilled, (state, action) => {
        if (action.payload.finished) {
          state.session.status = "completed";
          state.session.final_score = action.payload.final_score;
          state.session.final_summary = action.payload.summary;
          state.currentQuestion = null;
          state.timeRemaining = null;
        } else {
          state.currentQuestion = action.payload.next_question;
          state.timeRemaining = action.payload.next_question.time_limit;
        }
      });
  },
});
export const { setCurrentQuestion, tick, resetTimer } = sessionSlice.actions;
export default sessionSlice.reducer;


