import { APP_PREFIX_PATH } from 'constants/route.constant'
import { NAV_ITEM_TYPE_TITLE, NAV_ITEM_TYPE_COLLAPSE, NAV_ITEM_TYPE_ITEM } from 'constants/navigation.constant'
import { ADMIN, USER } from 'constants/roles.constant'


const navigationConfig = [
    {
        key: 'home',
		path: '/home',
		title: 'Home',
		translateKey: 'nav.home',
		icon: 'home',
		type: NAV_ITEM_TYPE_ITEM,
		authority: [],
        subMenu: []
    },
	{
		key: 'appsProject.scrumBoard',
		path: `${APP_PREFIX_PATH}/project/scrum-board`,
		title: 'Leads',
		translateKey: 'nav.appsProject.scrumBoard',
		icon: 'scrumBoard',
		type: NAV_ITEM_TYPE_ITEM,
		authority: [ADMIN, USER],
		subMenu: []
	},
	{
		key: 'appsSales.productList',
		path: `${APP_PREFIX_PATH}/subscribe/product-list`,
		title: 'Manage Lead Subscriptions',
		translateKey: 'nav.appsSales.productList',
		icon: 'subscriptions',
		type: NAV_ITEM_TYPE_ITEM,
		authority: [ADMIN, USER],
		subMenu: []
	},
	// {
	// 	key: 'appsAccount.settings',
	// 	path: `${APP_PREFIX_PATH}/account/settings/profile`,
	// 	title: 'Account',
	// 	translateKey: 'nav.appsAccount.settings',
	// 	icon: 'account',
	// 	type: NAV_ITEM_TYPE_ITEM,
	// 	authority: [ADMIN, USER],
	// 	subMenu: []
	// },
]

export default navigationConfig