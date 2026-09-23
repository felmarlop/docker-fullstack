import indigo from './colors/indigo'
import emerald from './colors/emerald'
import slate from './colors/slate'
import obsidian from './colors/obsidian'

export default {
  defaultTheme: 'obsidian',

  themes: {
    indigo: {
      dark: false,
      colors: indigo,
    },

    emerald: {
      dark: false,
      colors: emerald,
    },

    slate: {
      dark: false,
      colors: slate,
    },

    obsidian: {
      dark: true,
      colors: obsidian,
    },
  },
}
