/**
 * api.js – thin wrapper around the PhotoBooth FastAPI backend.
 */
import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || ''

const api = axios.create({ baseURL: BASE })

/** Detect all connected cameras. */
export const listCameras = () =>
  api.get('/list-cameras').then((r) => r.data)

/** Select a camera by its ID. */
export const selectCamera = (camera_id) =>
  api.post('/select-camera', { camera_id }).then((r) => r.data)

/** Start a new session. */
export const startSession = (layout, photo_count) =>
  api.post('/start-session', { layout, photo_count }).then((r) => r.data)

/** Start the camera preview stream. */
export const startPreview = () =>
  api.post('/start-preview').then((r) => r.data)

/** Stop the camera preview stream. */
export const stopPreview = () =>
  api.delete('/stop-preview').then((r) => r.data)

/** Capture one photo in the current session. */
export const capturePhoto = () =>
  api.post('/capture').then((r) => r.data)

/** Generate the collage for a session. */
export const processSession = (session_id) =>
  api.post('/process', { session_id }).then((r) => r.data)

/** Fetch the result for a session. */
export const getResult = (session_id) =>
  api.get(`/result/${session_id}`).then((r) => r.data)

/** URL of the MJPEG preview stream (use directly as <img src>). */
export const previewStreamUrl = () => `${BASE}/preview-stream`
