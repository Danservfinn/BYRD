import { NavLink } from 'react-router-dom';
import { clsx } from 'clsx';

interface NavItemProps {
  to: string;
  icon: string;
  label: string;
}

function NavItem({ to, icon, label }: NavItemProps) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        clsx(
          'flex items-center gap-3 px-4 py-2.5 rounded-lg transition-all duration-200',
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

export function Sidebar() {
  return (
    <aside className="w-64 border-r border-slate-200 dark:border-slate-700 bg-[var(--bg-secondary)] flex flex-col">
      {/* Logo */}
      <div className="h-16 flex items-center px-6 border-b border-slate-200 dark:border-slate-700">
        <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          BYRD
        </span>
        <span className="ml-2 text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wide">
          RSI Dashboard
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        <NavItem to="/" icon="📊" label="Dashboard" />
        <NavItem to="/rsi" icon="🔄" label="RSI Engine" />
        <NavItem to="/economic" icon="💰" label="Economic" />
        <NavItem to="/plasticity" icon="🧠" label="Plasticity" />
        <NavItem to="/scaling" icon="📈" label="Scaling" />
        <NavItem to="/verification" icon="✓" label="Verification" />
        <NavItem to="/controls" icon="⚙️" label="Controls" />
        <NavItem to="/visualization" icon="🌐" label="3D Topology" />
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
