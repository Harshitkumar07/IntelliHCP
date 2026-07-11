/**
 * ChatMessage — individual message bubble.
 *
 * Renders user messages aligned right (blue bubble) and
 * assistant messages aligned left (grey bubble) with
 * a slide-in animation.
 */

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`message-enter flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed shadow-sm ${
          isUser
            ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-br-md'
            : 'bg-[var(--color-surface-alt)] text-[var(--color-text-primary)] border border-[var(--color-border)] rounded-bl-md'
        }`}
      >
        <p className="whitespace-pre-wrap break-words">{message.content}</p>
        <p
          className={`text-[10px] mt-1 ${
            isUser ? 'text-blue-100' : 'text-[var(--color-text-muted)]'
          }`}
        >
          {new Date(message.timestamp).toLocaleTimeString('en-GB', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </div>
  );
}
