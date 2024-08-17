export interface IEmailVerificationRequest {
	email: string
}

export interface IEmailVerificationConfirm {
	code: BigInteger
}

export interface IRegForm {
	firstname: string
	lastname: string
	email: string
	password: string
	isRememberMe?: boolean
}

export interface IAuthForm {
	email: string
	password: string
	code?: string
}

export interface IUser {
	id: string // id в возвращаемом объекте — строка
	firstname: string
	lastname: string
	qualification: string | null
	post: string | null
	email: string
	description: string | null
	linkToVk: string | null
	avatarAttachmentId: number | null
}

export interface IAuthResponse {
	accessToken: string
	user: IUser
}

export type TypeUserForm = Omit<IUser, 'id'> & { password?: string }
