/**
 * ChatInput - Observatory Style Message Input
 */

import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { useByrdStore } from '../../stores/byrdStore';
import { cn } from '@lib/utils/cn';

export function ChatInput() {
  const [input, setInput] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { addMessage, isTyping } = useByrdStore();

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
  }, [input]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    addMessage({
      id: `msg_${Date.now()}`,
      type: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString(),
    });

    setInput('');

    // Simulate BYRD response (replace with actual API)
    setTimeout(() => {
      addMessage({
        id: `msg_${Date.now()}_response`,
        type: 'byrd',
        content: 'I received your message. Processing...',
        timestamp: new Date().toISOString(),
      });
    }, 1000);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn(
        'flex-shrink-0 bg-[var(--obs-bg-base)] border-t border-[var(--obs-border)] p-4',
        isFocused && 'shadow-[0_-4px_20px_rgba(0,255,255,0.1)]'
      )}
    >
      <div className="flex items-end gap-3 max-w-4xl mx-auto">
        {/* Input */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            placeholder="Transmit to BYRD..."
            rows={1}
            className={cn(
              'w-full px-4 py-3 rounded resize-none',
              'bg-[var(--obs-bg-surface)]',
              'border border-[var(--obs-border)]',
              'focus:bg-[var(--obs-bg-elevated)]',
              'focus:border-[var(--data-stream)] focus:ring-1 focus:ring-[var(--data-stream)]/20',
              'text-[var(--obs-text-primary)] placeholder-[var(--obs-text-tertiary)]',
              'transition-all duration-200',
              'max-h-48 overflow-y-auto',
              'text-sm font-mono'
            )}
            disabled={isTyping}
          />
        </div>

        {/* Send button */}
        <button
          type="submit"
          disabled={!input.trim() || isTyping}
          className={cn(
            'p-3 rounded transition-all duration-200',
            'bg-[var(--data-stream)] hover:bg-[var(--data-stream-hover)] text-[var(--obs-bg-base)]',
            'disabled:bg-[var(--obs-bg-elevated)] disabled:text-[var(--obs-text-tertiary)] disabled:cursor-not-allowed',
            'active:scale-95',
            'shadow-[0_0_12px_rgba(0,255,255,0.3)]',
            'disabled:shadow-none'
          )}
          aria-label="Send message"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>

      {/* Transmission indicator */}
      <div className="flex justify-center mt-2">
        <span className="obs-label text-[8px] text-[var(--obs-text-tertiary)]">
          {isTyping ? 'RECEIVING TRANSMISSION...' : 'READY TO TRANSMIT'}
        </span>
      </div>
    </form>
  );
}

export default ChatInput;
