const { heroui } = require('@heroui/react')

module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        nebula: {
          purple: '#7c3aed',
          gold: '#FFD34E',
          black: '#0b0b0e',
        },
      },
      backgroundColor: {
        black: '#0b0b0e',
      },
    },
  },
  plugins: [
    heroui({
      themes: {
        dark: {
          colors: {
            primary: '#7c3aed',
            warning: '#FFD34E',
            background: '#0b0b0e',
            foreground: '#f8fafc',
          },
        },
      },
    }),
  ],
}