import { UUID } from 'crypto'

export interface News {
	id: string
	name: string
	date: Date
	description: string | null
	likes: number | null
	reminder: string
	avatarAttachmentId: UUID
	avatarAttachment: {
		id: string
		name: string
		path: string
		uri: string
	} | null
}
