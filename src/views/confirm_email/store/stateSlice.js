import { createSlice } from '@reduxjs/toolkit'

const stateSlice = createSlice({
    name: 'projectTableView2/state',
    initialState: {
        deleteConfirmation: false,
        removeConfirmation: false,
        selectedProduct: '',
        sortedColumn: () => {},
    },
    reducers: {
        toggleDeleteConfirmation: (state, action) => {
            state.deleteConfirmation = action.payload
        },
        toggleRemoveConfirmation: (state, action) => {
            state.removeConfirmation = action.payload
        },
        setSortedColumn: (state, action) => {
            state.sortedColumn = action.payload
        },
        setSelectedProduct: (state, action) => {
            state.selectedProduct = action.payload
        },
    },
})

export const { 
    toggleDeleteConfirmation, 
    toggleRemoveConfirmation,
    setSortedColumn,
    setSelectedProduct
} = stateSlice.actions

export default stateSlice.reducer
