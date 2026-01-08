import { useEffect, useRef, useCallback } from 'react';
import { useEventStore } from '../stores/eventStore';
import type { ByrdEvent } from '../types/events';

const WS_CHECK_KEY = 'byrd_websocket_available';

// Safe localStorage access with fallback for iframe contexts
const safeGetStorage = (key: string): string | null => {
  try {
    return localStorage.getItem(key);
  } catch (e) {
    return null;
  }
};

const safeSetStorage = (key: string, value: string): void => {
  try {
    localStorage.setItem(key, value);
  } catch (e) {
    // Silently fail in contexts where localStorage is not available
  }
};

export function useWebSocket() {
  const ws = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 2; // Reduced from 10 to 2 for demo mode
  const hasLoggedRef = useRef(false);

  const addEvent = useEventStore((state) => state.addEvent);
  const setConnected = useEventStore((state) => state.setConnected);

  const connect = useCallback(() => {
    // Check if we've already determined WebSocket is unavailable
    const wsUnavailable = safeGetStorage(WS_CHECK_KEY) === 'false';
    if (wsUnavailable && reconnectAttempts.current >= maxReconnectAttempts) {
      if (!hasLoggedRef.current) {
        console.log('🟡 BYRD Demo Mode: WebSocket not available. Real-time events disabled.');
        hasLoggedRef.current = true;
      }
      return;
    }

    // Connect to Railway backend WebSocket (not relative to current page)
    const wsUrl = 'wss://byrd-api-production.up.railway.app/ws/events';

    try {
      ws.current = new WebSocket(wsUrl);

      ws.current.onopen = () => {
        console.log('🟢 WebSocket connected');
        setConnected(true);
        reconnectAttempts.current = 0;
        safeSetStorage(WS_CHECK_KEY, 'true');
      };

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as ByrdEvent;
          // Add timestamp if not present
          if (!data.timestamp) {
            data.timestamp = new Date().toISOString();
          }
          // Add unique ID if not present
          if (!data.id) {
            data.id = `${data.type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          }
          addEvent(data);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        setConnected(false);

        // Exponential backoff reconnect with max attempts
        if (reconnectAttempts.current < maxReconnectAttempts) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000);
          console.log(`Reconnecting in ${delay}ms... (attempt ${reconnectAttempts.current + 1}/${maxReconnectAttempts})`);
          setTimeout(() => {
            reconnectAttempts.current++;
            connect();
          }, delay);
        } else {
          // Mark WebSocket as unavailable after max attempts
          safeSetStorage(WS_CHECK_KEY, 'false');
          if (!hasLoggedRef.current) {
            console.log('🟡 BYRD Demo Mode: WebSocket unavailable after connection attempts. Real-time events disabled.');
            hasLoggedRef.current = true;
          }
        }
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (e) {
      console.error('Failed to create WebSocket:', e);
      safeSetStorage(WS_CHECK_KEY, 'false');
    }
  }, [addEvent, setConnected]);

  useEffect(() => {
    connect();

    // Keep-alive ping every 30 seconds
    const pingInterval = setInterval(() => {
      if (ws.current?.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);

    return () => {
      clearInterval(pingInterval);
      ws.current?.close();
    };
  }, [connect]);

  const send = useCallback((data: unknown) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(data));
    }
  }, []);

  return {
    isConnected: useEventStore((state) => state.connected),
    send,
  };
}
