
// import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { apiGetEmailStatus } from 'services/AuthService'

export const getEmailStatus = async () => {
    const response = await apiGetEmailStatus()
    // console.log(response)
    return response
}

// export const getLeads = createAsyncThunk('projectTableView2/data/getLeads', async () => {
//     const response = await apiGetEmailStatus()
//     console.log(response)
//     return response.data
// })

// const dataSlice = createSlice({
//     name: 'projectTableView2/data',
//     initialState: {
//         loading: false,
//         productList: [],
//     },
//     reducers: {
//         updateProductList: (state, action) => {
//             state.productList = action.payload
//         },
//         setTableData: (state, action) => {
//             state.tableData = action.payload
//         },
//         setFilterData: (state, action) => {
//             state.filterData = action.payload
//         },
//     },
//     extraReducers: {
//         [getLeads.fulfilled]: (state, action) => {
//             console.log('Soemnthing')
//             state.productList = JSON.parse(action.payload.data)
//             state.tableData.total = action.payload.total
//             state.loading = false
//         },
//         [getLeads.pending]: (state) => {
//             state.loading = true
//         },
//     }
// })

// export const { updateProductList, setTableData, setFilterData, setSortedColumn, updateCheckoutBasket } = dataSlice.actions

// export default dataSlice.reducer

