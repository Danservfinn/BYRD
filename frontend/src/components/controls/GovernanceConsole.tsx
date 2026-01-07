import { useEffect, useRef, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

interface ConsoleMessage {
  id: string;
  type: 'user' | 'system' | 'byrd';
  content: string;
  timestamp: string;
}

export function GovernanceConsole() {
  const { sendGovernanceCommand, getGovernanceHistory } = useByrdAPI();
  const [messages, setMessages] = useState<ConsoleMessage[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getGovernanceHistory();
      if (result?.messages) setMessages(result.messages);
    };
    fetch();
    const interval = setInterval(fetch, 5000);
    return () => clearInterval(interval);
  }, [getGovernanceHistory]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || sending) return;

    const userMessage: ConsoleMessage = {
      id: `msg_${Date.now()}`,
      type: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setSending(true);

    try {
      const result = await sendGovernanceCommand(input);
      if (result?.response) {
        const byrdMessage: ConsoleMessage = {
          id: `msg_${Date.now()}_response`,
          type: 'byrd',
          content: result.response,
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, byrdMessage]);
      }
    } catch (error) {
      const errorMessage: ConsoleMessage = {
        id: `msg_${Date.now()}_error`,
        type: 'system',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setSending(false);
    }
  };

  const messageStyles: Record<string, string> = {
    user: 'bg-blue-100 dark:bg-blue-900/30 text-blue-900 dark:text-blue-100 ml-8',
    system: 'bg-amber-100 dark:bg-amber-900/30 text-amber-900 dark:text-amber-100',
    byrd: 'bg-purple-100 dark:bg-purple-900/30 text-purple-900 dark:text-purple-100 mr-8',
  };

  return (
    <GlassPanel glow="none" padding="lg">
      <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4">
        Governance Console
      </h2>

      <div className="h-64 overflow-y-auto border border-slate-200 dark:border-slate-700 rounded-lg p-3 mb-4 bg-white/50 dark:bg-slate-800/50">
        {messages.length === 0 ? (
          <div className="text-center py-8 text-slate-400 text-sm">
            No messages yet. Use commands like:<br />
            <code className="text-purple-600">/status</code>,{' '}
            <code className="text-purple-600">/priority coding 0.9</code>,{' '}
            <code className="text-purple-600">/inject &lt;desire&gt;</code>
          </div>
        ) : (
          <div className="space-y-2">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={clsx('p-2 rounded-lg text-sm', messageStyles[msg.type])}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium capitalize text-xs opacity-70">
                    {msg.type}
                  </span>
                  <span className="text-xs opacity-50">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="whitespace-pre-wrap">{msg.content}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter governance command..."
          disabled={sending}
          className="flex-1 px-3 py-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={!input.trim() || sending}
          className={clsx(
            'px-4 py-2 rounded-lg text-sm font-medium text-white transition-colors',
            !input.trim() || sending
              ? 'bg-slate-400 cursor-not-allowed'
              : 'bg-purple-600 hover:bg-purple-700'
          )}
        >
          {sending ? '...' : 'Send'}
        </button>
      </form>
    </GlassPanel>
  );
}
