export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#edfdf7",
          300: "#73f0c0",
          400: "#2cd59f",
          500: "#14b87e",
          900: "#042f24"
        },
        ink: "#e6edf7",
        panel: "#0f172a"
      },
      fontFamily: {
        sans: ["Manrope", "sans-serif"],
        display: ["Space Grotesk", "sans-serif"]
      },
      boxShadow: {
        panel: "0 24px 80px rgba(15, 23, 42, 0.28)"
      }
    },
  },
  plugins: [],
};
