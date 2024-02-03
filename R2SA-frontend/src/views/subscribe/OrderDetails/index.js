import React, { useState, useEffect } from 'react'
// import classNames from 'classnames'
// import { Tag } from 'components/ui'
import { Loading, Container, DoubleSidedImage } from 'components/shared'
import OrderProducts from './components/OrderProducts'
import PaymentSummary from './components/PaymentSummary'
// import ShippingInfo from './components/ShippingInfo'
// import Activity from './components/Activity'
// import CustomerInfo from './components/CustomerInfo'
// import { HiOutlineCalendar } from 'react-icons/hi'
import { apiGetCheckoutBasket } from 'services/SubscribeService'
import { useLocation, useNavigate } from 'react-router-dom'
import isEmpty from 'lodash/isEmpty'
// import dayjs from 'dayjs'

// const paymentStatus = {
// 	0: { label: 'Paid', class: 'bg-emerald-100 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-100'},
// 	1: { label: 'Unpaid', class: 'text-red-500 bg-red-100 dark:text-red-100 dark:bg-red-500/20'},
// }

// const progressStatus = {
// 	0: { label: 'Fulfilled', class: 'bg-cyan-100 text-cyan-600 dark:bg-cyan-500/20 dark:text-cyan-100'},
// 	1: { label: 'Unfulfilled', class: 'text-amber-600 bg-amber-100 dark:text-amber-100 dark:bg-amber-500/20'},
// }

const OrderDetails = () => {

	const navigate = useNavigate()
    const TermsClick = () => {
        navigate(`/app/legals/terms-and-conditions`)
    }

	const location = useLocation()

	const [loading, setLoading] = useState(false)
	const [data, setData] = useState({})

	useEffect(() => {
		fetchData()
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [])

	const fetchData = async () => {
		const id = location.pathname.substring(location.pathname.lastIndexOf('/') + 1)
		if (id) {
			setLoading(true)
			const response = await apiGetCheckoutBasket({id})
			if (response) {
				setLoading(false)
				setData(response.data)
			}
		}
	}

	return (
		<Container className="h-full">
			<Loading loading={loading}>
				{!isEmpty(data) && (
					<>
						<div className="mb-6">
							<div className="flex items-center ">
								<h3>
									<span className="mb-2">Review Order</span>
									<span >
									<p style={{ fontSize: '12px', fontWeight: 'normal'}}>
										Upon payment, the subscription for the given cities will activate and payment will be taken.
										The subscription will be renewed automatically every calender month. 
										To cancel an active subscription, cancel it via the &nbsp;
										<button style={{ fontWeight: 'bold'}} onClick={TermsClick}> Manage Lead Subscriptions </button>
										&nbsp;page. 
										<br />
										Upon cancellation, the user will have access to the leads from the city in question until the next scheduled subscription date, 
										when the subscription will deactivate and the user will lose access to those leads. 
										For example, if a user subscribed on the 2nd of January, and cancelled on the 7th of February, 
										they would have had access to the leads from that city from the 2nd of January until the 2nd of March,
										and would have paid the susbcription fee from the 2nd of January until the 2nd of March.

									</p>
									</span>
									{/* <span className="ltr:ml-2 rtl:mr-2">#{data.name}</span> */}
								</h3>
								{/* <Tag 
									className={
										classNames(
											'border-0 rounded-md ltr:ml-2 rtl:mr-2', 
											paymentStatus[data.payementStatus].class
										)
									}
								>
									{paymentStatus[data.payementStatus].label}
								</Tag> */}
								{/* <Tag 
									className={
										classNames(
											'border-0 rounded-md ltr:ml-2 rtl:mr-2', 
											progressStatus[data.progressStatus].class
										)
									}
								>
									{progressStatus[data.progressStatus].label}
								</Tag> */}
							</div>
							<span className="flex items-center">
								{/* <HiOutlineCalendar className="text-lg" />
								<span className="ltr:ml-1 rtl:mr-1">
									{dayjs.unix(data.dateTime).format('ddd DD-MMM-YYYY, hh:mm A')}
								</span> */}
							</span>
						</div>
						<div className="xl:flex gap-4">
							<div className="w-full">
								<OrderProducts data={data.product} fetchData={fetchData} />
								
								<div className="xl:grid grid-cols-2 gap-4">
									{/* <ShippingInfo data={data.shipping}/> */}
									<PaymentSummary data={data.paymentSummary} product={data.product}/>
								</div>
								{/* <Activity data={data.activity} /> */}
							</div>
							{/* <div className="xl:max-w-[360px] w-full">
								<CustomerInfo data={data.customer} />
							</div> */}
						</div>
					</>
				)}
			</Loading>
			{(!loading && isEmpty(data)) && (
				<div className="h-full flex flex-col items-center justify-center">
					<DoubleSidedImage 
						src="/img/others/img-2.png"
						darkModeSrc="/img/others/img-2-dark.png"
						alt="No order found!"
					/>
					<h3 className="mt-8">No order found!</h3>
				</div>
			)}
		</Container>
	)
}

export default OrderDetails