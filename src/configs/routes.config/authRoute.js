import React from 'react'

const authRoute = [
    {
        key: 'signIn',
        path: `/sign-in`,
        component: React.lazy(() => import('views/auth/SignIn')),
        authority: [],
    },
    {
        key: 'signUp',
        path: `/sign-up`,
        component: React.lazy(() => import('views/auth/SignUp')),
        authority: [],
    },
    {
        key: 'forgotPassword',
        path: `/forgot-password`,
        component: React.lazy(() => import('views/auth/ForgotPassword')),
        authority: [],
    },
    {
        key: 'resetPassword',
        path: `/reset-password/:uid/:token`,
        component: React.lazy(() => import('views/auth/ResetPassword')),
        authority: [],
    },
    // {
    //     key: 'confirmEmail_not_auth',
    //     path: `/confirm-email/:uid/:token`,
    //     component: React.lazy(() => import('views/auth/EmailConfirmed')),
    //     authority: [],
    // }
]

export default authRoute