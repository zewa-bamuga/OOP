'use client'

import { useRouter } from 'next/navigation'

import Loader from '@/components/ui/Loader'

import { useAuth } from '@/hooks/useAuth'
import { useProfile } from '@/hooks/useProfile'

import { Profile } from './profile/Profile'

export function Header() {
	const { push } = useRouter()
	const { isAuthenticated, isLoading } = useAuth()
	const { data: profileData, isLoading: isProfileLoading } = useProfile()

	// Проверяем, идет ли загрузка данных профиля
	if (isLoading || isProfileLoading) {
		return (
			<header className='relative w-full h-[60px]'>
				<div className='absolute top-1/2 right-4 transform -translate-y-1/2 flex items-center'>
					<Loader />
				</div>
			</header>
		)
	}

	// Получаем URI аватара, если он есть
	const avatarUri = profileData?.avatarAttachment?.uri

	return (
		<header className='relative w-full h-[60px]'>
			<div className='bg-white text-oopblack p-2.5 box-border flex justify-between items-center h-full'>
				<div
					className='flex list-none m-0 ml-[120px]'
					style={{
						fontFamily: 'Lato, sans-serif',
						fontWeight: 100,
						letterSpacing: '0.09em'
					}}
				>
					<button
						className='text-oopblack border-none cursor-pointer py-2 px-5 text-sm transition-colors duration-300 ease-in-out hover:bg-ooplightblue rounded-3xl transition-all duration-300 ease-in-out'
						style={{ marginRight: '2rem' }}
						onClick={() => push('/employees')}
					>
						сотрудники
					</button>
					<button
						className='text-oopblack border-none cursor-pointer py-2 px-5 text-sm transition-colors duration-300 ease-in-out hover:bg-ooplightblue rounded-3xl transition-all duration-300 ease-in-out'
						style={{ marginRight: '2rem' }}
						onClick={() => push('/directions')}
					>
						направления
					</button>
					<button
						className='text-oopblack border-none cursor-pointer py-2 px-5 text-sm transition-colors duration-300 ease-in-out hover:bg-ooplightblue rounded-3xl'
						onClick={() => push('/news')}
					>
						новости
					</button>
				</div>
			</div>
			<div className='absolute left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[120px] h-[120px] bg-white rounded-full z-30 flex items-center justify-center'>
				<div className='w-[85px] h-[85px] bg-white rounded-full overflow-hidden shadow-inner'>
					{/* Если пользователь авторизован и есть аватар, показываем его, иначе показываем логотип */}
					{isAuthenticated && avatarUri ? (
						<img
							src={avatarUri}
							alt='User Avatar'
							className='w-full h-full object-cover'
						/>
					) : (
						<img
							src='/logo.png'
							alt='logo.png'
							className='w-full h-full object-cover'
						/>
					)}
				</div>
			</div>
			<div className='absolute top-1/2 right-4 transform -translate-y-1/2 flex items-center space-x-2 text-oopblack text-sm'>
				{!isAuthenticated ? (
					<>
						<button
							className='absolute bg-oopyellowopacity py-2 px-6 rounded-full flex items-center'
							style={{
								width: '250px',
								height: '35px',
								fontFamily: 'Lato, sans-serif',
								fontWeight: 100,
								letterSpacing: '0.09em',
								marginLeft: '-80px',
								boxShadow: 'inset 0 0 5px rgba(0, 0, 0, 0.15)'
							}}
							onClick={() => push('../auth')}
						>
							<span>войти</span>
						</button>
						<button
							className='bg-oopyellow rounded-full flex items-center justify-center z-30'
							style={{
								width: '250px',
								height: '35px',
								fontFamily: 'Lato, sans-serif',
								fontWeight: 100,
								letterSpacing: '0.09em',
								marginRight: '100px',
								boxShadow: 'inset 0 0 5px rgba(0, 0, 0, 0.15)'
							}}
							onClick={() => push('../register')}
						>
							<span>зарегистрироваться</span>
						</button>
					</>
				) : (
					<Profile />
				)}
			</div>
		</header>
	)
}
