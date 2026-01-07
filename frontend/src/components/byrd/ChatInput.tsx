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
        'flex-shrink-0 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-700 p-4',
        isFocused && 'shadow-lg'
      )}
    >
      <div className="flex items-end gap-2 max-w-4xl mx-auto">
        {/* Input */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Type to BYRD..."
            rows={1}
            className={cn(
              'w-full px-4 py-3 pr-2 rounded-xl resize-none',
              'bg-slate-100 dark:bg-slate-800',
              'border border-transparent',
              'focus:bg-white dark:focus:bg-slate-700',
              'focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20',
              'text-slate-900 dark:text-slate-100 placeholder-slate-400',
              'transition-all duration-200',
              'max-h-48 overflow-y-auto'
            )}
            disabled={isTyping}
          />
        </div>

        {/* Send button */}
        <button
          type="submit"
          disabled={!input.trim() || isTyping}
          className={cn(
            'p-3 rounded-xl transition-all duration-200',
            'bg-purple-600 hover:bg-purple-700 text-white',
            'disabled:bg-slate-300 dark:disabled:bg-slate-700 disabled:cursor-not-allowed',
            'active:scale-95'
          )}
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </form>
  );
}
