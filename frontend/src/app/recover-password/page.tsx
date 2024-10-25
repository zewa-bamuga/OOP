import type { Metadata } from 'next'

import { NO_INDEX_PAGE } from '@/constants/seo.constants'

import { RecoverPassword } from './RecoverPassword'

{
	/* cSpell:ignore Восстановление пароля */
}

export const metadata: Metadata = {
	title: 'Восстановление пароля',
	...NO_INDEX_PAGE
}

export default function AuthPage() {
	return <RecoverPassword />
}
