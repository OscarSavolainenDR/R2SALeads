import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { 
    apiGetLeadsTable, 
    apiUpdateLeadsListBackend,
    apiDownloadExcel,
    // apiGetScrumBoardtMembers,
} from 'services/ProjectService'

export const getLeads = createAsyncThunk('projectTableView/data/getLeads', async (data) => {
    const response = await apiGetLeadsTable(data)
    return response.data
})


export const updateLeadsListBackend = async (data) => {
    const response = await apiUpdateLeadsListBackend(data)
    return response.status
}

// original
// export const downloadExcelBackend = createAsyncThunk('projectTableView/downloadExcel', async (data) => {
//     const response = await apiDownloadExcel(data)
//     return response.data
// })

// attempt
export const downloadExcelBackend = async (data) => {
    const response = await apiDownloadExcel(data)
    return response.data
}

// export const getMembers = createAsyncThunk('scrumBoard/getMembers', async () => {
//     const response = await apiGetScrumBoardtMembers()
//     return response.data
// })

export const initialTableData = {
    total: 0,
    pageIndex: 1,
    pageSize: 10,
    query: '',
    sort: {
        order: '',
        key: ''
    }
}

export const initialFilterData = {
    name: '',
    // category: ['England', 'Wales', 'Scotland', 'Ireland'],
    // beds: [1, 2, 3, 4, 5],
    status: [0, 1, 2], // subscribed, in basket or not subscribed
    productStatus: 0,
}
// state.projectTableView.data.productList)
const dataSlice = createSlice({
    name: 'projectTableView/data',
    initialState: {
        loading: false,
        productList: [],
        // checkoutBasket: [],
        tableData: initialTableData,
        filterData: initialFilterData,
    },
    reducers: {
        updateProductList: (state, action) => {
            state.productList = action.payload
        },
        // updateCheckoutBasket: (state, action) => {
        //     state.checkoutBasket = action.payload
        // },
        setTableData: (state, action) => {
            state.tableData = action.payload
        },
        setFilterData: (state, action) => {
            state.filterData = action.payload
        },
    },
    extraReducers: {
        [getLeads.fulfilled]: (state, action) => {
            state.productList = JSON.parse(action.payload.data)
            state.tableData.total = action.payload.total
            state.loading = false
        },
        [getLeads.pending]: (state) => {
            state.loading = true
        },
        // [updateLeadsListBackend.fulfilled]: (state, action) => {
        //     console.log('here')
        //     // state.tableData.total = JSON.parse(JSON.stringify(state.tableData.total))
        //     // state.productList = JSON.parse(JSON.stringify(state.productList))
        //     state.loading = false
        // },
        // [updateLeadsListBackend.pending]: (state) => {
        //     console.log('what')
        //     state.loading = true
        // },
    }
})

export const { updateProductList, setTableData, setFilterData, setSortedColumn, updateCheckoutBasket } = dataSlice.actions

export default dataSlice.reducer
