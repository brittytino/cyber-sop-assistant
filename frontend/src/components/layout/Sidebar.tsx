import React from 'react'
import { MessageSquare, FileText, CheckSquare, BarChart3, HelpCircle } from 'lucide-react'
import { cn } from '@/lib/utils/cn'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const menuItems = [
    { icon: MessageSquare, label: 'Chat', href: '#' },
    { icon: FileText, label: 'Complaints', href: '#complaints' },
    { icon: CheckSquare, label: 'Evidence', href: '#evidence' },
    { icon: BarChart3, label: 'Analytics', href: '#analytics' },
    { icon: HelpCircle, label: 'Help', href: '#help' },
  ]

  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] w-64 bg-background border-r',
          'transform transition-transform duration-300 ease-in-out lg:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <nav className="p-4 space-y-2">
          {menuItems.map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-accent transition-colors"
              onClick={onClose}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.label}</span>
            </a>
          ))}
        </nav>
      </aside>
    </>
  )
}
