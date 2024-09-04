import { Clip } from '@/types/clips.types'

import { axiosWithAuth } from '@/api/interceptors'

class ClipService {
	private BASE_URL = '/clips/v1/get'

	async likeClip(clipId: string) {
		const response = await axiosWithAuth.post('/clips/v1/like', {
			clipId: parseInt(clipId, 10)
		})
		return response.data
	}

	async getClipById(clipIdNumber: number) {
		console.log(`Fetching project with ID: ${clipIdNumber}`)

		const response = await axiosWithAuth.get<Clip>(
			`/clips/v1/get/by/id/${clipIdNumber}`
		)
		return response.data
	}

	async getClips() {
		const response = await axiosWithAuth.get<{ items: Clip[] }>(`/clips/v1/get`)
		return response.data
	}
}

export const userService = new ClipService()
