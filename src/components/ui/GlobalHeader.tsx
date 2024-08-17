interface IHeading {
	title: string
	isButton?: boolean
	onClick?: () => void
	className?: string
}

export function GlobalHeader({
	title,
	isButton = false,
	onClick,
	className = ''
}: IHeading) {
	const Tag = isButton ? 'button' : 'h1'

	return (
		<Tag
			className={`relative text-center text-white text-5xl font-bold ${className} ${isButton ? 'group' : ''}`}
			onClick={isButton ? onClick : undefined}
		>
			{title}
			{isButton && (
				<span className='absolute bottom-[-2px] left-0 w-full h-0.5 bg-gray-500 transform scale-x-100 transition-transform duration-300 ease-in-out group-hover:scale-x-0' />
			)}
		</Tag>
	)
}
