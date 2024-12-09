export interface IEmailVerificationRequest {
    email: string
}

export interface IEmailVerificationConfirm {
    code: BigInteger
}

export interface IRegForm {
    email: string;
    code?: string | undefined;
    firstname: string;
    lastname: string;
    password: string;
}


export interface IAuthForm {
    email: string;
    password: string;
    code?: string;
    isRememberMe?: boolean;
}


export interface IUser {
    id: string
    firstname: string
    lastname: string
    qualification: string | null
    post: string | null
    email: string
    description: string | null
    linkToVk: string | null
    avatarAttachmentId: number | null
    avatarAttachment?: {
        uri: string
    } | null
}

export interface IAuthResponse {
    accessToken: string
    user: IUser
}

export type TypeUserForm = Omit<IUser, 'id'> & { password?: string }
