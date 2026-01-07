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
      className="flex-1 overflow-y-auto px-4 py-4 space-y-4"
    >
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
          <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center">
            <span className="text-3xl">🐦</span>
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              Start a conversation with BYRD
            </h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 max-w-xs">
              Ask about RSI cycles, set priorities, or inject new desires
            </p>
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
