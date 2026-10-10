<script setup lang="ts">
// 確認問題を 1 問表示する部品。
// 選択肢を選んで「答えを確認する」を押すまで、正解と解説は表示しない。
// 正解が 1 つなら 4 択（ラジオボタン）、2 つ以上なら複数選択（チェックボックス）になる。
import { computed, ref, useId } from 'vue'

const props = defineProps<{
  /** 問題の番号（「問 1」の 1） */
  number: number
  /** 問題文 */
  question: string
  /** 選択肢。上から順に A, B, C, ... のラベルが付く */
  choices: string[]
  /** 正解のラベル。複数ある場合はカンマで区切る（例: "B" / "A,C"） */
  answer: string
  /** 選び方の案内。省略すると「1 つ選んでください」などを自動で表示する */
  hint?: string
}>()

const LABELS = 'ABCDEFGH'
const groupId = useId()

const correctLabels = computed(() =>
  props.answer
    .split(',')
    .map((label) => label.trim().toUpperCase())
    .filter(Boolean)
    .sort(),
)
const isMultiple = computed(() => correctLabels.value.length > 1)
const hintText = computed(
  () => props.hint ?? `${correctLabels.value.length} つ選んでください`,
)

const selected = ref<string[]>([])
const checked = ref(false)

const isCorrect = computed(
  () => [...selected.value].sort().join(',') === correctLabels.value.join(','),
)

function toggle(label: string) {
  if (checked.value) return
  if (isMultiple.value) {
    selected.value = selected.value.includes(label)
      ? selected.value.filter((l) => l !== label)
      : [...selected.value, label]
  } else {
    selected.value = [label]
  }
}

function reset() {
  selected.value = []
  checked.value = false
}

/** 答えを確認したあとの、選択肢ごとの状態 */
function stateOf(label: string): 'correct' | 'wrong' | 'none' {
  if (!checked.value) return 'none'
  if (correctLabels.value.includes(label)) return 'correct'
  return selected.value.includes(label) ? 'wrong' : 'none'
}
</script>

<template>
  <div class="quiz">
    <fieldset class="quiz-fieldset">
      <legend class="quiz-question">
        <span class="quiz-number">問 {{ number }}.</span>
        {{ question }}
        <span class="quiz-hint">（{{ hintText }}）</span>
      </legend>

      <label
        v-for="(choice, index) in choices"
        :key="index"
        class="quiz-choice"
        :class="[`is-${stateOf(LABELS[index])}`, { 'is-selected': selected.includes(LABELS[index]) }]"
      >
        <input
          :type="isMultiple ? 'checkbox' : 'radio'"
          :name="groupId"
          :checked="selected.includes(LABELS[index])"
          :disabled="checked"
          @change="toggle(LABELS[index])"
        />
        <span class="quiz-label">{{ LABELS[index] }}.</span>
        <span class="quiz-text">{{ choice }}</span>
        <span v-if="stateOf(LABELS[index]) === 'correct'" class="quiz-mark">正解</span>
        <span v-else-if="stateOf(LABELS[index]) === 'wrong'" class="quiz-mark">不正解</span>
      </label>
    </fieldset>

    <div class="quiz-actions">
      <button
        v-if="!checked"
        type="button"
        class="quiz-button"
        :disabled="selected.length === 0"
        @click="checked = true"
      >
        答えを確認する
      </button>
      <button v-else type="button" class="quiz-button is-secondary" @click="reset">
        もう一度解く
      </button>
    </div>

    <div class="quiz-result" aria-live="polite">
      <template v-if="checked">
        <p class="quiz-verdict" :class="isCorrect ? 'is-correct' : 'is-wrong'">
          {{ isCorrect ? '○ 正解です' : '× 不正解です' }}
          <span class="quiz-answer">正解：{{ correctLabels.join('、') }}</span>
        </p>
        <div class="quiz-explanation">
          <slot />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.quiz {
  margin: 24px 0;
  padding: 16px 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background-color: var(--vp-c-bg-soft);
}

.quiz-fieldset {
  margin: 0;
  padding: 0;
  border: 0;
}

.quiz-question {
  padding: 0;
  margin-bottom: 12px;
  font-weight: 600;
  line-height: 1.7;
}

.quiz-number {
  margin-right: 4px;
}

.quiz-hint {
  display: inline-block;
  font-weight: 700;
  text-decoration: underline;
  text-underline-offset: 4px;
}

.quiz-choice {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin: 8px 0;
  padding: 8px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background-color: var(--vp-c-bg);
  line-height: 1.6;
  cursor: pointer;
}

.quiz-choice.is-selected {
  border-color: var(--vp-c-brand-1);
}

.quiz-choice.is-correct {
  border-color: var(--vp-c-success-1);
  background-color: var(--vp-c-success-soft);
}

.quiz-choice.is-wrong {
  border-color: var(--vp-c-danger-1);
  background-color: var(--vp-c-danger-soft);
}

.quiz-choice input {
  flex-shrink: 0;
  transform: translateY(1px);
}

.quiz-label {
  flex-shrink: 0;
  font-weight: 600;
}

.quiz-text {
  flex-grow: 1;
}

.quiz-mark {
  flex-shrink: 0;
  font-size: 0.85em;
  font-weight: 600;
}

.quiz-choice.is-correct .quiz-mark {
  color: var(--vp-c-success-1);
}

.quiz-choice.is-wrong .quiz-mark {
  color: var(--vp-c-danger-1);
}

.quiz-actions {
  margin-top: 12px;
}

.quiz-button {
  padding: 6px 16px;
  border: 1px solid var(--vp-button-brand-border);
  border-radius: 20px;
  color: var(--vp-button-brand-text);
  background-color: var(--vp-button-brand-bg);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.quiz-button:hover:not(:disabled) {
  background-color: var(--vp-button-brand-hover-bg);
}

.quiz-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quiz-button.is-secondary {
  border-color: var(--vp-button-alt-border);
  color: var(--vp-button-alt-text);
  background-color: var(--vp-button-alt-bg);
}

.quiz-button.is-secondary:hover {
  background-color: var(--vp-button-alt-hover-bg);
}

.quiz-verdict {
  margin: 16px 0 8px;
  font-weight: 600;
}

.quiz-verdict.is-correct {
  color: var(--vp-c-success-1);
}

.quiz-verdict.is-wrong {
  color: var(--vp-c-danger-1);
}

.quiz-answer {
  margin-left: 12px;
  color: var(--vp-c-text-1);
  font-weight: 400;
}

.quiz-explanation :deep(p) {
  margin: 8px 0;
}
</style>
