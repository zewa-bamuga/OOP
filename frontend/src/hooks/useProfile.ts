import { useQuery } from '@tanstack/react-query'

import { IUser } from '@/types/auth.types'

import { useAuth } from './useAuth'
import { userService } from '@/services/user.service'

export function useProfile() {
	const { isAuthenticated } = useAuth()
	const query = useQuery<IUser>({
		queryKey: ['profile'],
		queryFn: () => userService.getProfile(),
		enabled: isAuthenticated
	})

	return query
}
