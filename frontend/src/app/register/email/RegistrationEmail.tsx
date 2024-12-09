'use client'

import {useRouter} from 'next/navigation'
import {useEffect, useState} from 'react'
import {SubmitHandler, useForm, useFormState} from 'react-hook-form'
import {toast} from 'sonner'

import {Heading} from '@/components/ui/Heading'
import {Button} from '@/components/ui/buttons/Button'
import {Field} from '@/components/ui/fields/Field'

import {IRegForm} from '@/types/auth.types'

import {registerService} from '@/services/register.service'

export function RegByEmail() {
    const {register, handleSubmit, reset, watch, control, setValue} =
        useForm<IRegForm>({
            mode: 'onSubmit'
        })
    const {errors, isSubmitted} = useFormState({control})

    const [step, setStep] = useState(1)
    const [email, setEmail] = useState('')
    const [countdown, setCountdown] = useState(60)
    const [canResend, setCanResend] = useState(false)
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [passwordVisible, setPasswordVisible] = useState(false)

    const {push} = useRouter()

    const onSubmit: SubmitHandler<IRegForm> = async data => {
        if (step === 1) {
            setEmail(data.email)
            try {
                const response = await registerService.verification_email_request({
                    email: data.email
                })
                if (response.status === 200) {
                    setStep(2)
                    toast.success('Email sent!')
                } else {
                    toast.error('Failed to send email.')
                }
            } catch (error) {
                toast.error('An error occurred during the process')
                console.error('Error during email submission', error)
            }
        } else if (step === 2) {
            try {
                const response = await registerService.verification_email_confirm({
                    email: email,
                    code: data.code
                })
                if (response.status === 200) {
                    setStep(3)
                    toast.success('Code verified!')
                } else {
                    toast.error('Failed to verify code.')
                }
            } catch (error) {
                toast.error('An error occurred during the process')
                console.error('Error during code verification', error)
            }
        } else if (step === 3) {
            try {
                const response = await registerService.main({
                    firstname: data.firstname,
                    lastname: data.lastname,
                    email: data.email,
                    password: data.password
                })
                if (response.status === 200) {
                    toast.success('Registration completed!')
                    toast.success('Successfully login!')
                    reset()
                    push('../auth')
                } else {
                    toast.error('Failed to complete registration.')
                }
            } catch (error) {
                toast.error('An error occurred during the process')
                console.error('Error during registration', error)
            }
        }
    }

    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const [firstname, ...lastnameArray] = e.target.value.split(' ')
        const lastname = lastnameArray.join(' ')
        setValue('firstname', firstname || '')
        setValue('lastname', lastname || '')
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

    const handleResend = async () => {
        try {
            await registerService.verification_email_request({email})
            setCountdown(60)
            setCanResend(false)
            toast.success('Code resent!')
        } catch (error) {
            toast.error('An error occurred during the process')
            console.error('Error during code resend', error)
        }
    }

    const code = watch('code')
    useEffect(() => {
        if (code && code.length === 4) {
            // Эта часть может быть удалена, так как код будет подтвержден в `onSubmit`
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
                    style={{paddingLeft: '200px', marginLeft: '-20px', zIndex: 1}}
                >
                    клипы
                </button>
                <button
                    className={`promo-box bg-oopblue w-[320px] h-[35px] rounded-r-full flex items-center`}
                    style={{paddingLeft: '200px', marginLeft: '-20px', zIndex: 1}}
                >
                    проекты
                </button>
            </div>

            <div
                className='absolute mt-[110px]'
                style={{color: '#323232', paddingLeft: '350px'}}
            >
                <div className='text-left flex items-start'>
                    <img
                        src='/logo.png'
                        alt='logo.png'
                        className='w-[70px] h-[70px]'
                    />
                    <p
                        className='ml-3 text-lg font-light mb-1 leading-6'
                        style={{fontFamily: 'Helvetica', fontWeight: 300}}
                    >
                        Отдел
                        <br/>
                        Образовательных
                        <br/>
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
                            Команда, <br/>
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
                className={`bg-sidebar mt-28 ml-[900px] rounded-xl px-8 ${step === 3 ? 'w-[430px] h-[540px]' : 'w-[430px] h-[320px]'} transition-all duration-300`}
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
                            {' '}
                            <p className='text-xs font-bold text-oopgray'>
                                Отправили сообщение с кодом на почту {email}
                            </p>
                            <button
                                type='button'
                                className='relative mt-5 text-xs text-hyperlink group'
                                onClick={handleEdit}
                            >
                                Изменить
                                <span
                                    className='absolute bottom-[-1px] left-0 w-full h-px bg-hyperlink transform scale-x-100 transition-transform duration-300 ease-in-out group-hover:scale-x-0'/>
                            </button>
                        </div>
                        <Field
                            id='code'
                            label='Код'
                            placeholder=''
                            type='text'
                            extra='Укажите код из письма'
                            maxLength={4}
                            {...register('code', {
                                required: 'Поле обязательно для заполнения!'
                            })}
                            state={errors.code ? 'error' : undefined}
                            errorMessage={isSubmitted ? errors.code?.message : undefined}
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
									<span
                                        className='absolute bottom-[-1px] left-0 w-full h-px bg-hyperlink transform scale-x-100 transition-transform duration-300 ease-in-out group-hover:scale-x-0'/>
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
                        <p className='text-xs font-bold text-oopgray mb-4'>
                            Почта и пароль понадобятся для входа на сайт
                        </p>
                        <Field
                            id='name'
                            label='Как тебя зовут'
                            placeholder='Имя Фамилия'
                            type='text'
                            extra=''
                            onChange={handleNameChange}  // Обработчик для изменения
                            state={errors.firstname || errors.lastname ? 'error' : undefined}
                            errorMessage={
                                isSubmitted
                                    ? `${errors.firstname?.message} ${errors.lastname?.message}`
                                    : undefined
                            }
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
                        <Field
                            id="password"
                            label="Пароль"
                            placeholder=""
                            type={passwordVisible ? "text" : "password"}
                            extra={
                                <button
                                    type="button"
                                    className="text-gray-500"
                                    onClick={() => setPasswordVisible(!passwordVisible)}
                                >
                                    {passwordVisible ? "Скрыть" : "Показать"}
                                </button>
                            }
                            {...register("password", {
                                required: "Поле обязательно для заполнения!",
                                minLength: {
                                    value: 6,
                                    message: "Пароль должен содержать как минимум 6 символов",
                                },
                            })}
                            state={errors.password ? "error" : undefined}
                            errorMessage={isSubmitted ? errors.password?.message : undefined}
                        />

                        <p className='text-[12px] text-oopgray mt-2'>Минимум 6 символов</p>
                        <div className='flex flex-col items-center gap-4'>
                            <Button
                                variant='gray'
                                className='bg-oopgray mt-5'
                            >
                                Завершить регистрацию
                            </Button>
                        </div>
                    </>
                )}
            </form>
        </div>
    )
}
