import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] })
  ],
  // for hot module replacements
  server: {
    host: true, 
    port: 5173,
    watch: {
      usePolling: true, 
    },
    hmr: {
      clientPort: 5173, 
    },
  },
  // for absolute paths
  resolve: {
    alias: {
      src: "/src",
    },
  },
})
