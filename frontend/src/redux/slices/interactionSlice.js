/**
 * Interaction slice — manages the interaction form data.
 *
 * This is the single source of truth for the left-panel form.
 * The form is READ-ONLY — only Redux dispatches (from AI responses)
 * can modify this state. No manual user input.
 *
 * Actions:
 *   - updateInteraction: Merge AI-extracted form data (shallow merge)
 *   - clearInteraction: Reset form to empty state
 *   - setInteractionId: Set the current interaction's UUID
 *   - setFollowUpSuggestions: Set AI-generated follow-up suggestions
 *   - markFieldsUpdated: Track which fields were just updated (for animation)
 */

import { createSlice } from '@reduxjs/toolkit';

const emptyForm = {
  interaction_id: null,
  doctor_name: '',
  interaction_date: '',
  interaction_time: '',
  interaction_type: 'Meeting',
  attendees: '',
  topics: '',
  products: [],
  summary: '',
  sentiment: 'Neutral',
  brochures: [],
  samples: [],
  outcomes: '',
  follow_up: '',
  follow_up_suggestions: [],
};

const initialState = {
  formData: { ...emptyForm },
  isSaved: false,
  updatedFields: [], // Fields that were just updated (for highlight animation)
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    updateInteraction: (state, action) => {
      const newData = action.payload;
      if (!newData) return;

      // Track which fields changed for highlight animation
      const changedFields = [];
      for (const [key, value] of Object.entries(newData)) {
        if (key in state.formData && JSON.stringify(state.formData[key]) !== JSON.stringify(value)) {
          changedFields.push(key);
        }
      }

      // Shallow merge — only overwrite fields present in newData
      state.formData = { ...state.formData, ...newData };
      state.updatedFields = changedFields;

      // Set interaction_id if provided
      if (newData.interaction_id) {
        state.formData.interaction_id = newData.interaction_id;
        state.isSaved = true;
      }
    },
    clearInteraction: (state) => {
      state.formData = { ...emptyForm };
      state.isSaved = false;
      state.updatedFields = [];
    },
    setFollowUpSuggestions: (state, action) => {
      state.formData.follow_up_suggestions = action.payload || [];
      state.updatedFields = ['follow_up_suggestions'];
    },
    clearUpdatedFields: (state) => {
      state.updatedFields = [];
    },
  },
});

export const {
  updateInteraction,
  clearInteraction,
  setFollowUpSuggestions,
  clearUpdatedFields,
} = interactionSlice.actions;

export default interactionSlice.reducer;
