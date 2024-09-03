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
		if (videoRef.current) {
			const handlePlayPause = () => {
				if (videoRef.current?.paused) {
					setShowOverlay('pause')
					const timer = setTimeout(() => {
						setShowOverlay('')
					}, 1000) // Длительность отображения иконки паузы

					return () => {
						clearTimeout(timer)
					}
				} else {
					setShowOverlay('play')
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

	useEffect(() => {
		const updateTimeline = () => {
			if (videoRef.current && timelineRef.current) {
				const progress =
					(videoRef.current.currentTime / videoRef.current.duration) * 100
				timelineRef.current.style.width = `${progress}%`
				requestAnimationFrame(updateTimeline)
			}
		}
		if (isPlaying) {
			requestAnimationFrame(updateTimeline)
		}
	}, [isPlaying])

	const toggleLike = async (id: string) => {
		if (!isAuthenticated) {
			setShowAuthNotification(true)
			return
		}

		try {
			const clipId = parseInt(id, 10)

			if (likedClips[id]) {
				await userService.unlikeClip(clipId)
				setClips(prevClips =>
					prevClips.map(clip =>
						clip.id === id ? { ...clip, likes: (clip.likes || 0) - 1 } : clip
					)
				)
			} else {
				await userService.likeClip(clipId)
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

	const nextClip = () => {
		setCurrentClipIndex(prevIndex => (prevIndex + 1) % clips.length)
	}

	const togglePlayPause = () => {
		if (videoRef.current) {
			if (videoRef.current.paused) {
				videoRef.current.play()
				setIsPlaying(true)
			} else {
				videoRef.current.pause()
				setIsPlaying(false)
			}
		}
	}

	const handleVideoClick = () => {
		togglePlayPause()
	}

	const handleAuthRedirect = () => {
		// Перенаправление на страницу авторизации
	}

	const handleTimelineClick = (event: React.MouseEvent<HTMLDivElement>) => {
		if (videoRef.current) {
			const rect = (event.target as HTMLDivElement).getBoundingClientRect()
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
				<div className='relative flex flex-col items-center justify-center h-screen'>
					<div className='relative w-full h-full'>
						{clips.length > 0 && (
							<>
								<video
									ref={videoRef}
									src={clips[currentClipIndex].clipAttachment?.uri}
									alt={clips[currentClipIndex].name}
									className='absolute inset-0 transform scale-90 translate-x-1/10 translate-y-1/10 object-cover rounded-lg' // Масштабирование видео на 80% и сдвиг
									controls={false}
									autoPlay
									loop
									onClick={handleVideoClick}
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
								<div className='absolute bottom-0 left-0 w-full'>
									<div className='relative w-full h-1'>
										{/* Градиент для улучшения видимости текста не работает */}

										<div
											className='absolute inset-0 bg-gradient-to-t from-black to-transparent'
											style={{ height: '100%' }}
										/>
										<div
											className='w-full h-1 bg-gray-600 cursor-pointer relative'
											onClick={handleTimelineClick}
										>
											<div
												ref={timelineRef}
												className='bg-oopblue'
											/>
										</div>
									</div>
									<div className='absolute bottom-0 left-0 w-full p-4'>
										{/* Градиент для улучшения видимости текста не работает */}
										<div className='absolute inset-0 bottom-0 h-1/4 bg-gradient-to-t from-black via-transparent to-transparent z-10' />
										<div className='relative z-20 flex flex-col items-start'>
											<h3 className='text-white text-lg font-semibold'>
												{clips[currentClipIndex].name}
											</h3>
											<p className='text-gray-300'>
												{clips[currentClipIndex].description}
											</p>
										</div>
									</div>
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
				</div>
			</div>

			{showAuthNotification && (
				<div className='fixed inset-0 flex items-center justify-center z-50'>
					<div className='bg-white p-8 rounded-lg shadow-lg'>
						<h2 className='text-2xl font-bold mb-4'>Требуется авторизация</h2>
						<p className='mb-4'>
							Чтобы ставить лайки, пожалуйста, войдите в свою учетную запись.
						</p>
						<div className='flex justify-end'>
							<button
								onClick={handleAuthRedirect}
								className='bg-blue-500 text-white px-4 py-2 rounded-lg'
							>
								Войти
							</button>
						</div>
					</div>
					{/* Overlay для затемнения экрана */}
					<div className='fixed inset-0 bg-black opacity-50' />
				</div>
			)}
		</div>
	)
}
