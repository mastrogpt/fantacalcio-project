/** @type {import('tailwindcss').Config} */

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        primary: "#1b81a5",
        secondary: "#ffa944",
        light:"#5aaadb"
      },
    },
  },
  plugins: []
};
