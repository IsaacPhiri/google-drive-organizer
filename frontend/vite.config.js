import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  server: {
    // frontend
    host: "0.0.0.0",
    port: process.env.PORT || 3000,

    // backend server
    proxy: {
      '/api': {
        target: 'https://google-drive-organizer.onrender.com',
        changeOrigin: true,
      }
    },
  },
})
