import { cn } from '@lib/utils/cn';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({ label, error, className, ...props }: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
          {label}
        </label>
      )}
      <input
        className={cn(
          'w-full px-3 py-2 rounded-md',
          'bg-white dark:bg-slate-800',
          'border border-slate-300 dark:border-slate-600',
          'text-slate-900 dark:text-slate-100',
          'placeholder-slate-400',
          'text-sm',
          'focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
          'transition-all duration-150',
          error && 'border-red-500 focus:ring-red-500',
          className
        )}
        {...props}
      />
      {error && (
        <p className="mt-1 text-xs text-red-600 dark:text-red-400">{error}</p>
      )}
    </div>
  );
}
