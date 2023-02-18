import React, { useState, useEffect, useMemo } from 'react'
import { Avatar, Badge, toast, Notification, Button } from 'components/ui'
import { DataTable } from 'components/shared'
import { HiOutlineDownload } from 'react-icons/hi'
import { FiPackage } from 'react-icons/fi'
import { useDispatch, useSelector } from 'react-redux'
import { getLeads, setTableData, updateProductList, updateLeadsListBackend, downloadExcelBackend } from '../store/dataSlice'
import { setSortedColumn, setSelectedProduct, setAPICounter } from '../store/stateSlice'
import { addToggledStatusChanges} from '../store/stateSlice'
import useThemeClass from 'utils/hooks/useThemeClass'
// import LeadsProductDeleteConfirmation from './ProductDeleteConfirmation'
// import LeadsRemoveFromBasketConfirmation from './RemoveFromBasketConfirmation'
// import { useNavigate } from 'react-router-dom'
import cloneDeep from 'lodash/cloneDeep'
import exportFromJSON from 'export-from-json'


const inventoryStatusColor = {
	0: { label: 'Lead', textClass: 'text-grey-500'},
	1: { label: 'Contacted', textClass: 'text-amber-500' },
	// 2: { label: 'Not Subscribed', dotClass: 'bg-red-500', textClass: 'text-red-500' },
	2: { label: 'Viewing Booked',  textClass: 'text-emerald-500' }, //dotClass: 'bg-grey-500',
	3: { label: 'Ignore',  textClass: 'text-red-500' }, //dotClass: 'bg-grey-500',
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

const ActionColumn = ({row}) => {

	
	const dispatch = useDispatch()
	const { textTheme } = useThemeClass()
	// const navigate = useNavigate()
	const [basket, setBasket] = useState([]);
	// const basket = useSelector((state) => state.salesProductList.data.checkoutBasket)
	const data = useSelector((state) => state.projectTableView.data.productList)
	const tableData = useSelector((state) => state.projectTableView.data.tableData)
	const filterData = useSelector((state) => state.projectTableView.data.filterData)
	const toggledStatusChanges = useSelector((state) => state.projectTableView.state.toggledStatusChanges)
	// const [updateAPI, setUpdateAPI] = useState(0);
	// const [update, setUpdate] = useState([]);
	const updateAPI = useSelector((state) => state.projectTableView.state.APICounter)

	
	// const selectedProduct = useSelector((state) => state.salesProductList.state.selectedProduct)
	// const { status } = props.row.original


	const onToggleStatus = async () => {
		// not sure this works
		dispatch(setSelectedProduct(row.id))

		const listing_ids = data.map(({ id }) => id); // NOTE: is this mapping incorrect?
		const listing_id = listing_ids.indexOf(row.id)
		// console.log('selected product', row.id)
		// console.log('Listing_id', listing_id)
		// console.log('id', id)
		const listing_dict = data[listing_id]
		// console.log('listing dict', listing_dict)
		const status = listing_dict['status']

		// Update state here, not backend.
		// We are storing the status and row.id herem, so we can send them batched to the backend.
		// Also have to update the table.
		dispatch(addToggledStatusChanges([...toggledStatusChanges, {status: status, listing_id: row.id}]))
		const newData = cloneDeep(data)
		newData[listing_id].status = (newData[listing_id].status + 1) % 4
		// console.log('New status', newData[listing_id].status)
		dispatch(updateProductList(newData))
		// row.status = row.status + 1
		// setBasket([...basket, makeid(8)]);
		// console.log(toggledStatusChanges)
		dispatch(setAPICounter(updateAPI+1))

		console.log('UpdateAPi value:', updateAPI)

		// const updating = async () => {
		if (updateAPI > 10) {
			const success = await updateLeadsListBackend(toggledStatusChanges)
	
			console.log('Success')
			if (success){
				dispatch(setAPICounter(0))
				dispatch(addToggledStatusChanges([]))

				dispatch(getLeads({filterData: filterData, tableData: tableData}))
				setBasket([...basket, makeid(8)]);
				// console.log('Success')
			} else {
				// dispatch(getLeads({filterData: filterData, tableData: tableData}))
				// console.log('Failed')
			}
			
		}
		// }

		// const success = await updateLeadsListBackend({'status': status, 'id': row.id})

		// if (success){
		// 	dispatch(getLeads({filterData: filterData, tableData: tableData}))
		// 	setBasket([...basket, makeid(8)]);
		// 	// console.log('Success')
		// } else {
		// 	dispatch(getLeads({filterData: filterData, tableData: tableData}))
		// 	// console.log('Failed')
		// }
	}

	// console.log('used status', row.status)
	return (
		<div className="flex items-center gap-2">
		{/* <div className="flex justify-end text-lg"> */}
			<span onClick={onToggleStatus} className={`cursor-pointer capitalize hover:${textTheme} font-semibold ${inventoryStatusColor[row.status].textClass}`}>
				{inventoryStatusColor[row.status].label}				
			</span>
		{/* </div> */}
		</div>
	)
	
}

// const ProductColumn = ({row}) => {
	
// 	const avatar = row.img ? <Avatar src={row.img} /> : <Avatar icon={<FiPackage />} />

// 	return (
// 		<div className="flex items-center">
// 			{avatar}
// 			<span className={`ml-2 rtl:mr-2 font-semibold`}>
// 				{row.name}
// 			</span>
// 		</div>
// 	)
// }

const LeadsProductTable = () => {

	const dispatch = useDispatch()
	const { pageIndex, pageSize, sort, query, total } = useSelector((state) => state.projectTableView.data.tableData)
	const filterData = useSelector((state) => state.projectTableView.data.filterData)
	const loading = useSelector((state) => state.projectTableView.data.loading)
	const data = useSelector((state) => state.projectTableView.data.productList)
	// const { textTheme } = useThemeClass()

	// const newTableData = useSelector((state) => state.projectTableView.data.tableData)
	// const sortingColumn = useSelector((state) => state.projectTableView.state.sortedColumn)

	useEffect(() => {
		fetchData()
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [pageIndex, pageSize, sort])

	const tableData = useMemo(() => 
		({pageIndex, pageSize, sort, query, total}), 
	[pageIndex, pageSize, sort, query, total])

	const fetchData = () => {
		dispatch(getLeads({filterData: filterData, tableData: tableData}))
	}

	
	const downloadExcel = async (file_id, url) => {

		// console.log(file_id)

		const excel = await downloadExcelBackend({file_id: file_id})

		// console.log(excel)

		// dispatch(downloadExcelBackend(file_id))
		// dispatch(updateExcel(excel))
		
		const excel_array = JSON.parse(excel.data)

		// console.log(excel_array)

		const exportType =  exportFromJSON.types.csv
		const outputFilename = `${url}_due_diligence.csv`;
		if (excel != {}) {
			exportFromJSON({ data: excel_array, fileName: outputFilename, exportType: exportType }) 
		}
		
	}
	

	const columns = useMemo(() => [
		// {
		// 	Header: 'Name',
		// 	accessor: 'name',
		// 	sortable: true,
		// 	Cell: props => {
		// 		const row = props.row.original
		// 		return <ProductColumn row={row} />
		// 	},
		// },
		{
			Header: 'City',
			accessor: 'city',
			sortable: true,
			Cell: props => {
				const row = props.row.original
				return (
					<span className="capitalize">{row.city}</span>
				)
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
		// 	Header: 'Postcode',
		// 	accessor: 'postcode',
		// 	sortable: true,
		// 	Cell: props => {
		// 		const row = props.row.original
		// 		return (
		// 			<span className="capitalize">{row.postcode}</span>
		// 		)
		// 	},
		// },
		{
			Header: 'Bedrooms',
			accessor: 'bedrooms',
			sortable: true,
			Cell: props => {
				const { bedrooms } = props.row.original
				return (
					<span>{bedrooms}</span>
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
			id: 'status',
			sortable: true,
			accessor: (row) => row,
			Cell: props => <ActionColumn row={props.row.original} />
		},
		// {
		// 	Header: 'Status',
		// 	accessor: 'status',
		// 	sortable: true,
		// 	Cell: props => {
		// 		const { status, id } = props.row.original
		// 		const { textTheme } = useThemeClass()
		// 		return (
		// 			<div className="flex items-center gap-2">
		// 				{/* <Badge className={inventoryStatusColor[status].dotClass} /> */}
		// 				<span onClick={() => toggleLabel(status, id)} className={`cursor-pointer capitalize hover:${textTheme} font-semibold ${inventoryStatusColor[status].textClass}`}>
		// 					{inventoryStatusColor[status].label}
		// 				</span>
		// 			</div>
		// 		)
		// 	},
		// },
		{
			Header: 'Rent',
			accessor: 'rent',
			sortable: true,
			Cell: props => {
				const { rent } = props.row.original
				return (
					<span>£{rent}</span>
				)
			},
		},
		{
			Header: 'Breakeven Ocucpancy',
			accessor: 'breakeven_occupancy',
			sortable: true,
			Cell: props => {
				const { breakeven } = props.row.original
				return (
					<span>{breakeven}%</span>
				)
			},
		},
		{
			Header: 'Expected Turnover',
			accessor: 'expected_income',
			sortable: true,
			Cell: props => {
				const { expected_income } = props.row.original
				return (
					<span>£{expected_income}</span>
				)
			},
		},
		{
			Header: 'Profit',
			accessor: 'profit',
			sortable: true,
			Cell: props => {
				const { profit } = props.row.original
				return (
					<span>£{profit}</span>
				)
			},
		},
		{
			Header: 'Due Diligence Excel',
			accessor: 'excel',
			sortable: true,
			Cell: props => {
				// const { url } = props.row.original
				const { textTheme } = useThemeClass()
				return (
					<span className={`cursor-pointer p-2 hover:${textTheme}`} onClick={() => downloadExcel(props.row.original.id, props.row.original.url)}>
						<HiOutlineDownload/>
					</span>
				)
			},
		},
		{
			Header: 'URL',
			accessor: 'url',
			sortable: true,
			Cell: props => {
				const { url } = props.row.original
				const { textTheme } = useThemeClass()
				return (
					<span className={`cursor-pointer hover:${textTheme}`}>
						<a href={url} target="_blank">{url}</a>
					</span>
				)
			},
		},
		//  
														
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
		// console.log(newTableData.sort, sortingColumn)
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
			{/* <LeadsProductDeleteConfirmation />
			<LeadsRemoveFromBasketConfirmation /> */}
		</>
	)
}

export default LeadsProductTable