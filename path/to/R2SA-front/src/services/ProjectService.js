import ApiService from "./ApiService"

export async function apiGetScrumBoards () {
    return ApiService.fetchData({
        url: '/project/scrum-board/boards',
        method: 'post',
    })
}

export async function apiUpdateLeadsListBackend (data) {
    return ApiService.fetchData({
        url: '/project/leads-list/update-backend',
        method: 'post',
        data // We send the updated ordering.
    })
}

export async function apiGetLeadsTable (data) {
    return ApiService.fetchData({
        url: '/project/table-view/get-leads',
        method: 'post',
        data
    })
}


export async function apiUpdateBoardBackend (data) {
    return ApiService.fetchData({
        url: '/project/scrum-board/update-backend',
        method: 'post',
        data // We send the updated ordering.
    })
}

export async function apiDownloadExcel (data) {
    return ApiService.fetchData({
        url: '/project/scrum-board/download-excel',
        method: 'post',
        data // We send the specific listing we want the excel for
    })
}
