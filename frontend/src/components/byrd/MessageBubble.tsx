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
        <div className="flex items-center gap-2 px-4 py-2 bg-amber-100 dark:bg-amber-900/30 rounded-full">
          <AlertCircle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
          <span className="text-sm font-medium text-amber-900 dark:text-amber-100">
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
          'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
          isUser ? 'bg-blue-600 text-white' : 'bg-purple-600 dark:bg-purple-500 text-white'
        )}>
          {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
        </div>

        {/* Message content */}
        <div className={cn('flex flex-col', isUser ? 'items-end' : 'items-start')}>
          <div className={cn(
            'px-4 py-2.5 rounded-2xl text-sm leading-relaxed',
            isUser
              ? 'bg-blue-600 text-white rounded-br-sm'
              : 'bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-700 rounded-bl-sm'
          )}>
            {message.content}
          </div>
          <span className="text-xs text-slate-400 dark:text-slate-500 mt-1 px-1">
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
