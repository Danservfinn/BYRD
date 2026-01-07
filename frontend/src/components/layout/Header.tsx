import { ConnectionIndicator } from '../common/ConnectionIndicator';

interface HeaderProps {
  toggleSidebar: () => void;
}

export function Header({ toggleSidebar }: HeaderProps) {
  return (
    <header className="h-16 border-b border-slate-200 dark:border-slate-700 bg-[var(--bg-card)] flex items-center justify-between px-4 lg:px-6">
      {/* Left: Hamburger menu (mobile) + Title */}
      <div className="flex items-center gap-4">
        {/* Hamburger menu button - visible only on mobile */}
        <button
          onClick={toggleSidebar}
          className="lg:hidden p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          aria-label="Toggle menu"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>

        <h1 className="text-base lg:text-lg font-semibold text-slate-900 dark:text-slate-100 truncate">
          BYRD Control Center
        </h1>
      </div>

      {/* Right: Status indicators */}
      <div className="flex items-center gap-2 lg:gap-4">
        <ConnectionIndicator />
        <div className="hidden sm:block">
          <SystemStatusBadge />
        </div>
        <div className="hidden lg:block w-px h-6 bg-slate-200 dark:bg-slate-700" />
        <ThemeToggle />
      </div>
    </header>
  );
}

function SystemStatusBadge() {
  // This would be connected to the system status in a real implementation
  const status: 'running' | 'idle' | 'error' = 'idle';

  const statusConfig = {
    running: {
      bg: 'bg-green-100 dark:bg-green-900/30',
      text: 'text-green-700 dark:text-green-400',
      dot: 'bg-green-500',
      label: 'Running',
    },
    idle: {
      bg: 'bg-slate-100 dark:bg-slate-800',
      text: 'text-slate-700 dark:text-slate-400',
      dot: 'bg-slate-400',
      label: 'Idle',
    },
    error: {
      bg: 'bg-red-100 dark:bg-red-900/30',
      text: 'text-red-700 dark:text-red-400',
      dot: 'bg-red-500',
      label: 'Error',
    },
  };

  const config = statusConfig[status];

  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full ${config.bg}`}>
      <span className={`w-2 h-2 rounded-full ${config.dot} ${(status as string) === 'running' ? 'animate-pulse' : ''}`} />
      <span className={`text-xs font-medium ${config.text}`}>{config.label}</span>
    </div>
  );
}

function ThemeToggle() {
  const toggleTheme = () => {
    document.documentElement.classList.toggle('dark');
  };

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
      title="Toggle theme"
    >
      <span className="text-lg">🌓</span>
    </button>
  );
}
