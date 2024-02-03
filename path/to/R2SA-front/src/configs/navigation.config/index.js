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
		key: 'appsProject.tableView',
		path: `${APP_PREFIX_PATH}/project/table-view`,
		title: 'Leads',
		translateKey: 'nav.appsProject.tableView',
		icon: 'scrumBoard',
		type: NAV_ITEM_TYPE_ITEM,
		authority: [ADMIN, USER],
		subMenu: []
	},
	
	// {
	// 	key: 'appsProject',
	// 	path: '',
	// 	title: 'Leads',
	// 	translateKey: 'Leads',
	// 	icon: 'scrumBoard',
	// 	type: NAV_ITEM_TYPE_TITLE,
	// 	authority: [ADMIN, USER],
	// 	subMenu: [
	// 		{
	// 			key: 'appsProject.tableView',
	// 			path: `${APP_PREFIX_PATH}/project/table-view`,
	// 			title: 'Table View',
	// 			translateKey: 'nav.appsProject.tableView',
	// 			icon: '',
	// 			type: NAV_ITEM_TYPE_ITEM,
	// 			authority: [ADMIN, USER],
	// 			subMenu: []
	// 		},
	// 		// {
	// 		// 	key: 'appsProject.scrumBoard',
	// 		// 	path: `${APP_PREFIX_PATH}/project/scrum-board`,
	// 		// 	title: 'Board View',
	// 		// 	translateKey: 'nav.appsProject.scrumBoard',
	// 		// 	icon: '',
	// 		// 	type: NAV_ITEM_TYPE_ITEM,
	// 		// 	authority: [ADMIN, USER],
	// 		// 	subMenu: []
	// 		// },
	// 	]
	// },
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
	{
		key: 'appsGen.contact',
		path: `${APP_PREFIX_PATH}/contact`,
		title: 'Contact',
		translateKey: 'nav.appsGen.contact',
		icon: 'contact',
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