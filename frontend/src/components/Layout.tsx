import { AppBar, Toolbar, Typography, Button, Container, Box, IconButton, Tooltip } from '@mui/material'
import { Link, Outlet } from 'react-router-dom'
import Brightness4Icon from '@mui/icons-material/Brightness4'
import Brightness7Icon from '@mui/icons-material/Brightness7'
import { useThemeMode } from '../contexts/ThemeContext'
import ApiStatus from './ApiStatus'

/**
 * Layout Component
 *
 * This component wraps all pages and provides:
 * - A top navigation bar (AppBar)
 * - Navigation links
 * - Dark mode toggle button
 * - A container for page content
 *
 * The <Outlet /> component is where the current page's content is rendered.
 * Think of it like a placeholder that shows different pages based on the URL.
 */
function Layout() {
  const { mode, toggleTheme } = useThemeMode()

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* AppBar is MUI's navigation bar component */}
      <AppBar position="static">
        <Toolbar>
          {/* Typography is MUI's text component */}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            FillyTrckr
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
          <Button color="inherit" component={Link} to="/rolls">
            Rolls
          </Button>
          <Button color="inherit" component={Link} to="/about">
            About
          </Button>

          {/* API status indicator */}
          <ApiStatus />

          {/* Dark mode toggle button */}
          <Tooltip title={mode === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'} arrow>
            <IconButton onClick={toggleTheme} color="inherit" sx={{ ml: 1 }}>
              {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>

      {/* Main content area */}
      <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
        {/* This is where child routes (pages) are rendered */}
        <Outlet />
      </Container>

      {/* Footer */}
      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: 'footer.main'
        }}
      >
        <Container>
          <Typography variant="body2" color="text.secondary" align="center">
            © 2025 FillyTrckr
          </Typography>
        </Container>
      </Box>
    </Box>
  )
}

export default Layout
