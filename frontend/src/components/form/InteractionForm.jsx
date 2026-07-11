/**
 * InteractionForm — read-only form displaying AI-extracted interaction data.
 *
 * CRITICAL: This form has NO onChange handlers. All fields are controlled
 * by Redux state, which is only updated by the AI assistant.
 * This enforces the Golden Rule: "Never fill the form manually."
 *
 * Each field wrapper checks if it was recently updated and applies
 * the fieldHighlight CSS animation for visual feedback.
 */

import { useSelector, useDispatch } from 'react-redux';
import { useEffect } from 'react';
import { clearUpdatedFields } from '../../redux/slices/interactionSlice';
import { INTERACTION_TYPES, SENTIMENT_OPTIONS } from '../../utils/constants';

export default function InteractionForm() {
  const dispatch = useDispatch();
  const { formData, updatedFields } = useSelector((state) => state.interaction);

  // Clear the highlight animation after 1.5s
  useEffect(() => {
    if (updatedFields.length > 0) {
      const timer = setTimeout(() => dispatch(clearUpdatedFields()), 1500);
      return () => clearTimeout(timer);
    }
  }, [updatedFields, dispatch]);

  const isUpdated = (field) => updatedFields.includes(field);

  return (
    <div className="flex flex-col h-full overflow-y-auto p-6">
      <div className="space-y-6">
        <div>
          <h2 className="text-sm font-semibold text-[var(--color-text-secondary)] mb-4">
            Interaction Details
          </h2>

          {/* Row: HCP Name + Interaction Type */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className={isUpdated('doctor_name') ? 'field-updated' : ''}>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)] mb-1">
                HCP Name
              </label>
              <div className="w-full px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] text-sm text-[var(--color-text-primary)] min-h-[38px]">
                {formData.doctor_name || (
                  <span className="text-[var(--color-text-muted)]">Search or select HCP...</span>
                )}
              </div>
            </div>
            <div className={isUpdated('interaction_type') ? 'field-updated' : ''}>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)] mb-1">
                Interaction Type
              </label>
              <div className="w-full px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] text-sm text-[var(--color-text-primary)] min-h-[38px] flex items-center justify-between">
                <span>{formData.interaction_type || 'Meeting'}</span>
                <svg className="w-4 h-4 text-[var(--color-text-muted)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          {/* Row: Date + Time */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className={isUpdated('interaction_date') ? 'field-updated' : ''}>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)] mb-1">
                Date
              </label>
              <div className="w-full px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] text-sm text-[var(--color-text-primary)] min-h-[38px] flex items-center gap-2">
                <span>{formData.interaction_date || new Date().toLocaleDateString('en-GB')}</span>
                <svg className="w-4 h-4 text-[var(--color-text-muted)] ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div className={isUpdated('interaction_time') ? 'field-updated' : ''}>
              <label className="block text-xs font-medium text-[var(--color-text-secondary)] mb-1">
                Time
              </label>
              <div className="w-full px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] text-sm text-[var(--color-text-primary)] min-h-[38px] flex items-center gap-2">
                <span>{formData.interaction_time || new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}</span>
                <svg className="w-4 h-4 text-[var(--color-text-muted)] ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>

          {/* Attendees */}
          <div className={`mb-4 ${isUpdated('attendees') ? 'field-updated' : ''}`}>
            <label className="block text-xs font-medium text-[var(--color-text-secondary)] mb-1">
              Attendees
            </label>
            <div className="w-full px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] text-sm text-[var(--color-text-primary)] min-h-[38px]">
              {formData.attendees || (
                <span className="text-[var(--color-text-muted)]">Enter names or search...</span>
              )}
            </div>
          </div>

          {/* Topics Discussed */}
          <div className={`mb-3 ${isUpdated('topics') ? 'field-updated' : ''}`}>
            <label className="block text-xs font-medium text-[var(--color-text-secondary)] mb-1">
              Topics Discussed
            </label>
            <div className="w-full px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] text-sm text-[var(--color-text-primary)] min-h-[70px] whitespace-pre-wrap">
              {formData.topics || (
                <span className="text-[var(--color-text-muted)]">Enter key discussion points...</span>
              )}
            </div>
          </div>

          {/* Voice Note Button */}
          <button className="flex items-center gap-2 text-xs text-[var(--color-text-secondary)] border border-[var(--color-border)] rounded-lg px-3 py-1.5 hover:bg-[var(--color-surface-hover)] transition-colors cursor-default mb-1">
            <span>✨</span>
            <span>Summarize from Voice Note (Requires Consent)</span>
          </button>
        </div>

        {/* Section: Materials Shared / Samples Distributed */}
        <div className="">
          <h2 className="text-sm font-semibold text-[var(--color-text-secondary)] mb-4">
            Materials Shared / Samples Distributed
          </h2>

          {/* Materials Shared */}
          <div className={`mb-4 ${isUpdated('brochures') ? 'field-updated' : ''}`}>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-medium text-[var(--color-text-secondary)]">
                Materials Shared
              </label>
              <button className="flex items-center gap-1 text-xs text-[var(--color-text-accent)] font-medium cursor-default">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Search/Add
              </button>
            </div>
            <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] px-3 py-2 min-h-[38px]">
              {formData.brochures?.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {formData.brochures.map((b, i) => (
                    <span
                      key={i}
                      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200"
                    >
                      {b}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="text-xs text-[var(--color-text-muted)] italic">No materials added.</span>
              )}
            </div>
          </div>

          {/* Samples Distributed */}
          <div className={isUpdated('samples') ? 'field-updated' : ''}>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-medium text-[var(--color-text-secondary)]">
                Samples Distributed
              </label>
              <button className="flex items-center gap-1 text-xs text-[var(--color-text-accent)] font-medium cursor-default">
                <span>💊</span>
                Add Sample
              </button>
            </div>
            <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] px-3 py-2 min-h-[38px]">
              {formData.samples?.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {formData.samples.map((s, i) => (
                    <span
                      key={i}
                      className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="text-xs text-[var(--color-text-muted)] italic">No samples added.</span>
              )}
            </div>
          </div>
        </div>

        {/* Section: Sentiment */}
        <div className={`${isUpdated('sentiment') ? 'field-updated' : ''}`}>
          <h2 className="text-sm font-semibold text-[var(--color-text-secondary)] mb-3">
            Observed/Inferred HCP Sentiment
          </h2>
          <div className="flex items-center gap-6">
            {SENTIMENT_OPTIONS.map((option) => (
              <label
                key={option.value}
                className={`flex items-center gap-2 cursor-default ${
                  formData.sentiment === option.value
                    ? 'text-[var(--color-text-primary)] font-medium'
                    : 'text-[var(--color-text-muted)]'
                }`}
              >
                <span className="text-lg">{option.emoji}</span>
                <div
                  className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                    formData.sentiment === option.value
                      ? 'border-[var(--color-chat-accent)] bg-[var(--color-chat-accent)]'
                      : 'border-[var(--color-border)]'
                  }`}
                >
                  {formData.sentiment === option.value && (
                    <div className="w-1.5 h-1.5 rounded-full bg-white" />
                  )}
                </div>
                <span className="text-sm">{option.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Section: Outcomes */}
        <div className={`${isUpdated('outcomes') ? 'field-updated' : ''}`}>
          <h2 className="text-sm font-semibold text-[var(--color-text-secondary)] mb-3">
            Outcomes
          </h2>
          <div className="w-full px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] text-sm text-[var(--color-text-primary)] min-h-[70px] whitespace-pre-wrap">
            {formData.outcomes || (
              <span className="text-[var(--color-text-muted)]">Key outcomes or agreements...</span>
            )}
          </div>
        </div>

        {/* Section: Follow-up Actions */}
        <div className={`${isUpdated('follow_up') ? 'field-updated' : ''}`}>
          <h2 className="text-sm font-semibold text-[var(--color-text-secondary)] mb-3">
            Follow-up Actions
          </h2>
          <div className="w-full px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface-alt)] text-sm text-[var(--color-text-primary)] min-h-[70px] whitespace-pre-wrap">
            {formData.follow_up || (
              <span className="text-[var(--color-text-muted)]">Enter next steps or tasks...</span>
            )}
          </div>

          {/* AI Suggested Follow-ups */}
          {formData.follow_up_suggestions?.length > 0 && (
            <div className={`mt-4 ${isUpdated('follow_up_suggestions') ? 'field-updated' : ''}`}>
              <p className="text-xs font-semibold text-[var(--color-text-secondary)] mb-2">
                AI Suggested Follow-ups:
              </p>
              <ul className="space-y-1.5">
                {formData.follow_up_suggestions.map((suggestion, i) => (
                  <li
                    key={i}
                    className="text-sm text-[var(--color-positive)] font-medium cursor-default hover:text-green-700 transition-colors"
                  >
                    + {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
