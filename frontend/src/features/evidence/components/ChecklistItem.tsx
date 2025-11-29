import React from 'react'
import { Checkbox } from '@/components/ui/checkbox'
import { EvidenceItem } from '../types/evidence.types'

interface ChecklistItemProps {
  item: EvidenceItem
  onToggle: () => void
}

export const ChecklistItem: React.FC<ChecklistItemProps> = ({ item, onToggle }) => {
  return (
    <div className="flex items-start space-x-3 p-3 border rounded-lg">
      <Checkbox
        id={item.type}
        checked={item.collected}
        onChange={onToggle}
      />
      <div className="flex-1">
        <label htmlFor={item.type} className="text-sm font-medium cursor-pointer">
          {item.description}
          {item.required && <span className="text-destructive ml-1">*</span>}
        </label>
        {item.instructions && (
          <p className="text-xs text-muted-foreground mt-1">{item.instructions}</p>
        )}
      </div>
    </div>
  )
}
