import React, { useEffect, useState, useRef } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { updateColumns, updateExcel } from './store/dataSlice'
import { Spinner, Avatar, Tooltip, Card, Button, Input, Dropdown, Tag, Badge } from 'components/ui'
import UsersAvatarGroup from 'components/shared/UsersAvatarGroup'
import dayjs from 'dayjs'
import cloneDeep from 'lodash/cloneDeep'
import { downloadExcelBackend } from './store/dataSlice'
import { 
	HiOutlinePlus, 
	HiOutlineCheckCircle, 
	HiOutlineClipboardList,
	HiOutlinePaperClip,
	HiOutlineDownload,
	HiOutlineTrash,
	HiOutlineChatAlt,
	HiExternalLink,
	HiX
} from 'react-icons/hi'
import isEmpty from 'lodash/isEmpty'
import { createUID, taskLabelColors, labelList } from './utils'

import axios, { AxiosRequestConfig } from 'axios';
import appConfig from 'configs/app.config'

import exportFromJSON from 'export-from-json'



// function download_excel (ex_fileName, ex_data, exportType) {
// 	const excel_fileName = ex_fileName.value
// 	const excel_data = JSON.parse(ex_data.innerText)
// 	// const fields = $useFields.checked ? ['Name', 'Author', 'Subject'] : []

// 	exportFromJSON({ excel_data, excel_fileName, exportType })
// }


// Need to rename as user details
export const createCommentObject = (message, user_name, avatar) => {
	
	return {
		id: createUID(10),
		name: {user_name},
		src: {avatar},
		message: message,
		date: new Date()
	}
}

const TicketSection = ({title, icon, children, titleSize: Title = 'h6', ticketClose}) => {

	return(
		<div className="flex mb-10">
			<div className="text-2xl">{icon}</div>
			<div className="ml-2 rtl:mr-2 w-full">
				<div className="flex justify-between">
					<Title>{title}</Title>
					{
						ticketClose && <Button 
							size="sm" 
							shape="circle"
							variant="plain"
							icon={<HiX className="text-lg" />}
							onClick={() => ticketClose()}
						/>
					}
				</div>
				{children}
			</div>
		</div>
	)
}

const AddMoreMember = () => {
	return (
		<Tooltip title="Add More">
			<Avatar 
				className="cursor-pointer"
				shape="circle"
				size={30}
			>
				<HiOutlinePlus />
			</Avatar>
		</Tooltip>
	)
}


const TicketContent = ({onTicketClose}) => {

	const ticketId = useSelector(state => state.scrumBoard.state.ticketId)
	const columns = useSelector(state => state.scrumBoard.data.columns)
	const boardMembers = useSelector(state => state.scrumBoard.data.boardMembers)

	const { avatar, user_name} = useSelector((state) => state.auth.user)

	const dispatch = useDispatch()

	const [ticketData, setTicketData] = useState({})
	const [loading, setLoading] = useState(false)

	const commentInput = useRef()

	const excel = useSelector(state => state.scrumBoard.data.excel_json_str)

	const downloadExcel = async (file_id) => {

		dispatch(downloadExcelBackend(file_id))
		dispatch(updateExcel(excel))
		
		const excel_array = JSON.parse(excel)

		const exportType =  exportFromJSON.types.csv
		const outputFilename = `${file_id}_due_diligence.csv`;
		if (excel != {}) {
			exportFromJSON({ data: excel_array, fileName: outputFilename, exportType: exportType }) 
		}
		
	}
	
	const getTicketDetail = async () => {
		setLoading(true)
		let ticketDetail = {}
		for (const key in columns) {
			if (Object.hasOwnProperty.call(columns, key)) {
				const board = columns[key]
				const result = board.find(ticket => ticket.id === ticketId)
				if (result) {
					ticketDetail = result
				}
			}
		}
		setTicketData(ticketDetail)
		setLoading(false)
	}

	useEffect(() => {
		if (isEmpty(ticketData)) {
			getTicketDetail()
		} else {
			onUpdateColumn()
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [ticketData, ticketData])

	const submitComment = () => {
		const message = commentInput.current.value
		const comment = createCommentObject(message, user_name, avatar)
		const comments = cloneDeep(ticketData.comments)
		comments.push(comment)
		setTicketData( prevState => ({...prevState, ...{comments: comments}}))
		commentInput.current.value = ''
	}

	const handleTicketClose = () => {
		onTicketClose?.()
	}

	const onUpdateColumn = () => {
		const data = cloneDeep(columns)
		for (const key in data) {
			if (Object.hasOwnProperty.call(data, key)) {
				const board = data[key]
				board.forEach((ticket, index) => {
					if(ticket.id === ticketId) {
						data[key][index] = ticketData
					}
				})
			}
		}
		dispatch(updateColumns(data))
	}
	
	const onAddMemberClick = (id) => {
		const newMember = boardMembers.find(member => member.id === id)
		const members = cloneDeep(ticketData.members)
		members.push(newMember)
		setTicketData( prevState => ({...prevState, ...{members: members}}))
	}

	const onAddLabelClick = (label) => {
		const labels = cloneDeep(ticketData.labels)
		labels.push(label)
		setTicketData( prevState => ({...prevState, ...{labels: labels}}))
	}

	return (
		<>
			{
				loading 
				? 
				<div className="flex justify-center items-center min-h-[300px]">
					<Spinner size={40} />
				</div>
				:
				<>
					<div className="max-h-[700px] overflow-y-auto">
						<TicketSection 
							title={ticketData.name} 
							// title={ticketData.id} 
							icon={<HiOutlineCheckCircle />} 
							titleSize="h5"
							ticketClose={handleTicketClose}
						>
							<div className="grid grid-cols-2 gap-4">
								{/* <div className="mt-4">
									<div className="font-semibold mb-3 text-gray-900 dark:text-gray-100">Assigned to:</div>
									<UsersAvatarGroup 
										avatarProps={{className: 'mr-1 rtl:ml-1 cursor-pointer'}} 
										avatarGroupProps={{maxCount: 4}}
										chained={false} 
										users={ticketData.members}
									/>
									{boardMembers.length !== ticketData.members?.length && (
										<Dropdown renderTitle={<AddMoreMember />} >
											{
												boardMembers.map(member => (
													!ticketData.members?.some(m => m.id === member.id) && (
														<Dropdown.Item 
															onSelect={onAddMemberClick}
															eventKey={member.id}
															key={member.name}
														>
															<div className="flex items-center justify-between">
																<div className="flex items-center">
																	<Avatar shape="circle" size={22} src={member.img} />
																	<span className="ml-2 rtl:mr-2">{member.name}</span>
																</div>
															</div>
														</Dropdown.Item>
													)
												))
											}
										</Dropdown>
									)}
								</div> */}
								<div className="mt-4">
									<div className="font-semibold mb-3 text-gray-900 dark:text-gray-100">
										Label:
									</div>
									<div>
										{ticketData.labels?.map(label => (
											<Tag
												key={label}
												className="mr-2 rtl:ml-2 mb-2"
												prefix 
												prefixClass={`${taskLabelColors[label]}`}
											>
												{label}
											</Tag>
										))}
										<Dropdown 
											renderTitle={
												<Tag className="border-dashed cursor-pointer mr-2 rtl:ml-2">
													Add Label
												</Tag>
											}
											placement="bottom-end"
										>
											{
												labelList.map((label) => (
													!ticketData.labels?.includes(label) && (
														<Dropdown.Item 
															onSelect={onAddLabelClick}
															eventKey={label}
															key={label}
														>
															<div className="flex items-center">
																<Badge innerClass={`${taskLabelColors[label]}`} />
																<span className="ml-2 rtl:mr-2">{label}</span>
															</div>
														</Dropdown.Item>
													)
												))
											}
										</Dropdown>
										
									</div>
								</div>
							</div>
						</TicketSection>
						{ticketData.description && (
							<TicketSection title="Description" icon={<HiOutlineClipboardList />}>
								<div className="mt-2">
									<p className="mt-2">{ticketData.description}</p>
									<p className="mt-2">{ticketData.rent}</p>
									<p className="mt-2">{ticketData.breakeven_occupancy}</p>
								</div>
							</TicketSection>
						)}
						{ticketData.url && (
							<TicketSection title="Listing URL" icon={<HiExternalLink />}>
								<div className="mt-2">
									<p className="mt-2">{ticketData.url}</p>
								</div>
							</TicketSection>
						)}
						
						{
							ticketData?.attachments?.length > 0 
							&& 
							<TicketSection title="Attachments" icon={<HiOutlinePaperClip />}>
								<div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
									{
										ticketData.attachments.map(file => (
											<Card bodyClass="px-2 pt-2 pb-1" key={file.id}>
												<img className="max-w-full rounded" alt={file.name} src={file.src} />
												<div className="mt-1 flex justify-between items-center">
													<div>
														<div className="font-semibold text-gray-900 dark:text-gray-100">
															{file.name}
														</div>
														<span className="text-xs">{file.size}</span>
													</div>
													<div className="flex items-center">
														<Tooltip title="Download">
															<Button className="mr-1 rtl:ml-1" variant="plain" size="xs" icon={<HiOutlineDownload/>}  onClick={() => downloadExcel(ticketData.id)}/> 
														</Tooltip>
														{/* <Tooltip title="Delete">
															<Button variant="plain" size="xs" icon={<HiOutlineTrash />} />
														</Tooltip> */}
													</div>
												</div>
											</Card>
										))
									}
								</div>
							</TicketSection>
						}
						{/* Comment section */}
						{/* <TicketSection title="Comments" icon={<HiOutlineChatAlt />}>
							<div className="mt-2 w-full">
								{ ticketData?.comments?.length > 0 && 
									<>
										{ticketData.comments.map(comment => (
											<div className="mb-3 flex" key={comment.id}>
												<div className="mt-2">
													<Avatar shape="circle" src={comment.src} />
												</div>
												<div className="ml-2 rtl:mr-2 p-3 rounded w-100">
													<div className="flex items-center mb-2">
														<span className="font-semibold text-gray-900 dark:text-gray-100">{comment.name}</span>
														<span className="mx-1"> | </span>
														<span>{dayjs(comment.date).format('DD MMMM YYYY')}</span>
													</div>
													<p className="mb-0">{comment.message}</p>
												</div>
											</div>
										))}
									</>
								}
								<div className="mb-3 flex">
									<Avatar shape="circle" src="/img/avatars/thumb-1.jpg"/>
									<div className="ml-2 rtl:mr-2 px-3 rounded w-full">
										<Input
											ref={commentInput}
											placeholder="Write comment"
											suffix={
												<div 
													onClick={() => submitComment()} 
													className="cursor-pointer font-weight-semibold text-primary">
													Send
												</div>
											}
										/>
									</div>
								</div>
							</div>
						</TicketSection> */}
					</div>
					<div className="text-right mt-4">
						<Button 
							className="mr-2 rtl:ml-2"
							size="sm"
							variant="plain"
							onClick={() => handleTicketClose()}
						>
							Cancel
						</Button>
						<Button 
							variant="solid" 
							size="sm" 
							onClick={() => handleTicketClose()}
						>
							Change
						</Button>
					</div>
				</>
			}
		</>
	)
}

export default TicketContent
