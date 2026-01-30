/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    // PINDAHKAN FONT FAMILY KE SINI
    fontFamily: { 
      'mono-plex': ['"IBM Plex Mono"', 'monospace'],
      'italiana': ['"Italiana"', 'serif'],
      'linden': ['"Linden Hill"', 'serif'],
      'piazzolla': ['"Piazzolla"', 'serif'],
      'sans': ['ui-sans-serif', 'system-ui'], // Opsi: Tambahkan ini jika font default lain hilang
    },
    extend: {
      // Biarkan extend kosong atau untuk kustomisasi lain saja
    },
  },
  plugins: [],
}
