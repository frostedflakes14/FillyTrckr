# FillyTrckr Frontend

React + TypeScript frontend application with Material-UI.

## Prerequisites

- Node.js 18+ and npm (or use Docker)
- Backend running on `http://localhost:8000`

## Development Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Run development server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 3. Build for production

```bash
npm run build
```

This creates optimized files in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable React components
│   │   └── Layout.tsx  # Navigation bar and page wrapper
│   ├── pages/          # Page components (one per route)
│   │   ├── HomePage.tsx
│   │   └── AboutPage.tsx
│   ├── utils/          # Utility functions
│   │   └── api.ts      # API client configuration
│   ├── App.tsx         # Main app component with routes
│   ├── main.tsx        # Entry point
│   └── vite-env.d.ts   # TypeScript definitions
├── index.html          # HTML template
├── package.json        # Dependencies and scripts
├── tsconfig.json       # TypeScript configuration
├── vite.config.ts      # Vite build tool configuration
└── Dockerfile          # Docker production build
```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint to check code quality

## Key Technologies

- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **Material-UI (MUI)** - Component library
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

## Learning React + TypeScript

### Core Concepts

1. **Components** - Building blocks of React apps (like Python classes)
2. **Props** - Data passed to components (like function parameters)
3. **State** - Component's internal data (like instance variables)
4. **Hooks** - Functions that let you use React features
   - `useState` - Manage component state
   - `useEffect` - Run code when component loads or updates

### Example Component

```tsx
import { useState } from 'react'
import { Button, Typography } from '@mui/material'

function Counter() {
  // State: [value, setter function]
  const [count, setCount] = useState(0)

  return (
    <div>
      <Typography>Count: {count}</Typography>
      <Button onClick={() => setCount(count + 1)}>
        Increment
      </Button>
    </div>
  )
}
```

### Making API Calls

```tsx
import { useState, useEffect } from 'react'
import { api } from './utils/api'

function DataComponent() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch data when component loads
    const fetchData = async () => {
      try {
        const response = await api.get('/endpoint')
        setData(response.data)
      } catch (error) {
        console.error('Error:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, []) // Empty array = run once on mount

  if (loading) return <div>Loading...</div>

  return <div>{/* Render data */}</div>
}
```

## Next Steps

1. **Explore Material-UI components**: https://mui.com/material-ui/getting-started/
2. **Learn React basics**: https://react.dev/learn
3. **Add more pages** - Create new files in `src/pages/`
4. **Build forms** - Use MUI form components to interact with your API
5. **Add authentication** - Protect routes and store user tokens

## Docker

Build and run with Docker:

```bash
# Build image
docker build -t fillytrckr-frontend .

# Run container
docker run -p 80:80 fillytrckr-frontend
```

Or use docker-compose from the root directory:

```bash
docker-compose up
```
