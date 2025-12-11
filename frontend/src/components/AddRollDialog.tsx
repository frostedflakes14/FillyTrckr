import React, { useState, useEffect } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  TextField,
  Button,
  Box,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
} from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'
import { api } from '../utils/api'

type AddRollDialogProps = {
  open: boolean
  onClose: () => void
  onSuccess: (data: any) => void
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

/**
 * AddRollDialog - Dialog for adding a new filament roll
 * - Shows dropdowns for Type, Brand, Color, and Subtype
 * - Shows text field for original weight (defaults to 1000)
 * - Submits IDs to the API
 */
const AddRollDialog: React.FC<AddRollDialogProps> = ({ open, onClose, onSuccess }) => {
  const [brandId, setBrandId] = useState<number | ''>('')
  const [colorId, setColorId] = useState<number | ''>('')
  const [typeId, setTypeId] = useState<number | ''>('')
  const [subtypeId, setSubtypeId] = useState<number | ''>('')
  const [originalWeight, setOriginalWeight] = useState<string>('1000')

  const [brands, setBrands] = useState<Brand[]>([])
  const [colors, setColors] = useState<Color[]>([])
  const [types, setTypes] = useState<Type[]>([])
  const [subtypes, setSubtypes] = useState<Subtype[]>([])

  const [loading, setLoading] = useState(false)
  const [loadingData, setLoadingData] = useState(false)
  const [errors, setErrors] = useState({
    brandId: false,
    colorId: false,
    typeId: false,
    subtypeId: false,
    originalWeight: false,
  })

  // Fetch lookup data when dialog opens
  useEffect(() => {
    if (open) {
      // Reset form
      setBrandId('')
      setColorId('')
      setTypeId('')
      setSubtypeId('')
      setOriginalWeight('1000')
      setErrors({
        brandId: false,
        colorId: false,
        typeId: false,
        subtypeId: false,
        originalWeight: false,
      })
      setLoading(false)

      // Fetch lookup data
      fetchLookupData()
    }
  }, [open])

  const fetchLookupData = async () => {
    setLoadingData(true)
    try {
      const [brandsRes, colorsRes, typesRes, subtypesRes] = await Promise.all([
        api.get('/v1/filly/brands'),
        api.get('/v1/filly/colors'),
        api.get('/v1/filly/types'),
        api.get('/v1/filly/subtypes')
      ])

      setBrands(brandsRes.data.brands)
      setColors(colorsRes.data.colors)
      setTypes(typesRes.data.types)
      setSubtypes(subtypesRes.data.subtypes)
    } catch (err) {
      console.error('Failed to fetch lookup data:', err)
    } finally {
      setLoadingData(false)
    }
  }

  const handleAdd = async () => {
    // Validate all fields
    const newErrors = {
      brandId: brandId === '',
      colorId: colorId === '',
      typeId: typeId === '',
      subtypeId: subtypeId === '',
      originalWeight: !originalWeight.trim() || isNaN(Number(originalWeight)) || Number(originalWeight) <= 0,
    }

    setErrors(newErrors)

    // Check if any errors
    if (Object.values(newErrors).some(error => error)) {
      return
    }

    setLoading(true)
    try {
      const payload = {
        brand_id: Number(brandId),
        color_id: Number(colorId),
        type_id: Number(typeId),
        subtype_id: Number(subtypeId),
        original_weight_grams: Number(originalWeight),
      }

      const resp = await api.post('/v1/filly/rolls/add', payload)
      onSuccess(resp.data)
      onClose()
    } catch (err: any) {
      onSuccess({ error: true, detail: err?.response?.data || err?.message || String(err) })
      onClose()
    } finally {
      setLoading(false)
    }
  }

  const handleBrandChange = (event: SelectChangeEvent<number | ''>) => {
    setBrandId(event.target.value as number)
    if (errors.brandId && event.target.value !== '') {
      setErrors({ ...errors, brandId: false })
    }
  }

  const handleColorChange = (event: SelectChangeEvent<number | ''>) => {
    setColorId(event.target.value as number)
    if (errors.colorId && event.target.value !== '') {
      setErrors({ ...errors, colorId: false })
    }
  }

  const handleTypeChange = (event: SelectChangeEvent<number | ''>) => {
    setTypeId(event.target.value as number)
    if (errors.typeId && event.target.value !== '') {
      setErrors({ ...errors, typeId: false })
    }
  }

  const handleSubtypeChange = (event: SelectChangeEvent<number | ''>) => {
    setSubtypeId(event.target.value as number)
    if (errors.subtypeId && event.target.value !== '') {
      setErrors({ ...errors, subtypeId: false })
    }
  }

  const handleWeightChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setOriginalWeight(event.target.value)
    if (errors.originalWeight && event.target.value.trim() && !isNaN(Number(event.target.value)) && Number(event.target.value) > 0) {
      setErrors({ ...errors, originalWeight: false })
    }
  }

  const capitalizeWords = (str: string) => {
    return str
      .split(' ')
      .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ')
  }

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ m: 0, p: 2 }}>
        Add new roll
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{ position: 'absolute', right: 8, top: 8 }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        {loadingData ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 200 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.5 }}>
            <FormControl fullWidth error={errors.brandId}>
              <InputLabel id="brand-select-label">Brand</InputLabel>
              <Select
                labelId="brand-select-label"
                id="brand-select"
                value={brandId}
                label="Brand"
                onChange={handleBrandChange}
              >
                {brands.map((brand) => (
                  <MenuItem key={brand.id} value={brand.id}>
                    {capitalizeWords(brand.name)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth error={errors.typeId}>
              <InputLabel id="type-select-label">Type</InputLabel>
              <Select
                labelId="type-select-label"
                id="type-select"
                value={typeId}
                label="Type"
                onChange={handleTypeChange}
              >
                {types.map((type) => (
                  <MenuItem key={type.id} value={type.id}>
                    {type.name.toUpperCase()}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth error={errors.subtypeId}>
              <InputLabel id="subtype-select-label">Subtype</InputLabel>
              <Select
                labelId="subtype-select-label"
                id="subtype-select"
                value={subtypeId}
                label="Subtype"
                onChange={handleSubtypeChange}
              >
                {subtypes.map((subtype) => (
                  <MenuItem key={subtype.id} value={subtype.id}>
                    {capitalizeWords(subtype.name)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth error={errors.colorId}>
              <InputLabel id="color-select-label">Color</InputLabel>
              <Select
                labelId="color-select-label"
                id="color-select"
                value={colorId}
                label="Color"
                onChange={handleColorChange}
              >
                {colors.map((color) => (
                  <MenuItem key={color.id} value={color.id}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Box
                        sx={{
                          width: 20,
                          height: 20,
                          borderRadius: '50%',
                          backgroundColor: color.hex_code,
                          border: '1px solid #ccc',
                        }}
                      />
                      {capitalizeWords(color.name)}
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Original Weight (grams)"
              type="number"
              value={originalWeight}
              onChange={handleWeightChange}
              error={errors.originalWeight}
              helperText={errors.originalWeight ? 'Please enter a valid weight greater than 0' : ''}
              fullWidth
              inputProps={{ min: 0, step: 1 }}
            />
          </Box>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} color="inherit">
          Cancel
        </Button>
        <Button
          variant="contained"
          onClick={handleAdd}
          disabled={loading || loadingData}
          startIcon={loading ? <CircularProgress size={18} /> : undefined}
        >
          {loading ? 'Adding...' : 'Add new roll'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default AddRollDialog
