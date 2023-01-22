import ApiService from "./ApiService"

export async function apiGetSalesProducts (data) {
    return ApiService.fetchData({
        url: '/subscriptions/products',
        method: 'post',
        data
    })
}

export async function apiUnsubscribeCity (data) {
    return ApiService.fetchData({
        url: '/subscriptions/unsubscribe',
        method: 'post',
        data
    })
}

export async function apiAddCityToBasket (data) {
    return ApiService.fetchData({
        url: '/subscriptions/add-to-basket',
        method: 'post',
        data,
    })
}

export async function apiGetCheckoutBasket () {
    return ApiService.fetchData({
        url: '/subscriptions/get-basket',
        method: 'post',
    })
}