import React, { useState }  from 'react'
import { toast, Notification } from 'components/ui'
import { ConfirmDialog } from 'components/shared'
import { useSelector, useDispatch } from 'react-redux'
import { toggleDeleteConfirmation } from '../store/stateSlice'
import { unsubscribeCity, getProducts } from '../store/dataSlice'

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

const ProductDeleteConfirmation = () => {

	const dispatch = useDispatch()
	const dialogOpen = useSelector((state) => state.salesProductList.state.deleteConfirmation)
	const selectedProduct = useSelector((state) => state.salesProductList.state.selectedProduct)
	const tableData = useSelector((state) => state.salesProductList.data.tableData)
	const data = useSelector((state) => state.salesProductList.data.productList)
	const [basket, setBasket] = useState([]);

	const onDialogClose = () => {
		dispatch(toggleDeleteConfirmation(false))
	}

	const onDelete = async () => {
		dispatch(toggleDeleteConfirmation(false))
		const city_ids = data.map(({ id }) => id); // NOTE: is this mapping incorrect?
		const city_id = city_ids.indexOf(selectedProduct)
		const city_dict = data[city_id]
		const city_status = city_dict['status']
		const city_name = city_dict['name']
	

		const success = await unsubscribeCity({id: city_id, name: city_name})
 
		if (success) {
			setBasket([...basket, makeid(8)]);
			dispatch(getProducts(tableData))
			toast.push(
				<Notification title={"Successfuly Unsubscribed"} type="success" duration={2500}>
					Succesfully unsubscribed from {city_name}.
				</Notification>
				,{
					placement: 'bottom-end'
				}
			)
		}
	}

	return (
		<ConfirmDialog
			isOpen={dialogOpen}
			onClose={onDialogClose}
			onRequestClose={onDialogClose}
			type="danger"
			title="Unsubscribe"
			onCancel={onDialogClose}
			onConfirm={onDelete}
			confirmButtonColor="red-600"
		>
			<p>
				Are you sure you want to unsubscribe from this city? 
				You will lose all access to current and future listings.
				All record related to this product will be deleted as well. 
				This action cannot be undone without re-subscribing.
			</p>
		</ConfirmDialog>
	)

}

export default ProductDeleteConfirmation