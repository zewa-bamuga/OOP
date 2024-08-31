'use client'

import { ABeeZee } from 'next/font/google'
import { useEffect, useRef, useState } from 'react'

import { Header } from '@/components/main-layout/header/Header'
import { Sidebar } from '@/components/main-layout/sidebar/Sidebar'

import { Project } from '@/types/project.types'

import { useAuth } from '@/hooks/useAuth'

import { userService } from '@/services/project.service'

const images = ['/banner.png', '/banner2.jpg', '/banner3.jpg']

const abeezee = ABeeZee({
	subsets: ['latin'],
	weight: ['400']
})

export function Clips() {
	const [currentIndex, setCurrentIndex] = useState(0)
	const [startCount, setStartCount] = useState(false)
	const [projects, setProjects] = useState<Project[]>([])
	const [likedProjects, setLikedProjects] = useState<Record<string, boolean>>(
		{}
	)

	const { isAuthenticated } = useAuth()
	const [showAuthNotification, setShowAuthNotification] = useState(false)
	const statsRef = useRef<HTMLDivElement | null>(null)

	const nextSlide = () => {
		setCurrentIndex(prevIndex => (prevIndex + 1) % images.length)
	}

	const prevSlide = () => {
		setCurrentIndex(
			prevIndex => (prevIndex - 1 + images.length) % images.length
		)
	}

	const formatDate = (dateString: string) => {
		const date = new Date(dateString)
		return date.toLocaleDateString('ru-RU', {
			day: 'numeric',
			month: 'long'
		})
	}

	const formatDateRange = (startDate: Date, endDate: Date) => {
		const options = { day: 'numeric', month: 'long' } as const
		const start = new Intl.DateTimeFormat('ru-RU', options).format(startDate)
		const end = new Intl.DateTimeFormat('ru-RU', options).format(endDate)
		return `${start} - ${end}`
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
		const fetchProjects = async () => {
			try {
				const data = await userService.getProject()
				setProjects(data.items)
			} catch (error) {
				console.error('Ошибка при загрузке проектов:', error)
			}
		}

		fetchProjects()
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

	const saveLikedProjectsToLocalStorage = (
		likedProjects: Record<string, boolean>
	) => {
		localStorage.setItem('likedProjects', JSON.stringify(likedProjects))
	}

	const [projectsCount, setProjectsCount] = useState(0)
	const [employees, setEmployees] = useState(0)
	const [subscribers, setSubscribers] = useState(0)

	useEffect(() => {
		if (startCount) {
			animateValue(0, 6, 3000, setProjectsCount)
			animateValue(0, 38, 3000, setEmployees)
			animateValue(0, 1092, 3000, setSubscribers)
		}
	}, [startCount])

	useEffect(() => {
		const storedLikedProjects = localStorage.getItem('likedProjects')
		if (storedLikedProjects) {
			setLikedProjects(JSON.parse(storedLikedProjects))
		}
	}, [])

	const toggleLike = async (id: string) => {
		if (!isAuthenticated) {
			setShowAuthNotification(true)
			return
		}

		try {
			const projectId = parseInt(id, 10) // Преобразование строки в число

			if (likedProjects[id]) {
				await userService.unlikeProject(projectId)
				setProjects(prevProjects =>
					prevProjects.map(project =>
						project.id === id
							? { ...project, likes: (project.likes || 0) - 1 }
							: project
					)
				)
			} else {
				await userService.likeProject(projectId)
				setProjects(prevProjects =>
					prevProjects.map(project =>
						project.id === id
							? { ...project, likes: (project.likes || 0) + 1 }
							: project
					)
				)
			}

			const updatedLikedProjects = {
				...likedProjects,
				[id]: !likedProjects[id]
			}
			setLikedProjects(updatedLikedProjects)
			saveLikedProjectsToLocalStorage(updatedLikedProjects)
		} catch (error) {
			console.error('Ошибка при обновлении лайков:', error)
		}
	}

	const handleAuthRedirect = () => {
		window.location.href = '../auth'
		setShowAuthNotification(false)
	}

	const groupProjectsByYear = (projects: Project[]) => {
		return projects.reduce(
			(acc, project) => {
				const year = new Date(project.startDate).getFullYear()
				if (!acc[year]) {
					acc[year] = []
				}
				acc[year].push(project)
				return acc
			},
			{} as Record<number, Project[]>
		)
	}

	const groupedProjects = groupProjectsByYear(projects)

	return (
		<div className='flex min-h-screen font-helvetica'>
			<Header />
			<Sidebar />

			<div className='absolute mt-[60px] w-full h-[230px] flex'>
				{/* Левая половина с изображением и текстом */}
				<div className='w-1/2 h-full relative'>
					<img
						src='/qwerty.jpg'
						alt='Проекты'
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
							ПРОЕКТЫ
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
							Проект
						</span>{' '}
						- совокупность действий и мероприятий, направленных <br />
						на создание уникального продукта, в частности <br />{' '}
						образовательного
					</p>
				</div>
			</div>
		</div>
	)
}
