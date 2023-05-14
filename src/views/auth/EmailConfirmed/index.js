import React, { useEffect, useState } from 'react'
import { apiConfirmEmail } from 'services/AuthService'
import { useParams } from 'react-router-dom'


const EmailConfirmed = () => {
	
	const [confirmed, setConfirmed] = useState(true);
    const { uid, token } = useParams()
    
	useEffect(() => {

		const fetchData = async () =>
		{
            const email_confirmed = await apiConfirmEmail({'uid': uid, 'token': token})
			setConfirmed(email_confirmed)
		}
		fetchData();
	  });

    // Make API call, check email confirmation status

	if (confirmed)
	{		
		return (
			<div className="mb-8">
				<h3 className="mb-1">Your email has been confirmed!</h3>
				<p>This window can now be closed.</p>
			</div>
		)
	} else {
		return (
			<div className="mb-8">
				<h3 className="mb-1">Please wait a moment.</h3>
			</div>
		)
	}

}

export default EmailConfirmed