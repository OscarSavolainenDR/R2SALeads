import React, { useEffect, useState } from 'react'
import { Alert } from 'components/ui'
import useThemeClass from 'utils/hooks/useThemeClass'
import { Link } from "react-router-dom";
import useAuth from 'utils/hooks/useAuth'

const SampleLeadsBubble = () => {
	
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
					<p> This is a sample of 10 random R2SA leads, updated daily. 
                        <Link to={{pathname: `/sign-in`}} style={boldText} className={`cursor-pointer hover:${textTheme}`}>
						Sign in
						</Link>
						&nbsp;to your account to see the leads from the cities you have subscribed to, or to manage your subscriptions.
					</p>
				</Alert>}
			</div>
		)
	}

}

export default SampleLeadsBubble