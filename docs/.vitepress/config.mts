import { defineConfig } from 'vitepress'

// GitHub Pages では https://hyodo-oumasa.github.io/study-lab/ で公開されるため、
// サイトのルートを repo 名のサブパスに合わせる。
export default defineConfig({
  base: '/study-lab/',
  lang: 'ja-JP',
  title: 'study-lab',
  description: '個人の勉強で得た知見をまとめる学習ナレッジサイト',
  lastUpdated: true,

  // トップページの「ノートの棚」で使う書体（本文：BIZ UDPゴシック、見出し：Klee One）
  head: [
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    [
      'link',
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&family=Klee+One:wght@600&display=swap',
      },
    ],
  ],

  themeConfig: {
    nav: [
      { text: 'ホーム', link: '/' },
      { text: 'GH-300', link: '/gh-300/' },
      { text: '統計検定2級', link: '/stats-2/' },
      { text: 'Claude Code', link: '/claude-code/' },
      { text: 'Claude 認定資格', link: '/claude-cert/' },
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
          { text: 'Claude Code', link: '/claude-code/' },
          { text: 'Claude 認定資格', link: '/claude-cert/' },
          { text: 'Vue', link: '/vue/' },
          { text: 'Python ライブラリ', link: '/python-libs/' },
        ],
      },
      {
        text: 'GH-300（GitHub Copilot）',
        items: [
          { text: '概要とページの一覧', link: '/gh-300/' },
          { text: '03. 責任ある AI の 6 つの原則', link: '/gh-300/03-responsible-ai-principles' },
          { text: '10. プロンプトエンジニアリングの基本', link: '/gh-300/10-prompt-engineering-basics' },
          { text: '12. GitHub Copilot の仕組みとデータフロー', link: '/gh-300/12-copilot-data-flow' },
          { text: '13. GitHub Copilot のプライバシーとデータ保護', link: '/gh-300/13-privacy-and-content-exclusion' },
          { text: '14. 生成コードの著作権と安全対策', link: '/gh-300/14-ip-and-safeguards' },
        ],
      },
      {
        text: 'Claude Code',
        items: [
          { text: '概要とページの一覧', link: '/claude-code/' },
          { text: '01. Claude Code とは何か', link: '/claude-code/01-what-is-claude-code' },
          { text: '02. Claude Code を使う場所', link: '/claude-code/02-where-to-use' },
          { text: '03. 権限モードと、確認を減らす方法', link: '/claude-code/03-permission-modes' },
          { text: '04. 設定ファイルの仕組み', link: '/claude-code/04-settings-files' },
          { text: '05. CLAUDE.md とメモリ', link: '/claude-code/05-claude-md-and-memory' },
          { text: '06. Skills', link: '/claude-code/06-skills' },
          { text: '07. MCP とコネクター', link: '/claude-code/07-mcp-and-connectors' },
          { text: '08. MCP サーバーを自作する', link: '/claude-code/08-build-an-mcp-server' },
          { text: '09. Hooks', link: '/claude-code/09-hooks' },
          { text: '10. Plugins と「カスタマイズ」', link: '/claude-code/10-plugins' },
          { text: '11. Artifacts', link: '/claude-code/11-artifacts' },
        ],
      },
      {
        text: 'Claude 認定資格',
        items: [
          { text: '概要と学習計画', link: '/claude-cert/' },
          { text: 'Architect 分野 3：Claude Code の設定と使い方', link: '/claude-cert/architect-3-claude-code' },
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
