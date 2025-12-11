import * as React from 'react'
import { cn } from '@/lib/utils/cn'

const SelectContext = React.createContext<{
  value: string
  onValueChange: (value: string) => void
} | null>(null)

export interface SelectProps extends React.HTMLAttributes<HTMLDivElement> {
  value: string
  onValueChange: (value: string) => void
  disabled?: boolean
  children: React.ReactNode
}

const Select = React.forwardRef<HTMLDivElement, SelectProps>(
  ({ value, onValueChange, disabled, children, ...props }, ref) => {
    return (
      <SelectContext.Provider value={{ value, onValueChange }}>
        <div ref={ref} {...props}>
          {children}
        </div>
      </SelectContext.Provider>
    )
  }
)
Select.displayName = 'Select'

export interface SelectTriggerProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

const SelectTrigger = React.forwardRef<HTMLButtonElement, SelectTriggerProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        type="button"
        className={cn(
          'flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm',
          'ring-offset-background placeholder:text-muted-foreground',
          'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
          className
        )}
        {...props}
      >
        {children}
      </button>
    )
  }
)
SelectTrigger.displayName = 'SelectTrigger'

export interface SelectValueProps extends React.HTMLAttributes<HTMLSpanElement> {
  placeholder?: string
}

const SelectValue = React.forwardRef<HTMLSpanElement, SelectValueProps>(
  ({ placeholder, ...props }, ref) => {
    const context = React.useContext(SelectContext)
    const value = context?.value || placeholder || 'Select...'

    return (
      <span ref={ref} {...props}>
        {value}
      </span>
    )
  }
)
SelectValue.displayName = 'SelectValue'

export interface SelectContentProps extends React.HTMLAttributes<HTMLDivElement> {}

const SelectContent = React.forwardRef<HTMLDivElement, SelectContentProps>(
  ({ className, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'relative mt-1 max-h-60 w-full overflow-auto rounded-md border bg-popover text-popover-foreground shadow-md',
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)
SelectContent.displayName = 'SelectContent'

export interface SelectItemProps extends React.HTMLAttributes<HTMLDivElement> {
  value: string
}

const SelectItem = React.forwardRef<HTMLDivElement, SelectItemProps>(
  ({ className, value, children, ...props }, ref) => {
    const context = React.useContext(SelectContext)
    if (!context) {
      throw new Error('SelectItem must be used within Select')
    }

    const isSelected = context.value === value

    return (
      <div
        ref={ref}
        className={cn(
          'relative flex cursor-pointer select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none',
          'hover:bg-accent hover:text-accent-foreground',
          isSelected && 'bg-accent text-accent-foreground font-medium',
          'focus:bg-accent focus:text-accent-foreground',
          className
        )}
        onClick={() => context.onValueChange(value)}
        {...props}
      >
        {children}
      </div>
    )
  }
)
SelectItem.displayName = 'SelectItem'

export { Select, SelectTrigger, SelectValue, SelectContent, SelectItem }
