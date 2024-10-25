import type { Metadata } from 'next'

import { NO_INDEX_PAGE } from '@/constants/seo.constants'

import { Auth } from './Auth'

{
	/* cSpell:ignore Вход */
}

export const metadata: Metadata = {
	title: 'Вход',
	...NO_INDEX_PAGE
}

export default function AuthPage() {
	return <Auth />
}
