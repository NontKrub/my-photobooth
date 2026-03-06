/**
 * CameraSelectPage – detects connected cameras and lets the user pick one.
 * Props:
 *   onSelect(cameraId) – callback once a camera is chosen
 */
import React, { useEffect, useState } from 'react'
import { listCameras, selectCamera } from '../services/api'
import styles from './CameraSelectPage.module.css'

export default function CameraSelectPage({ onSelect }) {
  const [cameras, setCameras] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selecting, setSelecting] = useState(null)

  useEffect(() => {
    listCameras()
      .then((data) => setCameras(data.cameras))
      .catch(() => setError('Failed to detect cameras. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [])

  const handleSelect = async (camera) => {
    setSelecting(camera.id)
    try {
      await selectCamera(camera.id)
      onSelect(camera.id)
    } catch {
      setError('Failed to select camera.')
      setSelecting(null)
    }
  }

  const cameraIcon = (type) => (type === 'gphoto2' ? '📷' : '🎥')

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Select Camera</h1>

      {loading && <p className={styles.status}>Detecting cameras…</p>}
      {error   && <p className={styles.error}>{error}</p>}

      {!loading && cameras.length === 0 && (
        <p className={styles.status}>No cameras detected.</p>
      )}

      <div className={styles.grid}>
        {cameras.map((cam) => (
          <button
            key={cam.id}
            className={`${styles.card} ${selecting === cam.id ? styles.loading : ''}`}
            onClick={() => handleSelect(cam)}
            disabled={!!selecting}
          >
            <span className={styles.icon}>{cameraIcon(cam.type)}</span>
            <span className={styles.name}>{cam.name}</span>
            <span className={styles.meta}>
              {cam.type === 'gphoto2' ? cam.port : cam.resolution}
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}
