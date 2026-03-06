/**
 * LayoutPage – let the user choose a collage layout then start the session.
 * Props:
 *   onConfirm(layout, photoCount) – callback with the chosen settings
 */
import React, { useState } from 'react'
import LayoutSelector from '../components/LayoutSelector'
import styles from './LayoutPage.module.css'

const PHOTO_COUNTS = { '2x2': 4, '3x2': 6, '1x3': 3, '2x1': 2 }

export default function LayoutPage({ onConfirm }) {
  const [layout, setLayout] = useState('2x2')

  const photoCount = PHOTO_COUNTS[layout] ?? 4

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Choose Layout</h1>
      <p className={styles.subtitle}>Select how your photos will be arranged</p>

      <LayoutSelector selected={layout} onChange={setLayout} />

      <p className={styles.info}>
        {photoCount} photo{photoCount !== 1 ? 's' : ''} will be taken
      </p>

      <button className={styles.btn} onClick={() => onConfirm(layout, photoCount)}>
        Continue →
      </button>
    </div>
  )
}
