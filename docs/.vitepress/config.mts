import { defineConfig } from 'vitepress'

// GitHub Pages では https://hyodo-oumasa.github.io/study-lab/ で公開されるため、
// サイトのルートを repo 名のサブパスに合わせる。
export default defineConfig({
  base: '/study-lab/',
  lang: 'ja-JP',
  title: 'study-lab',
  description: '個人の勉強で得た知見をまとめる学習ナレッジサイト',
  lastUpdated: true,

  themeConfig: {
    nav: [
      { text: 'ホーム', link: '/' },
      { text: 'GH-300', link: '/gh-300/' },
      { text: '統計検定2級', link: '/stats-2/' },
      { text: 'MCP', link: '/mcp/' },
      { text: 'Vue', link: '/vue/' },
      { text: 'Python ライブラリ', link: '/python-libs/' },
      { text: 'CI/CD', link: '/cicd/' },
    ],

    sidebar: [
      {
        text: 'テーマ',
        items: [
          { text: 'GH-300（GitHub Copilot）', link: '/gh-300/' },
          { text: '統計検定2級', link: '/stats-2/' },
          { text: 'MCP', link: '/mcp/' },
          { text: 'Vue', link: '/vue/' },
          { text: 'Python ライブラリ', link: '/python-libs/' },
        ],
      },
      {
        text: 'GitHub Actions / CI/CD',
        items: [
          { text: '概要', link: '/cicd/' },
          { text: 'このサイトが公開されるまで', link: '/cicd/pages-deploy' },
          { text: 'Dependabot を導入して脆弱性を直すまで', link: '/cicd/dependabot' },
          { text: 'ブランチ保護（ルールセット）で main を守る', link: '/cicd/branch-protection' },
          { text: 'PR の承認の仕組みと、AI が作る PR', link: '/cicd/pr-approval-and-ai' },
          { text: 'Python のテストと lint を CI で自動実行する', link: '/cicd/python-ci' },
          { text: '通信するプログラムを、テストしやすく作る', link: '/cicd/testable-python' },
        ],
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/hyodo-oumasa/study-lab' },
    ],

    search: {
      provider: 'local',
    },

    outline: {
      label: 'このページの内容',
    },
    docFooter: {
      prev: '前のページ',
      next: '次のページ',
    },
    lastUpdated: {
      text: '最終更新',
    },
  },
})
