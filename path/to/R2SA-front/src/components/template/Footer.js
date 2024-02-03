import React from 'react'
// import  { Navigate } from 'react-router-dom'
import classNames from 'classnames'
import { Container } from 'components/shared'
import { APP_NAME } from 'constants/app.constant'
import { PAGE_CONTAINER_GUTTER_X } from 'constants/theme.constant' 
import { useNavigate } from 'react-router-dom'

const FooterContent = () => {
	const navigate = useNavigate()

	const onTermsClick = () => {
		navigate(`/app/legals/terms-and-conditions`)
	}

	const onPrivacyClick = () => {
		navigate(`/app/legals/privacy-policy`)
	}

	return (
		<div className="flex items-center justify-between flex-auto w-full">
			<span>Copyright  &copy;  {`${new Date().getFullYear()}`} <span className="font-semibold">{`${APP_NAME}`}</span> All rights reserved.</span>
			<div className="">
				<a className="text-gray cursor-pointer" onClick={onTermsClick}>Term & Conditions</a>
				<span className="mx-2 text-muted"> | </span>
				<a className="text-gray cursor-pointer" onClick={onPrivacyClick}>Privacy & Policy</a>
			</div>
		</div>
	)
}

export default function Footer ({ pageContainerType }) {
	
	return (
		<footer 
			className={
				classNames(
					`footer flex flex-auto items-center h-16 ${PAGE_CONTAINER_GUTTER_X}`,
				)
			}
		>
			{
				pageContainerType === 'contained' 
				? 
				<Container>
					<FooterContent />
				</Container>
				:
				<FooterContent />
			}
		</footer>
	)
}

