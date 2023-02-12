import React, { useEffect, useState } from 'react'
import { Alert } from 'components/ui'
// import { useDispatch, useSelector } from 'react-redux'
// import { getLeads } from '../store/dataSlice'
// import { useSelector, useDispatch } from 'react-redux'
// import { getEmailStatus } from '../store/dataSlice'
import { apiGetEmailStatus } from 'services/AuthService'


const ConfirmEmail = () => {

	const [confirmed, setConfirmed] = useState(true);

	// const dispatch = useDispatch()
	// dispatch(getLeads())
	// // const confirmed = useSelector((state) => state.confirmedEmail.data)
	// const confirmed = useSelector((state) => state.projectTableView2.data.productList)
	// // const confirmed = false
	// console.log('In element', confirmed)

	// useEffect( () => {
	// 	console.log('Called')
	// 	const status = await getEmailStatus()
	// 	console.log(status)
	// 	if (status) {
	// 		setConfirmed(true)
	// 	}
	// }, [])

	useEffect(() => {
		
		const fetchData = async () =>
		{
			const response = await apiGetEmailStatus()
			// console.log('Email confirmed', response.data.email_status)
			setConfirmed(response.data.email_status)
		}
		fetchData();
	  });

	const message = "To subscribe to a city to receive leads, you must confirm your email. \
	To confirm your email, please go to your signup email's inbox (check spam folder)."

	// const getStatus = async () => {

	// 	// Make API call, check email confirmation status
	// 	dispatch(getEmailStatus())
	// 	// const {status, data} = await getEmailStatus()
	// 	// console.log(status, data.email_message)
	// 	// const message = data.email_message
	// }

	if (confirmed)
	{		
		return (
			<div>
			</div>
		)
	} else {
		return (
			<div >
				{message && <Alert className="mb-4" type="info" showIcon>{message}</Alert>}
				
			</div>
		)
	}

}

export default ConfirmEmail