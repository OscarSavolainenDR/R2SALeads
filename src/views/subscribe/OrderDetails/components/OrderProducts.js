import React, { useState, useMemo, Fragment } from 'react'
import { AdaptableCard } from 'components/shared'
import { Table } from 'components/ui' // , Avatar 
import { useTable } from 'react-table'
import NumberFormat from 'react-number-format'
import isLastChild from 'utils/isLastChild'

import { HiX } from 'react-icons/hi'
import { toast, Notification } from 'components/ui'
import { useDispatch, useSelector } from 'react-redux'
import { getProducts, unsubscribeCity } from '../store/dataSlice'
import useThemeClass from 'utils/hooks/useThemeClass'

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

const { Tr, Th, Td, THead, TBody } = Table

const ActionColumn = ({data, row, fetchData }) => {
	const dispatch = useDispatch()

	const onRemove = async () => {
		const city_ids = data.map(({ id }) => id); // NOTE: is this mapping incorrect?
		const city_id = city_ids.indexOf(row.id)
		const city_dict = data[city_id]
		const city_name = city_dict['name']
		
		const success = await unsubscribeCity({id: city_id, name: city_name})
 
		if (success) {
			dispatch(fetchData)
			toast.push(
				<Notification title={"Removed from basket"} type="success" duration={1500}>
					Succesfully removed {city_name} from basket.
				</Notification>
				,{
					placement: 'bottom-end'
				}
			)
		}
	}

	// If in basket
	return (
		<div className="flex justify-end text-lg">
			<span className="cursor-pointer p-2 hover:text-grey-500" onClick={onRemove}>
				<HiX />
			</span>
		</div>
	)
}

const ProductColumn = ({row}) => {
	return (
		<div className="flex">
			{/* <Avatar size={90} src={row.img} /> */}
			<div className="ltr:ml-2 rtl:mr-2">
				<h6 className="mb-2">{row.name} - {row.country}</h6>
				{
					
					// Object.keys(row.details).map((key, i) => (
					// 	<div className="mb-1" key={key + i} value={key}>
					// 		<span className="capitalize">{key}: </span>
					// 		{row.details[key].map((item, j) => (
					// 			<Fragment key={item + j}>
					// 				<span className="font-semibold">
					// 					{item}
					// 				</span>
					// 				{!isLastChild(row.details[key], j) && <span>, </span>}
					// 			</Fragment>
					// 		))}
					// 	</div>
					// ))
				}
			</div>
		</div>
	)
}

const PriceAmount = ({amount}) => {
	return (
		<div>
			<NumberFormat
				displayType="text"
				value={(Math.round(amount * 100) / 100).toFixed(2)} 
				prefix={'£ '} 
				suffix={' / month'}
				thousandSeparator={true} 
			/>
		</div>
	)
}

const OrderProducts = ({data, fetchData}) => {

	const columns = useMemo(() => [
		{
			Header: 'Subscriptions',
			accessor: 'name',
			Cell: props => {
				const row = props.row.original
				return <ProductColumn row={row} />
			},
		},
		{
			Header: 'Price',
			accessor: 'price',
			Cell: props => {
				const row = props.row.original
				return <PriceAmount amount={row.price} />
			},
		},
		{
			Header: '',
			id: 'action',
			accessor: (row) => row,
			Cell: props => <ActionColumn data={data} row={props.row.original} fetchData={fetchData} />
		},
		// {
		// 	Header: 'Quantity',
		// 	accessor: 'quantity',
		// },
		// {
		// 	Header: 'Total',
		// 	accessor: 'total',
		// 	Cell: props => {
		// 		const row = props.row.original
		// 		return <PriceAmount amount={row.price} />
		// 	},
		// },
	], [])

	const {
		getTableProps,
		getTableBodyProps,
		headerGroups,
		rows,
		prepareRow,
	} = useTable({ columns, data })

	return (
		<AdaptableCard className="mb-4">
			<h5 className="mb-4">Basket</h5>
			<Table {...getTableProps()}>
				<THead className="!bg-transparent">
					{headerGroups.map(headerGroup => (
						<Tr {...headerGroup.getHeaderGroupProps()}>
							{headerGroup.headers.map(column => (
								<Th {...column.getHeaderProps()}>
									{column.render('Header')}
								</Th>
							))}
						</Tr>
					))}
				</THead>
				<TBody {...getTableBodyProps()}>
					{rows.map(
						(row, i) => {
						prepareRow(row)
						return (
							<Tr {...row.getRowProps()}>
								{row.cells.map(cell => {
									return (
									<Td {...cell.getCellProps()}>{cell.render('Cell')}</Td>
									)
								})}
							</Tr>
						)}
					)}
				</TBody>
			</Table>
		</AdaptableCard>
	)
}

export default OrderProducts