'use client'

import { useMutation } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { SubmitHandler, useForm } from 'react-hook-form'
import { toast } from 'sonner'

import { Heading } from '@/components/ui/Heading'
import { Button } from '@/components/ui/buttons/Button'

import { IAuthForm } from '@/types/auth.types'

import { DASHBOARD_PAGES } from '@/config/pages-url.config'

import { authService } from '@/services/auth.service'

{
	/* cSpell:ignore главная клипы проекты Отдел Образовательных Программ Команда призванная побеждать создаём классные проекты обучаем новому саморазвиваемся запомнить меня Вход Регистрация Почта Пароль забыли Отправим сообщение с кодом на указанную почту Далее почте */
}

export function Register() {
	const { register, handleSubmit, reset, control } = useForm<IAuthForm>({
		mode: 'onChange'
	})

	const [isLoginForm, setIsLoginForm] = useState(false)
	const [showBoxes, setShowBoxes] = useState(false)
	const [hideBoxes, setHideBoxes] = useState(false)
	const [showSecondBlock, setShowSecondBlock] = useState(false)

	const { push } = useRouter()

	const { mutate } = useMutation({
		mutationKey: ['register'],
		mutationFn: (data: IAuthForm) =>
			authService.main(isLoginForm ? 'login' : 'register', data),
		onSuccess() {
			toast.success('Successfully registration!')
			reset()
			push(DASHBOARD_PAGES.HOME)
		}
	})

	const onSubmit: SubmitHandler<IAuthForm> = data => {
		mutate(data)
	}

	useEffect(() => {
		const timer = setTimeout(() => {
			setShowBoxes(true)
		}, 50)

		const hideTimer = setTimeout(() => {
			setHideBoxes(true)
		}, 2500)

		const secondBlockTimer = setTimeout(() => {
			setShowSecondBlock(true)
		}, 2500)

		return () => {
			clearTimeout(timer)
			clearTimeout(hideTimer)
			clearTimeout(secondBlockTimer)
		}
	}, [])

	return (
		<div className='flex min-h-screen font-helvetica'>
			<div
				className={`flex flex-col items-start space-y-4 mt-28 absolute ${showSecondBlock ? 'show' : 'hidden'}`}
			>
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
			<div
				className={`flex flex-col items-start space-y-4 mt-28 absolute ${showBoxes ? 'show' : 'hidden'} ${hideBoxes ? 'hidden' : ''}`}
			>
				<button
					className={`promo-box-anim bg-oopyellow w-[300px] h-[35px] rounded-r-full flex items-center ${showBoxes ? 'show' : 'hidden'}`}
					style={{
						color: '#323232',
						paddingLeft: '180px',
						zIndex: 1
					}}
				>
					главная
				</button>
				<button
					className={`promo-box-anim bg-oopgray w-[300px] h-[35px] rounded-r-full flex items-center ${showBoxes ? 'show' : 'hidden'}`}
					style={{ paddingLeft: '180px' }}
				>
					клипы
				</button>
				<button
					className={`promo-box-anim bg-oopblue w-[300px] h-[35px] rounded-r-full flex items-center ${showBoxes ? 'show' : 'hidden'}`}
					style={{ paddingLeft: '180px' }}
				>
					проекты
				</button>
			</div>

			<div
				className='absolute mt-[110px]'
				style={{ color: '#323232', paddingLeft: '350px' }}
			>
				<div className='text-left flex items-start'>
					<img
						src='/logo.png'
						alt='logo.png'
						className='w-[70px] h-[70px]'
					/>
					<p
						className='ml-3 text-lg font-light mb-1 leading-6'
						style={{ fontFamily: 'Helvetica', fontWeight: 300 }}
					>
						Отдел
						<br />
						Образовательных
						<br />
						Программ
					</p>

					<div className='absolute flex flex-col mt-24'>
						<p
							className='text-4xl mb-4 leading-10'
							style={{
								fontFamily: 'Helvetica',
								fontWeight: 'bold',
								fontStyle: 'italic',
								whiteSpace: 'nowrap'
							}}
						>
							Команда, <br />
							призванная побеждать
						</p>
						<ul
							className='list-none text-sm leading-7'
							style={{
								fontFamily: 'Lato, sans-serif',
								fontWeight: 100,
								letterSpacing: '0.09em'
							}}
						>
							<li>- создаём классные проекты</li>
							<li>- обучаем новому</li>
							<li>- саморазвиваемся</li>
						</ul>
					</div>
				</div>
			</div>

			<form
				className='bg-sidebar mt-28 ml-[900px] rounded-xl px-8 w-[430px] h-[265px]'
				onSubmit={handleSubmit(onSubmit)}
			>
				<div className='flex items-center justify-between mb-6'>
					<Heading
						title='Вход'
						isButton={true}
						onClick={() => push('../auth')}
						className=' text-2xl pt-[25px] text-gray-600 font-bold'
					/>
					<Heading
						title='Регистрация'
						className='text-2xl pt-4 text-oopgray font-bold'
					/>
				</div>

				<div className='flex flex-col items-center gap-4'>
					<Button
						variant='gray'
						className={isLoginForm ? '' : 'bg-oopgray mt-4'}
						onClick={() => push('../register/email')}
					>
						По почте
					</Button>
					<Button
						variant='blue'
						className={isLoginForm ? '' : ''}
						onClick={() => setIsLoginForm(false)}
					>
						Войти с VK ID
					</Button>
				</div>
			</form>
		</div>
	)
}
