import ApiService from "./ApiService"

export async function apiGetNotificationCount () {
    return ApiService.fetchData({
        url: '/notification/count',
        method: 'get'
    })
}

export async function apiGetNotificationList () {
    return ApiService.fetchData({
        url: '/notification/list',
        method: 'get'
    })
}
