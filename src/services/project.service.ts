// project.service.ts
import { Project } from '@/types/project.types'

import { axiosWithAuth } from '@/api/interceptors'

class ProjectService {
	private BASE_URL = '/projects/v1/get'

	async getProject() {
		const response = await axiosWithAuth.get<{ items: Project[] }>(
			this.BASE_URL
		)
		return response.data
	}

	async likeProject(projectId: string) {
		const response = await axiosWithAuth.post('/projects/v1/like', {
			projectId: parseInt(projectId, 10)
		})
		return response.data
	}

	async unlikeProject(projectId: string) {
		const response = await axiosWithAuth.delete('/projects/v1/unlike', {
			headers: {
				'Content-Type': 'application/json'
			},
			data: {
				projectId: parseInt(projectId, 10) // передаем projectId в теле запроса
			}
		})
		return response.data
	}
}

export const userService = new ProjectService()
