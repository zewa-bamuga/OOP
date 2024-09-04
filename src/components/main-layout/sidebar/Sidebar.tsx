'use client'

import { useRouter } from 'next/navigation'

export function Sidebar() {
	const { push } = useRouter()

	return (
		<div
			className={`absolute flex flex-col items-start space-y-4 mt-[92px] left-0 top-0 h-full w-[320px]`}
		>
			<button
				className={`promo-box bg-oopyellow w-[320px] h-[35px] rounded-r-full flex items-center`}
				style={{
					color: '#323232',
					paddingLeft: '200px',
					marginLeft: '-20px',
					zIndex: 1
				}}
				onClick={() => push('../')}
			>
				главная
			</button>
			<button
				className={`promo-box bg-oopgray w-[320px] h-[35px] rounded-r-full flex items-center`}
				style={{ paddingLeft: '200px', marginLeft: '-20px', zIndex: 1 }}
				onClick={() => push('./clips')}
			>
				клипы
			</button>
			<button
				className={`promo-box bg-oopblue w-[320px] h-[35px] rounded-r-full flex items-center`}
				style={{ paddingLeft: '200px', marginLeft: '-20px', zIndex: 1 }}
				onClick={() => push('./projects')}
			>
				проекты
			</button>
		</div>
	)
}
