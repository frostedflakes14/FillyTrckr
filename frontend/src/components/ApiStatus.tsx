import { IconButton, Tooltip, CircularProgress } from '@mui/material'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import CancelIcon from '@mui/icons-material/Cancel'
import { useState, useEffect } from 'react'
import { checkHealth } from '../utils/api'

/**
 * ApiStatus Component
 *
 * Displays the current API connection status as an icon in the header.
 * - Green check mark: API is healthy
 * - Red X: API is unreachable or unhealthy
 * - Loading spinner: Checking status
 *
 * The component checks the API health every 30 seconds.
 */
function ApiStatus() {
  const [status, setStatus] = useState<'checking' | 'healthy' | 'unhealthy'>('checking')
  const [lastChecked, setLastChecked] = useState<Date | null>(null)

  const checkApiHealth = async () => {
    try {
      await checkHealth()
      setStatus('healthy')
      setLastChecked(new Date())
    } catch (error) {
      setStatus('unhealthy')
      setLastChecked(new Date())
    }
  }

  // Check health on mount and every 30 seconds
  useEffect(() => {
    checkApiHealth()
    const interval = setInterval(checkApiHealth, 30000)

    // Cleanup interval on unmount
    return () => clearInterval(interval)
  }, [])

  // Generate tooltip text based on status
  const getTooltipText = () => {
    const timeStr = lastChecked ? lastChecked.toLocaleTimeString() : 'Never'

    switch (status) {
      case 'healthy':
        return `API Status: Connected\nLast checked: ${timeStr}`
      case 'unhealthy':
        return `API Status: Disconnected\nLast checked: ${timeStr}`
      case 'checking':
        return 'Checking API status...'
    }
  }

  // Render different icons based on status
  const renderIcon = () => {
    switch (status) {
      case 'healthy':
        return <CheckCircleIcon sx={{ color: '#4caf50' }} />
      case 'unhealthy':
        return <CancelIcon sx={{ color: '#f44336' }} />
      case 'checking':
        return <CircularProgress size={24} sx={{ color: 'inherit' }} />
    }
  }

  return (
    <Tooltip title={getTooltipText()} arrow>
      <IconButton
        color="inherit"
        onClick={checkApiHealth}
        sx={{ ml: 1 }}
        aria-label="API status"
      >
        {renderIcon()}
      </IconButton>
    </Tooltip>
  )
}

export default ApiStatus
