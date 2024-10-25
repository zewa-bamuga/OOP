import type { Metadata } from 'next'

import { NO_INDEX_PAGE } from '@/constants/seo.constants'

import { Clips } from './Clips'

export const metadata: Metadata = {
	title: 'Клипы',
	...NO_INDEX_PAGE
}

export default function ProjectsPage() {
	return <Clips />
}
