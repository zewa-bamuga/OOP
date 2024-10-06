import type { Metadata } from 'next'

import { NO_INDEX_PAGE } from '@/constants/seo.constants'

import { Admin } from './Admin'

{
	/* cSpell:ignore Вход */
}

export const metadata: Metadata = {
	title: 'Администраторская панель',
	...NO_INDEX_PAGE
}

export default function AdminPage() {
	return <Admin />
}
