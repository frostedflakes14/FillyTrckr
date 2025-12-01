import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import App from './App'

// Create a Material-UI theme
// This defines the color scheme and styling for your entire app
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2', // Blue color for primary buttons, headers, etc.
    },
    secondary: {
      main: '#dc004e', // Pink/red for secondary elements
    },
  },
})

// This is the entry point of your React app
// ReactDOM.createRoot() attaches React to the 'root' div in index.html
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* ThemeProvider makes the MUI theme available to all components */}
    <ThemeProvider theme={theme}>
      {/* CssBaseline normalizes styles across browsers (like CSS reset) */}
      <CssBaseline />
      {/* BrowserRouter enables routing (navigation between pages) */}
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>,
)
