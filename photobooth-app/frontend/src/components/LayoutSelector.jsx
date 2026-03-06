/**
 * LayoutSelector – displays the available collage layouts.
 * Props:
 *   selected   – currently selected layout key
 *   onChange   – callback(layoutKey)
 */
import React from 'react'
import styles from './LayoutSelector.module.css'

const LAYOUTS = [
  { key: '2x2', label: '2 × 2', description: '4 photos', grid: [[1, 1], [1, 1]] },
  { key: '3x2', label: '3 × 2', description: '6 photos', grid: [[1, 1, 1], [1, 1, 1]] },
  { key: '1x3', label: '1 × 3', description: '3 photos', grid: [[1], [1], [1]] },
  { key: '2x1', label: '2 × 1', description: '2 photos', grid: [[1, 1]] },
]

function GridPreview({ grid }) {
  return (
    <div className={styles.gridPreview}>
      {grid.map((row, ri) => (
        <div key={ri} className={styles.gridRow}>
          {row.map((_, ci) => (
            <div key={ci} className={styles.gridCell} />
          ))}
        </div>
      ))}
    </div>
  )
}

export default function LayoutSelector({ selected, onChange }) {
  return (
    <div className={styles.container}>
      {LAYOUTS.map((layout) => (
        <button
          key={layout.key}
          className={`${styles.card} ${selected === layout.key ? styles.active : ''}`}
          onClick={() => onChange(layout.key)}
        >
          <GridPreview grid={layout.grid} />
          <span className={styles.label}>{layout.label}</span>
          <span className={styles.desc}>{layout.description}</span>
        </button>
      ))}
    </div>
  )
}
