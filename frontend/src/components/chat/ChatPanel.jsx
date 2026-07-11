/**
 * ChatPanel — AI Assistant interface (right panel).
 *
 * Contains:
 *   - Header with AI Assistant title
 *   - Scrollable message area with auto-scroll
 *   - Welcome message with usage example
 *   - Typing indicator during AI processing
 *   - Fixed input bar at the bottom
 */

import { useState, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { sendMessage } from '../../redux/thunks/chatThunks';
import ChatMessage from './ChatMessage';
import TypingIndicator from './TypingIndicator';
import { WELCOME_MESSAGE } from '../../utils/constants';

export default function ChatPanel() {
  const dispatch = useDispatch();
  const { messages, isLoading } = useSelector((state) => state.chat);
  const error = useSelector((state) => state.ui.error);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = () => {
    const trimmed = inputValue.trim();
    if (!trimmed || isLoading) return;

    dispatch(sendMessage(trimmed));
    setInputValue('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="border-b border-[var(--color-border)] px-5 py-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
              AI Assistant
            </h2>
            <p className="text-xs text-[var(--color-text-muted)]">
              Log interaction via chat
            </p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-5 py-4 space-y-4">
        {/* Welcome Message */}
        {messages.length === 0 && (
          <div className="message-enter">
            <div className="bg-[var(--color-surface-alt)] rounded-xl p-4 border border-[var(--color-border)]">
              <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
                {WELCOME_MESSAGE.content}
              </p>
            </div>
          </div>
        )}

        {/* Chat Messages */}
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {/* Typing Indicator */}
        {isLoading && <TypingIndicator />}

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 text-red-700 text-sm rounded-lg px-4 py-3 border border-red-200">
            {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <div className="border-t border-[var(--color-border)] px-4 py-3">
        <div className="flex items-center gap-2">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe interaction..."
            disabled={isLoading}
            className="flex-1 px-4 py-2 border border-[var(--color-border)] bg-white text-sm text-[var(--color-text-primary)] focus:outline-none focus:border-blue-500 transition-all disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !inputValue.trim()}
            className="flex items-center gap-1.5 px-4 py-2 bg-gray-500 text-white text-sm font-medium hover:bg-gray-600 focus:outline-none transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Log
          </button>
        </div>
      </div>
    </div>
  );
}
