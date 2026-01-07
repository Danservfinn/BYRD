export function TypingIndicator() {
  return (
    <div className="flex justify-start animate-slide-up">
      <div className="flex gap-3 max-w-[85%]">
        {/* Avatar */}
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-600 dark:bg-purple-500 flex items-center justify-center">
          <span className="text-sm">🐦</span>
        </div>

        {/* Typing animation */}
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 px-4 py-3 rounded-2xl rounded-bl-sm">
          <div className="flex gap-1.5">
            {[0, 1, 2].map((i) => (
              <span
                key={i}
                className="w-2 h-2 bg-slate-400 dark:bg-slate-500 rounded-full animate-pulse"
                style={{
                  animationDelay: `${i * 0.15}s`,
                  animationDuration: '0.8s',
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
