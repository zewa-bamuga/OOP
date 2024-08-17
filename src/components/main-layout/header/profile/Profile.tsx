'use client'

import Loader from '@/components/ui/Loader'

import { useProfile } from '@/hooks/useProfile'

export function Profile() {
	const { data, isLoading } = useProfile()
	console.log('Profile component data:', data)

	if (isLoading) {
		return (
			<div className='absolute top-big-layout right-big-layout'>
				<Loader />
			</div>
		)
	}

	return (
		<div className='absolute right-48 text-oopblack'>
			<p
				className='font-bold text-lg'
				style={{
					fontFamily: 'Helvetica',
					fontStyle: 'italic',
					whiteSpace: 'nowrap'
				}}
			>
				<span className='mr-2'>{data?.firstname}</span>
				<span>{data?.lastname}</span>
			</p>
		</div>
	)
}
