/**
 * CameraPreview – renders the live MJPEG stream from the backend.
 */
import React from 'react'
import { previewStreamUrl } from '../services/api'
import styles from './CameraPreview.module.css'

export default function CameraPreview({ style }) {
  return (
    <div className={styles.wrapper} style={style}>
      <img
        className={styles.stream}
        src={previewStreamUrl()}
        alt="Camera preview"
      />
    </div>
  )
}
