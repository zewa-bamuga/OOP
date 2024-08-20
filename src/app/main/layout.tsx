import type { PropsWithChildren } from 'react'

import MainLayout from '@/components/main-layout/MainLayout'

export default function Layout({ children }: PropsWithChildren<unknown>) {
	return <MainLayout>{children}</MainLayout>
}
