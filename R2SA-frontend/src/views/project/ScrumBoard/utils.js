export const reorder = (list, startIndex, endIndex) => {
	const result = Array.from(list)
	const [removed] = result.splice(startIndex, 1)
	result.splice(endIndex, 0, removed)
	return result
}

export const reorderQuoteMap = ({ quoteMap, source, destination }) => {
	const current = [...quoteMap[source.droppableId]]
	const next = [...quoteMap[destination.droppableId]]
	const target = current[source.index]

	// moving to same list
	if (source.droppableId === destination.droppableId) {
		const reordered = reorder( current, source.index, destination.index)
		const result = {
			...quoteMap,
			[source.droppableId]: reordered,
		}
		return {
			quoteMap: result,
		}
	}
	current.splice(source.index, 1)
	next.splice(destination.index, 0, target)
	const result = {
		...quoteMap,
		[source.droppableId]: current,
		[destination.droppableId]: next,
	}

	return {
		quoteMap: result,
	}
}

const clone = (obj) => Object.assign({}, obj)

export const renameKey = (object, key, newKey) => {
	const clonedObj = clone(object)
	const targetKey = clonedObj[key]
	delete clonedObj[key]
	clonedObj[newKey] = targetKey
	return clonedObj
}

export const createUID = len => {
	const buf = [],
		chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
		charlen = chars.length,
		length = len || 32
			
	for (let i = 0; i < length; i++) {
		buf[i] = chars.charAt(Math.floor(Math.random() * charlen))
	}
	return buf.join('')
}

export const createCardObject = () => {
	return {
		id: createUID(10),
		name: 'Untitled Card',
		description: 'Your next cash-flowing asset!',
		cover: '',
		members: [],
		labels: [],
		attachments: [],
		checklists: [],
		comments: [],
		dueDate: null
	}
}

export const taskLabelColors = {
	'Studio': 'bg-rose-500',
	'1 bed': 'bg-blue-500',
	'2 bed': 'bg-amber-400',
	'3 bed': 'bg-indigo-500',
	'4 bed': 'bg-indigo-600',
	'5+ bed': 'bg-indigo-700'
}

export const labelList = ['Studio', '1 bed', '2 bed', '3 bed', '4 bed', '5+ bed']