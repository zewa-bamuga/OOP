import { UUID } from 'crypto'

export interface Project {
	id: string
	name: string
	startDate: Date
	endDate: Date
	description: string | null
	participants: number
	lessons: number
	likes: number | null
	avatarAttachmentId: UUID
	avatarAttachment: {
		id: string
		name: string
		path: string
		uri: string
	} | null
}
