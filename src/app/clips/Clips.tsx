'use client'

import { ABeeZee } from 'next/font/google'
import { useEffect, useRef, useState } from 'react'

import { Header } from '@/components/main-layout/header/Header'
import { Sidebar } from '@/components/main-layout/sidebar/Sidebar'

import { Clip } from '@/types/clips.types'

import { useAuth } from '@/hooks/useAuth'

import { userService } from '@/services/clip.service'

const abeezee = ABeeZee({
	subsets: ['latin'],
	weight: ['400']
})

export function Clips() {
	const [currentClipIndex, setCurrentClipIndex] = useState(0)
	const [clips, setClips] = useState<Clip[]>([])
	const [likedClips, setLikedClips] = useState<Record<string, boolean>>({})
	const [isPlaying, setIsPlaying] = useState(true)
	const [showOverlay, setShowOverlay] = useState('')
	const [currentTime, setCurrentTime] = useState(0)
	const [duration, setDuration] = useState(0)

	const { isAuthenticated } = useAuth()
	const [showAuthNotification, setShowAuthNotification] = useState(false)

	const videoRef = useRef<HTMLVideoElement | null>(null)
	const timelineRef = useRef<HTMLDivElement | null>(null)
	const backgroundTimelineRef = useRef<HTMLDivElement | null>(null)
	const animationRef = useRef<number | null>(null)

	useEffect(() => {
		const fetchClips = async () => {
			try {
				const data = await userService.getClips()
				setClips(data.items)
			} catch (error) {
				console.error('Ошибка при загрузке клипов:', error)
			}
		}

		fetchClips()
	}, [])

	useEffect(() => {
		const storedLikedClips = localStorage.getItem('likedClips')
		if (storedLikedClips) {
			setLikedClips(JSON.parse(storedLikedClips))
		}
	}, [])

	useEffect(() => {
		const handleKeyDown = (event: KeyboardEvent) => {
			if (event.key === 'ArrowDown') {
				nextClip()
			}
			if (event.key === 'ArrowUp') {
				previousClip()
			}
			if (event.key === ' ') {
				event.preventDefault() // Предотвращаем скроллинг страницы при нажатии пробела
				togglePlayPause()
			}
		}

		window.addEventListener('keydown', handleKeyDown)
		return () => {
			window.removeEventListener('keydown', handleKeyDown)
		}
	}, [clips, currentClipIndex, isPlaying])

	useEffect(() => {
		const updateTimeline = () => {
			if (videoRef.current && timelineRef.current) {
				const progress =
					(videoRef.current.currentTime / videoRef.current.duration) * 100
				timelineRef.current.style.width = `${progress}%`
				animationRef.current = requestAnimationFrame(updateTimeline)
			}
		}

		if (isPlaying) {
			animationRef.current = requestAnimationFrame(updateTimeline)
		} else if (animationRef.current) {
			cancelAnimationFrame(animationRef.current)
		}

		return () => {
			if (animationRef.current) {
				cancelAnimationFrame(animationRef.current)
			}
		}
	}, [isPlaying])

	useEffect(() => {
		if (videoRef.current) {
			const handlePlayPause = () => {
				if (videoRef.current?.paused) {
					setShowOverlay('pause')
					setIsPlaying(false)
					const timer = setTimeout(() => {
						setShowOverlay('')
					}, 1000) // Длительность отображения иконки паузы

					return () => {
						clearTimeout(timer)
					}
				} else {
					setShowOverlay('play')
					setIsPlaying(true)
					const timer = setTimeout(() => {
						setShowOverlay('')
					}, 1000) // Длительность отображения иконки воспроизведения

					return () => {
						clearTimeout(timer)
					}
				}
			}

			const handleTimeUpdate = () => {
				if (videoRef.current) {
					setCurrentTime(videoRef.current.currentTime)
					setDuration(videoRef.current.duration)
				}
			}

			videoRef.current.addEventListener('play', handlePlayPause)
			videoRef.current.addEventListener('pause', handlePlayPause)
			videoRef.current.addEventListener('timeupdate', handleTimeUpdate)

			return () => {
				videoRef.current?.removeEventListener('play', handlePlayPause)
				videoRef.current?.removeEventListener('pause', handlePlayPause)
				videoRef.current?.removeEventListener('timeupdate', handleTimeUpdate)
			}
		}
	}, [videoRef.current])

	const togglePlayPause = () => {
		if (videoRef.current) {
			if (videoRef.current.paused) {
				videoRef.current.play()
			} else {
				videoRef.current.pause()
			}
		}
	}

	const nextClip = () => {
		setCurrentClipIndex(prevIndex => (prevIndex + 1) % clips.length)
	}

	const previousClip = () => {
		setCurrentClipIndex(
			prevIndex => (prevIndex - 1 + clips.length) % clips.length
		)
	}

	const toggleLike = async (id: string) => {
		if (!isAuthenticated) {
			setShowAuthNotification(true)
			return
		}

		try {
			const clipId = parseInt(id, 10)

			if (likedClips[id]) {
				await userService.likeClip(clipId) // Удаление лайка
				setClips(prevClips =>
					prevClips.map(clip =>
						clip.id === id ? { ...clip, likes: (clip.likes || 0) - 1 } : clip
					)
				)
			} else {
				await userService.likeClip(clipId) // Добавление лайка
				setClips(prevClips =>
					prevClips.map(clip =>
						clip.id === id ? { ...clip, likes: (clip.likes || 0) + 1 } : clip
					)
				)
			}

			const updatedLikedClips = {
				...likedClips,
				[id]: !likedClips[id]
			}
			setLikedClips(updatedLikedClips)
			saveLikedClipsToLocalStorage(updatedLikedClips)
		} catch (error) {
			console.error('Ошибка при обновлении лайков:', error)
		}
	}

	const handleAuthRedirect = () => {
		window.location.href = '../auth'
		setShowAuthNotification(false)
	}

	const handleTimelineClick = (event: React.MouseEvent<HTMLDivElement>) => {
		if (videoRef.current) {
			const rect = (
				event.currentTarget as HTMLDivElement
			).getBoundingClientRect()
			const clickX = event.clientX - rect.left
			const newTime = (clickX / rect.width) * duration
			videoRef.current.currentTime = newTime
			setCurrentTime(newTime)
		}
	}

	if (clips.length === 0) {
		return (
			<div className='flex min-h-screen items-center justify-center'>
				<p className='text-gray-700 text-2xl'>Нет доступных клипов.</p>
			</div>
		)
	}

	return (
		<div className='flex min-h-screen items-center flex-col bg-black'>
			<Header />
			<Sidebar />

			<div className='relative flex-grow w-full max-w-xs md:max-w-sm lg:max-w-md xl:max-w-lg'>
				<div className='relative flex flex-col scale-75 items-center justify-center h-screen'>
					<div className='relative w-full h-full'>
						{clips.length > 0 && (
							<>
								<video
									ref={videoRef}
									src={clips[currentClipIndex].clipAttachment?.uri}
									alt={clips[currentClipIndex].name}
									className='relative z-10 w-full h-full object-cover rounded-lg'
									controls={false}
									autoPlay
									loop
									onClick={() => togglePlayPause()}
								/>
								<div
									className={`overlay ${showOverlay === 'pause' ? 'show-pause' : ''}`}
								>
									<span className='icon'>❚❚</span>
								</div>
								<div
									className={`overlay ${showOverlay === 'play' ? 'show-play' : ''}`}
								>
									<span className='icon'>▶</span>
								</div>
								<div className='absolute bottom-0 z-20 items-start p-4'>
									<h3 className='text-white text-lg font-semibold'>
										{clips[currentClipIndex].name}
									</h3>
									<p className='text-gray-300'>
										{clips[currentClipIndex].description}
									</p>
								</div>
								<div className='absolute bottom-0 left-0 z-30 w-[98%] ml-[5px] rounded-full bg-gray-700'>
									<div
										ref={backgroundTimelineRef}
										className='relative h-2 bg-gray-400 rounded-full'
										style={{ width: '100%' }}
									>
										<div
											ref={timelineRef}
											className='absolute bg-oopblue h-full rounded-full cursor-pointer'
											style={{ width: '0%', transition: 'width 0.1s linear' }}
											onClick={handleTimelineClick}
										/>
									</div>
								</div>
								<div className='absolute bottom-0 z-10 right-0 p-4'>
									<button
										onClick={() => toggleLike(clips[currentClipIndex].id)}
										className={`w-6 h-6 transition-colors duration-300 ease-in-out ${
											likedClips[clips[currentClipIndex].id]
												? 'bg-red-500'
												: 'bg-yellow-500'
										} rounded-md flex items-center justify-center hover:bg-red-600`}
									>
										<img
											src='/heart.png'
											alt='like'
											className='w-4 h-4 filter invert'
										/>
									</button>
								</div>
							</>
						)}
					</div>
					<div className='absolute right-0 top-1/2 transform -translate-y-1/2'>
						<button
							onClick={nextClip}
							className='text-white text-4xl hover:text-gray-400 focus:outline-none'
						>
							↓
						</button>
					</div>
					<div className='absolute left-0 top-1/2 transform -translate-y-1/2'>
						<button
							onClick={previousClip}
							className='text-white text-4xl hover:text-gray-400 focus:outline-none'
						>
							↑
						</button>
					</div>
				</div>
			</div>

			{showAuthNotification && (
				<div className='fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75'>
					<div className='bg-white p-6 rounded-lg shadow-lg text-center'>
						<h2 className='text-oopblack text-lg font-bold mb-4'>
							Необходима авторизация
						</h2>
						<p className='text-oopblack mb-6'>
							Пожалуйста, войдите в систему, чтобы использовать эту функцию.
						</p>
						<button
							onClick={handleAuthRedirect}
							className='bg-blue-500 text-white px-4 py-2 rounded-md'
						>
							Перейти на страницу авторизации
						</button>
					</div>
				</div>
			)}
		</div>
	)
}

const saveLikedClipsToLocalStorage = (likedClips: Record<string, boolean>) => {
	localStorage.setItem('likedClips', JSON.stringify(likedClips))
}
