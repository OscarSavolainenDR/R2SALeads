import React from 'react'
import { Button } from 'components/ui'
import { HiDownload, HiShoppingCart } from 'react-icons/hi'
import LeadsProductTableSearch from './LeadsProductTableSearch'
// import ProductFilter from './ProductFilter'
import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'

const LeadsProductTableTools = () => {

	// Get number of elements in checkout basket
	const data = useSelector((state) => state.projectTableView.data.productList)
	// const sum_checkout_basket = data.reduce((prev,next) => prev + (next.status == 1),0);

	return (
		<div className="flex flex-col lg:flex-row lg:items-center">
			<LeadsProductTableSearch />
			{/* <ProductFilter /> */}
			{/* <Link 
				className="block lg:inline-block md:mx-2 md:mb-0 mb-4" 
				to="/data/product-list.csv" 
				target="_blank" 
				download
			>
				<Button
					block
					size="sm" 
					icon={<HiDownload />}
				>
					Export
				</Button>
			</Link> */}
		</div>
	)

}

export default LeadsProductTableTools