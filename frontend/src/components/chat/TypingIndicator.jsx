/**
 * TypingIndicator — three-dot bouncing animation shown
 * while the AI agent is processing a request.
 */

export default function TypingIndicator() {
  return (
    <div className="flex justify-start message-enter">
      <div className="bg-[var(--color-surface-alt)] rounded-2xl rounded-bl-md px-4 py-3 border border-[var(--color-border)] shadow-sm">
        <div className="flex items-center gap-1">
          <div className="typing-dot" />
          <div className="typing-dot" />
          <div className="typing-dot" />
        </div>
      </div>
    </div>
  );
}
