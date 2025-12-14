import { useState, useEffect } from 'react'
import { Typography, Box, Alert, Snackbar, AlertColor, Tooltip, Fab } from '@mui/material'
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid'
import AddIcon from '@mui/icons-material/Add'
import { api } from '../utils/api'
import AddItemDialog from '../components/AddItemDialog'
import { createDateTimeColumn } from '../utils/dateColumn'

interface Color {
  id: number
  name: string
  hex_code: string
  created_at: string
}

function ColorsPage() {
  const [colors, setColors] = useState<Color[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // Dialog state
  const [addOpen, setAddOpen] = useState(false)

  // Snackbar state
  const [snackOpen, setSnackOpen] = useState(false)
  const [snackMsg, setSnackMsg] = useState('')
  const [snackSeverity, setSnackSeverity] = useState<AlertColor>('success')
  const [snackAutoHideDuration, setSnackAutoHideDuration] = useState<number | null>(4000)

  const fetchColors = async () => {
    setLoading(true)
    try {
      // `api` has baseURL '/api' so endpoints passed to it should be relative to that base.
      // Use '/v1/filly/colors' instead of '/api/v1/filly/colors' to avoid doubling /api in the request URL.
      const response = await api.get('/v1/filly/colors')
      setColors(response.data?.colors || [])
      setError(null)
    } catch (err) {
      setError('Failed to fetch colors. Make sure your backend is running.')
      console.error('API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchColors()
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
    {
      field: 'hex_code',
      headerName: 'Color',
      flex: 1,
      minWidth: 70,
      // center the color circle
      // align: 'center',
      // headerAlign: 'center',
      renderCell: (params: GridRenderCellParams) => {
        const hexCode = params.value as string
        if (!hexCode) return null

        return (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              // Centers it in the column
              // justifyContent: 'center',
              width: '100%',
              height: '100%',
            }}
          >
            <Tooltip title={hexCode} placement="bottom">
              <Box
                sx={{
                  width: 32,
                  height: 32,
                  borderRadius: '50%',
                  backgroundColor: hexCode,
                  border: '2px solid #ccc',
                  cursor: 'pointer',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'scale(1.2)',
                  }
                }}
              />
            </Tooltip>
          </Box>
        )
      }
    },
    createDateTimeColumn(),
  ]

  return (
    <Box>
      {/* Title */}
      <Box sx={{ mb: 1 }}>
        <Typography variant="h3" component="h1" sx={{ fontSize: { xs: '1.75rem', sm: '2.5rem', md: '3rem' } }}>
          Filament Colors
        </Typography>
      </Box>

      <Typography variant="body1" paragraph sx={{ mb: 2 }}>
        View all filament colors in the database.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ height: { xs: 'calc(100vh - 250px)', md: 'calc(100vh - 300px)' }, minHeight: 400, width: '100%', position: 'relative' }}>
        <DataGrid
          rows={colors}
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
          aria-label="add color"
          sx={{
            position: 'absolute',
            bottom: 72, // Position above footer (footer is typically ~56px)
            right: 16,
            pointerEvents: 'auto',
            zIndex: 1,
          }}
          onClick={() => setAddOpen(true)}
        >
          <AddIcon />
        </Fab>
      </Box>

      {/* Add item dialog */}
      <AddItemDialog
        open={addOpen}
        onClose={() => setAddOpen(false)}
        // pass endpoint relative to api.baseURL ('/api')
        apiEndpoint={'/v1/filly/colors/add'}
        itemType={'color'}
        showColorPicker={true}
        onSuccess={(data: any) => {
          // data may be success or error object depending on AddItemDialog
          if (data && data.error) {
            setSnackMsg(typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail))
            setSnackSeverity('error')
            setSnackOpen(true)
          } else if (data) {
            // Assuming backend returns { id: <newId>, name: <name> }
            const newId = data.id ?? (data.result && data.result.id)
            const newName = data.name ?? ''
            setSnackMsg(`Color ${newName || ''} successfully added to the database. New ID: ${newId ?? 'unknown'}`)
            setSnackSeverity('success')
            setSnackOpen(true)
            // Refresh table to include the new color
            fetchColors()
          }
        }}
      />

      {/* Snackbar for feedback */}
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

export default ColorsPage
