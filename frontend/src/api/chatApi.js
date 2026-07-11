/**
 * Chat API functions.
 *
 * Encapsulates all HTTP calls to the chat endpoint.
 * Used by the chatThunks async thunk.
 */

import axiosClient from './axiosClient';

/**
 * Send a chat message to the LangGraph agent.
 *
 * @param {string} message - User's natural language message
 * @param {string} sessionId - Conversation session ID for MemorySaver
 * @param {object|null} currentForm - Current interaction form state
 * @returns {Promise<{reply: string, tool_used: string|null, form_data: object|null, interaction_id: string|null}>}
 */
export async function sendChatMessage(message, sessionId, currentForm = null) {
  const response = await axiosClient.post('/chat', {
    message,
    session_id: sessionId,
    current_form: currentForm,
  });
  return response.data;
}

/**
 * Fetch a specific interaction by ID.
 */
export async function getInteraction(interactionId) {
  const response = await axiosClient.get(`/interactions/${interactionId}`);
  return response.data;
}

/**
 * List all interactions.
 */
export async function listInteractions(skip = 0, limit = 50) {
  const response = await axiosClient.get('/interactions', {
    params: { skip, limit },
  });
  return response.data;
}

/**
 * Search doctors in the HCP database.
 */
export async function searchDoctors(query) {
  const response = await axiosClient.get('/doctors/search', {
    params: { q: query },
  });
  return response.data;
}
