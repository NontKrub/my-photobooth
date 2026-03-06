/**
 * App.jsx – top-level state machine driving the photobooth workflow.
 *
 * Flow:
 *   idle → cameraSelect → layoutSelect → preview → result → idle
 */
import React, { useState, useCallback } from 'react'
import IdlePage          from './pages/IdlePage'
import CameraSelectPage  from './pages/CameraSelectPage'
import LayoutPage        from './pages/LayoutPage'
import PreviewPage       from './pages/PreviewPage'
import ResultPage        from './pages/ResultPage'
import { startSession }  from './services/api'
import styles            from './App.module.css'

const SCREEN = {
  IDLE:    'idle',
  CAMERA:  'camera',
  LAYOUT:  'layout',
  PREVIEW: 'preview',
  RESULT:  'result',
}

export default function App() {
  const [screen,     setScreen]     = useState(SCREEN.IDLE)
  const [sessionId,  setSessionId]  = useState(null)
  const [photoCount, setPhotoCount] = useState(4)
  const [result,     setResult]     = useState(null)
  const [error,      setError]      = useState(null)

  const reset = useCallback(() => {
    setScreen(SCREEN.IDLE)
    setSessionId(null)
    setResult(null)
    setError(null)
  }, [])

  const handleStart = () => setScreen(SCREEN.CAMERA)

  const handleCameraSelect = () => setScreen(SCREEN.LAYOUT)

  const handleLayoutConfirm = async (layout, count) => {
    try {
      const data = await startSession(layout, count)
      setSessionId(data.session_id)
      setPhotoCount(count)
      setScreen(SCREEN.PREVIEW)
    } catch {
      setError('Failed to start session. Is the backend running?')
    }
  }

  const handleComplete = (res) => {
    setResult(res)
    setScreen(SCREEN.RESULT)
  }

  const handleError = (msg) => {
    setError(msg)
  }

  return (
    <div className={styles.app}>
      {error && (
        <div className={styles.errorBanner}>
          ⚠ {error}
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {screen === SCREEN.IDLE   && <IdlePage onStart={handleStart} />}
      {screen === SCREEN.CAMERA && <CameraSelectPage onSelect={handleCameraSelect} />}
      {screen === SCREEN.LAYOUT && <LayoutPage onConfirm={handleLayoutConfirm} />}
      {screen === SCREEN.PREVIEW && (
        <PreviewPage
          sessionId={sessionId}
          photoCount={photoCount}
          onComplete={handleComplete}
          onError={handleError}
        />
      )}
      {screen === SCREEN.RESULT && (
        <ResultPage result={result} onReset={reset} />
      )}
    </div>
  )
}
