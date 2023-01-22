import ApiService from "./ApiService"

export async function apiGetAccountSettingData () {
    return ApiService.fetchData({
        url: '/account/setting',
        method: 'post'
    })
}

export async function apiGetAccountSettingBillingData () {
    return ApiService.fetchData({
        url: '/account/setting/billing',
        method: 'post'
    })
}

export async function apiUpdatePassword (data) {
    return ApiService.fetchData({
        url: '/account/update-password',
        method: 'post',
        data,
    })
}
