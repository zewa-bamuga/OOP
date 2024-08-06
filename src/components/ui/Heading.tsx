interface IHeading {
	title: string
	isButton?: boolean
	onClick?: () => void
	className?: string
}

export function Heading({
	title,
	isButton = false,
	onClick,
	className = ''
}: IHeading) {
	const Tag = isButton ? 'button' : 'h1'

	return (
		<Tag
			className={`relative pt-6 px-3 text-2xl font-bold font-helvetica ${className} ${isButton ? 'group' : ''}`}
			onClick={isButton ? onClick : undefined}
		>
			{title}
			{isButton && (
				<span className='absolute bottom-[-2px] left-0 w-full h-0.5 bg-gray-500 transform scale-x-100 transition-transform duration-300 ease-in-out group-hover:scale-x-0' />
			)}
		</Tag>
	)
}
