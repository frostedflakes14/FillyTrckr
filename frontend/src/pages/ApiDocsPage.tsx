import { Box } from '@mui/material'

/**
 * ApiDocsPage Component
 *
 * This page embeds the FastAPI documentation (Swagger UI) within the app layout.
 * The iframe displays the /api-docs endpoint from the backend.
 */
function ApiDocsPage() {
  return (
    <Box
      sx={{
        position: 'fixed',
        top: '64px', // Height of AppBar
        left: 0,
        right: 0,
        bottom: '72px', // Approximate height of footer
        width: '100vw',
        height: 'auto',
        margin: 0,
        padding: 0,
      }}
    >
      <iframe
        src="/api-docs"
        style={{
          width: '100%',
          height: '100%',
          border: 'none',
          margin: 0,
          padding: 0,
          display: 'block',
        }}
        title="API Documentation"
      />
    </Box>
  )
}

export default ApiDocsPage
