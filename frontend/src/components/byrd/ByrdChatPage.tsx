import { ArrowLeft, Settings } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { AvatarCanvas } from '../visualization/AvatarCanvas';
import { StatusBar } from './StatusBar';
import { ChatMessages } from './ChatMessages';
import { ChatInput } from './ChatInput';

export function ByrdChatPage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col h-screen bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <header className="flex-shrink-0 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 px-4 py-3">
        <div className="flex items-center justify-between max-w-4xl mx-auto">
          <button
            onClick={() => navigate(-1)}
            className="p-2 -ml-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
            aria-label="Go back"
          >
            <ArrowLeft className="w-5 h-5 text-slate-600 dark:text-slate-400" />
          </button>

          <h1 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
            BYRD
          </h1>

          <button
            className="p-2 -mr-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors"
            aria-label="Settings"
          >
            <Settings className="w-5 h-5 text-slate-600 dark:text-slate-400" />
          </button>
        </div>
      </header>

      {/* 3D Avatar - 45% of viewport height */}
      <div className="flex-shrink-0 h-[45vh] min-h-[320px] max-h-[600px] relative">
        <AvatarCanvas
          modelPath="/models/cat.glb"
          animationState="idle"
          autoRotate={false}
          className="w-full h-full"
        />
      </div>

      {/* Status Bar - Collapsible */}
      <StatusBar />

      {/* Chat Messages - Fills remaining space */}
      <div className="flex-1 min-h-0 bg-white dark:bg-slate-800">
        <ChatMessages />
      </div>

      {/* Chat Input - Fixed at bottom */}
      <ChatInput />
    </div>
  );
}
