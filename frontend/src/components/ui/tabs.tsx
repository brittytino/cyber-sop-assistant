import * as React from 'react'
import { cn } from '@/lib/utils'

const Tabs = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { value: string; onValueChange: (value: string) => void }
>(({ className, value, onValueChange, ...props }, ref) => (
  <div ref={ref} className={cn('', className)} {...props} />
))
Tabs.displayName = 'Tabs'

const TabsList = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'inline-flex h-10 items-center justify-center rounded-md bg-gray-100 dark:bg-gray-800 p-1 text-gray-500 dark:text-gray-400',
      className
    )}
    {...props}
  />
))
TabsList.displayName = 'TabsList'

const TabsTrigger = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement> & { value: string }
>(({ className, value, ...props }, ref) => {
  const parent = React.useContext(TabsContext)

  return (
    <button
      ref={ref}
      type="button"
      onClick={() => parent?.onValueChange(value)}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-white transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
        parent?.value === value
          ? 'bg-white dark:bg-gray-950 text-gray-950 dark:text-gray-50 shadow-sm'
          : 'hover:bg-gray-200 dark:hover:bg-gray-700',
        className
      )}
      {...props}
    />
  )
})
TabsTrigger.displayName = 'TabsTrigger'

const TabsContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { value: string }
>(({ className, value, children, ...props }, ref) => {
  const parent = React.useContext(TabsContext)

  if (parent?.value !== value) return null

  return (
    <div
      ref={ref}
      className={cn(
        'mt-2 ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
})
TabsContent.displayName = 'TabsContent'

const TabsContext = React.createContext<{
  value: string
  onValueChange: (value: string) => void
} | null>(null)

const TabsProvider = Tabs as React.ForwardRefExoticComponent<
  React.HTMLAttributes<HTMLDivElement> & {
    value: string
    onValueChange: (value: string) => void
  } & React.RefAttributes<HTMLDivElement>
> & {
  (props: React.HTMLAttributes<HTMLDivElement> & {
    value: string
    onValueChange: (value: string) => void
  }): JSX.Element
}

const TabsComponent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { value: string; onValueChange: (value: string) => void }
>(({ value, onValueChange, ...props }, ref) => (
  <TabsContext.Provider value={{ value, onValueChange }}>
    <Tabs ref={ref} value={value} onValueChange={onValueChange} {...props} />
  </TabsContext.Provider>
))
TabsComponent.displayName = 'Tabs'

export { TabsComponent as Tabs, TabsList, TabsTrigger, TabsContent }
