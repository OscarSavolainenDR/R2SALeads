import ApiService from './ApiService'

export async function apiSignIn (data) {
    return ApiService.fetchData({
        url: '/sign-in',
        method: 'post',
        data
    })
}

export async function apiSignUp (data) {
    return ApiService.fetchData({
        url: '/sign-up',
        method: 'post',
        data
    })
}

export async function apiSignOut (data) {
    return ApiService.fetchData({
        url: '/sign-out',
        method: 'post',
        data
    })
}

export async function apiForgotPassword (data) {
    return ApiService.fetchData({
        url: '/forgot-password',
        method: 'post',
        data,
    })
}

export async function apiResetPassword (data) {
    return ApiService.fetchData({
        url: '/reset-password',
        method: 'post',
        data,
    })
}

export async function apiGetEmailStatus () {
    return ApiService.fetchData({
        url: '/get-email-status',
        method: 'post',
    })
}


// We send this from the page the user is directed to from their email, we
// feed the token and uid back to the backend to confirm the email.
export async function apiConfirmEmail (data) {
    return ApiService.fetchData({
        url: '/confirm-email',
        method: 'post',
        data
    })
}

export async function apiResendConfirmEmail (data) {
    return ApiService.fetchData({
        url: '/resend-confirm-email',
        method: 'post',
        data
    })
}

