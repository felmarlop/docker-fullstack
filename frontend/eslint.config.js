import { defineConfig, globalIgnores } from 'eslint/config'
import js from '@eslint/js'
import globals from 'globals'
import pluginVue from 'eslint-plugin-vue'
import skipFormatting from 'eslint-config-prettier/flat'

export default defineConfig([
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,mjs,cjs,vue}'],
  },

  globalIgnores([
    '**/dist/**',
    '**/dist-ssr/**',
    '**/coverage/**',
    '**/node_modules/**',
    '**/.pnpm-store/**',
    '**/.vite/**',
    '**/.vite-temp/**',
  ]),

  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',

      globals: {
        ...globals.browser,
      },
    },
  },

  // JavaScript
  js.configs.recommended,

  // Vue
  ...pluginVue.configs['flat/recommended'],

  // Project rules
  {
    rules: {
      'no-console': 'warn',
      'no-debugger': 'warn',

      // We prefer App.vue, Home.vue, etc.
      'vue/multi-word-component-names': 'off',
    },
  },

  // Prettier owns formatting
  skipFormatting,
])
