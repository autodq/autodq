<script setup>
import { ref } from 'vue'

const report = ref(null)
const error = ref('')
const statuses = {
  pass: 'Пройдено', warn: 'Есть предупреждения', fail: 'Есть нарушения', skip: 'Недостаточно данных'
}
const isCount = value => Number.isSafeInteger(value) && value >= 0
const validOutcome = value => typeof value === 'string' && Object.hasOwn(statuses, value)
const validProbability = value => value === null || (Number.isFinite(value) && value >= 0 && value <= 1)
const isStringList = value => Array.isArray(value) && value.every(item => typeof item === 'string')

function isReport(data) {
  return data?.version === 1 && validOutcome(data.outcome) &&
    isCount(data.rows) && isCount(data.eligible_rules) && isCount(data.evaluated_rules) &&
    data.evaluated_rules <= data.eligible_rules && validProbability(data.rule_coverage) &&
    (data.quality_score === null || (Number.isFinite(data.quality_score) && data.quality_score >= 0 && data.quality_score <= 100)) &&
    isStringList(data.missing_columns) && isStringList(data.extra_columns) &&
    Array.isArray(data.results) && data.results.length === data.eligible_rules &&
    data.results.every(item => item && typeof item.rule_id === 'string' &&
      typeof item.column === 'string' && typeof item.kind === 'string' &&
      typeof item.reason === 'string' && validOutcome(item.outcome) &&
      isCount(item.observations) && validProbability(item.adjusted_p_value))
}

let selection = 0
async function loadReport(event) {
  const file = event.target.files?.[0]
  if (!file) return
  const request = ++selection
  error.value = ''
  report.value = null
  try {
    const data = JSON.parse(await file.text())
    if (!isReport(data)) throw new Error('Unsupported report format')
    if (request === selection) report.value = data
  } catch {
    if (request === selection) error.value = 'Выберите JSON-отчёт, созданный командой autodq check.'
  } finally {
    if (request === selection) event.target.value = ''
  }
}

function clear() {
  selection += 1
  report.value = null
  error.value = ''
}
</script>

<template>
  <section class="card local-report" aria-labelledby="local-report-title">
    <div class="ch">
      <h3 id="local-report-title">Отчёт локального анализа</h3>
      <button v-if="report || error" type="button" class="btn ghost sm" @click="clear">Закрыть отчёт</button>
    </div>
    <div class="cb">
      <label for="engine-report">JSON из <code>autodq check</code></label>
      <input id="engine-report" type="file" accept=".json,application/json" @change="loadReport">
      <p v-if="error" role="alert">{{ error }}</p>
      <template v-if="report">
        <p role="status"><strong>{{ statuses[report.outcome] }}</strong> · строк {{ report.rows }}
          · правил {{ report.evaluated_rules }} / {{ report.eligible_rules }}
          · оценка {{ report.quality_score === null ? '—' : report.quality_score + ' / 100' }}</p>
        <p v-if="report.missing_columns.length">Отсутствуют колонки · {{ report.missing_columns.join(', ') }}</p>
        <p v-if="report.extra_columns.length">Новые колонки · {{ report.extra_columns.join(', ') }}</p>
        <div class="tw">
          <table>
            <thead><tr><th>Колонка</th><th>Правило</th><th>Результат</th><th>Наблюдений</th><th>Скорр. p</th></tr></thead>
            <tbody>
              <tr v-for="result in report.results" :key="result.rule_id">
                <td class="m">{{ result.column }}</td>
                <td>{{ result.kind }}</td>
                <td :title="result.reason">{{ statuses[result.outcome] }}</td>
                <td class="m">{{ result.observations }}</td>
                <td class="m">{{ result.adjusted_p_value?.toPrecision(3) ?? '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
  </section>
</template>

<style scoped>
input { display: block; margin-block: 6px 0; max-width: 100%; font: inherit }
table { min-width: 540px; width: 100%; border-collapse: collapse; text-align: left }
th, td { border-top: 1px solid #eeeee9; padding: 8px 12px }
p[role='alert'] { color: #a8361e }
</style>
