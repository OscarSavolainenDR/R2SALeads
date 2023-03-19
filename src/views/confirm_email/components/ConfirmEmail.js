import React, { useEffect, useState } from 'react'
import { Alert } from 'components/ui'
import { apiGetEmailStatus, apiResendConfirmEmail } from 'services/AuthService'
import useThemeClass from 'utils/hooks/useThemeClass'
import { Link } from "react-router-dom";

const ConfirmEmail = () => {
	

	// Styling
	const { textTheme } = useThemeClass()
    const boldText = {
        fontWeight: 'bold',
        marginLeft: '5px'
    }
	const divStyle = {
        display: 'flex',
    }

	const [confirmed, setConfirmed] = useState(true);

	const ResendEmail = async () => {
        const response = await apiResendConfirmEmail()
		setConfirmed(false)
    }

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
	To confirm your email, please go to your signup email's inbox (check spam folder). Please sign out before you confirm your email."
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
				{message && <Alert className="mb-4" type="info" showIcon>
					{message}
					<p> Click
						<Link onClick={ResendEmail} style={boldText} className={`cursor-pointer hover:${textTheme}`}>
						    here
						</Link>
						&nbsp;to resend a confirmation email.
					</p>
					{/* <div style={divStyle}>
						<p>Click </p><button  style={boldText} className={`cursor-pointer hover:${textTheme}`} onClick={ResendEmail}>here </button> 
						<p>&nbsp;to resend a confirmation email.</p>
					</div> */}
				</Alert>}
				
			</div>
		)
	}

}

export default ConfirmEmail