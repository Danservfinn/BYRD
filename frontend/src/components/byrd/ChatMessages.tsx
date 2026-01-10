/**
 * ChatMessages - Observatory Style Message Display
 */

import { useRef, useEffect } from 'react';
import { useByrdStore } from '../../stores/byrdStore';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';

export function ChatMessages() {
  const { messages, isTyping } = useByrdStore();
  const scrollRef = useRef<HTMLDivElement>(null);
  const prevMessagesLength = useRef(messages.length);

  // Auto-scroll to bottom when new message arrives
  useEffect(() => {
    if (messages.length > prevMessagesLength.current) {
      scrollRef.current?.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: 'smooth',
      });
    }
    prevMessagesLength.current = messages.length;
  }, [messages.length]);

  return (
    <div
      ref={scrollRef}
      className="flex-1 overflow-y-auto px-4 py-4 space-y-4 scrollbar-thin"
    >
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
          <div className="w-16 h-16 observatory-panel rounded-full flex items-center justify-center">
            <span
              className="text-3xl animate-eye-glow"
              style={{ textShadow: '0 0 20px var(--cat-eye-gold)' }}
            >
              🐱
            </span>
          </div>
          <div className="space-y-2">
            <h3 className="obs-label text-sm text-[var(--obs-text-primary)]">
              COMMUNICATION TERMINAL
            </h3>
            <p className="text-xs text-[var(--obs-text-tertiary)] max-w-xs">
              Direct interface to BYRD's consciousness.
              <br />
              Ask about RSI cycles, set priorities, or inject new desires.
            </p>
          </div>

          {/* Suggested prompts */}
          <div className="flex flex-wrap gap-2 justify-center max-w-sm">
            <SuggestionChip text="What's your current state?" />
            <SuggestionChip text="Show emergence metrics" />
            <SuggestionChip text="Start RSI cycle" />
          </div>
        </div>
      )}

      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}

      {isTyping && <TypingIndicator />}
    </div>
  );
}

function SuggestionChip({ text }: { text: string }) {
  const { addMessage } = useByrdStore();

  const handleClick = () => {
    addMessage({
      id: `msg_${Date.now()}`,
      type: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    });
  };

  return (
    <button
      onClick={handleClick}
      className="obs-label text-[9px] px-3 py-1.5 rounded bg-[var(--obs-bg-elevated)] text-[var(--obs-text-secondary)] border border-[var(--obs-border)] hover:border-[var(--data-stream)] hover:text-[var(--data-stream)] transition-colors"
    >
      {text}
    </button>
  );
}

export default ChatMessages;
