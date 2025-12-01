import { useState, useEffect } from 'react'
import { Typography, Paper, Box, CircularProgress, Alert } from '@mui/material'
import axios from 'axios'

/**
 * HomePage Component
 *
 * This demonstrates:
 * - useState: React's way of managing component state (like class attributes)
 * - useEffect: Runs code when component loads (like __init__ but async)
 * - API calls with axios
 * - Conditional rendering based on state
 */
function HomePage() {
  // State variables (like instance variables in a Python class)
  // useState returns [value, setter_function]
  const [apiStatus, setApiStatus] = useState<'healthy' | 'unhealthy' | null>(null)
  const [apiDetail, setApiDetail] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // useEffect runs when the component first renders
  // Similar to making an API call in __init__ (but async)
  useEffect(() => {
    // Define an async function to fetch data from your FastAPI backend
    const fetchApiStatus = async () => {
      try {
        // Make a GET request to your backend
        // The proxy in vite.config.ts forwards this to http://localhost:8000
        const response = await axios.get('/api/health')

        // Update state with the response
        setApiStatus(response.data.status)
        setApiDetail(response.data.detail || null)
        setError(null)
      } catch (err) {
        // Handle errors (like try/except in Python)
        setError('Failed to connect to API. Make sure your backend is running on port 8000.')
        console.error('API Error:', err)
      } finally {
        // Always run this, whether success or error
        setLoading(false)
      }
    }

    // Call the function
    fetchApiStatus()
  }, []) // Empty array means "run only once when component mounts"

  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome to FillyTrckr
      </Typography>

      <Typography variant="body1" paragraph>
        This is a React + TypeScript frontend connected to your FastAPI backend.
      </Typography>

      {/* Paper is a MUI component that creates a card-like container */}
      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h5" gutterBottom>
          API Status
        </Typography>

        {/* Conditional rendering based on state */}
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
            <CircularProgress />
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {!loading && !error && apiStatus && (
          <Alert
            severity={apiStatus === 'healthy' ? 'success' : 'warning'}
            sx={{ mt: 2 }}
          >
            {apiStatus === 'healthy'
              ? 'API is healthy and running'
              : apiDetail || 'API is unhealthy'}
          </Alert>
        )}
      </Paper>

      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h5" gutterBottom>
          Next Steps
        </Typography>
        <Typography variant="body1" component="div">
          <ul>
            <li>Review the code in <code>src/pages/HomePage.tsx</code></li>
            <li>Check out Material-UI components at <a href="https://mui.com/material-ui/getting-started/" target="_blank">mui.com</a></li>
            <li>Create new pages for your application features</li>
            <li>Build forms to interact with your FastAPI endpoints</li>
          </ul>
        </Typography>
      </Paper>
    </Box>
  )
}

export default HomePage
