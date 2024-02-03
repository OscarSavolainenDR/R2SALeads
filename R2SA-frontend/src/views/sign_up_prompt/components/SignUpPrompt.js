import React, { useEffect, useState } from 'react'
import { Alert } from 'components/ui'
import useThemeClass from 'utils/hooks/useThemeClass'
import { Link } from "react-router-dom";
import useAuth from 'utils/hooks/useAuth'

const SignUpPrompt = () => {
	
	// Styling
	const { textTheme } = useThemeClass()
    const boldText = {
        fontWeight: 'bold',
        marginLeft: '5px'
    }
	const divStyle = {
        display: 'flex',
    }

	const { authenticated } = useAuth()

	if (authenticated)
	{		
		return (
			<div>
			</div>
		)
	} else {
		return (
			<div >
				{<Alert className="mb-4" type="info" showIcon>
					<p> To be able to subscribe to a city, please 
						<Link to={{pathname: `/sign-in`}} style={boldText} className={`cursor-pointer hover:${textTheme}`}>
						sign in.
						</Link>
						&nbsp;It is also recommended that you confirm your email before signing in again, as you will need to sign out to confirm your email.
					</p>
				</Alert>}
			</div>
		)
	}

}

export default SignUpPrompt