<script setup lang="ts">
// トップページの「ノートの棚」。テーマごとのノートを背表紙として並べ、
// 書いたページの数に応じて、背表紙を厚くする。
// ページの数は、docs/<テーマ>/ の中の Markdown（index.md を除く）を数えて求める。
import { withBase } from 'vitepress'

const pages = Object.keys(import.meta.glob('../../../*/*.md'))

type Notebook = { dir: string; title: string; total?: number }

// total は、テーマのトップページで予定しているページの数。決めていないテーマは書かない。
const notebooks: Notebook[] = [
  { dir: 'claude-code', title: 'Claude Code', total: 20 },
  { dir: 'claude-cert', title: 'Claude 認定資格' },
  { dir: 'gh-300', title: 'GH-300', total: 21 },
  { dir: 'cicd', title: 'CI/CD' },
  { dir: 'stats-2', title: '統計検定2級' },
  { dir: 'vue', title: 'Vue' },
  { dir: 'python-libs', title: 'Python ライブラリ' },
]

function countPages(dir: string): number {
  return pages.filter((p) => p.includes(`/${dir}/`) && !p.endsWith('/index.md')).length
}

const shelf = notebooks.map((n) => {
  const count = countPages(n.dir)
  return {
    ...n,
    count,
    // 0 ページでも背表紙が見えるように、最低の厚さを持たせる
    width: `${2.2 + Math.min(count, 20) * 0.32}rem`,
    label: n.total ? `${count} / ${n.total}` : `${count}`,
  }
})
</script>

<template>
  <section class="shelf-hero">
    <h1 class="shelf-title">study-lab</h1>
    <p class="shelf-lead">試しながら書き足していく、学習ノート</p>
  </section>

  <section class="shelf" aria-labelledby="shelf-heading">
    <h2 id="shelf-heading" class="shelf-heading">ノートの棚</h2>
    <ul class="shelf-row">
      <li v-for="n in shelf" :key="n.dir">
        <a
          class="spine"
          :class="{ 'spine--empty': n.count === 0 }"
          :href="withBase(`/${n.dir}/`)"
          :style="{ minWidth: n.width }"
        >
          <span class="spine-title">{{ n.title }}</span>
          <span class="spine-count">{{ n.label }}</span>
        </a>
      </li>
    </ul>
    <p class="shelf-note">背表紙の厚さは、書いたページの数です。</p>
  </section>
</template>
