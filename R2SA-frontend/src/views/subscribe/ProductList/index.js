import React from 'react'
import reducer from './store'
import { injectReducer } from 'store/index'
import { AdaptableCard } from 'components/shared'
import ProductTable from './components/ProductTable'
import ProductTableTools from './components/ProductTableTools'
import ConfirmEmail from 'views/confirm_email/components/ConfirmEmail'
import SignUpPrompt from 'views/sign_up_prompt/components/SignUpPrompt'

injectReducer('salesProductList', reducer)

const ProductList = () => {
	return (
		<div>
			<SignUpPrompt />
			<ConfirmEmail />
		
			<AdaptableCard className="h-full" bodyClass="h-full">
				<div className="lg:flex items-center justify-between mb-4">
					<h3 className="mb-4 lg:mb-0">Products</h3>
					<ProductTableTools />
				</div>
				<ProductTable />
			</AdaptableCard>
		</div>
	)
}

export default ProductList