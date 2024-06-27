/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      boxShadow: {
        'glass': '0 0 5px 2px rgba(0, 0, 0, .2)',
      },
    },
  },
  plugins: [],
}

