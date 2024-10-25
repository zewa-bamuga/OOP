import { News } from '@/types/news.types'

import { axiosWithAuth } from '@/api/interceptors'

class NewsService {
	private BASE_URL = '/news/v1/get'

	async getNews() {
		const response = await axiosWithAuth.get<{ items: News[] }>(this.BASE_URL)
		return response.data
	}

	async likeNews(newsId: string) {
		const response = await axiosWithAuth.post('/news/v1/like', {
			projectId: parseInt(newsId, 10)
		})
		return response.data
	}

	async unlikeNews(newsId: string) {
		const response = await axiosWithAuth.delete('/projects/v1/like', {
			headers: {
				'Content-Type': 'application/json'
			},
			data: {
				newsId: parseInt(newsId, 10) // передаем projectId в теле запроса
			}
		})
		return response.data
	}

	async getNewsById(newsIdNumber: number) {
		console.log(`Fetching project with ID: ${newsIdNumber}`)

		const response = await axiosWithAuth.get<News>(
			`/news/v1/news/by/id/${newsIdNumber}`
		)
		return response.data
	}
}

export const userService = new NewsService()
