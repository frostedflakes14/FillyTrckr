import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ThemeContextProvider } from './contexts/ThemeContext'
import ErrorBoundary from './components/ErrorBoundary'
import App from './App'

// This is the entry point of your React app
// ReactDOM.createRoot() attaches React to the 'root' div in index.html
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* ErrorBoundary catches any rendering errors and shows a friendly error page */}
    <ErrorBoundary>
      {/* ThemeContextProvider manages light/dark mode and provides theme to all components */}
      <ThemeContextProvider>
        {/* BrowserRouter enables routing (navigation between pages) */}
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </ThemeContextProvider>
    </ErrorBoundary>
  </React.StrictMode>,
)
