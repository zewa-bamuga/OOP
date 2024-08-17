'use client'

import { ChevronLeft, ChevronRight } from 'lucide-react'
import { useState } from 'react'

import { Header } from '@/components/main-layout/header/Header'

const images = ['/banner.png', '/banner2.jpg', '/banner3.jpg']

export function Main() {
	const [currentIndex, setCurrentIndex] = useState(0)

	const nextSlide = () => {
		setCurrentIndex(prevIndex => (prevIndex + 1) % images.length)
	}

	const prevSlide = () => {
		setCurrentIndex(
			prevIndex => (prevIndex - 1 + images.length) % images.length
		)
	}

	const getSlideClass = index => {
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

	return (
		<div className='flex min-h-screen font-helvetica'>
			<Header />

			<div className='absolute mt-[60px] w-full h-[640px]'>
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
									className='text-[65px] mb-4 leading-tight'
									style={{
										fontFamily: 'Helvetica',
										fontWeight: 'bold',
										whiteSpace: 'nowrap'
									}}
								>
									ООО - КОМАНДА,
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

			<div className='absolute mt-[720px] w-full bg-oopgray py-12 flex flex-col items-center'>
				<h2 className='text-2xl font-bold -mt-5'>О нас в цифрах</h2>
				<p className='text-lg text-center'>
					6<br />
					проектов
					<br />
					за 2023 - 2024
					<br />
					учебный год
				</p>
			</div>

			<div className={`flex flex-col items-start space-y-4 mt-[92px] absolute`}>
				<button
					className={`promo-box bg-oopyellow w-[320px] h-[35px] rounded-r-full flex items-center`}
					style={{
						color: '#323232',
						paddingLeft: '200px',
						marginLeft: '-20px',
						zIndex: 1
					}}
				>
					главная
				</button>
				<button
					className={`promo-box bg-oopgray w-[320px] h-[35px] rounded-r-full flex items-center`}
					style={{ paddingLeft: '200px', marginLeft: '-20px', zIndex: 1 }}
				>
					клипы
				</button>
				<button
					className={`promo-box bg-oopblue w-[320px] h-[35px] rounded-r-full flex items-center`}
					style={{ paddingLeft: '200px', marginLeft: '-20px', zIndex: 1 }}
				>
					проекты
				</button>
			</div>
		</div>
	)
}
