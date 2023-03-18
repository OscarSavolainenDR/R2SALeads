import React from 'react'
import authRoute from './authRoute'
import { APP_PREFIX_PATH } from 'constants/route.constant'
import { ADMIN, USER } from 'constants/roles.constant'

export const publicRoutes = [
    ...authRoute
]

export const protectedRoutes = [
    {
        key: 'home',
        path: '/home',
        component: React.lazy(() => import('views/LandingPage')),
        authority: [ADMIN, USER],
    },
    {
        key: 'appsProject.scrumBoard',
        path: `${APP_PREFIX_PATH}/project/scrum-board`,
        component: React.lazy(() => import('views/project/ScrumBoard')),
        authority: [ADMIN, USER],
        meta: {
            pageContainerType: 'gutterless'
        }
    },
    {
        key: 'appsProject.tableView',
        path: `${APP_PREFIX_PATH}/project/table-view`,
        component: React.lazy(() => import('views/project/ProductList')),
        authority: [ADMIN, USER],
        meta: {
            pageContainerType: 'gutterless'
        }
    },
    {
        key: 'appsSales.productList',
        path: `${APP_PREFIX_PATH}/subscribe/product-list`,
        component: React.lazy(() => import('views/subscribe/ProductList')),
        authority: [ADMIN, USER],
    },
    {
        key: 'appsSales.checkout',
        path: `${APP_PREFIX_PATH}/subscribe/checkout-basket`,
        component: React.lazy(() => import('views/subscribe/OrderDetails')),
        authority: [ADMIN, USER],
    },
    {
        key: 'appsLegals.terms',
        path: `${APP_PREFIX_PATH}/legals/terms-and-conditions`,
        component: React.lazy(() => import('views/legals/TermsAndConditions')),
        authority: [ADMIN, USER],
    },
    {
        key: 'appsLegals.privacy',
        path: `${APP_PREFIX_PATH}/legals/privacy-policy`,
        component: React.lazy(() => import('views/legals/PrivacyPolicy')),
        authority: [ADMIN, USER],
    },
    // {
    //     key: 'appsAccount.settings',
    //     path: `${APP_PREFIX_PATH}/account/settings/:tab`,
    //     component: React.lazy(() => import('views/account/Settings')),
    //     authority: [ADMIN, USER],
    //     meta: {
    //         header: 'Account',
    //         headerContainer: true
    //     }
    // },
    {
        key: 'appsGen.contact',
        path: `${APP_PREFIX_PATH}/contact`,
        component: React.lazy(() => import('views/feedback')),
        authority: [ADMIN, USER],
        meta: {
            header: 'Contact',
            headerContainer: true
        }
    },
    {
        key: 'confirmEmail',
        path: `${APP_PREFIX_PATH}/confirm-email/:token`,
        component: React.lazy(() => import('views/auth/EmailConfirmed')), 
        authority: [ADMIN, USER],
    }

]