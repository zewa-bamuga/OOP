import { useEffect, useState } from 'react'

import { getAccessToken } from '@/services/auth-token.service'
import { userService } from '@/services/user.service'

export function useAuth() {
	const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)
	const [isLoading, setIsLoading] = useState<boolean>(true)

	useEffect(() => {
		const checkAuth = async () => {
			try {
				const token = getAccessToken()

				if (!token) {
					setIsAuthenticated(false)
					setIsLoading(false)
					return
				}

				await userService.getProfile()
				setIsAuthenticated(true)
			} catch {
				setIsAuthenticated(false)
			} finally {
				setIsLoading(false)
			}
		}

		checkAuth()
	}, [])

	return { isAuthenticated, isLoading }
}
