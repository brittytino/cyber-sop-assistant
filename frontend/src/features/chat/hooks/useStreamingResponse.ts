import { useState, useCallback } from 'react'

export function useStreamingResponse() {
  const [streamingText, setStreamingText] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)

  const simulateStreaming = useCallback((text: string, speed: number = 20) => {
    setIsStreaming(true)
    setStreamingText('')

    let index = 0
    const interval = setInterval(() => {
      if (index < text.length) {
        setStreamingText((prev) => prev + text[index])
        index++
      } else {
        setIsStreaming(false)
        clearInterval(interval)
      }
    }, speed)

    return () => clearInterval(interval)
  }, [])

  return {
    streamingText,
    isStreaming,
    simulateStreaming,
    resetStreaming: () => {
      setStreamingText('')
      setIsStreaming(false)
    },
  }
}
