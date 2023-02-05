import React from 'react'
import reducer from './store'
import { injectReducer } from 'store/index'
import { AdaptableCard } from 'components/shared'
import LeadsProductTable from './components/LeadsProductTable'
import LeadsProductTableTools from './components/LeadsProductTableTools'

injectReducer('projectTableView', reducer)

const LeadsTableView = () => {
	return (
		<AdaptableCard className="h-full" bodyClass="h-full">
			<div className="lg:flex items-center justify-between mb-4">
				<h3 className="mb-4 lg:mb-0">Listings</h3>
				<LeadsProductTableTools />
			</div>
			<LeadsProductTable />
		</AdaptableCard>
	)
}

export default LeadsTableView