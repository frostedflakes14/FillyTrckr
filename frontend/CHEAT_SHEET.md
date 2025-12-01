# React + TypeScript Cheat Sheet for Python Developers

## Component Patterns

### Basic Component (like a Python function)
```tsx
function MyComponent() {
  return (
    <div>
      <h1>Hello World</h1>
    </div>
  )
}

export default MyComponent
```

### Component with Props (like function parameters)
```tsx
interface MyComponentProps {
  name: string
  age: number
  isActive?: boolean  // ? means optional
}

function MyComponent({ name, age, isActive = false }: MyComponentProps) {
  return (
    <div>
      <h1>Hello {name}</h1>
      <p>Age: {age}</p>
      {isActive && <p>Status: Active</p>}
    </div>
  )
}

// Usage: <MyComponent name="John" age={30} />
```

### Component with State (like instance variables)
```tsx
import { useState } from 'react'

function Counter() {
  // [current_value, setter_function]
  const [count, setCount] = useState(0)
  const [name, setName] = useState('')

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>

      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter name"
      />
    </div>
  )
}
```

### Component with Effects (like __init__ or lifecycle hooks)
```tsx
import { useState, useEffect } from 'react'

function DataFetcher() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  // Runs after component mounts (similar to __init__)
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/data')
      const result = await response.json()
      setData(result)
      setLoading(false)
    }

    fetchData()
  }, []) // Empty array = run once on mount

  // Runs when 'count' changes
  useEffect(() => {
    console.log('Data changed:', data)
  }, [data]) // Run when data changes

  if (loading) return <p>Loading...</p>

  return <div>{/* render data */}</div>
}
```

## Common Patterns

### Conditional Rendering
```tsx
function Example({ isLoggedIn, user }) {
  // Pattern 1: if/else
  if (!isLoggedIn) {
    return <LoginButton />
  }

  // Pattern 2: Ternary operator
  return (
    <div>
      {isLoggedIn ? <Dashboard /> : <LoginButton />}
    </div>
  )

  // Pattern 3: && operator (show if true)
  return (
    <div>
      {isLoggedIn && <Dashboard />}
      {user?.name && <p>Welcome {user.name}</p>}
    </div>
  )
}
```

### Lists (like Python for loops)
```tsx
function ItemList({ items }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}

// Like Python: [<li>{item.name}</li> for item in items]
```

### Forms
```tsx
function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault() // Prevent page reload

    try {
      const response = await api.post('/login', { email, password })
      console.log('Success:', response.data)
    } catch (error) {
      console.error('Error:', error)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  )
}
```

## Material-UI Patterns

### Basic MUI Components
```tsx
import {
  Button,
  TextField,
  Typography,
  Box,
  Paper,
  Grid
} from '@mui/material'

function MUIExample() {
  return (
    <Box sx={{ p: 3 }}>  {/* sx prop for styling */}
      <Typography variant="h4" gutterBottom>
        Title
      </Typography>

      <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
        <TextField
          label="Name"
          variant="outlined"
          fullWidth
        />

        <Button variant="contained" color="primary">
          Submit
        </Button>
      </Paper>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>Column 1</Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>Column 2</Paper>
        </Grid>
      </Grid>
    </Box>
  )
}
```

### MUI Form Example
```tsx
import { useState } from 'react'
import {
  TextField,
  Button,
  Box,
  Alert
} from '@mui/material'

function CreateItemForm() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    try {
      await api.post('/items', { name, description })
      setSuccess(true)
      setName('')
      setDescription('')
    } catch (err) {
      setError('Failed to create item')
    }
  }

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>Item created!</Alert>}

      <TextField
        label="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        fullWidth
        required
        sx={{ mb: 2 }}
      />

      <TextField
        label="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        fullWidth
        multiline
        rows={4}
        sx={{ mb: 2 }}
      />

      <Button type="submit" variant="contained" color="primary">
        Create Item
      </Button>
    </Box>
  )
}
```

## API Calls with Axios

### GET Request
```tsx
import { useState, useEffect } from 'react'
import { api } from './utils/api'

function ItemList() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await api.get('/items')
        setItems(response.data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchItems()
  }, [])

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error}</p>

  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}
```

### POST Request
```tsx
const createItem = async (itemData) => {
  try {
    const response = await api.post('/items', itemData)
    console.log('Created:', response.data)
    return response.data
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}
```

### PUT Request (Update)
```tsx
const updateItem = async (id, updates) => {
  try {
    const response = await api.put(`/items/${id}`, updates)
    return response.data
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}
```

### DELETE Request
```tsx
const deleteItem = async (id) => {
  try {
    await api.delete(`/items/${id}`)
    console.log('Deleted')
  } catch (error) {
    console.error('Error:', error)
    throw error
  }
}
```

## TypeScript Types

### Basic Types
```tsx
// Primitives
const name: string = 'John'
const age: number = 30
const isActive: boolean = true

// Arrays
const numbers: number[] = [1, 2, 3]
const names: string[] = ['John', 'Jane']

// Objects
const user: { name: string; age: number } = {
  name: 'John',
  age: 30
}

// Union types (can be multiple types)
const id: string | number = 123
```

### Interfaces (like TypedDict in Python)
```tsx
interface User {
  id: number
  name: string
  email: string
  age?: number  // Optional
}

interface ApiResponse<T> {
  data: T
  status: number
  message: string
}

// Usage
const user: User = {
  id: 1,
  name: 'John',
  email: 'john@example.com'
}

const response: ApiResponse<User[]> = {
  data: [user],
  status: 200,
  message: 'Success'
}
```

### Type for Component Props
```tsx
interface ButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

function CustomButton({ label, onClick, disabled = false, variant = 'primary' }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  )
}
```

## Common Hooks

### useState - Manage State
```tsx
const [count, setCount] = useState(0)
const [user, setUser] = useState(null)
const [items, setItems] = useState([])

// Update state
setCount(count + 1)
setUser({ name: 'John', age: 30 })
setItems([...items, newItem])
```

### useEffect - Side Effects
```tsx
// Run once on mount
useEffect(() => {
  console.log('Component mounted')
}, [])

// Run when dependencies change
useEffect(() => {
  console.log('Count changed:', count)
}, [count])

// Cleanup function
useEffect(() => {
  const timer = setInterval(() => {
    console.log('Tick')
  }, 1000)

  // Cleanup on unmount
  return () => clearInterval(timer)
}, [])
```

### Custom Hook (like a utility function)
```tsx
// Custom hook for API calls
function useApi<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get(url)
        setData(response.data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [url])

  return { data, loading, error }
}

// Usage
function MyComponent() {
  const { data, loading, error } = useApi<User[]>('/users')

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error}</p>

  return <div>{/* render data */}</div>
}
```

## React Router

### Navigation
```tsx
import { Link, useNavigate } from 'react-router-dom'

function Navigation() {
  const navigate = useNavigate()

  return (
    <div>
      {/* Declarative navigation */}
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>

      {/* Programmatic navigation */}
      <button onClick={() => navigate('/profile')}>
        Go to Profile
      </button>

      <button onClick={() => navigate(-1)}>
        Go Back
      </button>
    </div>
  )
}
```

### Route Parameters
```tsx
import { useParams } from 'react-router-dom'

// In App.tsx: <Route path="/users/:id" element={<UserDetail />} />

function UserDetail() {
  const { id } = useParams()  // Get 'id' from URL

  const [user, setUser] = useState(null)

  useEffect(() => {
    const fetchUser = async () => {
      const response = await api.get(`/users/${id}`)
      setUser(response.data)
    }
    fetchUser()
  }, [id])

  return <div>{user?.name}</div>
}
```

## Styling with sx Prop (MUI)

```tsx
<Box
  sx={{
    // Spacing (1 unit = 8px)
    p: 2,         // padding: 16px
    m: 3,         // margin: 24px
    mt: 1,        // marginTop: 8px
    mb: 2,        // marginBottom: 16px

    // Colors
    backgroundColor: 'primary.main',
    color: 'text.primary',

    // Layout
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',

    // Sizing
    width: '100%',
    height: 300,
    minHeight: '50vh',

    // Borders
    border: 1,
    borderColor: 'divider',
    borderRadius: 2,

    // Responsive
    width: {
      xs: '100%',   // mobile
      sm: '80%',    // tablet
      md: '60%',    // desktop
    },
  }}
>
  Content
</Box>
```

## Comparison: Python vs JavaScript/TypeScript

| Concept | Python | JavaScript/TypeScript |
|---------|--------|----------------------|
| Function | `def func():` | `function func() {}` or `() => {}` |
| Class | `class MyClass:` | `class MyClass {}` |
| Method | `def method(self):` | `method() {}` |
| Import | `from module import thing` | `import { thing } from 'module'` |
| String format | `f"Hello {name}"` | `` `Hello ${name}` `` |
| List comp | `[x*2 for x in items]` | `items.map(x => x * 2)` |
| Filter | `[x for x in items if x > 5]` | `items.filter(x => x > 5)` |
| Dictionary | `{"key": "value"}` | `{ key: "value" }` |
| Try/Except | `try/except` | `try/catch` |
| Async | `async def func():` | `async function func() {}` |
| Await | `await func()` | `await func()` |
| None | `None` | `null` or `undefined` |
| Boolean | `True/False` | `true/false` |
| And/Or | `and/or` | `&&/||` |
| Not | `not` | `!` |

## Common Mistakes for Beginners

1. **Forgetting to return JSX**
```tsx
// ❌ Wrong
function MyComponent() {
  <div>Hello</div>  // Missing return!
}

// ✅ Correct
function MyComponent() {
  return <div>Hello</div>
}
```

2. **Not using arrow functions in event handlers**
```tsx
// ❌ Wrong - function gets called immediately
<button onClick={doSomething()}>Click</button>

// ✅ Correct - pass function reference
<button onClick={doSomething}>Click</button>

// ✅ Correct - use arrow function for parameters
<button onClick={() => doSomething(param)}>Click</button>
```

3. **Mutating state directly**
```tsx
// ❌ Wrong
items.push(newItem)
setItems(items)

// ✅ Correct - create new array
setItems([...items, newItem])
```

4. **Missing key prop in lists**
```tsx
// ❌ Wrong
{items.map(item => <li>{item.name}</li>)}

// ✅ Correct
{items.map(item => <li key={item.id}>{item.name}</li>)}
```

5. **Using if statements in JSX**
```tsx
// ❌ Wrong
return (
  <div>
    if (isLoggedIn) {
      <Dashboard />
    }
  </div>
)

// ✅ Correct
return (
  <div>
    {isLoggedIn && <Dashboard />}
  </div>
)
```
