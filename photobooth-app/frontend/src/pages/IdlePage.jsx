/**
 * IdlePage – the "attract" screen shown between sessions.
 * Props:
 *   onStart – callback to advance to camera selection
 */
import React from 'react'
import styles from './IdlePage.module.css'

export default function IdlePage({ onStart }) {
  return (
    <div className={styles.container}>
      <div className={styles.logo}>📸</div>
      <h1 className={styles.title}>PHOTO BOOTH</h1>
      <p className={styles.subtitle}>Capture the moment together</p>
      <button className={styles.startBtn} onClick={onStart}>
        TAP TO START
      </button>
    </div>
  )
}
