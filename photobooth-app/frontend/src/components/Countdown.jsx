/**
 * Countdown – animated countdown timer component.
 * Props:
 *   seconds  – initial count (e.g. 3)
 *   onDone   – callback invoked when the counter reaches 0
 */
import React, { useEffect, useState } from 'react'
import styles from './Countdown.module.css'

export default function Countdown({ seconds = 3, onDone }) {
  const [count, setCount] = useState(seconds)

  useEffect(() => {
    if (count <= 0) {
      onDone?.()
      return
    }
    const id = setTimeout(() => setCount((c) => c - 1), 1000)
    return () => clearTimeout(id)
  }, [count, onDone])

  return (
    <div className={styles.overlay}>
      <span className={`${styles.number} ${styles.animate}`} key={count}>
        {count > 0 ? count : '📸'}
      </span>
    </div>
  )
}
