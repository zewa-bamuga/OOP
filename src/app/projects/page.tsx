import type { Metadata } from 'next'

import { NO_INDEX_PAGE } from '@/constants/seo.constants'

import { Projects } from './Projects'

export const metadata: Metadata = {
	title: 'Проекты',
	...NO_INDEX_PAGE
}

export default function MainPage() {
	return <Projects />
}
