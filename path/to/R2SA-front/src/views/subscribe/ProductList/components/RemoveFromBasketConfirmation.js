import React, { useState } from 'react'
import { toast, Notification } from 'components/ui'
import { ConfirmDialog } from 'components/shared'
import { useSelector, useDispatch } from 'react-redux'
import { toggleRemoveConfirmation } from '../store/stateSlice'
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

const RemoveFromBasketConfirmation = () => {

	const dispatch = useDispatch()
	const dialogOpen = useSelector((state) => state.salesProductList.state.removeConfirmation)
	const selectedProduct = useSelector((state) => state.salesProductList.state.selectedProduct)
	const tableData = useSelector((state) => state.salesProductList.data.tableData)
	const data = useSelector((state) => state.salesProductList.data.productList)
	const [basket, setBasket] = useState([]);


	const onDialogClose = () => {
		dispatch(toggleRemoveConfirmation(false))
	}

	const onRemove = async () => {
		dispatch(toggleRemoveConfirmation(false))
		const city_ids = data.map(({ id }) => id); // NOTE: is this mapping incorrect?
		const city_id = city_ids.indexOf(selectedProduct)
		const city_dict = data[city_id]
		const city_name = city_dict['name']

		const success = await unsubscribeCity({id: city_id, name: city_name})
 
		if (success) {
			dispatch(getProducts(tableData))
			setBasket([...basket, makeid(8)]);
			toast.push(
				<Notification title={"Removed from basket"} type="success" duration={2500}>
					Succesfully removed {city_name} from basket.
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
			title="Remove"
			onCancel={onDialogClose}
			onConfirm={onRemove}
			confirmButtonColor="red-600"
		>
			<p>
				Remove from basket?
			</p>
		</ConfirmDialog>
	)

}

export default RemoveFromBasketConfirmation