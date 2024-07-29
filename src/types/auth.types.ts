export interface IRegForm {
	firstname: string
	lastname: string
	email: string
	password: string
}

export interface IAuthForm {
	firstname: string
	lastname: string
	email: string
	password: string
}

export interface IUser {
	id: number
	firstname: string
	lastname: string
	qualification: string
	post: string
	email: string
	description: string
	linkToVk: string
	avatarAttachmentId: number
}

export interface IAuthResponse {
	accessToken: string
	user: IUser
}

export type TypeUserForm = Omit<IUser, 'id'> & { password?: string }
