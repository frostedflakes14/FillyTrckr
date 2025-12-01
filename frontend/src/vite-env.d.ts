/// <reference types="vite/client" />

/**
 * TypeScript definitions for Vite environment variables
 *
 * This file tells TypeScript about environment variables available in your app.
 * In Vite, env variables are accessed via import.meta.env
 */

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  // Add more env variables here as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
