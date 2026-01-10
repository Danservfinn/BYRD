import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { StatusBadge } from '../../../components/common/StatusBadge'

describe('StatusBadge', () => {
  describe('rendering', () => {
    it('should render children content', () => {
      render(<StatusBadge variant="info">Test Content</StatusBadge>)

      expect(screen.getByText('Test Content')).toBeInTheDocument()
    })

    it('should render as a span element', () => {
      render(<StatusBadge variant="success">Status</StatusBadge>)

      const badge = screen.getByText('Status')
      expect(badge.tagName).toBe('SPAN')
    })
  })

  describe('variants', () => {
    it('should apply success variant styles', () => {
      render(<StatusBadge variant="success">Success</StatusBadge>)

      const badge = screen.getByText('Success')
      expect(badge.className).toContain('bg-green-100')
      expect(badge.className).toContain('text-green-700')
    })

    it('should apply warning variant styles', () => {
      render(<StatusBadge variant="warning">Warning</StatusBadge>)

      const badge = screen.getByText('Warning')
      expect(badge.className).toContain('bg-amber-100')
      expect(badge.className).toContain('text-amber-700')
    })

    it('should apply critical variant styles', () => {
      render(<StatusBadge variant="critical">Critical</StatusBadge>)

      const badge = screen.getByText('Critical')
      expect(badge.className).toContain('bg-red-100')
      expect(badge.className).toContain('text-red-700')
    })

    it('should apply info variant styles', () => {
      render(<StatusBadge variant="info">Info</StatusBadge>)

      const badge = screen.getByText('Info')
      expect(badge.className).toContain('bg-blue-100')
      expect(badge.className).toContain('text-blue-700')
    })
  })

  describe('dark mode styles', () => {
    it('should include dark mode classes for success', () => {
      render(<StatusBadge variant="success">Success</StatusBadge>)

      const badge = screen.getByText('Success')
      expect(badge.className).toContain('dark:bg-green-900/30')
      expect(badge.className).toContain('dark:text-green-300')
    })

    it('should include dark mode classes for warning', () => {
      render(<StatusBadge variant="warning">Warning</StatusBadge>)

      const badge = screen.getByText('Warning')
      expect(badge.className).toContain('dark:bg-amber-900/30')
      expect(badge.className).toContain('dark:text-amber-300')
    })

    it('should include dark mode classes for critical', () => {
      render(<StatusBadge variant="critical">Critical</StatusBadge>)

      const badge = screen.getByText('Critical')
      expect(badge.className).toContain('dark:bg-red-900/30')
      expect(badge.className).toContain('dark:text-red-300')
    })

    it('should include dark mode classes for info', () => {
      render(<StatusBadge variant="info">Info</StatusBadge>)

      const badge = screen.getByText('Info')
      expect(badge.className).toContain('dark:bg-blue-900/30')
      expect(badge.className).toContain('dark:text-blue-300')
    })
  })

  describe('base styles', () => {
    it('should apply base inline-flex style', () => {
      render(<StatusBadge variant="info">Badge</StatusBadge>)

      const badge = screen.getByText('Badge')
      expect(badge.className).toContain('inline-flex')
    })

    it('should apply base items-center style', () => {
      render(<StatusBadge variant="info">Badge</StatusBadge>)

      const badge = screen.getByText('Badge')
      expect(badge.className).toContain('items-center')
    })

    it('should apply rounded-full style', () => {
      render(<StatusBadge variant="info">Badge</StatusBadge>)

      const badge = screen.getByText('Badge')
      expect(badge.className).toContain('rounded-full')
    })

    it('should apply text-xs font style', () => {
      render(<StatusBadge variant="info">Badge</StatusBadge>)

      const badge = screen.getByText('Badge')
      expect(badge.className).toContain('text-xs')
    })

    it('should apply font-medium style', () => {
      render(<StatusBadge variant="info">Badge</StatusBadge>)

      const badge = screen.getByText('Badge')
      expect(badge.className).toContain('font-medium')
    })

    it('should apply border style', () => {
      render(<StatusBadge variant="info">Badge</StatusBadge>)

      const badge = screen.getByText('Badge')
      expect(badge.className).toContain('border')
    })

    it('should apply padding styles', () => {
      render(<StatusBadge variant="info">Badge</StatusBadge>)

      const badge = screen.getByText('Badge')
      expect(badge.className).toContain('px-2.5')
      expect(badge.className).toContain('py-0.5')
    })
  })

  describe('border colors', () => {
    it('should apply success border color', () => {
      render(<StatusBadge variant="success">Success</StatusBadge>)

      const badge = screen.getByText('Success')
      expect(badge.className).toContain('border-green-200')
      expect(badge.className).toContain('dark:border-green-800')
    })

    it('should apply warning border color', () => {
      render(<StatusBadge variant="warning">Warning</StatusBadge>)

      const badge = screen.getByText('Warning')
      expect(badge.className).toContain('border-amber-200')
      expect(badge.className).toContain('dark:border-amber-800')
    })

    it('should apply critical border color', () => {
      render(<StatusBadge variant="critical">Critical</StatusBadge>)

      const badge = screen.getByText('Critical')
      expect(badge.className).toContain('border-red-200')
      expect(badge.className).toContain('dark:border-red-800')
    })

    it('should apply info border color', () => {
      render(<StatusBadge variant="info">Info</StatusBadge>)

      const badge = screen.getByText('Info')
      expect(badge.className).toContain('border-blue-200')
      expect(badge.className).toContain('dark:border-blue-800')
    })
  })

  describe('className prop', () => {
    it('should apply custom className', () => {
      render(
        <StatusBadge variant="info" className="custom-class">
          Custom
        </StatusBadge>
      )

      const badge = screen.getByText('Custom')
      expect(badge.className).toContain('custom-class')
    })

    it('should merge custom className with base styles', () => {
      render(
        <StatusBadge variant="success" className="my-4 w-full">
          Merged
        </StatusBadge>
      )

      const badge = screen.getByText('Merged')
      expect(badge.className).toContain('my-4')
      expect(badge.className).toContain('w-full')
      expect(badge.className).toContain('inline-flex')
      expect(badge.className).toContain('bg-green-100')
    })
  })

  describe('children', () => {
    it('should render text children', () => {
      render(<StatusBadge variant="info">Plain Text</StatusBadge>)

      expect(screen.getByText('Plain Text')).toBeInTheDocument()
    })

    it('should render JSX children', () => {
      render(
        <StatusBadge variant="info">
          <span data-testid="inner">Inner Content</span>
        </StatusBadge>
      )

      expect(screen.getByTestId('inner')).toBeInTheDocument()
      expect(screen.getByText('Inner Content')).toBeInTheDocument()
    })

    it('should render multiple children', () => {
      render(
        <StatusBadge variant="warning">
          <span>Icon</span>
          <span>Text</span>
        </StatusBadge>
      )

      expect(screen.getByText('Icon')).toBeInTheDocument()
      expect(screen.getByText('Text')).toBeInTheDocument()
    })
  })
})
