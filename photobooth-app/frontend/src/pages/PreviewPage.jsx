/**
 * PreviewPage – shows the live camera preview, runs countdown, captures
 * photos, then calls onComplete with the session result.
 *
 * Props:
 *   sessionId  – active session ID
 *   photoCount – how many photos to capture
 *   onComplete(result) – called after all photos are captured & processed
 *   onError    – called on unrecoverable error
 */
import React, { useCallback, useEffect, useRef, useState } from 'react'
import CameraPreview from '../components/CameraPreview'
import Countdown from '../components/Countdown'
import { capturePhoto, processSession, startPreview, stopPreview } from '../services/api'
import styles from './PreviewPage.module.css'

const COUNTDOWN_SECONDS = 3

export default function PreviewPage({ sessionId, photoCount, onComplete, onError }) {
  const [phase, setPhase]           = useState('preview')   // preview | countdown | capturing | processing
  const [capturedCount, setCaptured] = useState(0)
  const [thumbs, setThumbs]          = useState([])
  const capturing = useRef(false)

  // Start preview on mount, stop on unmount
  useEffect(() => {
    startPreview().catch(() => onError?.('Failed to start preview'))
    return () => { stopPreview().catch(() => {}) }
  }, [onError])

  const doCapture = useCallback(async () => {
    if (capturing.current) return
    capturing.current = true
    setPhase('capturing')
    try {
      const data = await capturePhoto()
      setThumbs((t) => [...t, data.url])
      setCaptured(data.total)
      if (data.complete) {
        setPhase('processing')
        const result = await processSession(sessionId)
        onComplete(result)
      } else {
        // Wait briefly before the next countdown
        setTimeout(() => { capturing.current = false; setPhase('preview') }, 800)
      }
    } catch (err) {
      onError?.(err?.response?.data?.detail ?? 'Capture failed')
    }
  }, [sessionId, onComplete, onError])

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>Get Ready!</h2>
        <p className={styles.counter}>
          {capturedCount} / {photoCount} photos
        </p>
      </div>

      <div className={styles.previewWrapper}>
        <CameraPreview style={{ width: '100%', height: '100%' }} />
        {phase === 'countdown' && (
          <Countdown seconds={COUNTDOWN_SECONDS} onDone={doCapture} />
        )}
        {phase === 'capturing' && (
          <div className={styles.flash} />
        )}
        {phase === 'processing' && (
          <div className={styles.processingOverlay}>
            <span>✨ Creating collage…</span>
          </div>
        )}
      </div>

      {/* Thumbnail strip */}
      {thumbs.length > 0 && (
        <div className={styles.strip}>
          {thumbs.map((url, i) => (
            <img key={i} className={styles.thumb} src={url} alt={`Shot ${i + 1}`} />
          ))}
        </div>
      )}

      {phase === 'preview' && (
        <button
          className={styles.captureBtn}
          onClick={() => setPhase('countdown')}
        >
          📸 Take Photo {capturedCount + 1} of {photoCount}
        </button>
      )}
    </div>
  )
}
