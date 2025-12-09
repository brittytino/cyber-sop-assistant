import { useState } from 'react'
import { storage } from '@/lib/utils/storage'

export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = storage.get<T>(key)
      return item ?? initialValue
    } catch (error) {
      console.error('Error reading from storage:', error)
      return initialValue
    }
  })

  const setValue = (value: T) => {
    try {
      setStoredValue(value)
      storage.set(key, value)
    } catch (error) {
      console.error('Error saving to storage:', error)
    }
  }

  return [storedValue, setValue]
}
