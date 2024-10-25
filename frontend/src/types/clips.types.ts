import { UUID } from 'crypto'

export interface Clip {
	id: string
	name: string
	date: Date
	description: string | null
	likes: number | null
	clipAttachmentId: UUID
	clipAttachment: {
		id: string
		name: string
		path: string
		uri: string
	} | null
}
