import ApiService from "./ApiService"

export async function apiPostFeedback (data) {
    return ApiService.fetchData({
        url: '/feedback/submit',
        method: 'post',
        data,
    })
}
