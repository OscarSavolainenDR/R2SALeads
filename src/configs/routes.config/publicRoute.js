import React from 'react'
import { APP_PREFIX_PATH } from 'constants/route.constant'

const authRoute = [
    {
        key: 'home',
        path: '/home',
        component: React.lazy(() => import('views/LandingPage')),
        authority: [],
    },
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
    {
        key: 'confirmEmail_not_auth',
        path: `/confirm-email/:uid/:token`,
        component: React.lazy(() => import('views/auth/EmailConfirmed')),
        authority: [],
    },
    {
        key: 'appsLegals.terms',
        path: `${APP_PREFIX_PATH}/legals/terms-and-conditions`,
        component: React.lazy(() => import('views/legals/TermsAndConditions')),
        authority: [], // If private, should be [ADMIN, USER]
    },
    {
        key: 'appsLegals.privacy',
        path: `${APP_PREFIX_PATH}/legals/privacy-policy`,
        component: React.lazy(() => import('views/legals/PrivacyPolicy')),
        authority: [], // If private, should be [ADMIN, USER]
    },
    {
        key: 'appsProject.tableView',
        path: `${APP_PREFIX_PATH}/project/table-view`,
        component: React.lazy(() => import('views/project/ProductList')),
        authority: [], // If private, should be [ADMIN, USER]
        meta: {
            pageContainerType: 'gutterless'
        }
    },
    {
        key: 'appsSales.productList',
        path: `${APP_PREFIX_PATH}/subscribe/product-list`,
        component: React.lazy(() => import('views/subscribe/ProductList')),
        authority: [], // If private, should be [ADMIN, USER]
    },
]

export default authRoute