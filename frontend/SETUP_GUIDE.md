# Frontend Setup Guide

## ⚠️ Prerequisites Installation Required

You need to install Node.js before you can run the frontend.

### Installing Node.js

**Option 1: Download from official website (Recommended)**
1. Go to https://nodejs.org/
2. Download the LTS (Long Term Support) version
3. Run the installer
4. Restart your terminal after installation

**Option 2: Using Windows Package Manager (winget)**
```bash
winget install OpenJS.NodeJS.LTS
```

**Verify installation:**
```bash
node --version   # Should show v20.x.x or higher
npm --version    # Should show v10.x.x or higher
```

---

## 🚀 Quick Start (After Node.js is installed)

### 1. Navigate to the frontend directory
```bash
cd c:/Users/fchri/Desktop/GIT/FillyTrckr/frontend
```

### 2. Install dependencies
```bash
npm install
```
This will take a few minutes and create a `node_modules` folder with all dependencies.

### 3. Start the development server
```bash
npm run dev
```

The application will be available at: http://localhost:3000

### 4. In another terminal, make sure your backend is running
```bash
cd c:/Users/fchri/Desktop/GIT/FillyTrckr
# Run your FastAPI backend (adjust command as needed)
python backend/main.py
```

---

## 📚 What Did We Just Create?

### Project Structure Overview

```
frontend/
├── src/                          # All your source code
│   ├── components/               # Reusable UI components
│   │   └── Layout.tsx           # Navigation bar wrapper
│   ├── pages/                   # Page components (one per route)
│   │   ├── HomePage.tsx         # Main landing page (demos API call)
│   │   └── AboutPage.tsx        # About page
│   ├── utils/                   # Helper functions
│   │   └── api.ts              # Centralized API configuration
│   ├── App.tsx                 # Main app (defines routes)
│   ├── main.tsx                # Entry point (starts React)
│   └── vite-env.d.ts          # TypeScript definitions
│
├── public/                      # Static assets (if needed)
├── index.html                   # Single HTML file
├── package.json                 # Dependencies (like requirements.txt)
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Build tool configuration
├── Dockerfile                   # Production Docker image
├── nginx.conf                   # Production web server config
└── README.md                    # Documentation
```

### Key Files Explained

**package.json** - Defines all dependencies and scripts
- Like Python's `requirements.txt` + setup.py combined
- Lists React, TypeScript, Material-UI, etc.

**tsconfig.json** - TypeScript compiler settings
- Enables strict type checking (like Python type hints on steroids)

**vite.config.ts** - Development server configuration
- Proxies `/api/*` requests to your FastAPI backend (port 8000)
- Hot reload for instant updates when you save files

**src/main.tsx** - Application entry point
- Sets up Material-UI theme
- Wraps app with providers (theme, routing)

**src/App.tsx** - Route definitions
- Maps URLs to components (like FastAPI routes but for frontend)
- `/` → HomePage
- `/about` → AboutPage

**src/components/Layout.tsx** - Navigation wrapper
- Material-UI AppBar (navigation bar)
- Wraps all pages with consistent header/footer

**src/pages/HomePage.tsx** - Main page with API demo
- Shows loading spinner
- Fetches data from `/api/health`
- Displays response or error

**src/utils/api.ts** - Centralized API client
- Configures axios (HTTP library)
- Easy to add authentication headers later

---

## 🎨 Material-UI Components Used

We're using **Material-UI (MUI)** - a popular React component library that implements Google's Material Design.

### Components in the Project

1. **AppBar + Toolbar** - Top navigation bar
2. **Typography** - Styled text (headings, paragraphs)
3. **Button** - Clickable buttons with Material Design styling
4. **Container** - Responsive container for content
5. **Box** - Flexible container for layout
6. **Paper** - Card-like surface with shadow
7. **CircularProgress** - Loading spinner
8. **Alert** - Error/success messages

### Explore More Components

Browse the full component library: https://mui.com/material-ui/getting-started/

Common ones you'll use:
- **TextField** - Form inputs
- **Select** - Dropdown menus
- **Table** - Data tables
- **Dialog** - Modal popups
- **Drawer** - Side navigation
- **Card** - Content cards
- **Grid** - Responsive layout grid

---

## 🔧 Development Workflow

### Making Changes

1. **Edit files** - Save any `.tsx` file in `src/`
2. **Auto reload** - Browser updates automatically
3. **Check console** - Browser console shows errors/logs

### Adding a New Page

1. Create `src/pages/NewPage.tsx`:
```tsx
import { Typography, Box } from '@mui/material'

function NewPage() {
  return (
    <Box>
      <Typography variant="h3">New Page</Typography>
      <Typography>Content here</Typography>
    </Box>
  )
}

export default NewPage
```

2. Add route in `src/App.tsx`:
```tsx
import NewPage from './pages/NewPage'

// Inside <Route path="/" element={<Layout />}>
<Route path="newpage" element={<NewPage />} />
```

3. Add navigation link in `src/components/Layout.tsx`:
```tsx
<Button color="inherit" component={Link} to="/newpage">
  New Page
</Button>
```

### Calling Your API

Use the `api` utility from `src/utils/api.ts`:

```tsx
import { useState, useEffect } from 'react'
import { api } from '../utils/api'

function MyComponent() {
  const [data, setData] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/your-endpoint')
        setData(response.data)
      } catch (error) {
        console.error('Error:', error)
      }
    }
    fetchData()
  }, [])

  return <div>{/* render data */}</div>
}
```

---

## 🐛 Common Issues

### Port already in use
If port 3000 is busy, Vite will suggest another port or you can specify:
```bash
npm run dev -- --port 3001
```

### Can't connect to API
1. Make sure backend is running on port 8000
2. Check `vite.config.ts` proxy configuration
3. Look at browser console (F12) for CORS errors

### TypeScript errors
- Red squiggles are type errors
- Most will go away after `npm install`
- You can hover over them for explanations

---

## 📖 Learning Path

### Week 1: JavaScript/TypeScript Basics
- Variables: `const`, `let`
- Functions: arrow functions `() => {}`
- Arrays: `map()`, `filter()`, `forEach()`
- Objects: `{ key: value }`
- Async/await: like Python's async/await
- Promises: like Python's futures

**Resource:** https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html

### Week 2: React Fundamentals
- **Components**: Functions that return JSX (HTML-like syntax)
- **Props**: Data passed to components (like function parameters)
- **State**: Component's internal data (`useState` hook)
- **Effects**: Run code on component mount (`useEffect` hook)
- **Events**: `onClick`, `onChange`, etc.

**Resource:** https://react.dev/learn

### Week 3: Material-UI
- Browse components
- Copy/paste examples
- Customize with `sx` prop
- Use the `Grid` system for layouts

**Resource:** https://mui.com/material-ui/getting-started/

### Week 4: Build Your Features
- Create forms with MUI components
- Connect to your FastAPI endpoints
- Handle loading states and errors
- Add authentication if needed

---

## 🏗️ Building for Production

### Development vs Production

**Development** (`npm run dev`):
- Fast refresh (instant updates)
- Helpful error messages
- Source maps for debugging
- Runs on port 3000

**Production** (`npm run build`):
- Optimized and minified
- No debugging info
- Smaller file sizes
- Static files ready to deploy

### Build Steps

```bash
# Build the application
npm run build

# Preview the build locally
npm run preview
```

This creates a `dist/` folder with optimized files.

### Docker Deployment

The Dockerfile creates a production-ready image:
- Builds React app
- Serves with nginx
- Proxies `/api/*` to backend

```bash
cd frontend
docker build -t fillytrckr-frontend .
docker run -p 80:80 fillytrckr-frontend
```

---

## 🎯 Next Steps

1. **Install Node.js** (if you haven't already)
2. **Run `npm install`** in the frontend directory
3. **Start dev server** with `npm run dev`
4. **Open http://localhost:3000** in your browser
5. **Make sure backend is running** on port 8000
6. **Explore the code** - Start with `src/pages/HomePage.tsx`
7. **Make changes** and watch them update live
8. **Read Material-UI docs** - Browse components
9. **Build your first feature** - Maybe a simple form?

---

## 💡 Tips for Python Developers

### Similarities to Python

| Python | JavaScript/TypeScript |
|--------|---------------------|
| `import module` | `import { thing } from 'module'` |
| `def function():` | `function() {}` or `() => {}` |
| `class MyClass:` | `class MyClass {}` |
| `self.variable` | `this.variable` |
| `async/await` | `async/await` (same!) |
| `try/except` | `try/catch` |
| List comprehension | `.map()`, `.filter()` |
| `f"{var}"` | `` `${var}` `` (template literal) |

### Key Differences

1. **No indentation rules** - Use `{}` for blocks
2. **Semicolons optional** - But can use them
3. **Const vs Let** - `const` can't be reassigned, `let` can
4. **Arrow functions** - `() => {}` is shorthand for functions
5. **JSON-like objects** - `{ key: value }` everywhere
6. **JSX syntax** - HTML-like syntax in JavaScript

---

## 🆘 Getting Help

- **Material-UI Docs**: https://mui.com/
- **React Docs**: https://react.dev/
- **TypeScript Docs**: https://www.typescriptlang.org/docs/
- **Vite Docs**: https://vitejs.dev/
- **Stack Overflow**: Search for React + MUI questions

---

## ✅ Summary

You now have a fully configured React + TypeScript frontend with:
- ✅ Material-UI for professional-looking components
- ✅ React Router for navigation
- ✅ Axios for API calls
- ✅ TypeScript for type safety
- ✅ Vite for fast development
- ✅ Example pages and API integration
- ✅ Docker support for production
- ✅ Extensive comments explaining everything

**The code is ready to run once you install Node.js!**
