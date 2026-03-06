/**
 * ResultPage – shows the generated collage and individual photos.
 * Props:
 *   result  – { session_id, photos, collage }
 *   onReset – callback to go back to the idle screen
 */
import React from 'react'
import ResultView from '../components/ResultView'
import styles from './ResultPage.module.css'

export default function ResultPage({ result, onReset }) {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>🎉 All done!</h1>
      <ResultView result={result} onReset={onReset} />
    </div>
  )
}
