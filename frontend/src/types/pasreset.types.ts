export interface IPasswordResetRequest {
	email: string;
}

export interface IPasswordResetConfirm {
	email: string;
	code: string;
	password: string;
}
