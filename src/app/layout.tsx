import type { Metadata } from "next"
import { Lato } from "next/font/google"
import { Toaster } from 'sonner'

import { SITE_NAME } from '@/constants/seo.constants'

import "./globals.scss"
import { Providers } from './providers'

const lato = Lato({
	subsets: ['latin'],
	weight: ['300', '400', '700'],
	display: 'swap',
	variable: '--font-lato',
	style: ['normal']
});

export const metadata: Metadata = {
	title: {
		default: SITE_NAME,
		template: `%s | ${SITE_NAME}`
	},
	description: 'Website for Student Department of Educational Programs'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
		<html lang='en'>
			<body className={lato.className}>
				<Providers>
					{children}

					<Toaster
						theme='dark'
						position='bottom-right'
						duration={1500}
					/>
				</Providers>
			</body>
		</html>
  );
}
