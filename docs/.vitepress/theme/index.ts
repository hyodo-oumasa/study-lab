// VitePress の標準のテーマを土台にして、このサイト独自の部品を追加する。
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'

import QuizQuestion from './components/QuizQuestion.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // Markdown の中で <QuizQuestion> と書けば使えるようにする
    app.component('QuizQuestion', QuizQuestion)
  },
} satisfies Theme
