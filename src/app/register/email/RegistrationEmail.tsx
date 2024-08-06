'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { SubmitHandler, useForm, useFormState } from 'react-hook-form'
import { toast } from 'sonner'

import { Heading } from '@/components/ui/Heading'
import { Button } from '@/components/ui/buttons/Button'
import { Field } from '@/components/ui/fields/Field'

import { IAuthForm } from '@/types/auth.types'

{
	/* cSpell:ignore главная клипы проекты Отдел Образовательных Программ Команда призванная побеждать создаём классные проекты обучаем новому саморазвиваемся запомнить меня Вход Регистрация Почта Пароль забыли Отправим сообщение указанную почту пришло Поле обязательно заполнения Восстановление пароля Восстановить Изменить Отправили письмо Отправить Повторная отправка через Минимум символов Завершить регистрацию завершена успешно зарегистрировались Фамилия Закрыть кодом Далее */
}

export function RegByEmail() {
	const { register, handleSubmit, reset, watch, control } = useForm<IAuthForm>({
		mode: 'onSubmit'
	})
	const { errors, isSubmitted } = useFormState({ control })

	const [step, setStep] = useState(1)
	const [email, setEmail] = useState('')
	const [countdown, setCountdown] = useState(60)
	const [canResend, setCanResend] = useState(false)
	const [isModalOpen, setIsModalOpen] = useState(false)
	const [passwordVisible, setPasswordVisible] = useState(false)
	const [showSecondBlock, setShowSecondBlock] = useState(false)
	const [showBoxes, setShowBoxes] = useState(false)
	const [hideBoxes, setHideBoxes] = useState(false)

	const { push } = useRouter()

	const fakeMutation = (data: IAuthForm): Promise<void> => {
		return new Promise((resolve, reject) => {
			setTimeout(() => {
				if (data.email || data.code || data.password) {
					resolve()
				} else {
					reject(new Error('Mutation error'))
				}
			}, 1000)
		})
	}

	const onSubmit: SubmitHandler<IAuthForm> = data => {
		if (step === 1) {
			setEmail(data.email)
		}
		fakeMutation(data)
			.then(() => {
				if (step === 1) {
					setStep(2)
					toast.success('Email sent!')
				} else if (step === 2) {
					setStep(3)
					toast.success('Code verified!')
				} else if (step === 3) {
					setIsModalOpen(true)
					toast.success('Registration complete!')
					// push(DASHBOARD_PAGES.HOME)
				}
			})
			.catch(error => {
				console.error('Error during mutation', error)
				toast.error('An error occurred during the process')
			})
	}

	useEffect(() => {
		if (step === 2 && countdown > 0) {
			const timer = setInterval(() => {
				setCountdown(prev => {
					if (prev === 1) {
						setCanResend(true)
					}
					return prev - 1
				})
			}, 1000)
			return () => clearInterval(timer)
		}
	}, [step, countdown])

	const handleEdit = () => {
		setStep(1)
		setCountdown(60)
		setCanResend(false)
	}

	const handleResend = () => {
		toast.success('Code resent!')
		setCountdown(60)
		setCanResend(false)
	}

	const code = watch('code')
	useEffect(() => {
		if (code && code.length === 4) {
			fakeMutation({ code })
				.then(() => {
					setStep(3)
					toast.success('Code verified!')
				})
				.catch(error => {
					console.error('Error during mutation', error)
					toast.error('An error occurred during the process')
				})

			setShowBoxes(false)
			setHideBoxes(false)
			setShowSecondBlock(false)
		}
	}, [code])

	return (
		<div className='flex min-h-screen font-helvetica'>
			<div className={`flex flex-col items-start space-y-4 mt-28 absolute`}>
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
				className={`bg-sidebar mt-28 ml-[900px] rounded-xl px-8 ${step === 3 ? 'w-[430px] h-[490px]' : 'w-[430px] h-[320px]'} transition-all duration-300`}
				onSubmit={handleSubmit(onSubmit)}
			>
				<div className='flex items-center justify-between mb-6'>
					<div className='flex items-center'>
						<button
							type='button'
							className='flex mt-7 items-center justify-center w-8 h-8 bg-[#f0f4ff] rounded-full hover:bg-gray-300 focus:outline-none transition-colors duration-200'
							onClick={() => push('../register')}
						>
							<img
								src='/chevron-left.png'
								alt='chevron-left.png'
								className='w-4 h-4'
							/>
						</button>
						<Heading
							title='Регистрация'
							className='text-2xl pt-4 ml-4 text-oopgray font-bold'
						/>
					</div>
					<p className='text-gray-300 text-3xl font-bold mt-7'>
						{step === 3 ? '2/2' : '1/2'}
					</p>
				</div>
				{step === 1 && (
					<>
						<p className='text-xs font-bold text-oopgray mb-4'>
							Отправим сообщение с кодом на указанную почту
						</p>
						<Field
							id='email'
							label='Почта'
							placeholder=''
							type='email'
							extra=''
							{...register('email', {
								required: 'Поле обязательно для заполнения!'
							})}
							state={errors.email ? 'error' : undefined}
							errorMessage={isSubmitted ? errors.email?.message : undefined}
						/>
						<div className='flex flex-col items-center gap-4'>
							<Button
								variant='gray'
								className='bg-oopgray mt-6'
							>
								Далее
							</Button>
						</div>
					</>
				)}
				{step === 2 && (
					<>
						<div className='flex justify-between items-center mb-4'>
							<p className='text-xs font-bold text-oopgray'>
								Отправили сообщение с кодом на почту {email}
							</p>
							<button
								type='button'
								className='relative mt-5 text-xs text-hyperlink group'
								onClick={handleEdit}
							>
								Изменить
								<span className='absolute bottom-[-1px] left-0 w-full h-px bg-hyperlink transform scale-x-100 transition-transform duration-300 ease-in-out group-hover:scale-x-0' />
							</button>
						</div>

						<Field
							id='code'
							label='Код'
							placeholder=''
							type='text'
							maxLength={4}
							extra=''
							{...register('code', {
								required: 'Code is required!',
								minLength: {
									value: 4,
									message: ''
								},
								maxLength: {
									value: 4,
									message: ''
								}
							})}
						/>
						{canResend ? (
							<button
								type='button'
								className='relative mt-5 text-xs flex items-center group'
								onClick={handleResend}
							>
								<span className='text-oopgray'>Не пришло сообщение? </span>
								<span className='relative ml-2 text-xs text-hyperlink group'>
									Отправить еще раз
									<span className='absolute bottom-[-1px] left-0 w-full h-px bg-hyperlink transform scale-x-100 transition-transform duration-300 ease-in-out group-hover:scale-x-0' />
								</span>
							</button>
						) : (
							<p className='text-[14.1px] text-oopgray mt-5'>
								Не пришло сообщение? Повторная отправка через {countdown} сек
							</p>
						)}
					</>
				)}
				{step === 3 && (
					<>
						<Field
							id='name'
							label='Имя'
							placeholder='Имя Фамилия'
							type='text'
							extra=''
							{...register('name', {
								required: 'Поле обязательно для заполнения!'
							})}
							state={errors.name ? 'error' : undefined}
							errorMessage={isSubmitted ? errors.name?.message : undefined}
						/>
						<Field
							id='email'
							label='Почта'
							placeholder=''
							type='email'
							extra=''
							{...register('email', {
								required: 'Поле обязательно для заполнения!'
							})}
							state={errors.email ? 'error' : undefined}
							errorMessage={isSubmitted ? errors.email?.message : undefined}
						/>
						<button
							type='button'
							className='absolute ml-[330px] mt-14 z-[1] transform -translate-y-1/2'
							onClick={() => setPasswordVisible(prev => !prev)}
						>
							<img
								src={passwordVisible ? '/eye-off.png' : '/eye.png'}
								alt={passwordVisible ? 'Hide password' : 'Show password'}
								className='w-5 h-5'
							/>
						</button>
						<div className='relative'>
							<Field
								id='password'
								label='Пароль'
								placeholder=''
								type={passwordVisible ? 'text' : 'password'}
								extra=''
								{...register('password', {
									required: 'Минимум 6 символов',
									minLength: {
										value: 6,
										message: 'Минимум 6 символов'
									}
								})}
								state={errors.password ? 'error' : undefined}
								errorMessage={
									isSubmitted ? errors.password?.message : undefined
								}
							/>
						</div>
						<p className='text-[12px] text-oopgray mt-2'>Минимум 6 символов</p>
						<div className='flex flex-col items-center gap-4'>
							<Button
								variant='gray'
								className='bg-oopgray mt-6'
								type='submit'
							>
								Завершить регистрацию
							</Button>
						</div>
					</>
				)}
			</form>

			{/* Заглушка */}
			{isModalOpen && (
				<div className='fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center'>
					<div className='bg-white p-6 rounded-lg shadow-lg'>
						<h2 className='text-xl text-oopgray font-bold'>
							Регистрация завершена
						</h2>
						<p className='mt-2'>Вы успешно зарегистрировались!</p>
						<div className='mt-4 flex justify-end'>
							<Button
								variant='gray'
								className='bg-oopgray'
								onClick={() => setIsModalOpen(false)}
							>
								Закрыть
							</Button>
						</div>
					</div>
				</div>
			)}
		</div>
	)
}
