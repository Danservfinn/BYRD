import { NavLink } from 'react-router-dom';
import { clsx } from 'clsx';

interface NavItemProps {
  to: string;
  icon: string;
  label: string;
  closeMobile?: () => void;
}

function NavItem({ to, icon, label, closeMobile }: NavItemProps) {
  return (
    <NavLink
      to={to}
      onClick={closeMobile}
      className={({ isActive }) =>
        clsx(
          'flex items-center gap-3 px-4 py-3 lg:py-2.5 rounded-lg transition-all duration-200',
          isActive
            ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 font-medium'
            : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
        )
      }
    >
      <span className="text-lg">{icon}</span>
      <span className="text-sm">{label}</span>
    </NavLink>
  );
}

interface SidebarProps {
  closeMobile?: () => void;
}

export function Sidebar({ closeMobile }: SidebarProps) {
  return (
    <aside className="w-64 border-r border-slate-200 dark:border-slate-700 bg-[var(--bg-secondary)] flex flex-col">
      {/* Logo */}
      <div className="h-16 flex items-center justify-between px-6 border-b border-slate-200 dark:border-slate-700">
        <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          BYRD
        </span>
        <span className="ml-2 text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wide hidden sm:inline">
          RSI Dashboard
        </span>
      </div>

      {/* Close button for mobile */}
      <button
        onClick={closeMobile}
        className="lg:hidden absolute top-4 right-4 p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        aria-label="Close menu"
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
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        <NavItem to="/" icon="📊" label="Dashboard" closeMobile={closeMobile} />
        <NavItem to="/rsi" icon="🔄" label="RSI Engine" closeMobile={closeMobile} />
        <NavItem to="/economic" icon="💰" label="Economic" closeMobile={closeMobile} />
        <NavItem to="/plasticity" icon="🧠" label="Plasticity" closeMobile={closeMobile} />
        <NavItem to="/scaling" icon="📈" label="Scaling" closeMobile={closeMobile} />
        <NavItem to="/verification" icon="✓" label="Verification" closeMobile={closeMobile} />
        <NavItem to="/controls" icon="⚙️" label="Controls" closeMobile={closeMobile} />
        <NavItem to="/visualization" icon="🌐" label="3D Topology" closeMobile={closeMobile} />
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-200 dark:border-slate-700">
        <div className="text-xs text-slate-500 dark:text-slate-400">
          <div>BYRD v3.0</div>
          <div>Digital ASI Research</div>
        </div>
      </div>
    </aside>
  );
}
