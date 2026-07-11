/**
 * UI slice — manages global UI state.
 *
 * Actions:
 *   - setError: Set/clear global error message
 *   - setGlobalLoading: Toggle global loading overlay
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  isLoading: false,
  error: null,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setError: (state, action) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    setGlobalLoading: (state, action) => {
      state.isLoading = action.payload;
    },
  },
});

export const { setError, clearError, setGlobalLoading } = uiSlice.actions;
export default uiSlice.reducer;
