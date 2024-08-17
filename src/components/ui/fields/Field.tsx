import { forwardRef } from 'react'

interface InputFieldProps {
	id: string
	label: string
	extra?: string
	placeholder?: string
	variant?: string
	state?: 'error' | 'success'
	disabled?: boolean
	type?: string
	isNumber?: boolean
	errorMessage?: string
}

export const Field = forwardRef<HTMLInputElement, InputFieldProps>(
	(
		{
			label,
			id,
			extra,
			type,
			placeholder,
			state,
			disabled,
			isNumber,
			errorMessage,
			...rest
		},
		ref
	) => {
		return (
			<div className={`${extra} mb-3 relative`}>
				<label
					htmlFor={id}
					className={`text-xs text-white/60 dark:text-white font-medium`}
					style={{ color: '#323232' }}
				>
					{label}
				</label>
				<input
					ref={ref}
					disabled={disabled}
					type={type}
					id={id}
					className={`flex w-full items-center justify-center rounded-lg border border-border bg-[#DDE2F2] p-3 text-base outline-none duration-500 transition-colors focus:border-primary ${
						disabled
							? '!border-none !bg-gray-100 dark:!bg-white/5 dark:placeholder:!text-[rgba(255,255,255,0.15)]'
							: state === 'error'
								? 'border-red-500 text-red-500 placeholder:text-red-500 dark:!border-red-400 dark:!text-red-400 dark:placeholder:!text-red-400'
								: state === 'success'
									? 'border-green-500 text-green-500 placeholder:text-green-500 dark:!border-green-400 dark:!text-green-400 dark:placeholder:!text-green-400'
									: ''
					}`}
					placeholder={placeholder}
					style={{ color: '#323232' }}
					onKeyDown={event => {
						if (
							isNumber &&
							!/^[0-9]*$/.test(event.key) &&
							event.key !== 'Backspace' &&
							event.key !== 'Tab' &&
							event.key !== 'Enter' &&
							event.key !== 'ArrowLeft' &&
							event.key !== 'ArrowRight'
						) {
							event.preventDefault()
						}
					}}
					{...rest}
				/>
				{state === 'error' && errorMessage && (
					<div className='absolute right-0  flex items-center'>
						<div className='bg-red-500 -mt-28 text-white text-xs rounded-lg py-1 px-2'>
							{errorMessage}
						</div>
					</div>
				)}
			</div>
		)
	}
)

Field.displayName = 'field'
