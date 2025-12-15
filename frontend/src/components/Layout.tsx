import { AppBar, Toolbar, Typography, Button, Container, Box, IconButton, Tooltip, Drawer, List, ListItem, ListItemButton, ListItemText, useTheme, useMediaQuery, Divider } from '@mui/material'
import { Link, Outlet, useLocation } from 'react-router-dom'
import Brightness4Icon from '@mui/icons-material/Brightness4'
import Brightness7Icon from '@mui/icons-material/Brightness7'
import MenuIcon from '@mui/icons-material/Menu'
import { useState } from 'react'
import { useThemeMode } from '../contexts/ThemeContext'
import ApiStatus from './ApiStatus'

/**
 * Layout Component
 *
 * This component wraps all pages and provides:
 * - A top navigation bar (AppBar) - responsive for mobile/desktop
 * - Navigation links (drawer on mobile, buttons on desktop)
 * - Dark mode toggle button
 * - A container for page content
 *
 * The <Outlet /> component is where the current page's content is rendered.
 * Think of it like a placeholder that shows different pages based on the URL.
 */
function Layout() {
  const { mode, toggleTheme } = useThemeMode()
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('md'))
  const [drawerOpen, setDrawerOpen] = useState(false)
  const location = useLocation()

  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Brands', path: '/brands' },
    { label: 'Types', path: '/types' },
    { label: 'Subtypes', path: '/subtypes' },
    { label: 'Colors', path: '/colors' },
    { label: 'About', path: '/about' },
  ]

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen)
  }

  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ width: 250 }}>
      <Box sx={{ p: 2 }}>
        <Typography variant="h6">FillyTrckr</Typography>
      </Box>
      <Divider />
      <List>
        {navItems.map((item) => (
          <ListItem key={item.path} disablePadding>
            <ListItemButton
              component={Link}
              to={item.path}
              selected={location.pathname === item.path}
            >
              <ListItemText primary={item.label} />
            </ListItemButton>
          </ListItem>
        ))}
        <ListItem disablePadding>
          <ListItemButton component="a" href="/api-docs">
            <ListItemText primary="API Docs" />
          </ListItemButton>
        </ListItem>
      </List>
      <Divider />
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="body2">Theme</Typography>
        <IconButton onClick={toggleTheme} color="inherit" size="small">
          {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>
      </Box>
    </Box>
  )

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* AppBar is MUI's navigation bar component */}
      <AppBar position="static">
        <Toolbar>
          {/* Mobile menu icon */}
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}

          {/* Typography is MUI's text component */}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            FillyTrckr
          </Typography>

          {/* Desktop Navigation buttons */}
          {!isMobile && (
            <>
              {navItems.map((item) => (
                <Button key={item.path} color="inherit" component={Link} to={item.path}>
                  {item.label}
                </Button>
              ))}

              {/* API Docs - uses regular anchor tag since it goes to backend */}
              <Button color="inherit" component="a" href="/api-docs">
                API Docs
              </Button>
            </>
          )}

          {/* API status indicator */}
          <ApiStatus />

          {/* Dark mode toggle button - desktop only */}
          {!isMobile && (
            <Tooltip title={mode === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'} arrow>
              <IconButton onClick={toggleTheme} color="inherit" sx={{ ml: 1 }}>
                {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
              </IconButton>
            </Tooltip>
          )}
        </Toolbar>
      </AppBar>

      {/* Mobile Drawer */}
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile
        }}
      >
        {drawer}
      </Drawer>

      {/* Main content area */}
      <Container
        component="main"
        sx={{
          mt: { xs: 2, sm: 3, md: 4 },
          mb: { xs: 2, sm: 3, md: 4 },
          px: { xs: 2, sm: 3 },
          flex: 1
        }}
      >
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
