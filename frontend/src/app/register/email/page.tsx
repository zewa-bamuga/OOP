import type { Metadata } from 'next'

import { NO_INDEX_PAGE } from '@/constants/seo.constants'

import { RegByEmail } from './RegistrationEmail'

{
	/* cSpell:ignore Регистрация */
}

export const metadata: Metadata = {
	title: 'Регистрация',
	...NO_INDEX_PAGE
}

export default function AuthPage() {
	return <RegByEmail />
}
