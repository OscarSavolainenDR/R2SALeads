import React from 'react'
import { Button } from 'components/ui'
import { HiDownload, HiShoppingCart } from 'react-icons/hi'
import ProductTableSearch from './ProductTableSearch'
// import ProductFilter from './ProductFilter'
import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'

const ProductTableTools = () => {

	// Get number of elements in checkout basket
	const data = useSelector((state) => state.salesProductList.data.productList)
	const sum_checkout_basket = data.reduce((prev,next) => prev + (next.status == 1),0);

	if (sum_checkout_basket > 0) {
		return (
			<div className="flex flex-col lg:flex-row lg:items-center">
				<div style={{marginRight: '10px'}}>
					<ProductTableSearch />
				</div>
				
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
				<Link 
					className="block lg:inline-block md:mb-0 mb-4"
					 to="/app/subscribe/checkout-basket" 
				>
					<Button
						block
						variant="solid"
						size="sm" 
						icon={<HiShoppingCart />}
					>
						Checkout
					</Button>
				</Link>
			</div>
		)
	} else {
		return (
			<div className="flex flex-col lg:flex-row lg:items-center">
				<ProductTableSearch />
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

}

export default ProductTableTools