/** @type {import('next').NextConfig} */
const nextConfig = {
	output: 'standalone',
	images: {
		domains: [
			's3.storage.selcloud.ru',
			'edd89111-ff53-4d6b-a356-5c2505c1ab94.selstorage.ru'
		]
	}
}

export default nextConfig
