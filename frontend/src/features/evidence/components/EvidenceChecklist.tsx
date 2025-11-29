import React from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { ChecklistItem } from './ChecklistItem'
import { EvidenceItem } from '../types/evidence.types'

interface EvidenceChecklistProps {
  items: EvidenceItem[]
  onToggle: (index: number) => void
}

export const EvidenceChecklist: React.FC<EvidenceChecklistProps> = ({ items, onToggle }) => {
  const progress = items.filter((item) => item.collected).length
  const total = items.length

  return (
    <Card>
      <CardHeader>
        <CardTitle>Evidence Collection Progress: {progress}/{total}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {items.map((item, index) => (
            <ChecklistItem
              key={index}
              item={item}
              onToggle={() => onToggle(index)}
            />
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
