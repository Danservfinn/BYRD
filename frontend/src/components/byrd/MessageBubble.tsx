/**
 * MessageBubble - Observatory Style Chat Message
 */

import { User, Bot, AlertCircle } from 'lucide-react';
import type { ChatMessage } from '../../types/api';
import { formatRelativeTime } from '@lib/utils/format';

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.type === 'user';
  const isSystem = message.type === 'system';

  if (isSystem) {
    return (
      <div className="flex justify-center animate-fade-in">
        <div className="flex items-center gap-2 px-4 py-2 observatory-panel rounded-full">
          <AlertCircle className="w-4 h-4 text-[var(--status-caution)]" />
          <span className="obs-label text-[10px] text-[var(--status-caution)]">
            {message.content}
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className={cn('flex', isUser ? 'justify-end' : 'justify-start', 'animate-slide-up')}>
      <div className={cn('flex gap-3 max-w-[85%]', isUser ? 'flex-row-reverse' : 'flex-row')}>
        {/* Avatar */}
        <div className={cn(
          'flex-shrink-0 w-8 h-8 rounded flex items-center justify-center',
          isUser
            ? 'bg-[var(--data-stream)] text-[var(--obs-bg-base)]'
            : 'observatory-panel text-[var(--cat-eye-gold)]'
        )}>
          {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
        </div>

        {/* Message content */}
        <div className={cn('flex flex-col', isUser ? 'items-end' : 'items-start')}>
          {/* Sender label */}
          <span className="obs-label text-[8px] text-[var(--obs-text-tertiary)] mb-1 px-1">
            {isUser ? 'OPERATOR' : 'BYRD'}
          </span>

          <div className={cn(
            'px-4 py-3 rounded text-sm leading-relaxed',
            isUser
              ? 'bg-[var(--data-stream)] text-[var(--obs-bg-base)]'
              : 'observatory-panel text-[var(--obs-text-primary)]'
          )}>
            {message.content}
          </div>

          <span className="obs-label text-[8px] text-[var(--obs-text-tertiary)] mt-1 px-1">
            {formatRelativeTime(message.timestamp)}
          </span>
        </div>
      </div>
    </div>
  );
}

function cn(...classes: (string | boolean | undefined | null)[]) {
  return classes.filter(Boolean).join(' ');
}

export default MessageBubble;
