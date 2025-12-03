import { AppBar, Toolbar, Typography, Button, Container, Box } from '@mui/material'
import { Link, Outlet } from 'react-router-dom'

/**
 * Layout Component
 *
 * This component wraps all pages and provides:
 * - A top navigation bar (AppBar)
 * - Navigation links
 * - A container for page content
 *
 * The <Outlet /> component is where the current page's content is rendered.
 * Think of it like a placeholder that shows different pages based on the URL.
 */
function Layout() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* AppBar is MUI's navigation bar component */}
      <AppBar position="static">
        <Toolbar>
          {/* Typography is MUI's text component */}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Filly Trckr
          </Typography>

          {/* Navigation buttons */}
          <Button color="inherit" component={Link} to="/">
            Home
          </Button>
          <Button color="inherit" component={Link} to="/brands">
            Brands
          </Button>
          <Button color="inherit" component={Link} to="/types">
            Types
          </Button>
          <Button color="inherit" component={Link} to="/subtypes">
            Subtypes
          </Button>
          <Button color="inherit" component={Link} to="/colors">
            Colors
          </Button>
          <Button color="inherit" component={Link} to="/about">
            About
          </Button>
        </Toolbar>
      </AppBar>

      {/* Main content area */}
      <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
        {/* This is where child routes (pages) are rendered */}
        <Outlet />
      </Container>

      {/* Footer */}
      <Box component="footer" sx={{ py: 3, px: 2, mt: 'auto', backgroundColor: '#f5f5f5' }}>
        <Container>
          <Typography variant="body2" color="text.secondary" align="center">
            © 2025 Filly Trckr
          </Typography>
        </Container>
      </Box>
    </Box>
  )
}

export default Layout
