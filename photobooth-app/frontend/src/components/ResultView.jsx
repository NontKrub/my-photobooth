/**
 * ResultView – displays captured photos and the generated collage.
 * Props:
 *   result   – { session_id, photos: [], collage: string|null }
 *   onReset  – callback to restart the photobooth
 */
import React from 'react'
import styles from './ResultView.module.css'

export default function ResultView({ result, onReset }) {
  if (!result) return null

  return (
    <div className={styles.container}>
      {result.collage && (
        <div className={styles.collageWrapper}>
          <h2 className={styles.heading}>Your Collage</h2>
          <img
            className={styles.collage}
            src={result.collage}
            alt="Collage"
          />
          <a
            className={styles.download}
            href={result.collage}
            download={`collage_${result.session_id}.jpg`}
          >
            ⬇ Download Collage
          </a>
        </div>
      )}

      <div className={styles.strip}>
        {result.photos.map((url, i) => (
          <img key={i} className={styles.thumb} src={url} alt={`Photo ${i + 1}`} />
        ))}
      </div>

      <button className={styles.resetBtn} onClick={onReset}>
        🔄 New Session
      </button>
    </div>
  )
}
