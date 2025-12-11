import { useState, useEffect } from 'react'
import { Typography, Box, Alert, Snackbar, AlertColor, Tooltip, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Select, MenuItem, FormControl, InputLabel, FormControlLabel, Switch } from '@mui/material'
import AddIcon from '@mui/icons-material/Add'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ToggleOnIcon from '@mui/icons-material/ToggleOn'
import ToggleOffIcon from '@mui/icons-material/ToggleOff'
import { api } from '../utils/api'
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

interface GroupedRoll {
  id: string // Composite key: brand_id-color_id-type_id-subtype_id
  brand_id: number
  color_id: number
  type_id: number
  subtype_id: number
  brand_name: string
  color_name: string
  color_hex: string
  type_name: string
  subtype_name: string
  original_weight_grams: number
  rolls: RollWithDetails[]
  openedRolls: RollWithDetails[]
  unopenedRolls: RollWithDetails[]
  oldestRoll: RollWithDetails
  created_at: string
  updated_at: string
}

function RollsPage() {
  const [groupedRolls, setGroupedRolls] = useState<GroupedRoll[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // Lookup data for filters
  const [brands, setBrands] = useState<Brand[]>([])
  const [colors, setColors] = useState<Color[]>([])
  const [types, setTypes] = useState<Type[]>([])
  const [subtypes, setSubtypes] = useState<Subtype[]>([])

  // Filter state
  const [filterBrandId, setFilterBrandId] = useState<number | ''>('')
  const [filterColorId, setFilterColorId] = useState<number | ''>('')
  const [filterTypeId, setFilterTypeId] = useState<number | ''>('')
  const [filterSubtypeId, setFilterSubtypeId] = useState<number | ''>('')
  const [filterOpenedOnly, setFilterOpenedOnly] = useState(false)
  const [filterInUseOnly, setFilterInUseOnly] = useState(false)

  // Dialog state
  const [addOpen, setAddOpen] = useState(false)
  const [weightDialogOpen, setWeightDialogOpen] = useState(false)
  const [editingRoll, setEditingRoll] = useState<RollWithDetails | null>(null)
  const [newWeight, setNewWeight] = useState<string>('')

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

      const brandsList = brandsRes.data.brands
      const colorsList = colorsRes.data.colors
      const typesList = typesRes.data.types
      const subtypesList = subtypesRes.data.subtypes

      // Set state for filter dropdowns
      setBrands(brandsList)
      setColors(colorsList)
      setTypes(typesList)
      setSubtypes(subtypesList)

      const brandsMap = new Map<number, Brand>()
      brandsList.forEach((b: Brand) => brandsMap.set(b.id, b))

      const colorsMap = new Map<number, Color>()
      colorsList.forEach((c: Color) => colorsMap.set(c.id, c))

      const typesMap = new Map<number, Type>()
      typesList.forEach((t: Type) => typesMap.set(t.id, t))

      const subtypesMap = new Map<number, Subtype>()
      subtypesList.forEach((s: Subtype) => subtypesMap.set(s.id, s))

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

      // Build filter params
      const params: any = {}
      if (filterBrandId !== '') params.brand_id = filterBrandId
      if (filterColorId !== '') params.color_id = filterColorId
      if (filterTypeId !== '') params.type_id = filterTypeId
      if (filterSubtypeId !== '') params.subtype_id = filterSubtypeId
      if (filterOpenedOnly) params.opened = true
      if (filterInUseOnly) params.in_use = true

      const response = await api.get('/v1/filly/rolls/filter', { params })
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

      // Group rolls by brand, color, type, subtype
      const grouped = groupRollsByType(enrichedRolls)
      setGroupedRolls(grouped)

      setError(null)
    } catch (err) {
      setError('Failed to fetch rolls. Make sure your backend is running.')
      console.error('API Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const groupRollsByType = (rolls: RollWithDetails[]): GroupedRoll[] => {
    // Apply filters at the individual roll level
    let filteredRolls = rolls.filter(roll => {
      // Brand filter
      if (filterBrandId !== '' && roll.brand_id !== filterBrandId) return false
      // Color filter
      if (filterColorId !== '' && roll.color_id !== filterColorId) return false
      // Type filter
      if (filterTypeId !== '' && roll.type_id !== filterTypeId) return false
      // Subtype filter
      if (filterSubtypeId !== '' && roll.subtype_id !== filterSubtypeId) return false
      // Opened only filter
      if (filterOpenedOnly && !roll.opened) return false
      // In use only filter
      if (filterInUseOnly && !roll.in_use) return false

      return true
    })

    const groups = new Map<string, RollWithDetails[]>()

    // Group rolls by composite key
    filteredRolls.forEach(roll => {
      const key = `${roll.brand_id}-${roll.color_id}-${roll.type_id}-${roll.subtype_id}`
      if (!groups.has(key)) {
        groups.set(key, [])
      }
      groups.get(key)!.push(roll)
    })

    // Convert to GroupedRoll array
    const result: GroupedRoll[] = []
    groups.forEach((rollsInGroup, key) => {
      // Sort opened rolls by created_at (ascending - oldest first)
      const openedRolls = rollsInGroup
        .filter(r => r.opened)
        .sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
      const unopenedRolls = rollsInGroup.filter(r => !r.opened)

      // Sort by created_at to find oldest
      const sortedByDate = [...rollsInGroup].sort((a, b) =>
        new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      )
      const oldestRoll = sortedByDate[0]

      result.push({
        id: key,
        brand_id: oldestRoll.brand_id,
        color_id: oldestRoll.color_id,
        type_id: oldestRoll.type_id,
        subtype_id: oldestRoll.subtype_id,
        brand_name: oldestRoll.brand_name,
        color_name: oldestRoll.color_name,
        color_hex: oldestRoll.color_hex,
        type_name: oldestRoll.type_name,
        subtype_name: oldestRoll.subtype_name,
        original_weight_grams: oldestRoll.original_weight_grams,
        rolls: rollsInGroup,
        openedRolls,
        unopenedRolls,
        oldestRoll,
        created_at: oldestRoll.created_at,
        updated_at: oldestRoll.updated_at,
      })
    })

    return result
  }

  useEffect(() => {
    fetchRolls()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterBrandId, filterColorId, filterTypeId, filterSubtypeId, filterOpenedOnly, filterInUseOnly])

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

  const handleWeightClick = (roll: RollWithDetails) => {
    setEditingRoll(roll)
    setNewWeight('')
    setWeightDialogOpen(true)
  }

  const handleWeightDialogClose = () => {
    setWeightDialogOpen(false)
    setEditingRoll(null)
    setNewWeight('')
  }

  const handleWeightUpdate = async () => {
    if (!editingRoll) return

    const weightValue = parseFloat(newWeight)
    if (isNaN(weightValue) || weightValue < 0) {
      setSnackMsg('Please enter a valid weight')
      setSnackSeverity('error')
      setSnackOpen(true)
      return
    }

    try {
      // If roll is not opened, mark it as opened first
      if (!editingRoll.opened) {
        await api.post(`/v1/filly/rolls/${editingRoll.id}/set_opened`)
      }

      // Update the weight
      await api.post(`/v1/filly/rolls/${editingRoll.id}/update_weight`, {
        new_weight_grams: weightValue
      })

      setSnackMsg('Weight updated successfully!')
      setSnackSeverity('success')
      setSnackOpen(true)
      handleWeightDialogClose()
      fetchRolls()
    } catch (err) {
      setSnackMsg('Failed to update weight')
      setSnackSeverity('error')
      setSnackOpen(true)
      console.error('Update weight error:', err)
    }
  }

  const handleClearFilters = () => {
    setFilterBrandId('')
    setFilterColorId('')
    setFilterTypeId('')
    setFilterSubtypeId('')
    setFilterOpenedOnly(false)
    setFilterInUseOnly(false)
  }

  const handleDuplicateGroup = async (group: GroupedRoll) => {
    try {
      // Duplicate using the oldest roll in the group, with the original weight from the group
      await api.post(`/v1/filly/rolls/${group.oldestRoll.id}/duplicate`, {
        original_weight_grams: group.original_weight_grams
      })
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

  const handleOpenNewRoll = async (group: GroupedRoll) => {
    if (group.unopenedRolls.length === 0) return

    // Open the oldest unopened roll
    const rollToOpen = group.unopenedRolls.sort((a, b) =>
      new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
    )[0]

    try {
      await api.post(`/v1/filly/rolls/${rollToOpen.id}/set_opened`)
      setSnackMsg('Roll opened successfully!')
      setSnackSeverity('success')
      setSnackOpen(true)
      fetchRolls()
    } catch (err) {
      setSnackMsg('Failed to open roll')
      setSnackSeverity('error')
      setSnackOpen(true)
      console.error('Open roll error:', err)
    }
  }

  return (
    <Box>
      {/* Title with Add Button */}
      <Box sx={{ mb: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h3" component="h1">
          Filament Rolls
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setAddOpen(true)}
        >
          Add Roll
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Filter Section */}
      <Box sx={{ mb: 2, p: 1.5, backgroundColor: 'background.paper', borderRadius: 1, border: '1px solid', borderColor: 'divider' }}>
        <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 'bold' }}>Filters</Typography>
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 1.5, mb: 1.5 }}>
          {/* Brand Filter */}
          <FormControl fullWidth size="small">
            <InputLabel>Brand</InputLabel>
            <Select
              value={filterBrandId}
              label="Brand"
              onChange={(e) => setFilterBrandId(e.target.value as number | '')}
            >
              <MenuItem value="">All</MenuItem>
              {brands.map((brand) => (
                <MenuItem key={brand.id} value={brand.id}>
                  {brand.name.split(' ').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Type Filter */}
          <FormControl fullWidth size="small">
            <InputLabel>Type</InputLabel>
            <Select
              value={filterTypeId}
              label="Type"
              onChange={(e) => setFilterTypeId(e.target.value as number | '')}
            >
              <MenuItem value="">All</MenuItem>
              {types.map((type) => (
                <MenuItem key={type.id} value={type.id}>
                  {type.name.toUpperCase()}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Subtype Filter */}
          <FormControl fullWidth size="small">
            <InputLabel>Subtype</InputLabel>
            <Select
              value={filterSubtypeId}
              label="Subtype"
              onChange={(e) => setFilterSubtypeId(e.target.value as number | '')}
            >
              <MenuItem value="">All</MenuItem>
              {subtypes.map((subtype) => (
                <MenuItem key={subtype.id} value={subtype.id}>
                  {subtype.name.split(' ').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Color Filter */}
          <FormControl fullWidth size="small">
            <InputLabel>Color</InputLabel>
            <Select
              value={filterColorId}
              label="Color"
              onChange={(e) => setFilterColorId(e.target.value as number | '')}
            >
              <MenuItem value="">All</MenuItem>
              {colors.map((color) => (
                <MenuItem key={color.id} value={color.id}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Box
                      sx={{
                        width: 16,
                        height: 16,
                        borderRadius: '50%',
                        backgroundColor: color.hex_code,
                        border: '1px solid #ccc',
                      }}
                    />
                    {color.name.split(' ').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {/* Opened Only Toggle */}
          <FormControlLabel
            control={
              <Switch
                size="small"
                checked={filterOpenedOnly}
                onChange={(e) => setFilterOpenedOnly(e.target.checked)}
              />
            }
            label="Opened Only"
          />

          {/* In Use Only Toggle */}
          <FormControlLabel
            control={
              <Switch
                size="small"
                checked={filterInUseOnly}
                onChange={(e) => setFilterInUseOnly(e.target.checked)}
              />
            }
            label="In Use Only"
          />

          {/* Clear Filters Button */}
          <Button
            size="small"
            variant="outlined"
            onClick={handleClearFilters}
            sx={{ ml: 'auto' }}
          >
            Clear Filters
          </Button>
        </Box>
      </Box>

      <Box sx={{ height: 'calc(100vh - 300px)', minHeight: 400, width: '100%', position: 'relative', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
              <Typography>Loading...</Typography>
            </Box>
          ) : (
            groupedRolls.map((group) => (
              <Box key={group.id} sx={{ mb: 1, border: '1px solid', borderColor: 'divider', borderRadius: 1, overflow: 'hidden' }}>
                {/* Main Row */}
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 2,
                    p: 1.5,
                    backgroundColor: 'background.paper',
                  }}
                >
                  {/* Brand - TYPE - Subtype */}
                  <Typography variant="body2" sx={{ minWidth: 250 }}>
                    {group.brand_name.split(' ').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}
                    {' - '}
                    {group.type_name.toUpperCase()}
                    {' - '}
                    {group.subtype_name.split(' ').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}
                  </Typography>

                  {/* Color */}
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 120 }}>
                    <Box
                      sx={{
                        width: 20,
                        height: 20,
                        borderRadius: '50%',
                        backgroundColor: group.color_hex,
                        border: '2px solid #ccc',
                        flexShrink: 0,
                      }}
                    />
                    <Typography variant="body2">
                      {group.color_name.split(' ').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}
                    </Typography>
                  </Box>

                  {/* Original Weight */}
                  <Typography variant="body2" sx={{ minWidth: 60 }}>
                    {group.original_weight_grams}g
                  </Typography>

                  {/* Unopened Rolls Info */}
                  {group.unopenedRolls.length > 0 && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, ml: 'auto' }}>
                      <Typography variant="body2" color="text.secondary">
                        {group.unopenedRolls.length} unopened
                      </Typography>
                      <Button
                        size="small"
                        variant="contained"
                        onClick={(e) => {
                          e.stopPropagation()
                          handleOpenNewRoll(group)
                        }}
                        startIcon={<CheckCircleIcon />}
                      >
                        Open New
                      </Button>
                    </Box>
                  )}

                  {/* Duplicate Button */}
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDuplicateGroup(group)
                    }}
                    startIcon={<ContentCopyIcon />}
                    sx={{ ml: group.unopenedRolls.length === 0 ? 'auto' : 0 }}
                  >
                    Duplicate
                  </Button>
                </Box>

                {/* Opened Rolls Sub-section */}
                {group.openedRolls.length > 0 && (
                  <Box>
                    {group.openedRolls.map((roll) => (
                      <Box
                        key={roll.id}
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1.5,
                          p: 1,
                          pl: 4,
                          backgroundColor: 'background.paper',
                          borderTop: '1px solid',
                          borderColor: 'divider',
                        }}
                      >
                        <Box sx={{ flex: 1 }}>
                          <Tooltip
                            title={
                              <Box>
                                <Typography variant="caption" display="block">
                                  Created: {new Date(roll.created_at + 'Z').toLocaleString()}
                                </Typography>
                                <Typography variant="caption" display="block">
                                  Updated: {new Date(roll.updated_at + 'Z').toLocaleString()}
                                </Typography>
                              </Box>
                            }
                            placement="left"
                          >
                            <Typography variant="body2" sx={{ fontWeight: 'bold', cursor: 'help', display: 'inline' }}>
                              Roll #{roll.id}
                            </Typography>
                          </Tooltip>
                        </Box>
                        <Box
                          onClick={(e) => {
                            e.stopPropagation()
                            handleWeightClick(roll)
                          }}
                          sx={{
                            cursor: 'pointer',
                            padding: '4px 8px',
                            borderRadius: '4px',
                            backgroundColor: 'action.hover',
                            transition: 'background-color 0.2s',
                            '&:hover': {
                              backgroundColor: 'action.selected',
                            },
                          }}
                        >
                          <Typography variant="body2">
                            {roll.weight_grams}g
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', gap: 0.5 }}>
                          <Button
                            size="small"
                            variant="text"
                            onClick={async (e) => {
                              e.stopPropagation()
                              try {
                                await api.post(`/v1/filly/rolls/${roll.id}/update_weight`, {
                                  decrease_by_grams: 50
                                })
                                fetchRolls()
                              } catch (err) {
                                console.error('Weight update error:', err)
                              }
                            }}
                            sx={{ minWidth: 'auto', px: 0.5, fontSize: '0.7rem' }}
                          >
                            -50g
                          </Button>
                          <Button
                            size="small"
                            variant="text"
                            onClick={async (e) => {
                              e.stopPropagation()
                              try {
                                await api.post(`/v1/filly/rolls/${roll.id}/update_weight`, {
                                  decrease_by_grams: 100
                                })
                                fetchRolls()
                              } catch (err) {
                                console.error('Weight update error:', err)
                              }
                            }}
                            sx={{ minWidth: 'auto', px: 0.5, fontSize: '0.7rem' }}
                          >
                            -100g
                          </Button>
                          <Button
                            size="small"
                            variant="text"
                            onClick={async (e) => {
                              e.stopPropagation()
                              try {
                                await api.post(`/v1/filly/rolls/${roll.id}/update_weight`, {
                                  new_weight_grams: 0
                                })
                                fetchRolls()
                              } catch (err) {
                                console.error('Weight update error:', err)
                              }
                            }}
                            sx={{ minWidth: 'auto', px: 0.5, fontSize: '0.7rem' }}
                          >
                            empty
                          </Button>
                        </Box>
                        <Button
                          size="small"
                          variant="outlined"
                          color={roll.in_use ? 'primary' : 'inherit'}
                          onClick={(e) => {
                            e.stopPropagation()
                            handleToggleInUse(roll.id, roll.in_use)
                          }}
                          startIcon={roll.in_use ? <ToggleOnIcon /> : <ToggleOffIcon />}
                        >
                          In Use
                        </Button>
                      </Box>
                    ))}
                  </Box>
                )}
              </Box>
            ))
          )}
        </Box>
      </Box>

      {/* Add Roll Dialog */}
      <AddRollDialog
        open={addOpen}
        onClose={() => setAddOpen(false)}
        onSuccess={handleAddSuccess}
      />

      {/* Weight Edit Dialog */}
      <Dialog open={weightDialogOpen} onClose={handleWeightDialogClose} maxWidth="xs" fullWidth>
        <DialogTitle>
          Update Weight
          {editingRoll && !editingRoll.opened && (
            <Typography variant="caption" display="block" color="warning.main" sx={{ mt: 1 }}>
              This roll will be marked as opened
            </Typography>
          )}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              autoFocus
              label="New Weight (grams)"
              type="number"
              fullWidth
              value={newWeight}
              onChange={(e) => setNewWeight(e.target.value)}
              inputProps={{ min: 0, step: 0.1 }}
            />
            {editingRoll && (
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                <Typography variant="body2" color="text.secondary">
                  Current Weight: {editingRoll.weight_grams}g
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Original Weight: {editingRoll.original_weight_grams}g
                </Typography>
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleWeightDialogClose} color="inherit">
            Cancel
          </Button>
          <Button onClick={handleWeightUpdate} variant="contained">
            Update
          </Button>
        </DialogActions>
      </Dialog>

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
