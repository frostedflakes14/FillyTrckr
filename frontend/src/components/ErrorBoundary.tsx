import React, { Component, ErrorInfo, ReactNode } from 'react'
import { Box, Container, Typography, Button, Paper } from '@mui/material'
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline'

interface Props {
  children?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

/**
 * Error Boundary Component
 *
 * Catches JavaScript errors anywhere in the child component tree and displays
 * a fallback UI instead of crashing the entire app with a blank page.
 *
 * Common causes:
 * - Invalid date/timestamp parsing
 * - Network errors when fetching data
 * - Undefined property access
 */
class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    }
  }

  static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return {
      hasError: true,
      error,
      errorInfo: null
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log the error to console for debugging
    console.error('ErrorBoundary caught an error:', error, errorInfo)

    this.setState({
      error,
      errorInfo
    })
  }

  handleReset = () => {
    // Reset the error boundary and try again
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null
    })
  }

  handleReload = () => {
    // Reload the entire page
    window.location.reload()
  }

  render() {
    if (this.state.hasError) {
      return (
        <Container maxWidth="md">
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              minHeight: '100vh',
              py: 4
            }}
          >
            <Paper
              elevation={3}
              sx={{
                p: 4,
                textAlign: 'center',
                maxWidth: 600,
                width: '100%'
              }}
            >
              <ErrorOutlineIcon
                sx={{
                  fontSize: 80,
                  color: 'error.main',
                  mb: 2
                }}
              />

              <Typography variant="h4" gutterBottom color="error">
                Oops! Something went wrong
              </Typography>

              <Typography variant="body1" color="text.secondary" paragraph>
                We encountered an unexpected error while rendering this page.
                This could be due to invalid data or a temporary issue.
              </Typography>

              {this.state.error && (
                <Paper
                  variant="outlined"
                  sx={{
                    p: 2,
                    mb: 3,
                    backgroundColor: 'grey.100',
                    textAlign: 'left',
                    overflow: 'auto'
                  }}
                >
                  <Typography
                    variant="caption"
                    component="pre"
                    sx={{
                      whiteSpace: 'pre-wrap',
                      wordBreak: 'break-word',
                      fontFamily: 'monospace',
                      fontSize: '0.75rem'
                    }}
                  >
                    {this.state.error.toString()}
                    {this.state.errorInfo && (
                      '\n\n' + this.state.errorInfo.componentStack
                    )}
                  </Typography>
                </Paper>
              )}

              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={this.handleReset}
                >
                  Try Again
                </Button>

                <Button
                  variant="outlined"
                  color="primary"
                  onClick={this.handleReload}
                >
                  Reload Page
                </Button>

                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={() => window.location.href = '/'}
                >
                  Go Home
                </Button>
              </Box>
            </Paper>
          </Box>
        </Container>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
