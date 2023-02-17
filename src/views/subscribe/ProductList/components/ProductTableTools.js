import React, { useEffect, useState } from 'react'
import { Button } from 'components/ui'
import { HiDownload, HiShoppingCart } from 'react-icons/hi'
import ProductTableSearch from './ProductTableSearch'
import { checkout } from '../store/dataSlice'
// import ProductFilter from './ProductFilter'
import { useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import { loadStripe } from "@stripe/stripe-js"
import { apiGetEmailStatus } from 'services/AuthService'


let stripePromise
const getStripe = () => {
    if (!stripePromise) {
        stripePromise = loadStripe(process.env.REACT_APP_STRIPE_KEY) // need
    }
    return stripePromise
}


const ProductTableTools = () => {

	const [confirmed, setConfirmed] = useState(false);

	useEffect(() => {
		
		const fetchData = async () =>
		{
			const response = await apiGetEmailStatus()
			// console.log('Email confirmed', response.data.email_status)
			setConfirmed(response.data.email_status)
		}
		fetchData();
	  });

	


	// const navigate = useNavigate()
	// Make API call to backend, which returns url to redirect to
	const onCheckout = async () => {
		const response = await checkout({data: data})
		const resp = JSON.parse(response.data)
		// console.log(resp)
		const lineItems = resp.items
		const email = resp.email

		const checkoutOptions = {
			lineItems: lineItems,
			mode: "subscription",
			successUrl: `${window.location.origin}/app/subscribe/product-list`,
			cancelUrl: `${window.location.origin}/app/subscribe/product-list`,
			customerEmail: email,
		}

		// console.log(response)

		if (response.status) {
			console.log('redirect to checkout')

			// Set Loading to true

			const stripe = await getStripe()
			const { error } = await stripe.redirectToCheckout(checkoutOptions)
			console.log("Stripe checkout error", error)
		}
	} 

	// Get number of elements in checkout basket
	const data = useSelector((state) => state.salesProductList.data.productList)
	const sum_checkout_basket = data.reduce((prev,next) => prev + (next.status == 1),0);

		//  && (confirmed)
	if ((sum_checkout_basket > 0)) {
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
				{/* <Link 
					className="block lg:inline-block md:mb-0 mb-4"
					 to="/app/subscribe/checkout-basket" 
				> */}
					<Button
						block
						variant="solid"
						size="sm" 
						onClick={onCheckout}
						icon={<HiShoppingCart />}
					>
						Checkout
					</Button>
				{/* </Link> */}
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