import cn from 'clsx'
import type { ButtonHTMLAttributes, PropsWithChildren } from 'react'

type TypeButton = ButtonHTMLAttributes<HTMLButtonElement> & {
	variant?: 'default' | 'blue' | 'gray'
	active?: boolean
}

export function Button({
	children,
	className,
	variant = 'default',
	active = false,
	...rest
}: PropsWithChildren<TypeButton>) {
	return (
		<button
			className={cn(
				'linear rounded-lg border-primary w-full h-full text-lg font-medium text-white transition p-3',
				{
					'bg-oopgray hover:bg-oopgrayhover': variant === 'gray',
					'bg-oopblue hover:bg-blue-700': variant === 'blue' && !active,
					'bg-blue-300 hover:bg-blue-400 active:bg-blue-500':
						variant === 'blue' && active
				},
				className
			)}
			{...rest}
		>
			{children}
		</button>
	)
}
