import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { apiGetSalesProducts, apiUnsubscribeCity, apiAddCityToBasket, apiCheckout } from 'services/SubscribeService'

export const getProducts = createAsyncThunk('salesProductList/data/getProducts',async (data) => {
    const response = await apiGetSalesProducts(data)
    return response.data
})

export const checkout = async (data) => {
    const response = await apiCheckout(data)
    return response
}

export const unsubscribeCity = async (data) => {
    const response = await apiUnsubscribeCity(data)
    return response.status
}

export const addCityToBasket = async (data) => {
    const response = await apiAddCityToBasket(data)
    return response.status
}

export const initialTableData = {
    total: 0,
    pageIndex: 1,
    pageSize: 100,
    query: '',
    sort: {
        order: '',
        key: ''
    }
}

export const initialFilterData = {
    name: '',
    category: ['England', 'Wales', 'Scotland', 'Ireland'],
    // beds: [1, 2, 3, 4, 5],
    status: [0, 1, 2], // subscribed, in basket or not subscribed
    productStatus: 0,
}

const dataSlice = createSlice({
    name: 'salesProductList/data',
    initialState: {
        loading: false,
        productList: [],
        checkoutBasket: [],
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
        [getProducts.fulfilled]: (state, action) => {
            state.productList = JSON.parse(action.payload.data)
            state.tableData.total = action.payload.total
            state.loading = false
        },
        [getProducts.pending]: (state) => {
            state.loading = true
        },
    }
})

export const { updateProductList, setTableData, setFilterData, setSortedColumn, updateCheckoutBasket } = dataSlice.actions

export default dataSlice.reducer
