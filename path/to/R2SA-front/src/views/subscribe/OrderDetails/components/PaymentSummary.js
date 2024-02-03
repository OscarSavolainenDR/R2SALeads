import React from 'react'
import { Card } from 'components/ui'
import NumberFormat from 'react-number-format'
import StripeCheckoutForm from './StripeCheckoutForm'
import {Elements} from '@stripe/react-stripe-js';
import {loadStripe} from "@stripe/stripe-js/pure";
import { PUBLIC_STRIPE_KEY } from 'constants/stripe.constant';

const stripePromise = loadStripe(PUBLIC_STRIPE_KEY); 


const PaymentInfo = ({label, value, isLast}) => {

	return (
		<li className={`flex items-center justify-between${!isLast ? ' mb-3' : ''}`}>
			<span>{label}</span>
			
			<span className="font-semibold">
				<NumberFormat
					displayType="text"
					value={(Math.round(value * 100) / 100).toFixed(2)} 
					prefix={'£ '} 
					suffix={' / month, billed monthly'}
					thousandSeparator={true} 
				/>
			</span>
		</li>
	)
}

const PaymentSummary = ({data, product}) => {
	return (
		<div>
			<Card className="mb-4">
				<h5 className="mb-4">Payment Summary</h5>
				<ul>
					<PaymentInfo label="Subtotal" value={data.subTotal} />
					{/* <PaymentInfo label="Delivery fee" value={data.deliveryFees} /> */}
					{/* <PaymentInfo label="Tax(6%)" value={data.tax} /> */}
					<hr className="mb-3" />
					<PaymentInfo label="Total" value={data.total} isLast />
				</ul>
			</Card>
			{/* <Card className="mb-4"> */}
			<Elements stripe={stripePromise}>
				<StripeCheckoutForm product={product} />
			</Elements>
			{/* </Card> */}
		</div>
	)
}

export default PaymentSummary