import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/kit/vite';


/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			fallback: "index.html",
			pages: "web",
			assets: "web",
			precompress: false,
			strict: true
		}),
		files: {
			assets: "web"
		}
	},
  	preprocess: vitePreprocess()
};
export default config;
