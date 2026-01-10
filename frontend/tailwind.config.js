/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Manual dark mode toggle
  theme: {
    extend: {
      colors: {
        // BYRD brand colors
        byrd: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed', // Primary
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        // Observatory Design System
        obs: {
          base: '#050508',
          surface: '#0a0c12',
          elevated: '#12151f',
          accent: '#1a1e2e',
        },
        // Status colors - Mission Control
        nominal: '#00ff88',
        caution: '#ffaa00',
        critical: '#ff3366',
        // Data stream cyan
        stream: '#00ffff',
        // Cat eye gold
        'cat-gold': '#d4af37',
        // Functional colors (preserved)
        success: {
          50: '#ecfdf5',
          500: '#10b981',
          600: '#059669',
        },
        warning: {
          50: '#fffbeb',
          500: '#f59e0b',
          600: '#d97706',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 3s linear infinite',
        // Observatory animations
        'emergence-pulse': 'emergencePulse 3s ease-in-out infinite',
        'status-beacon': 'statusBeacon 2s ease-in-out infinite',
        'scanner': 'scannerRotate 8s linear infinite',
        'metric-pulse': 'metricPulse 2s ease-in-out infinite',
        'eye-glow': 'eyeGlow 3s ease-in-out infinite',
        'data-flow': 'dataFlow 2s linear infinite',
        'float-up': 'floatUp 4s ease-out infinite',
        'breathe': 'breathe 4s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        // Observatory keyframes
        emergencePulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(0, 255, 255, 0.2)' },
          '50%': { boxShadow: '0 0 40px rgba(0, 255, 255, 0.4), 0 0 60px rgba(0, 255, 255, 0.1)' },
        },
        statusBeacon: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.4' },
        },
        scannerRotate: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        metricPulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.85' },
        },
        eyeGlow: {
          '0%, 100%': { filter: 'drop-shadow(0 0 8px #d4af37)', opacity: '0.8' },
          '50%': { filter: 'drop-shadow(0 0 20px #d4af37)', opacity: '1' },
        },
        dataFlow: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(200%)' },
        },
        floatUp: {
          '0%': { transform: 'translateY(0) scale(1)', opacity: '0.8' },
          '100%': { transform: 'translateY(-100px) scale(0.5)', opacity: '0' },
        },
        breathe: {
          '0%, 100%': { transform: 'scaleY(1)' },
          '50%': { transform: 'scaleY(1.05)' },
        },
      },
    },
  },
  plugins: [
    function({ addUtilities }) {
      addUtilities({
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            display: 'none',
          },
        },
      });
    },
  ],
}
