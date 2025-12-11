import { useState, useEffect } from 'react'
import { Typography, Box, Alert, Snackbar, AlertColor, Tooltip, Button, Fab } from '@mui/material'
import { DataGrid, GridColDef, GridRenderCellParams, GridActionsCellItem } from '@mui/x-data-grid'
import AddIcon from '@mui/icons-material/Add'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ToggleOnIcon from '@mui/icons-material/ToggleOn'
import ToggleOffIcon from '@mui/icons-material/ToggleOff'
import { api } from '../utils/api'
import { createDateTimeColumn } from '../utils/dateColumn'
import AddRollDialog from '../components/AddRollDialog'

interface Roll {
  id: number
  brand_id: number
  color_id: number
  type_id: number
  subtype_id: number
  created_at: string
  updated_at: string
  weight_grams: number
  original_weight_grams: number
  in_use: boolean
  opened: boolean
}

interface Brand {
  id: number
  name: string
}

interface Color {
  id: number
  name: string
  hex_code: string
}

interface Type {
  id: number
  name: string
}

interface Subtype {
  id: number
  name: string
}

interface RollWithDetails extends Roll {
  brand_name: string
  color_name: string
  color_hex: string
  type_name: string
  subtype_name: string
}

function RollsPage() {
  const [rolls, setRolls] = useState<RollWithDetails[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // Dialog state
  const [addOpen, setAddOpen] = useState(false)

  // Snackbar state
  const [snackOpen, setSnackOpen] = useState(false)
  const [snackMsg, setSnackMsg] = useState('')
  const [snackSeverity, setSnackSeverity] = useState<AlertColor>('success')

  const fetchLookupData = async () => {
    try {
      const [brandsRes, colorsRes, typesRes, subtypesRes] = await Promise.all([
        api.get('/v1/filly/brands'),
        api.get('/v1/filly/colors'),
        api.get('/v1/filly/types'),
        api.get('/v1/filly/subtypes')
      ])

      const brandsMap = new Map<number, Brand>()
      brandsRes.data.brands.forEach((b: Brand) => brandsMap.set(b.id, b))

      const colorsMap = new Map<number, Color>()
      colorsRes.data.colors.forEach((c: Color) => colorsMap.set(c.id, c))

      const typesMap = new Map<number, Type>()
      typesRes.data.types.forEach((t: Type) => typesMap.set(t.id, t))

      const subtypesMap = new Map<number, Subtype>()
      subtypesRes.data.subtypes.forEach((s: Subtype) => subtypesMap.set(s.id, s))

      // Return the maps so they can be used immediately
      return { brandsMap, colorsMap, typesMap, subtypesMap }
    } catch (err) {
      console.error('Failed to fetch lookup data:', err)
      throw err
    }
  }

  const fetchRolls = async () => {
    setLoading(true)
    try {
      const lookupData = await fetchLookupData()

      const response = await api.get('/v1/filly/rolls/active')
      const rollsData: Roll[] = response.data.rolls

      // Enrich rolls with lookup data using the returned maps
      const enrichedRolls: RollWithDetails[] = rollsData.map((roll) => ({
        ...roll,
        brand_name: lookupData.brandsMap.get(roll.brand_id)?.name || 'Unknown',
        color_name: lookupData.colorsMap.get(roll.color_id)?.name || 'Unknown',
        color_hex: lookupData.colorsMap.get(roll.color_id)?.hex_code || '#000000',
        type_name: lookupData.typesMap.get(roll.type_id)?.name || 'Unknown',
        subtype_name: lookupData.subtypesMap.get(roll.subtype_id)?.name || 'Unknown',
      }))

      setRolls(enrichedRolls)
      setError(null)
    } catch (err) {
      setError('Failed to fetch rolls. Make sure your backend is running.')
      console.error('API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchRolls()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const handleDuplicate = async (id: number) => {
    try {
      await api.post(`/v1/filly/rolls/${id}/duplicate`)
      setSnackMsg('Roll duplicated successfully!')
      setSnackSeverity('success')
      setSnackOpen(true)
      fetchRolls()
    } catch (err) {
      setSnackMsg('Failed to duplicate roll')
      setSnackSeverity('error')
      setSnackOpen(true)
      console.error('Duplicate error:', err)
    }
  }

  const handleSetOpened = async (id: number) => {
    try {
      await api.post(`/v1/filly/rolls/${id}/set_opened`)
      setSnackMsg('Roll marked as opened!')
      setSnackSeverity('success')
      setSnackOpen(true)
      fetchRolls()
    } catch (err) {
      setSnackMsg('Failed to mark roll as opened')
      setSnackSeverity('error')
      setSnackOpen(true)
      console.error('Set opened error:', err)
    }
  }

  const handleToggleInUse = async (id: number, currentInUse: boolean) => {
    try {
      await api.post(`/v1/filly/rolls/${id}/set_in_use`, { in_use: !currentInUse })
      setSnackMsg(`Roll marked as ${!currentInUse ? 'in use' : 'not in use'}!`)
      setSnackSeverity('success')
      setSnackOpen(true)
      fetchRolls()
    } catch (err) {
      setSnackMsg('Failed to update roll in-use status')
      setSnackSeverity('error')
      setSnackOpen(true)
      console.error('Toggle in-use error:', err)
    }
  }

  const handleSnackClose = () => {
    setSnackOpen(false)
  }

  const handleAddSuccess = (data: any) => {
    if (data.error) {
      setSnackMsg('Failed to add roll: ' + (data.detail?.detail || data.detail || 'Unknown error'))
      setSnackSeverity('error')
    } else {
      setSnackMsg('Roll added successfully!')
      setSnackSeverity('success')
      fetchRolls()
    }
    setSnackOpen(true)
  }

  // Define columns for DataGrid
  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 80 },
    {
      field: 'brand_name',
      headerName: 'Brand',
      flex: 1,
      minWidth: 120,
      valueGetter: (value: string) => {
        return value
          .split(' ')
          .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ')
      }
    },
    {
      field: 'type_name',
      headerName: 'Type',
      flex: 1,
      minWidth: 100,
      valueGetter: (value: string) => {
        return value.toUpperCase()
      }
    },
    {
      field: 'subtype_name',
      headerName: 'Subtype',
      flex: 1,
      minWidth: 100,
      valueGetter: (value: string) => {
        return value
          .split(' ')
          .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ')
      }
    },
    {
      field: 'color_name',
      headerName: 'Color',
      flex: 1,
      minWidth: 150,
      renderCell: (params: GridRenderCellParams) => {
        const row = params.row as RollWithDetails
        const colorName = row.color_name
          .split(' ')
          .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
          .join(' ')

        return (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              width: '100%',
              height: '100%',
            }}
          >
            <Tooltip title={row.color_hex} placement="bottom">
              <Box
                sx={{
                  width: 24,
                  height: 24,
                  borderRadius: '50%',
                  backgroundColor: row.color_hex,
                  border: '2px solid #ccc',
                  flexShrink: 0,
                }}
              />
            </Tooltip>
            <span>{colorName}</span>
          </Box>
        )
      }
    },
    {
      field: 'weight_grams',
      headerName: 'Weight',
      flex: 1,
      minWidth: 130,
      renderCell: (params: GridRenderCellParams) => {
        const row = params.row as RollWithDetails
        return `${row.weight_grams} / ${row.original_weight_grams}`
      }
    },
    {
      field: 'opened',
      headerName: 'Opened',
      width: 120,
      renderCell: (params: GridRenderCellParams) => {
        const row = params.row as RollWithDetails
        if (row.opened) {
          return (
            <Button
              size="small"
              variant="outlined"
              color="success"
              disabled
              startIcon={<CheckCircleIcon />}
            >
              Opened
            </Button>
          )
        }
        return (
          <Button
            size="small"
            variant="outlined"
            onClick={() => handleSetOpened(row.id)}
            startIcon={<CheckCircleIcon />}
          >
            Open
          </Button>
        )
      }
    },
    {
      field: 'in_use',
      headerName: 'In Use',
      width: 120,
      renderCell: (params: GridRenderCellParams) => {
        const row = params.row as RollWithDetails
        return (
          <Button
            size="small"
            variant="outlined"
            color={row.in_use ? 'primary' : 'inherit'}
            onClick={() => handleToggleInUse(row.id, row.in_use)}
            startIcon={row.in_use ? <ToggleOnIcon /> : <ToggleOffIcon />}
          >
            {row.in_use ? 'In Use' : 'Not In Use'}
          </Button>
        )
      }
    },
    createDateTimeColumn('updated_at', 'Last Updated', 1, 150),
    createDateTimeColumn('created_at', 'Created At', 1, 150),
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Duplicate Roll',
      width: 120,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<ContentCopyIcon />}
          label="Duplicate"
          onClick={() => handleDuplicate(params.id as number)}
          showInMenu={false}
        />
      ]
    }
  ]

  return (
    <Box>
      {/* Title */}
      <Box sx={{ mb: 1 }}>
        <Typography variant="h3" component="h1">
          Filament Rolls
        </Typography>
      </Box>

      <Typography variant="body1" paragraph sx={{ mb: 2 }}>
        View all active filament rolls in the database.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ height: 'calc(100vh - 300px)', minHeight: 400, width: '100%', position: 'relative' }}>
        <DataGrid
          rows={rolls}
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
          aria-label="add roll"
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

      {/* Add Roll Dialog */}
      <AddRollDialog
        open={addOpen}
        onClose={() => setAddOpen(false)}
        onSuccess={handleAddSuccess}
      />

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackOpen}
        autoHideDuration={4000}
        onClose={handleSnackClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleSnackClose} severity={snackSeverity} sx={{ width: '100%' }}>
          {snackMsg}
        </Alert>
      </Snackbar>
    </Box>
  )
}

export default RollsPage
