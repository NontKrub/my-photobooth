import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/list-cameras':   'http://localhost:8000',
      '/select-camera':  'http://localhost:8000',
      '/start-session':  'http://localhost:8000',
      '/start-preview':  'http://localhost:8000',
      '/stop-preview':   'http://localhost:8000',
      '/preview-stream': 'http://localhost:8000',
      '/capture':        'http://localhost:8000',
      '/process':        'http://localhost:8000',
      '/result':         'http://localhost:8000',
      '/sessions':       'http://localhost:8000',
      '/photos':         'http://localhost:8000',
    },
  },
})
