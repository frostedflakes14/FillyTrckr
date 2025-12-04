import { useState, useEffect } from 'react'
import { Typography, Box, Alert, Button, Snackbar, AlertColor } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import { api } from '../utils/api'
import AddItemDialog from '../components/AddItemDialog'

interface Type {
  id: number
  name: string
  created_at: string
}

function TypesPage() {
  const [types, setTypes] = useState<Type[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // Dialog state
  const [addOpen, setAddOpen] = useState(false)

  // Snackbar state
  const [snackOpen, setSnackOpen] = useState(false)
  const [snackMsg, setSnackMsg] = useState('')
  const [snackSeverity, setSnackSeverity] = useState<AlertColor>('success')
  const [snackAutoHideDuration, setSnackAutoHideDuration] = useState<number | null>(4000)

  const fetchTypes = async () => {
    setLoading(true)
    try {
      const response = await api.get('/v1/filly/types')
      setTypes(response.data.types)
      setError(null)
    } catch (err) {
      setError('Failed to fetch types. Make sure your backend is running.')
      console.error('API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTypes()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Define columns for DataGrid
  const columns: GridColDef[] = [
    {
      field: 'name',
      headerName: 'Name',
      flex: 1,
      minWidth: 150,
      valueGetter: (value: string) => {
        // Capitalize entire string (like Python's str.upper())
        return value.toUpperCase()
      }
    },
    { field: 'id', headerName: 'ID', width: 100 },
    { field: 'created_at', headerName: 'Created At', flex: 1, minWidth: 200 },
  ]

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Typography variant="h3" component="h1" sx={{ mr: 2 }}>
          Filament Types
        </Typography>
        <Button variant="contained" onClick={() => setAddOpen(true)}>
          Add Type
        </Button>
      </Box>

      <Typography variant="body1" paragraph sx={{ mb: 2 }}>
        View all filament types in the database.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ height: 'calc(100vh - 300px)', minHeight: 400, width: '100%' }}>
        <DataGrid
          rows={types}
          columns={columns}
          loading={loading}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 25 },
            },
          }}
          pageSizeOptions={[10, 25, 50, 100]}
          disableRowSelectionOnClick
          autoPageSize
        />
      </Box>

      <AddItemDialog
        open={addOpen}
        onClose={() => setAddOpen(false)}
        apiEndpoint={'/v1/filly/types/add'}
        itemType={'type'}
        showColorPicker={false}
        onSuccess={(data: any) => {
          if (data && data.error) {
            setSnackMsg(typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail))
            setSnackSeverity('error')
            setSnackOpen(true)
          } else if (data) {
            const newId = data.id ?? (data.result && data.result.id)
            const newName = data.name ?? ''
            setSnackMsg(`Type ${newName || ''} successfully added to the database. New ID: ${newId ?? 'unknown'}`)
            setSnackSeverity('success')
            setSnackOpen(true)
            fetchTypes()
          }
        }}
      />

      <Snackbar
        open={snackOpen}
        autoHideDuration={snackAutoHideDuration ?? undefined}
        onClose={() => setSnackOpen(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onMouseEnter={() => setSnackAutoHideDuration(null)}
          onMouseLeave={() => setSnackAutoHideDuration(4000)}
          onClose={() => setSnackOpen(false)}
          severity={snackSeverity}
          sx={{ width: '100%' }}
        >
          {snackMsg}
        </Alert>
      </Snackbar>
    </Box>
  )
}

export default TypesPage
