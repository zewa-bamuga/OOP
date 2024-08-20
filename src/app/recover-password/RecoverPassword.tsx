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
	/* cSpell:ignore главная клипы проекты Отдел Образовательных Программ Команда призванная побеждать создаём классные проекты обучаем новому саморазвиваемся запомнить меня Вход Регистрация Почта Пароль забыли Отправим сообщение указанную почту пришло Поле обязательно заполнения Восстановление пароля Восстановить Изменить Отправили письмо Отправить Повторная отправка через Минимум символов Завершить регистрацию завершена успешно зарегистрировались Фамилия Закрыть Понятно связаться нами Если возникли сложности можете */
}

export function RecoverPassword() {
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
				className={`bg-sidebar mt-28 ml-[900px] rounded-xl px-8 ${step === 2 ? 'w-[430px] h-[310px]' : 'w-[430px] h-[310px]'} transition-all duration-300`}
				onSubmit={handleSubmit(onSubmit)}
			>
				<div className='flex items-center justify-between mb-6'>
					<div className='flex items-center'>
						<button
							type='button'
							className='flex mt-7 items-center justify-center w-8 h-8 bg-[#f0f4ff] rounded-full hover:bg-gray-300 focus:outline-none transition-colors duration-200'
							onClick={() => push('../auth')}
						>
							<img
								src='/chevron-left.png'
								alt='chevron-left.png'
								className='w-4 h-4'
							/>
						</button>
						<Heading
							title='Восстановление пароля'
							className='text-[25px] pt-4 ml-4 text-oopgray font-bold'
						/>
					</div>
				</div>
				{step === 1 && (
					<>
						<p className='text-xs font-bold text-oopgray mb-4'>
							Отправим сообщение на указанную почту
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
								Восстановить
							</Button>
						</div>
					</>
				)}
				{step === 2 && (
					<>
						<div className='flex justify-between items-center mb-4'>
							<p className='text-xs font-bold text-oopgray'>
								Отправили письмо на {email}
							</p>
							<button
								type='button'
								className='relative mt-5 text-xs text-hyperlink group'
								onClick={handleEdit}
							>
								Изменить
								<span className='underline-span' />
							</button>
						</div>
						<p className='text-xs text-oopgray'>
							Если у вас возникли сложности, вы можете{' '}
							<a
								href='https://vk.com/oop_tusur'
								className='relative text-hyperlink'
								target='_blank'
								rel='noopener noreferrer'
							>
								связаться с нами
							</a>
						</p>

						<div className='flex flex-col items-center gap-4'>
							<Button
								variant='gray'
								className='bg-oopgray mt-[43px]'
								type='submit'
								onClick={() => push('../auth')}
							>
								Понятно
							</Button>
						</div>
					</>
				)}
			</form>
		</div>
	)
}
