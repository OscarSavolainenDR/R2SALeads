import React, { cloneElement } from 'react'
import Logo from 'components/template/Logo'
import { APP_NAME } from 'constants/app.constant'

const Cover = ({children, content, ...rest }) => {
	return (
		<div className="grid lg:grid-cols-3 h-full">
			<div 
				className="col-span-2 bg-no-repeat bg-cover py-6 px-16 flex-col justify-between bg-white dark:bg-gray-800 hidden lg:flex"
				style={{backgroundImage: `url('/img/others/auth-cover-bg.jpg')`}}
			>
				<Logo mode="dark" />
				<div>
					<h3 className="text-white mb-4">Find your next Rent to Serviced Accomodation property with R2SA Leads!</h3>
					<p className="text-lg text-white opacity-80 max-w-[700px]">R2SA Leads automatically scans all of the major rental listing websites and compares the listings to data from Airbnb. We provide lists of properties that are suitable for R2SA with all of the due diligence already done! Spend less time searching for properties, and more time growing your business!</p>
				</div>
				<span className="text-white">Copyright  &copy;  {`${new Date().getFullYear()}`} <span className="font-semibold">{`${APP_NAME}`}</span> </span>
			</div>
			<div className="flex flex-col justify-center items-center bg-white dark:bg-gray-800">
				<div className="xl:min-w-[450px] px-8">
					<div className="mb-8">
						{content}
					</div>
					{children ? cloneElement(children, { ...rest }) : null}
				</div>
			</div>
		</div>
	)
}

export default Cover