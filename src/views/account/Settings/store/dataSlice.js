// import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { 
    apiUpdatePassword
    // apiGetScrumBoardtMembers,
} from 'services/AccountServices'

export const updatePassword = async (data) => {
    const response = await apiUpdatePassword(data)
    return response.status
}



// export const getMembers = createAsyncThunk('scrumBoard/getMembers', async () => {
//     const response = await apiGetScrumBoardtMembers()
//     return response.data
// })

// const dataSlice = createSlice({
//     name: 'scrumBoard/data',
//     initialState: {
//         loading: false,
//         columns: {},
//         ordered: [],
//         excel_json_str: {},
//         boardMembers: [],
//         allMembers: []
//     },
//     reducers: {
//         updateColumns: (state, action) => {
//             state.columns = action.payload
//         },
//         updateExcel: (state, action) => {
//             state.excel_json_str = action.payload.data
//         },
//     },
//     extraReducers: {
//         [getBoards.fulfilled]: (state, { payload }) => {
//             state.columns = payload
//             state.ordered = Object.keys(payload)
//             state.loading = false
//         },
//         [getBoards.pending]: (state) => {
//             state.loading = true
//         },
//     }
// })

// export const { updatePassword } = dataSlice.actions

// export default dataSlice.reducer
