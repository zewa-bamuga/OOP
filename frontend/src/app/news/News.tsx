'use client'

import { ABeeZee } from 'next/font/google'
import { useEffect, useRef, useState } from 'react'

import { Header } from '@/components/main-layout/header/Header'
import { Sidebar } from '@/components/main-layout/sidebar/Sidebar'

import { useAuth } from '@/hooks/useAuth'

import { userService } from '@/services/news.service'
import { News } from '@/types/news.types'

const images = ['/banner.png', '/banner2.jpg', '/banner3.jpg']

const abeezee = ABeeZee({
	subsets: ['latin'],
	weight: ['400']
})

export function News() {
	const [currentIndex, setCurrentIndex] = useState(0)
	const [startCount, setStartCount] = useState(false)
	const [news, setNews] = useState<News[]>([])
	const [likedNews, setLikedNews] = useState<Record<string, boolean>>({})

	const { isAuthenticated } = useAuth()
	const [showAuthNotification, setShowAuthNotification] = useState(false)
	const statsRef = useRef<HTMLDivElement | null>(null)

	const nextSlide = () => {
		setCurrentIndex(prevIndex => (prevIndex + 1) % images.length)
	}

	const prevSlide = () => {
		setCurrentIndex(prevIndex => (prevIndex - 1 + images.length) % images.length)
	}

	const formatDate = (dateString: Date) => {
		const date = new Date(dateString)
		return date.toLocaleDateString('ru-RU', {
			day: 'numeric',
			month: 'long'
		})
	}

	const getSlideClass = (index: number) => {
		if (index === currentIndex) {
			return 'translate-x-0'
		} else if (index === (currentIndex - 1 + images.length) % images.length) {
			return '-translate-x-full z-[-1]'
		} else {
			return 'translate-x-full z-[-2]'
		}
	}

	useEffect(() => {
		const observer = new IntersectionObserver(
			entries => {
				if (entries[0].isIntersecting) {
					setStartCount(true)
				}
			},
			{ threshold: 0.3 }
		)

		if (statsRef.current) {
			observer.observe(statsRef.current)
		}

		return () => {
			if (statsRef.current) {
				observer.unobserve(statsRef.current)
			}
		}
	}, [])

	useEffect(() => {
		const fetchNews = async () => {
			try {
				const data = await userService.getNews()
				setNews(data.items)
			} catch (error) {
				console.error('Ошибка при загрузке новостей:', error)
			}
		}

		fetchNews()
	}, [])

	const animateValue = (
		start: number,
		end: number,
		duration: number,
		setValue: React.Dispatch<React.SetStateAction<number>>
	) => {
		let startTime: number | null = null
		const easing = (t: number) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t))

		const step = (currentTime: number) => {
			if (!startTime) startTime = currentTime
			const timeElapsed = currentTime - startTime
			const progress = Math.min(timeElapsed / duration, 1)
			const easedProgress = easing(progress)
			setValue(Math.floor(easedProgress * (end - start) + start))

			if (progress < 1) {
				window.requestAnimationFrame(step)
			}
		}

		window.requestAnimationFrame(step)
	}

	const saveLikedNewsToLocalStorage = (
		likedNews: Record<string, boolean>
	) => {
		localStorage.setItem('likedNews', JSON.stringify(likedNews))
	}

	const [newsCount, setNewsCount] = useState(0)
	const [employees, setEmployees] = useState(0)
	const [subscribers, setSubscribers] = useState(0)

	useEffect(() => {
		if (startCount) {
			animateValue(0, 6, 3000, setNewsCount)
			animateValue(0, 38, 3000, setEmployees)
			animateValue(0, 1092, 3000, setSubscribers)
		}
	}, [startCount])

	useEffect(() => {
		const storedLikedNews = localStorage.getItem('likedNews')
		if (storedLikedNews) {
			setLikedNews(JSON.parse(storedLikedNews))
		}
	}, [])

	const toggleLike = async (id: string) => {
		if (!isAuthenticated) {
			setShowAuthNotification(true)
			return
		}

		try {
			const newsId = parseInt(id, 10)

			if (likedNews[id]) {
				await userService.unlikeNews(newsId)
				setNews(prevNews =>
					prevNews.map(news =>
						news.id === id
							? { ...news, likes: (news.likes || 0) - 1 }
							: news
					)
				)
			} else {
				await userService.likeNews(newsId)
				setNews(prevNews =>
					prevNews.map(news =>
						news.id === id
							? { ...news, likes: (news.likes || 0) + 1 }
							: news
					)
				)
			}

			const updatedLikedNews = {
				...likedNews,
				[id]: !likedNews[id]
			}
			setLikedNews(updatedLikedNews)
			saveLikedNewsToLocalStorage(updatedLikedNews)
		} catch (error) {
			console.error('Ошибка при обновлении лайков:', error)
		}
	}

	const handleAuthRedirect = () => {
		window.location.href = '../auth'
		setShowAuthNotification(false)
	}

	const remindAboutNews = (id: string) => {
		alert(`Вы поставили напоминание для новости с ID: ${id}`);
	}

	const groupNewsByYear = (news: News[]) => {
		return news.reduce(
			(acc, newsItem) => {
				const year = new Date(newsItem.date).getFullYear()
				if (!acc[year]) {
					acc[year] = []
				}
				acc[year].push(newsItem)
				return acc
			},
			{} as Record<number, News[]>
		)
	}

	const groupedNews = groupNewsByYear(news)

	return (
		<div className='flex min-h-screen font-helvetica'>
			<Header />
			<Sidebar />

			<div className='absolute mt-[60px] w-full h-[230px] flex'>
				{/* Левая половина с изображением и текстом */}
				<div className='w-1/2 h-full relative'>
					<img
						src='/qwerty.jpg'
						alt='Новости'
						className='w-full h-full object-cover'
					/>
					<div className='absolute inset-0 flex items-center justify-center'>
						<h1
							className='text-[65px] text-white leading-tight'
							style={{
								fontFamily: 'IntroFriday',
								fontWeight: 'bold',
								whiteSpace: 'nowrap'
							}}
						>
							НОВОСТИ
						</h1>
					</div>
				</div>

				{/* Правая половина с серым фоном и текстом */}
				<div className='w-1/2 h-full bg-oopgray flex items-center justify-center'>
					<p className='text-white text-[20px] leading-tight px-10'>
						<span
							className='text-oopyellow'
							style={{
								fontStyle: 'italic'
							}}
						>
							Новости
						</span>{' '}
						- совокупность событий и обновлений, которые происходят <br />
						в нашем сообществе и мире в целом.
					</p>
				</div>
			</div>

			<div className='absolute mt-[340px] px-48'>
				<div className='space-y-8'>
					{Object.keys(groupedNews)
						.sort()
						.reverse()
						.map(year => (
							<div key={year}>
								<h2
									className='text-oopblack text-4xl font-bold ml-4 mb-1'
									style={{
										fontFamily: 'Helvetica',
										fontWeight: 'bold'
									}}
								>
									{year}
								</h2>
								<div className='flex flex-wrap'>
									{groupedNews[year].map(news => (
										<div
											key={news.id}
											className='w-[370px] h-[320px] m-4 border border-[#E5E5E5] bg-white shadow-card'
										>
											<img
												src={news.avatarAttachment?.uri || ''}
												alt={news.name}
												className='w-[368px] h-[200px] object-cover'
											/>
											<div className='p-4'>
												<p className='text-[#808080] text-sm'>
													{formatDate(news.date)}
												</p>
												<h3 className='text-xl font-bold text-[#2B2B2B]'>
													{news.name}
												</h3>
												<p className='text-sm text-[#6F6F6F] mt-1'>
													{news.description}
												</p>
												<div className='flex justify-between mt-3'>
													<button
														onClick={() => toggleLike(news.id)}
														className={`${
															likedNews[news.id]
																? 'text-red-500'
																: 'text-gray-400'
														} focus:outline-none`}
													>
														❤️ {news.likes || 0}
													</button>

													{/* Новая кнопка "Напомнить" */}
													<button
														onClick={() => remindAboutNews(news.id)}
														className='text-blue-500 focus:outline-none'
													>
														🔔 Напомнить
													</button>
												</div>
											</div>
										</div>
									))}
								</div>
							</div>
						))}
				</div>
			</div>
		</div>
	)
}
