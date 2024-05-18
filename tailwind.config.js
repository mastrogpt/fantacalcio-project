/** @type {import('tailwindcss').Config} */

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				// Base colors
				black: '#000000',
				white: '#FFFFFF',
				dark: '#1A263A',
				light: '#FDFDFD',

				// Palette
				primary: '#10987D',
				accent: '#FFD700'
			}
		},
		fontFamily: {
			sans: ['Inter', 'Roboto', 'sans-serif'],
			serif: ['Francois One', 'Roboto Serif', 'serif']
		}
	},
	plugins: []
};
