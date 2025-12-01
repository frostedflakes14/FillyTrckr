import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import AboutPage from './pages/AboutPage'

/**
 * Main App Component
 *
 * This defines the routes (pages) of your application.
 * Think of Routes like URL endpoints in FastAPI, but for the frontend.
 *
 * The Layout component wraps all pages and provides the navigation bar.
 */
function App() {
  return (
    <Routes>
      {/* Layout is a wrapper that appears on all pages */}
      <Route path="/" element={<Layout />}>
        {/* index means this is the default route at "/" */}
        <Route index element={<HomePage />} />
        <Route path="about" element={<AboutPage />} />
        {/* Add more routes here as you build features */}
      </Route>
    </Routes>
  )
}

export default App
