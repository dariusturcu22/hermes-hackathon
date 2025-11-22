import type { Config } from "tailwindcss";

export default {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#0096C7",
        secondary: "#0077B6",
        accent: "#00B4D8",
        background: "#CAF0F8",
        dark_background: "#03045E",
        medium_dark_background: "#023E8A",
        light_background_for_event_card: "#ADE8F4",
        medium_background_for_event_card: "#90E0EF",
        vibrant_background_for_event_card: "#48CAE4",
        card: "#CAF0F8",
      }
    }
  },
  plugins: [],
} satisfies Config;
