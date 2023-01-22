import React, { useState, useEffect, useMemo } from 'react'
import { Avatar, Badge, toast, Notification } from 'components/ui'
import { DataTable } from 'components/shared'
import { HiX, HiShoppingCart } from 'react-icons/hi'
import { FiPackage } from 'react-icons/fi'
import { useDispatch, useSelector } from 'react-redux'
import { getProducts, setTableData, addCityToBasket } from '../store/dataSlice'
import { setSortedColumn, setSelectedProduct } from '../store/stateSlice'
import { toggleDeleteConfirmation, toggleRemoveConfirmation } from '../store/stateSlice'
import useThemeClass from 'utils/hooks/useThemeClass'
import ProductDeleteConfirmation from './ProductDeleteConfirmation'
import RemoveFromBasketConfirmation from './RemoveFromBasketConfirmation'
// import { useNavigate } from 'react-router-dom'
import cloneDeep from 'lodash/cloneDeep'

const inventoryStatusColor = {
	0: { label: 'Subscribed', dotClass: 'bg-emerald-500', textClass: 'text-emerald-500'},
	1: { label: 'In Basket', dotClass: 'bg-amber-500', textClass: 'text-amber-500' },
	// 2: { label: 'Not Subscribed', dotClass: 'bg-red-500', textClass: 'text-red-500' },
	2: { label: 'Not Subscribed',  textClass: 'text-grey-500' }, //dotClass: 'bg-grey-500',
}

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

const ActionColumn = ({status, row}) => {
	
	const dispatch = useDispatch()
	const { textTheme } = useThemeClass()
	// const navigate = useNavigate()
	const [basket, setBasket] = useState([]);
	// const basket = useSelector((state) => state.salesProductList.data.checkoutBasket)
	const data = useSelector((state) => state.salesProductList.data.productList)
	const tableData = useSelector((state) => state.salesProductList.data.tableData)
	// const selectedProduct = useSelector((state) => state.salesProductList.state.selectedProduct)
	// const { status } = props.row.original


	const onAddToBasket = async () => {
		// not sure this works
		dispatch(setSelectedProduct(row.id))

		const city_ids = data.map(({ id }) => id); // NOTE: is this mapping incorrect?
		const city_id = city_ids.indexOf(row.id)
		// console.log('selected product', row.id)
		// console.log('City_id', city_id)
		// console.log('id', id)
		const city_dict = data[city_id]
		const city_name = city_dict['name']
		const success = await addCityToBasket({id: city_id, name: city_name})

		// Add alert notification
		if (success){
			dispatch(getProducts(tableData))
			toast.push(
				<Notification title={"Added to Basket"} type="success" duration={1500}>
					Added {city_name} to basket.
				</Notification>
				,{
					placement: 'bottom-end'
				}
			)
			// // Update subscription state to show "In Basket"
			setBasket([...basket, makeid(8)]);
			// Not used anywhere, may cause a memory leak.
		} else {
			dispatch(getProducts(tableData))
			toast.push(
				<Notification title={"NOT added to Basket"} type="success" duration={2500}>
					Adding {city_name} to basket failed.
				</Notification>
				,{
					placement: 'bottom-end'
				}
			)
		}
		// navigate(`/app/subscribe/buying-panel/${row.id}`)
	}

	const onDelete = () => {
		dispatch(toggleDeleteConfirmation(true))
		dispatch(setSelectedProduct(row.id))  // not sure this works
	}

	const onRemove = () => {
		dispatch(toggleRemoveConfirmation(true))
		dispatch(setSelectedProduct(row.id))  // not sure this works
	}
	
	{/* If unsubscribed */}
	if (row.status == 2) {
		return (
			<div className="flex justify-end text-lg">
				<span className={`cursor-pointer p-2 hover:${textTheme}`} onClick={onAddToBasket}>
					<HiShoppingCart />
				</span>
			</div>
		)
	} else if (row.status == 0) {
		// If subscribed
		return (
			<div className="flex justify-end text-lg">
				<span className="cursor-pointer p-2 hover:text-red-500" onClick={onDelete}>
					<HiX />
				</span>
			</div>
		)
	} else if (row.status == 1) {
		// If in basket
		return (
			<div className="flex justify-end text-lg">
				<span className="cursor-pointer p-2 hover:text-red-500" onClick={onRemove}>
					<HiX />
				</span>
			</div>
		)
	}
}

const ProductColumn = ({row}) => {
	
	const avatar = row.img ? <Avatar src={row.img} /> : <Avatar icon={<FiPackage />} />

	return (
		<div className="flex items-center">
			{avatar}
			<span className={`ml-2 rtl:mr-2 font-semibold`}>
				{row.name}
			</span>
		</div>
	)
}

const ProductTable = () => {

	const dispatch = useDispatch()
	const { pageIndex, pageSize, sort, query, total } = useSelector((state) => state.salesProductList.data.tableData)
	const filterData = useSelector((state) => state.salesProductList.data.filterData)
	const loading = useSelector((state) => state.salesProductList.data.loading)
	const data = useSelector((state) => state.salesProductList.data.productList)

	useEffect(() => {
		fetchData()
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [pageIndex, pageSize, sort])

	const tableData = useMemo(() => 
		({pageIndex, pageSize, sort, query, total}), 
	[pageIndex, pageSize, sort, query, total])

	const fetchData = () => {
		dispatch(getProducts({pageIndex, pageSize, sort, query, filterData}))
	}

	const columns = useMemo(() => [
		{
			Header: 'Name',
			accessor: 'name',
			sortable: true,
			Cell: props => {
				const row = props.row.original
				return <ProductColumn row={row} />
			},
		},
		{
			Header: 'Country',
			accessor: 'country',
			sortable: true,
			Cell: props => {
				const row = props.row.original
				return (
					<span className="capitalize">{row.country}</span>
				)
			},
		},
		// {
		// 	Header: 'Quantity',
		// 	accessor: 'stock',
		// 	sortable: true,
		// },
		{
			Header: 'Status',
			accessor: 'status',
			sortable: true,
			Cell: props => {
				const { status } = props.row.original
				return (
					<div className="flex items-center gap-2">
						<Badge className={inventoryStatusColor[status].dotClass} />
						<span className={`capitalize font-semibold ${inventoryStatusColor[status].textClass}`}>
							{inventoryStatusColor[status].label}
						</span>
					</div>
				)
			},
		},
		{
			Header: 'Price',
			accessor: 'price',
			sortable: true,
			Cell: props => {
				const { price } = props.row.original
				return (
					<span>£{price}</span>
				)
			},
		},
		{
			Header: '',
			id: 'action',
			accessor: (row) => row,
			Cell: props => <ActionColumn status={props.row.original} row={props.row.original} />
		},
	], [])

	const onPaginationChange = page => {
		const newTableData = cloneDeep(tableData)
		newTableData.pageIndex =  page
		dispatch(setTableData(newTableData))
	}

	const onSelectChange = value => {
		const newTableData = cloneDeep(tableData)
		newTableData.pageSize =  Number(value)
		newTableData.pageIndex = 1
		dispatch(setTableData(newTableData))
	}

	const onSort = (sort, sortingColumn) => {
		const newTableData = cloneDeep(tableData)
		newTableData.sort = sort
		dispatch(setTableData(newTableData))
		dispatch(setSortedColumn(sortingColumn))
	}

	return (
		<>
			<DataTable 
				columns={columns} 
				data={data}
				skeletonAvatarColumns={[0]}
				skeletonAvatarProps={{className: 'rounded-md'}}
				loading={loading}
				pagingData={tableData}
				onPaginationChange={onPaginationChange}
				onSelectChange={onSelectChange}
				onSort={onSort}
			/>
			<ProductDeleteConfirmation />
			<RemoveFromBasketConfirmation />
		</>
	)
}

export default ProductTable