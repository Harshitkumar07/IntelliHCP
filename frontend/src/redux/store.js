/**
 * Redux store configuration.
 *
 * Centralises all state management. Each slice handles
 * one domain concern:
 *   - chatSlice: conversation messages and loading state
 *   - interactionSlice: form data (AI-controlled)
 *   - uiSlice: global UI flags (loading, errors)
 */

import { configureStore } from '@reduxjs/toolkit';
import chatReducer from './slices/chatSlice';
import interactionReducer from './slices/interactionSlice';
import uiReducer from './slices/uiSlice';

const store = configureStore({
  reducer: {
    chat: chatReducer,
    interaction: interactionReducer,
    ui: uiReducer,
  },
  devTools: import.meta.env.DEV,
});

export default store;
