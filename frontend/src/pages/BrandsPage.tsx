import { useState, useEffect } from 'react'
import { Typography, Box, Alert, Snackbar, AlertColor, Fab } from '@mui/material'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import AddIcon from '@mui/icons-material/Add'
import { api } from '../utils/api'
import AddItemDialog from '../components/AddItemDialog'
import { createDateTimeColumn } from '../utils/dateColumn'

interface Brand {
  id: number
  name: string
  created_at: string
}

function BrandsPage() {
  const [brands, setBrands] = useState<Brand[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // Dialog state
  const [addOpen, setAddOpen] = useState(false)

  // Snackbar state
  const [snackOpen, setSnackOpen] = useState(false)
  const [snackMsg, setSnackMsg] = useState('')
  const [snackSeverity, setSnackSeverity] = useState<AlertColor>('success')
  const [snackAutoHideDuration, setSnackAutoHideDuration] = useState<number | null>(4000)

  const fetchBrands = async () => {
    setLoading(true)
    try {
      const response = await api.get('/v1/filly/brands')
      setBrands(response.data.brands)
      setError(null)
    } catch (err) {
      setError('Failed to fetch brands. Make sure your backend is running.')
      console.error('API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchBrands()
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
        // Capitalize first letter of each word (like Python's str.title())
        return value
          .split(' ')
          .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ')
      }
    },
    { field: 'id', headerName: 'ID', width: 100 },
    createDateTimeColumn(),
  ]

  return (
    <Box>
      <Box sx={{ mb: 1 }}>
        <Typography variant="h3" component="h1">
          Filament Brands
        </Typography>
      </Box>

      <Typography variant="body1" paragraph sx={{ mb: 2 }}>
        View all filament brands in the database.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ height: 'calc(100vh - 300px)', minHeight: 400, width: '100%', position: 'relative' }}>
        <DataGrid
          rows={brands}
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
          sx={{
            '& .MuiDataGrid-main': {
              position: 'relative',
            },
          }}
        />

        {/* Floating Action Button inside data area */}
        <Fab
          color="primary"
          aria-label="add brand"
          sx={{
            position: 'absolute',
            bottom: 72,
            right: 16,
            pointerEvents: 'auto',
            zIndex: 1,
          }}
          onClick={() => setAddOpen(true)}
        >
          <AddIcon />
        </Fab>
      </Box>

      <AddItemDialog
        open={addOpen}
        onClose={() => setAddOpen(false)}
        apiEndpoint={'/v1/filly/brands/add'}
        itemType={'brand'}
        showColorPicker={false}
        onSuccess={(data: any) => {
          if (data && data.error) {
            setSnackMsg(typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail))
            setSnackSeverity('error')
            setSnackOpen(true)
          } else if (data) {
            const newId = data.id ?? (data.result && data.result.id)
            const newName = data.name ?? ''
            setSnackMsg(`Brand ${newName || ''} successfully added to the database. New ID: ${newId ?? 'unknown'}`)
            setSnackSeverity('success')
            setSnackOpen(true)
            fetchBrands()
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

export default BrandsPage
