/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Existing
        sans: ['Geist', 'sans-serif'],
        
        // New
        body: ['Inter', 'sans-serif'],
        display: ['"DM Serif Display"', 'serif'],
        typewriter: ['"Special Elite"', 'serif'],
        poster: ['"Bebas Neue"', 'sans-serif'],
      },
      colors: {
        wandor: {
          // Existing keys from Hero.tsx
          dark: '#0a0a0a',
          text: '#1a1a1a',
          muted: '#767676',
          prompt: '#905831',

          // New design system keys
          bg: '#F7F3EA',
          card: '#FBF8F1',
          'text-primary': '#111111',
          'text-secondary': '#6F6A62',
          'text-muted': '#8A847A',
          border: '#D8D1C5',
          'border-light': '#E7E1D7',
          terracotta: '#A85D3B',
          orange: '#B86B47',
          olive: '#77745A',
          'olive-dark': '#55543F',
          brown: '#514133',
          'brown-light': '#92745B',
          'illu-cream': '#E8DDC7',
        },
      },
    },
  },
  plugins: [],
}
