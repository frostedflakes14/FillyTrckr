import { GridColDef, GridRenderCellParams } from '@mui/x-data-grid'
import { formatDistanceToNow } from 'date-fns'
import { Tooltip } from '@mui/material'

/**
 * Creates a reusable datetime column configuration for DataGrid.
 * Displays relative time (e.g., "3 days ago") with a tooltip showing the full date.
 * Handles UTC timestamps from the backend by appending 'Z' for proper timezone conversion.
 *
 * @param field - The field name in the data (default: 'created_at')
 * @param headerName - The column header text (default: 'Created At')
 * @param flex - The flex value for column width (default: 1)
 * @param minWidth - The minimum width in pixels (default: 200)
 * @returns GridColDef configuration object
 */
export function createDateTimeColumn(
  field: string = 'created_at',
  headerName: string = 'Created At',
  flex: number = 1,
  minWidth: number = 200
): GridColDef {
  return {
    field,
    headerName,
    flex,
    minWidth,
    type: 'dateTime',
    valueGetter: (value: string) => {
      if (!value) return null
      // Check if the timestamp already has timezone info (ends with 'Z' or has '+'/'-' offset)
      const hasTimezone = value.endsWith('Z') || /[+-]\d{2}:\d{2}$/.test(value)
      // If no timezone info, append 'Z' to treat it as UTC
      return new Date(hasTimezone ? value : value + 'Z')
    },
    renderCell: (params: GridRenderCellParams) => {
      const date = params.value as Date
      if (!date) return null

      return (
        <Tooltip title={date.toLocaleString()} placement="bottom">
          <span>{formatDistanceToNow(date, { addSuffix: true })}</span>
        </Tooltip>
      )
    }
  }
}
