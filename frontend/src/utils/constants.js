/**
 * Constants used across the application.
 */

export const INTERACTION_TYPES = [
  'Meeting',
  'Call',
  'Email',
  'Video Call',
  'Conference',
];

export const SENTIMENT_OPTIONS = [
  { value: 'Positive', label: 'Positive', emoji: '😊' },
  { value: 'Neutral', label: 'Neutral', emoji: '😐' },
  { value: 'Negative', label: 'Negative', emoji: '😞' },
];

export const WELCOME_MESSAGE = {
  role: 'assistant',
  content:
    'Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.',
};
