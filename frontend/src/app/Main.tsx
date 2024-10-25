'use client'

import { ChevronLeft, ChevronRight } from 'lucide-react'
import { ABeeZee } from 'next/font/google'
import { useRouter } from 'next/navigation'
import { useEffect, useRef, useState } from 'react'

import { Header } from '@/components/main-layout/header/Header'
import { Sidebar } from '@/components/main-layout/sidebar/Sidebar'

import './globals.scss'

const abeezee = ABeeZee({
	subsets: ['latin'],
	weight: ['400']
})

const images = ['/banner.png', '/banner2.jpg', '/banner3.jpg']

export function Main() {
	const [currentIndex, setCurrentIndex] = useState(0)
	const [startCount, setStartCount] = useState(false)

	const { push } = useRouter()

	const statsRef = useRef(null)

	const nextSlide = () => {
		setCurrentIndex(prevIndex => (prevIndex + 1) % images.length)
	}

	const prevSlide = () => {
		setCurrentIndex(
			prevIndex => (prevIndex - 1 + images.length) % images.length
		)
	}

	const getSlideClass = (index: number) => {
		if (index === currentIndex) {
			// Активный слайд
			return 'translate-x-0'
		} else if (index === (currentIndex - 1 + images.length) % images.length) {
			// Предыдущий слайд
			return '-translate-x-full z-[-1]'
		} else {
			// Все остальные (следующие) слайды
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

	const animateValue = (
		start: number,
		end: number,
		duration: number,
		setValue: React.Dispatch<React.SetStateAction<number>>
	) => {
		let startTime: number | null = null; // Указываем, что startTime может быть числом или null

		const easing = (t: number) => {
			return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
		};

		const step = (currentTime: number) => {
			if (!startTime) startTime = currentTime;
			const timeElapsed = currentTime - startTime;
			const progress = Math.min(timeElapsed / duration, 1);
			const easedProgress = easing(progress);
			setValue(Math.floor(easedProgress * (end - start) + start));

			if (progress < 1) {
				window.requestAnimationFrame(step);
			}
		};

		window.requestAnimationFrame(step);
	}

	const [projects, setProjects] = useState(0)
	const [employees, setEmployees] = useState(0)
	const [subscribers, setSubscribers] = useState(0)

	useEffect(() => {
		if (startCount) {
			animateValue(0, 6, 3000, setProjects)
			animateValue(0, 38, 3000, setEmployees)
			animateValue(0, 1092, 3000, setSubscribers)
		}
	}, [startCount])

	return (
		<div className='flex min-h-screen font-helvetica'>
			<Header />
			<Sidebar />

			<div className='absolute mt-[60px] w-full h-[790px]'>
				<div className='w-full h-full overflow-hidden relative'>
					{images.map((image, index) => (
						<div
							key={index}
							className={`absolute top-0 left-0 w-full h-full transition-transform duration-700 ease-in-out ${getSlideClass(index)}`}
							style={{
								background: `
                  linear-gradient(
                    to right,
                    rgba(50, 50, 50, 0.35) 0%,
                    rgba(50, 50, 50, 0.15) 50%,
                    rgba(50, 50, 50, 0.35) 100%
                  ),
                  url(${image}) center/cover no-repeat
                `
							}}
						>
							<div className='absolute inset-0 flex flex-col items-center justify-center text-white text-center'>
								<h1
									className='text-[65px] mb-4 leading-tight font-intro'
									style={{
										fontFamily: 'IntroFriday',
										fontWeight: 'bold',
										whiteSpace: 'nowrap'
									}}
								>
									ООП - КОМАНДА,
									<br />
									ПРИЗВАННАЯ
									<br />
									ПОБЕЖДАТЬ
								</h1>
							</div>
						</div>
					))}

					<button
						onClick={prevSlide}
						className='absolute top-1/2 transform -translate-y-1/2 left-40'
					>
						<ChevronLeft className='w-14 h-14 filter invert brightness-0 opacity-50 hover:opacity-85 transition-opacity duration-300' />
					</button>

					<button
						onClick={nextSlide}
						className='absolute top-1/2 transform -translate-y-1/2 right-40'
					>
						<ChevronRight className='w-14 h-14 filter invert brightness-0 opacity-50 hover:opacity-65 transition-opacity duration-300' />
					</button>

					<div className='absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2'>
						{images.map((_, index) => (
							<div
								key={index}
								className={`w-3 h-3 rounded-full transition-colors duration-300 ${
									index === currentIndex
										? 'bg-white opacity-100'
										: 'bg-gray-500 opacity-50'
								}`}
							/>
						))}
					</div>
				</div>
			</div>
			<div
				ref={statsRef}
				className='absolute ${abeezee.className} mt-[890px] w-full h-[496px] bg-oopgray flex flex-col items-center'
			>
				<h2
					className='text-4xl mt-10'
					style={{
						fontWeight: 100,
						fontStyle: 'italic',
						whiteSpace: 'nowrap'
					}}
				>
					О нас в цифрах
				</h2>

				<p className='text-lg text-center mr-[770px] mt-11'>
					<span
						className='text-9xl'
						style={{
							fontFamily: 'IntroFriday',
							fontWeight: 'bold',
							whiteSpace: 'nowrap'
						}}
					>
						{projects}
					</span>
					<br />
					<span
						className='text-oopblue'
						style={{
							fontFamily: 'Lato, sans-serif',
							fontWeight: 400,
							position: 'relative',
							top: '-55px',
							whiteSpace: 'nowrap'
						}}
					>
						проектов
					</span>

					<br />
					<span
						style={{
							fontFamily: 'sans-serif',
							fontWeight: 100,
							position: 'relative',
							top: '-55px',
							whiteSpace: 'nowrap'
						}}
					>
						за 2023 - 2024 <br /> учебный год
					</span>
				</p>

				<div className='absolute mt-36 text-center'>
					<span
						className='text-9xl'
						style={{
							fontFamily: 'IntroFriday',
							fontWeight: 'bold',
							whiteSpace: 'nowrap'
						}}
					>
						{employees}
					</span>
					<br />
					<span
						className='text-oopyellow'
						style={{
							fontFamily: 'Lato, sans-serif',
							fontWeight: 400,
							position: 'relative',
							top: '-55px',
							whiteSpace: 'nowrap'
						}}
					>
						сотрудников
					</span>
					<br />
					<span
						className='font-light'
						style={{
							fontFamily: 'Lato, sans-serif',
							fontWeight: 100,
							position: 'relative',
							top: '-55px',
							whiteSpace: 'nowrap'
						}}
					>
						в подразделении
					</span>
				</div>

				<div className='flex flex-col items-center text-center ml-[770px] mt-[-320px]'>
					<span
						className='text-9xl'
						style={{
							fontFamily: 'IntroFriday',
							fontWeight: 'bold',
							whiteSpace: 'nowrap'
						}}
					>
						{subscribers}
					</span>
					<br />
					<span
						className='text-oopblue -mt-7'
						style={{
							fontFamily: 'Lato, sans-serif',
							fontWeight: 400,
							position: 'relative',
							top: '-55px',
							whiteSpace: 'nowrap'
						}}
					>
						подписчиков
					</span>
					<br />
					<span
						className='font-light -mt-7'
						style={{
							fontFamily: 'Lato, sans-serif',
							fontWeight: 100,
							position: 'relative',
							top: '-55px',
							whiteSpace: 'nowrap'
						}}
					>
						в социальной <br />
					</span>
					<div className='inline-flex items-center'>
						<span
							className='font-light'
							style={{
								fontFamily: 'Lato, sans-serif',
								fontWeight: 100,
								position: 'relative',
								top: '-55px',
								whiteSpace: 'nowrap'
							}}
						>
							сети
						</span>
						<a
							href='https://vk.com/oop_tusur'
							target='_blank'
							rel='noopener noreferrer'
						>
							<img
								src='/vk-icon-blue.png'
								alt='VK Icon'
								className='w-6 h-6 ml-2 mt-[-66px]'
							/>
						</a>
					</div>
				</div>
			</div>
		</div>
	)
}
