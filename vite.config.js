import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		port: 8080,
		proxy: {
			"/api/my": {
				target: process.env.NUVDEV_HOST,
				changeOrigin: true
			}
		}
	}
})
