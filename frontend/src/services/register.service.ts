import axios from 'axios'

import {
    IEmailVerificationConfirm,
    IEmailVerificationRequest,
    IRegForm
} from '@/types/auth.types'

import {axiosClassic} from '@/api/interceptors'

export const registerService = {
    async main(data: IRegForm) {
        try {
            const response = await axiosClassic.post(
                `/authentication/v1/registration`,
                data
            );
            if (response.status === 200) {
                console.log('Registration successful:', response.data);
            } else {
                console.error('Registration failed:', response.data);
            }
            return response;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.response) {
                    console.error('Error response:', error.response.data);
                } else {
                    console.error('Error message:', error.message);
                }
            } else {
                console.error('Unexpected error:', error);
            }
            throw error;
        }
    },

    async verification_email_request(data: IEmailVerificationRequest) {
        const response = await axiosClassic.post(
            '/authentication/v1/email/verification/request',
            data
        )
        return response
    },

    async verification_email_confirm(data: { code: string | undefined; email: string }) {
        const response = await axiosClassic.post(
            '/authentication/v1/email/verification/confirm',
            data
        )
        return response
    }
}
