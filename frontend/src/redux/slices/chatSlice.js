/**
 * Chat slice — manages conversation messages and loading state.
 *
 * Actions:
 *   - appendMessage: Add a user or assistant message
 *   - setLoading: Toggle loading state (for typing indicator)
 *   - clearMessages: Reset conversation
 */

import { createSlice } from '@reduxjs/toolkit';
import { v4 as uuidv4 } from 'uuid';

const initialState = {
  messages: [],
  isLoading: false,
  sessionId: uuidv4(),
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    appendMessage: (state, action) => {
      const { role, content } = action.payload;
      state.messages.push({
        id: uuidv4(),
        role,        // 'user' | 'assistant'
        content,
        timestamp: new Date().toISOString(),
      });
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    clearMessages: (state) => {
      state.messages = [];
      state.sessionId = uuidv4();
    },
    resetSession: (state) => {
      state.messages = [];
      state.isLoading = false;
      state.sessionId = uuidv4();
    },
  },
});

export const { appendMessage, setLoading, clearMessages, resetSession } = chatSlice.actions;
export default chatSlice.reducer;
