import { X } from 'lucide-react';

interface DemoModeBannerProps {
  onDismiss: () => void;
}

export function DemoModeBanner({ onDismiss }: DemoModeBannerProps) {
  return (
    <div className="relative bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 border-b border-amber-200 dark:border-amber-800">
      <div className="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-3">
            <span className="flex-shrink-0 inline-flex items-center justify-center h-6 w-6 rounded-full bg-amber-100 dark:bg-amber-900/50">
              <span className="text-amber-600 dark:text-amber-400 text-xs font-semibold">ℹ️</span>
            </span>
            <div className="flex-1 flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
              <p className="text-sm font-medium text-amber-900 dark:text-amber-100">
                Demo Mode
              </p>
              <p className="text-xs text-amber-700 dark:text-amber-300 hidden sm:block">
                ·
              </p>
              <p className="text-xs text-amber-700 dark:text-amber-300">
                Backend API not connected. Frontend UI is active for demonstration.
              </p>
            </div>
          </div>
          <button
            onClick={onDismiss}
            className="flex-shrink-0 inline-flex text-amber-700 hover:text-amber-900 dark:text-amber-400 dark:hover:text-amber-200 focus:outline-none focus:ring-2 focus:ring-amber-500 rounded-md p-1"
            aria-label="Dismiss"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
