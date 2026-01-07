import { useEffect, useState } from 'react';
import { GlassPanel } from '../common/GlassPanel';
import { useByrdAPI } from '../../hooks/useByrdAPI';
import { clsx } from 'clsx';

export function DirectionEditor() {
  const { getDirection, updateDirection } = useByrdAPI();
  const [content, setContent] = useState('');
  const [originalContent, setOriginalContent] = useState('');
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  useEffect(() => {
    const fetch = async () => {
      const result = await getDirection();
      if (result?.content) {
        setContent(result.content);
        setOriginalContent(result.content);
      }
    };
    fetch();
  }, [getDirection]);

  const hasChanges = content !== originalContent;

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateDirection(content);
      setOriginalContent(content);
      setLastSaved(new Date());
    } finally {
      setSaving(false);
    }
  };

  const handleReset = () => {
    setContent(originalContent);
  };

  return (
    <GlassPanel glow="purple" padding="lg" className="h-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
          Direction Editor
        </h2>
        <div className="flex items-center gap-2">
          {lastSaved && (
            <span className="text-xs text-slate-500">
              Last saved: {lastSaved.toLocaleTimeString()}
            </span>
          )}
          {hasChanges && (
            <span className="text-xs text-amber-600 font-medium">
              Unsaved changes
            </span>
          )}
        </div>
      </div>

      <p className="text-sm text-slate-500 mb-3">
        Edit the direction file to guide BYRD's development priorities.
      </p>

      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="# Direction for BYRD

## Current Focus
- ...

## Priorities
1. ...
2. ...

## Constraints
- ..."
        className="w-full h-64 p-3 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm font-mono text-slate-900 dark:text-slate-100 placeholder-slate-400 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
      />

      <div className="flex justify-end gap-2 mt-4">
        <button
          onClick={handleReset}
          disabled={!hasChanges || saving}
          className={clsx(
            'px-3 py-1.5 rounded text-sm font-medium transition-colors',
            !hasChanges || saving
              ? 'text-slate-400 cursor-not-allowed'
              : 'text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800'
          )}
        >
          Reset
        </button>
        <button
          onClick={handleSave}
          disabled={!hasChanges || saving}
          className={clsx(
            'px-3 py-1.5 rounded text-sm font-medium text-white transition-colors',
            !hasChanges || saving
              ? 'bg-slate-400 cursor-not-allowed'
              : 'bg-purple-600 hover:bg-purple-700'
          )}
        >
          {saving ? 'Saving...' : 'Save Direction'}
        </button>
      </div>
    </GlassPanel>
  );
}
