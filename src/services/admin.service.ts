import { Project } from '@/types/project.types'

import { axiosWithAuth } from '@/api/interceptors'

class ProjectService {
	private BASE_URL = '/projects/v1'

	async createProject(
		token: string,
		projectData: {
			name: string
			startDate: string
			endDate: string
			description: string
			participants: number
			lessons: number
		}
	) {
		const response = await axiosWithAuth.post(
			`${this.BASE_URL}/create`,
			projectData,
			{
				headers: {
					Authorization: `Bearer ${token}`
				}
			}
		)
		return response.data
	}

	async addStaffToProject(token: string, projectId: number, staffId: string) {
		const response = await axiosWithAuth.post(
			`${this.BASE_URL}/add/employees`,
			{
				projectId,
				staffId
			},
			{
				headers: {
					Authorization: `Bearer ${token}`
				}
			}
		)
		return response.data
	}

	async getProjects(token: string) {
		const response = await axiosWithAuth.get(`${this.BASE_URL}/get`, {
			headers: {
				Authorization: `Bearer ${token}`
			}
		})
		return response.data
	}

	async getProjectById(projectIdNumber: number) {
		console.log(`Fetching project with ID: ${projectIdNumber}`)

		const response = await axiosWithAuth.get<Project>(
			`/projects/v1/project/by/id/${projectIdNumber}`
		)
		return response.data
	}

	async createNews(
		token: string,
		newsData: { name: string; date: string; description: string }
	) {
		const response = await axiosWithAuth.post(`/news/v1/create`, newsData, {
			headers: {
				Authorization: `Bearer ${token}`
			}
		})
		return response.data
	}

	async getNews(token: string) {
		const response = await axiosWithAuth.get(`/news/v1/get`, {
			headers: {
				Authorization: `Bearer ${token}`
			}
		})
		return response.data
	}

	async getNewsById(token: string, newsId: number) {
		const response = await axiosWithAuth.get(`/news/v1/get/by/id/${newsId}`, {
			headers: {
				Authorization: `Bearer ${token}`
			}
		})
		return response.data
	}
}

export const projectService = new ProjectService()
