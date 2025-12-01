import { Typography, Paper, Box } from '@mui/material'

/**
 * AboutPage Component
 *
 * A simple static page demonstrating basic Material-UI components.
 * This is where you might put information about your application.
 */
function AboutPage() {
  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        About Filly Trckr
      </Typography>

      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h5" gutterBottom>
          Technology Stack
        </Typography>

        <Typography variant="body1" paragraph>
          <strong>Frontend:</strong>
        </Typography>
        <ul>
          <li>React 18 - UI library</li>
          <li>TypeScript - Type-safe JavaScript</li>
          <li>Material-UI (MUI) - Component library</li>
          <li>React Router - Navigation</li>
          <li>Axios - HTTP client</li>
          <li>Vite - Build tool</li>
        </ul>

        <Typography variant="body1" paragraph sx={{ mt: 2 }}>
          <strong>Backend:</strong>
        </Typography>
        <ul>
          <li>Python FastAPI</li>
          <li>PostgreSQL</li>
        </ul>
      </Paper>

      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h5" gutterBottom>
          Learning Resources
        </Typography>

        <Typography variant="body1" component="div">
          <ul>
            <li>
              <a href="https://react.dev/learn" target="_blank" rel="noopener noreferrer">
                React Documentation
              </a> - Official React tutorial and reference
            </li>
            <li>
              <a href="https://www.typescriptlang.org/docs/" target="_blank" rel="noopener noreferrer">
                TypeScript Documentation
              </a> - Learn TypeScript basics
            </li>
            <li>
              <a href="https://mui.com/material-ui/getting-started/" target="_blank" rel="noopener noreferrer">
                Material-UI Documentation
              </a> - Browse components and examples
            </li>
            <li>
              <a href="https://reactrouter.com/en/main" target="_blank" rel="noopener noreferrer">
                React Router Documentation
              </a> - Routing and navigation
            </li>
          </ul>
        </Typography>
      </Paper>
    </Box>
  )
}

export default AboutPage
