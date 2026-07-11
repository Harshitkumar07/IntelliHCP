/**
 * Chat async thunk — orchestrates the chat → API → Redux flow.
 *
 * Data flow:
 *   1. Dispatch appendMessage (user message)
 *   2. Set loading state (typing indicator)
 *   3. POST /api/v1/chat with message + session_id + current_form
 *   4. Dispatch appendMessage (assistant reply)
 *   5. Dispatch updateInteraction (form data from tool result)
 *   6. Clear loading state
 */

import { sendChatMessage } from '../../api/chatApi';
import { appendMessage, setLoading } from '../slices/chatSlice';
import { updateInteraction, setFollowUpSuggestions } from '../slices/interactionSlice';
import { setError } from '../slices/uiSlice';

/**
 * Send a message to the AI assistant and process the response.
 *
 * @param {string} message - User's natural language message
 */
export function sendMessage(message) {
  return async (dispatch, getState) => {
    const state = getState();
    const sessionId = state.chat.sessionId;
    const currentForm = state.interaction.formData;

    // 1. Add user message to chat
    dispatch(appendMessage({ role: 'user', content: message }));

    // 2. Show typing indicator
    dispatch(setLoading(true));
    dispatch(setError(null));

    try {
      // 3. Call the backend
      const response = await sendChatMessage(message, sessionId, currentForm);

      // 4. Add assistant reply to chat
      dispatch(appendMessage({ role: 'assistant', content: response.reply }));

      // 5. Update form data if tool returned form_data
      if (response.form_data) {
        // Handle follow-up suggestions separately
        if (response.form_data.follow_up_suggestions && !response.form_data.doctor_name) {
          dispatch(setFollowUpSuggestions(response.form_data.follow_up_suggestions));
        } else if (!response.form_data.search_results && !response.form_data.recommendations) {
          // Standard form data update (from log/edit tools)
          dispatch(updateInteraction(response.form_data));
        }
        // search_results and recommendations are displayed in chat, not form
      }
    } catch (error) {
      dispatch(setError(error.message));
      dispatch(
        appendMessage({
          role: 'assistant',
          content: `Sorry, I encountered an error: ${error.message}. Please try again.`,
        })
      );
    } finally {
      // 6. Hide typing indicator
      dispatch(setLoading(false));
    }
  };
}
