import { useState, useEffect } from 'react'
import { Typography, Box, Alert } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import axios from 'axios'

interface Type {
  id: number
  name: string
  created_at: string
}

function TypesPage() {
  const [types, setTypes] = useState<Type[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTypes = async () => {
      try {
        const response = await axios.get('/api/v1/filly/types')
        setTypes(response.data.types)
        setError(null)
      } catch (err) {
        setError('Failed to fetch types. Make sure your backend is running.')
        console.error('API Error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchTypes()
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
      <Typography variant="h3" component="h1" gutterBottom>
        Filament Types
      </Typography>

      <Typography variant="body1" paragraph>
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
    </Box>
  )
}

export default TypesPage
