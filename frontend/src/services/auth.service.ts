import axios, {AxiosError} from 'axios'

import {IAuthForm, IAuthResponse} from '@/types/auth.types'

import {axiosClassic} from '@/api/interceptors'

import {removeFromStorage, saveTokenStorage} from './auth-token.service'

export const authService = {
    async main(data: IAuthForm) {
        try {
            const response = await axiosClassic.post<IAuthResponse>(
                `/authentication/v1/authentication`,
                data
            )

            if (response.data.accessToken) saveTokenStorage(response.data.accessToken)

            return response
        } catch (error) {
            if (axios.isAxiosError(error)) {
                if (error.response) {
                    console.error('Error response:', error.response.data)
                } else {
                    console.error('Error message:', error.message)
                }
            } else {
                console.error('Unexpected error:', error)
            }
            throw error
        }
    },

    async getNewTokens() {
        const response = await axiosClassic.post<IAuthResponse>(
            '/authentication/v1/refresh'
        )

        if (response.data.accessToken) saveTokenStorage(response.data.accessToken)

        return response
    },

    async logout() {
        const response = await axiosClassic.post<boolean>('/auth/logout')

        if (response.data) removeFromStorage()

        return response
    }
}
