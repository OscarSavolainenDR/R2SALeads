import { createSlice } from '@reduxjs/toolkit'

const stateSlice = createSlice({
    name: 'projectTableView/state',
    initialState: {
        deleteConfirmation: false,
        removeConfirmation: false,
        selectedProduct: '',
        sortedColumn: () => {},
        toggledStatusChanges: [],
        APICounter: 0,
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
        addToggledStatusChanges: (state, action) => {
            // console.log(state.toggledStatusChanges, action.payload)
            state.toggledStatusChanges = action.payload 
            
        },
        setAPICounter: (state, action) => {
            // console.log(state.toggledStatusChanges, action.payload)
            state.APICounter = action.payload 
        },
    },
})

export const { 
    toggleDeleteConfirmation, 
    toggleRemoveConfirmation,
    setSortedColumn,
    setSelectedProduct,
    addToggledStatusChanges,
    setAPICounter,
} = stateSlice.actions

export default stateSlice.reducer
