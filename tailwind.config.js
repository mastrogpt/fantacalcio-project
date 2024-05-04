/** @type {import('tailwindcss').Config} */

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        //text: coal
        'text': '#0a0e15',
        //background: light gray 
        'light': '#fafafa',
        //primary: manticore wing  (similar)
        'primary': '#E18012',
        //secondary: persian green
        'secondary': '#28af60',
        //acceent: casandora yellow 
        'accent': '#feca57'
       },
    },
    fontFamily: {
      'sans': ['Quattrocento Sans', 'Roboto', 'sans-serif'],
      'serif': ['Quattrocento', 'Roboto Serif', 'serif'],
    },
  },
  plugins: []
};
