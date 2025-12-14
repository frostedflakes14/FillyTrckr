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
  Typography,
  CircularProgress,
} from '@mui/material'
import CloseIcon from '@mui/icons-material/Close'
import { HexColorPicker } from 'react-colorful'
import { api } from '../utils/api'

type AddItemDialogProps = {
  open: boolean
  onClose: () => void
  onSuccess: (data: any) => void
  apiEndpoint: string
  itemType?: string
  showColorPicker?: boolean
}

/**
 * Reusable AddItemDialog
 * - Shows a dialog with a name field and a color picker
 * - Performs a POST to `apiEndpoint` with { name } (hex is available in code but commented out)
 */
const AddItemDialog: React.FC<AddItemDialogProps> = ({ open, onClose, onSuccess, apiEndpoint, itemType = 'item', showColorPicker = true }) => {
  const [name, setName] = useState('')
  const [color, setColor] = useState('#aabbcc')
  const [nameError, setNameError] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (open) {
      setName('')
      setColor('#aabbcc')
      setNameError(false)
      setLoading(false)
    }
  }, [open])

  const handleAdd = async () => {
    if (!name.trim()) {
      setNameError(true)
      return
    }

    setLoading(true)
    try {
      const payload: any = { name: name.trim() }
      // Include hex_code if color picker is shown
      if (showColorPicker) {
        payload.hex_code = color
      }

      const resp = await api.post(apiEndpoint, payload)
      // resp.data is passed back to caller for message/display
      onSuccess(resp.data)
      onClose()
    } catch (err: any) {
      // Pass error object back so caller can show message
      onSuccess({ error: true, detail: err?.response?.data || err?.message || String(err) })
      onClose()
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ m: 0, p: 2 }}>
        Add new {itemType}
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{ position: 'absolute', right: 8, top: 8 }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label={`${itemType.charAt(0).toUpperCase() + itemType.slice(1)} name`}
            value={name}
            onChange={(e) => {
              setName(e.target.value)
              if (nameError && e.target.value.trim()) setNameError(false)
            }}
            error={nameError}
            helperText={nameError ? `Please type a name for the new ${itemType}` : ''}
            fullWidth
            autoFocus
          />
          {showColorPicker && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Color (preview)
              </Typography>

              <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                <Box sx={{ width: 220 }}>
                  <HexColorPicker color={color} onChange={setColor} />
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Box sx={{ width: 56, height: 56, borderRadius: 1, backgroundColor: color, border: '1px solid rgba(0,0,0,0.12)' }} />
                  <TextField
                    label="Hex Code"
                    value={color.toUpperCase()}
                    onChange={(e) => {
                      const value = e.target.value.trim()
                      // Allow typing # prefix or not
                      if (value.match(/^#?[0-9A-Fa-f]{0,6}$/)) {
                        const normalized = value.startsWith('#') ? value : `#${value}`
                        setColor(normalized)
                      }
                    }}
                    placeholder="#AABBCC"
                    size="small"
                    sx={{ width: 120 }}
                  />
                </Box>
              </Box>
            </Box>
          )}
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} color="inherit">
          Cancel
        </Button>
        <Button variant="contained" onClick={handleAdd} disabled={loading} startIcon={loading ? <CircularProgress size={18} /> : undefined}>
          {loading ? 'Adding...' : `Add new ${itemType}`}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default AddItemDialog
