import { useState, useEffect } from 'react'
import { Typography, Box, Alert } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import axios from 'axios'

interface Brand {
  id: number
  name: string
  created_at: string
}

function BrandsPage() {
  const [brands, setBrands] = useState<Brand[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchBrands = async () => {
      try {
        const response = await axios.get('/api/v1/filly/brands')
        setBrands(response.data.brands)
        setError(null)
      } catch (err) {
        setError('Failed to fetch brands. Make sure your backend is running.')
        console.error('API Error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchBrands()
  }, [])

  // Define columns for DataGrid
  const columns: GridColDef[] = [
    {
      field: 'name',
      headerName: 'Name',
      flex: 1,
      minWidth: 150,
      valueGetter: (value: string) => {
        // Capitalize first letter of each word (like Python's str.title())
        return value
          .split(' ')
          .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ')
      }
    },
    { field: 'id', headerName: 'ID', width: 100 },
    { field: 'created_at', headerName: 'Created At', flex: 1, minWidth: 200 },
  ]

  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        Filament Brands
      </Typography>

      <Typography variant="body1" paragraph>
        View all filament brands in the database.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={brands}
          columns={columns}
          loading={loading}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 10 },
            },
          }}
          pageSizeOptions={[5, 10, 25, 50]}
          disableRowSelectionOnClick
        />
      </Box>
    </Box>
  )
}

export default BrandsPage
