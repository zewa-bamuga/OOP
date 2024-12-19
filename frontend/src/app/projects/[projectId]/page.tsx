'use client'

import {useEffect, useRef, useState} from 'react'

import {Header} from '@/components/main-layout/header/Header'
import {Sidebar} from '@/components/main-layout/sidebar/Sidebar'

import {Project} from '@/types/project.types'

import {useAuth} from '@/hooks/useAuth'

import '../../globals.scss'

import {userService} from '@/services/project.service'

interface ProjectPageProps {
    params: { projectId: string }
}

export default function ProjectPage({params}: ProjectPageProps) {
    const projectId = Number(params.projectId)
    const {isAuthenticated} = useAuth()
    const [project, setProject] = useState<Project | null>(null)
    const [likedProjects, setLikedProjects] = useState<Record<string, boolean>>(
        {}
    )
    const [showAuthNotification, setShowAuthNotification] = useState(false)

    const [participants, setParticipants] = useState(0)
    const [lessons, setLessons] = useState(0)
    const [startCount, setStartCount] = useState(false)

    const participantsRef = useRef(0)
    const lessonsRef = useRef(0)
    const statsRef = useRef<HTMLDivElement>(null)

    const animateValue = (
        start: number,
        end: number,
        duration: number,
        setValue: React.Dispatch<React.SetStateAction<number>>,
        ref: React.MutableRefObject<number>
    ) => {
        let startTime: number | null = null

        const easing = (t: number) => {
            return t === 1 ? 1 : 1 - Math.pow(2, -10 * t)
        }

        const step = (currentTime: number) => {
            if (!startTime) startTime = currentTime
            const timeElapsed = currentTime - startTime
            const progress = Math.min(timeElapsed / duration, 1)
            const easedProgress = easing(progress)
            const newValue = Math.floor(easedProgress * (end - start) + start)
            if (ref.current !== newValue) {
                setValue(newValue)
                ref.current = newValue
                console.log('Animating:', newValue)
            }

            if (progress < 1) {
                window.requestAnimationFrame(step)
            }
        }

        window.requestAnimationFrame(step)
    }

    useEffect(() => {
        const observer = new IntersectionObserver(
            entries => {
                console.log('Intersection Observer Entries:', entries)
                if (entries[0].isIntersecting) {
                    console.log('Element is intersecting')
                    setStartCount(true)
                    console.log('Updated startCount to true')
                    observer.disconnect()
                }
            },
            {threshold: 0.3}
        )

        if (statsRef.current) {
            console.log('Observing:', statsRef.current)
            observer.observe(statsRef.current)
        } else {
            console.error('statsRef.current is null')
        }

        return () => {
            if (statsRef.current) {
                console.log('Stopped observing:', statsRef.current)
                observer.unobserve(statsRef.current)
            }
        }
    }, [])

    useEffect(() => {
        const fetchProject = async () => {
            try {
                const fetchedProject = await userService.getProjectById(projectId)
                console.log('Fetched Project:', fetchedProject)
                console.log('startCount in fetchProject:', startCount)

                if (fetchedProject) {
                    setProject(fetchedProject)
                    console.log('Setting project data:', fetchedProject)

                    if (
                        fetchedProject.participants !== participantsRef.current &&
                        startCount
                    ) {
                        animateValue(
                            participantsRef.current,
                            fetchedProject.participants,
                            3000,
                            setParticipants,
                            participantsRef
                        )
                    }
                    if (fetchedProject.lessons !== lessonsRef.current && startCount) {
                        animateValue(
                            lessonsRef.current,
                            fetchedProject.lessons,
                            3000,
                            setLessons,
                            lessonsRef
                        )
                    }
                }
            } catch (error) {
                console.error('Ошибка при загрузке проекта:', error)
            }
        }

        fetchProject()
    }, [projectId, startCount])

    const formatDateRange = (startDate: Date, endDate: Date) => {
        const options = {day: 'numeric', month: 'long'} as const
        const start = new Intl.DateTimeFormat('ru-RU', options).format(startDate)
        const end = new Intl.DateTimeFormat('ru-RU', options).format(endDate)
        return `${start} - ${end}`
    }

    const toggleLike = async (id: string) => {
        if (!isAuthenticated) {
            setShowAuthNotification(true)
            return
        }

        try {
            if (likedProjects[id]) {
                await userService.likeProject(id.toString())
                setLikedProjects(prevLikedProjects => ({
                    ...prevLikedProjects,
                    [id]: false
                }))
            } else {
                await userService.likeProject(id.toString())
                setLikedProjects(prevLikedProjects => ({
                    ...prevLikedProjects,
                    [id]: true
                }))
            }
        } catch (error) {
            console.error('Ошибка при обновлении лайков:', error)
        }
    }

    if (!project) {
        return null
    }

    return (
        <div className='flex min-h-screen font-helvetica'>
            <Header/>
            <Sidebar/>
            <div className='absolute mt-[60px] w-full h-[640px]'>
                <div className='w-full h-full overflow-hidden relative'>
                    <div className='absolute top-0 left-0 w-full h-full transition-transform duration-700 ease-in-out'>
                        <img
                            src='/qwerty.jpg'
                            alt='logo.png'
                        />
                        <div
                            className='absolute inset-0 flex flex-col items-center justify-center text-white text-center mb-[430px]'>
                            <h1
                                className='text-[65px] leading-tight mt-5'
                                style={{
                                    fontFamily: 'IntroFriday',
                                    fontWeight: 'bold',
                                    whiteSpace: 'nowrap'
                                }}
                            >
                                {project.name}
                            </h1>
                        </div>
                    </div>
                </div>
            </div>

            {/* Контейнер для изображения и текста справа от него */}
            {project.avatarAttachment && (
                <div className='absolute mt-[350px] w-[1000px] flex ml-52'>
                    <div className='flex items-start space-x-8'>
                        <img
                            src={project.avatarAttachment.uri}
                            alt={project.avatarAttachment.name || 'Project Image'}
                            className='w-[400px] h-[400px] object-cover rounded-full border-4 border-oopblue'
                        />

                        {/* Текстовое описание справа от изображения */}
                        <div className='flex flex-col text-oopblack'>
							<span
                                className='text-oopblack text-base font-bold ml-24 mb-1'
                                style={{
                                    fontFamily: 'Helvetica',
                                    fontWeight: 'bold',
                                    fontStyle: 'italic',
                                    whiteSpace: 'nowrap'
                                }}
                            >
								Дата проведения:
							</span>
                            {project.startDate && project.endDate && (
                                <p
                                    className='text-oopgray text-base mb-4 ml-24'
                                    style={{
                                        fontFamily: 'Lato, sans-serif',
                                        fontWeight: 300
                                    }}
                                >
                                    {formatDateRange(
                                        new Date(project.startDate),
                                        new Date(project.endDate)
                                    )}
                                </p>
                            )}
                            {project.startDate && !project.endDate && (
                                <p className=''>
                                    {' '}
                                    {new Date(project.startDate).toLocaleDateString('ru-RU', {
                                        day: 'numeric',
                                        month: 'long'
                                    })}
                                </p>
                            )}
                            <span
                                className='text-oopblack text-base font-bold ml-24 mb-1'
                                style={{
                                    fontFamily: 'Helvetica',
                                    fontWeight: 'bold',
                                    fontStyle: 'italic',
                                    whiteSpace: 'nowrap'
                                }}
                            >
								Описание:
							</span>
                            <p
                                className='text-oopgray text-base mb-4 ml-24 break-all'
                                style={{
                                    fontFamily: 'Lato, sans-serif',
                                    fontWeight: 300
                                }}
                            >
                                {project.description}
                            </p>

                            <div className='absolute flex items-center ml-[520px]'>
								<span
                                    className='text-oopgray text-sm mr-2 leading-7'
                                    style={{
                                        fontFamily: 'Lato, sans-serif',
                                        fontWeight: 400,
                                        letterSpacing: '0.09em'
                                    }}
                                >
									{project.likes}
								</span>
                                <button
                                    onClick={() => toggleLike(project.id)}
                                    className={`w-6 h-6 transition-colors duration-300 ease-in-out ${
                                        likedProjects[projectId] ? 'bg-red-500' : 'bg-oopyellow'
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
                    </div>
                </div>
            )}

            <div className='absolute t-60 flex mt-[900px] overflow-hidden'>
				<span
                    className='absolute text-oopblack text-4xl mt-20 ml-[200px]'
                    style={{
                        fontFamily: 'Helvetica',
                        fontWeight: 'bold',
                        fontStyle: 'italic',
                        whiteSpace: 'nowrap'
                    }}
                >
					Проект в цифрах
				</span>
                <div
                    className='absolute mt-52 ml-[200px] flex space-x-16'
                    ref={statsRef}
                >
                    <div className='flex flex-col items-center'>
						<span
                            className='text-oopblack text-9xl'
                            style={{
                                fontFamily: 'IntroFriday',
                                fontWeight: 'bold',
                                whiteSpace: 'nowrap'
                            }}
                        >
							{participants}
						</span>
                        <span
                            className='text-oopblack mt-5'
                            style={{
                                fontFamily: 'Lato, sans-serif',
                                fontWeight: 400,
                                position: 'relative',
                                top: '-55px',
                                whiteSpace: 'nowrap'
                            }}
                        >
							участников
						</span>
                    </div>
                    <div className='flex flex-col items-center'>
						<span
                            className='text-oopblack text-9xl'
                            style={{
                                fontFamily: 'IntroFriday',
                                fontWeight: 'bold',
                                whiteSpace: 'nowrap'
                            }}
                        >
							{lessons}
						</span>
                        <span
                            className='text-oopblack mt-5'
                            style={{
                                fontFamily: 'Lato, sans-serif',
                                fontWeight: 400,
                                position: 'relative',
                                top: '-55px',
                                whiteSpace: 'nowrap'
                            }}
                        >
							занятий
						</span>
                    </div>
                </div>
                <img
                    src='/Vector.png'
                    alt='Your Photo'
                    className='ml-[580px] max-w-full h-auto'
                />
            </div>

            <div className='absolute flex mt-[1600px] '>
				<span
                    className='absolute text-oopblack text-4xl ml-[200px]'
                    style={{
                        fontFamily: 'Helvetica',
                        fontWeight: 'bold',
                        fontStyle: 'italic',
                        whiteSpace: 'nowrap'
                    }}
                >
					Сотрудники на проекте
				</span>
            </div>
        </div>
    )
}
