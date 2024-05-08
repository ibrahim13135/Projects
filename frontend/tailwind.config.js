/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{html,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e3f2fd',  // Light shade of primary
          100: '#bbdefb',
          200: '#90caf9',
          300: '#64b5f6',
          400: '#42a5f5',
          500: '#2196f3',  // Base primary color (e.g., blue)
          600: '#1e88e5',
          700: '#1976d2',
          800: '#1565c0',
          900: '#0d47a1',  // Darkest shade
        },
        secondary: {
          50: '#fbe9e7',  // Light shade of secondary
          100: '#ffccbc',
          200: '#ffab91',
          300: '#ff8a65',
          400: '#ff7043',
          500: '#ff5722',  // Base secondary color (e.g., orange-red)
          600: '#f4511e',
          700: '#e64a19',
          800: '#d84315',
          900: '#bf360c',  // Darkest shade
        },
      },
    },
  },
  plugins: [],
}

