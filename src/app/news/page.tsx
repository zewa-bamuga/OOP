import type { Metadata } from 'next'

import { NO_INDEX_PAGE } from '@/constants/seo.constants'

import { News } from './News'

export const metadata: Metadata = {
	title: 'Новости',
	...NO_INDEX_PAGE
}

export default function NewsPage() {
	return <News />
}
