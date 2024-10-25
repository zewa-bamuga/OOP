import { IUser, TypeUserForm } from '@/types/auth.types'

import { axiosWithAuth } from '@/api/interceptors'

import { getAccessToken } from './auth-token.service'

class UserService {
	private BASE_URL = '/profile/v1/me'

	async getProfile() {
		const response = await axiosWithAuth.get<IUser>(this.BASE_URL)

		return response.data
	}

	async update(data: TypeUserForm) {
		const token = getAccessToken()

		const response = await axiosWithAuth.put(this.BASE_URL, data, {
			headers: {
				Authorization: `${token}`
			}
		})

		return response.data
	}
}

export const userService = new UserService()
