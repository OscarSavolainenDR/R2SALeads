import React, { useEffect, useState } from 'react'
import { Alert } from 'components/ui'
import { apiGetEmailStatus } from 'services/AuthService'


const ConfirmEmail = () => {

	const [confirmed, setConfirmed] = useState(true);

	useEffect(() => {
		
		const fetchData = async () =>
		{
			const response = await apiGetEmailStatus()
			// console.log('Email confirmed', response.data.email_status)
			setConfirmed(response.data.email_status)
		}
		fetchData();
	  });

	const message = "To subscribe to a city and checkout to receive leads, you must confirm your email. \
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