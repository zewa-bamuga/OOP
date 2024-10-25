const Checkbox = (props: {
	id?: string
	extra?: string
	color?:
		| 'red'
		| 'blue'
		| 'green'
		| 'yellow'
		| 'orange'
		| 'teal'
		| 'navy'
		| 'lime'
		| 'cyan'
		| 'pink'
		| 'purple'
		| 'amber'
		| 'indigo'
		| 'gray'
	[x: string]: any
}) => {
	const { extra, color, id, ...rest } = props
	return (
		<input
			id={id}
			type='checkbox'
			className={`defaultCheckbox relative inline-flex h-[20px] min-h-[20px] w-[20px] min-w-[20px] appearance-none items-center
							justify-center rounded-md border border-black text-white/0 outline-none transition ease-linear
							checked:bg-blue checked:border-blue hover:cursor-pointer dark:border-black ${extra}`}
			name='weekly'
			{...rest}
		/>
	)
}

export default Checkbox
