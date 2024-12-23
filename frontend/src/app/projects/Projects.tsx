'use client'

import {ABeeZee} from 'next/font/google'
import Link from 'next/link'
import {useEffect, useRef, useState} from 'react'

import {Header} from '@/components/main-layout/header/Header'
import {Sidebar} from '@/components/main-layout/sidebar/Sidebar'

import {Project} from '@/types/project.types'

import {useAuth} from '@/hooks/useAuth'

import {userService} from '@/services/project.service'

const images = ['/banner.png', '/banner2.jpg', '/banner3.jpg']

const abeezee = ABeeZee({
    subsets: ['latin'],
    weight: ['400']
})

export function Projects() {
    const [currentIndex, setCurrentIndex] = useState(0)
    const [startCount, setStartCount] = useState(false)
    const [projects, setProjects] = useState<Project[]>([])
    const [likedProjects, setLikedProjects] = useState<Record<string, boolean>>(
        {}
    )

    const {isAuthenticated} = useAuth()
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

    const formatDate = (dateString: Date) => {
        return dateString.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long'
        })
    }


    const formatDateRange = (startDate: Date, endDate: Date) => {
        const options = {day: 'numeric', month: 'long'} as const
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
            {threshold: 0.3}
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
            const projectId = parseInt(id, 10)

            if (likedProjects[id]) {
                await userService.unlikeProject(id)
                setProjects(prevProjects =>
                    prevProjects.map(project =>
                        project.id === id
                            ? {...project, likes: (project.likes || 0) - 1}
                            : project
                    )
                )
            } else {
                await userService.unlikeProject(id)
                setProjects(prevProjects =>
                    prevProjects.map(project =>
                        project.id === id
                            ? {...project, likes: (project.likes || 0) + 1}
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
            <Header/>
            <Sidebar/>

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
                        - совокупность действий и мероприятий, направленных <br/>
                        на создание уникального продукта, в частности <br/>{' '}
                        образовательного
                    </p>
                </div>
            </div>

            <div className='absolute mt-[340px] px-48'>
                <div className='space-y-8'>
                    {Object.keys(groupedProjects)
                        .sort()
                        .reverse()
                        .map(year => (
                            <div key={year}>
                                <h2
                                    className='text-oopblack text-4xl font-bold ml-4 mb-1'
                                    style={{
                                        fontFamily: 'Helvetica',
                                        fontWeight: 'bold',
                                        fontStyle: 'italic',
                                        whiteSpace: 'nowrap'
                                    }}
                                >
                                    {year}
                                </h2>
                                <div className='grid grid-cols-3 gap-8'>
                                    {groupedProjects[+year].map(project => {
                                        const {
                                            id: projectId,
                                            avatarAttachment,
                                            name,
                                            startDate,
                                            endDate,
                                            likes
                                        } = project

                                        return (
                                            <div
                                                key={projectId}
                                                className='rounded-md p-4'
                                            >
                                                {avatarAttachment && (
                                                    <img
                                                        src={avatarAttachment.uri}
                                                        alt={avatarAttachment.name}
                                                        className='w-[300px] h-[300px] object-cover rounded-md mb-4'
                                                    />
                                                )}

                                                <div className='flex justify-between mb-1'>
                                                    <h3
                                                        className='text-oopblack text-lg font-semibold'
                                                        style={{
                                                            fontFamily: 'Helvetica',
                                                            fontStyle: 'bold',
                                                            whiteSpace: 'nowrap'
                                                        }}
                                                    >
                                                        {name}
                                                    </h3>
                                                    <div className='flex items-center'>
														<span
                                                            className='text-oopgray text-sm mr-2 leading-7'
                                                            style={{
                                                                fontFamily: 'Lato, sans-serif',
                                                                fontWeight: 400,
                                                                letterSpacing: '0.09em'
                                                            }}
                                                        >
															{likes}
														</span>
                                                        <button
                                                            onClick={() => toggleLike(projectId)}
                                                            className={`w-6 h-6 transition-colors duration-300 ease-in-out ${
                                                                likedProjects[projectId]
                                                                    ? 'bg-red-500'
                                                                    : 'bg-oopyellow'
                                                            } rounded-md flex items-center justify-center hover:bg-oopredhover`}
                                                        >
                                                            <img
                                                                src='/heart.png'
                                                                alt='like'
                                                                className={`w-4 h-4 filter invert`}
                                                            />
                                                        </button>
                                                    </div>
                                                </div>

                                                <p
                                                    className='text-oopgray text-base mb-4'
                                                    style={{
                                                        fontFamily: 'Lato, sans-serif',
                                                        fontWeight: 300
                                                    }}
                                                >
                                                    {endDate
                                                        ? formatDateRange(
                                                            new Date(startDate),
                                                            new Date(endDate)
                                                        )
                                                        : formatDate(new Date(startDate))}
                                                </p>

                                                <Link
                                                    href={`/projects/${projectId}`}
                                                    className='bg-oopyellow text-oopblack px-4 py-2 rounded-md transition-colors duration-300 ease-in-out hover:bg-oopyellowhover'
                                                >
                                                    перейти
                                                </Link>
                                            </div>
                                        )
                                    })}
                                </div>
                            </div>
                        ))}
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
