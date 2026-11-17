<script setup>
import { computed, onUnmounted, reactive, ref, watch } from 'vue'
import WorkspaceShell from './WorkspaceShell.vue'
import LoginPage from './pages/LoginPage.vue'
import OverviewPage from './pages/OverviewPage.vue'
import DatasetsPage from './pages/DatasetsPage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import RulesPage from './pages/RulesPage.vue'
import ChecksPage from './pages/ChecksPage.vue'
import SchedulePage from './pages/SchedulePage.vue'
import AuditPage from './pages/AuditPage.vue'
import IncidentsPage from './pages/IncidentsPage.vue'
import ReportsPage from './pages/ReportsPage.vue'
import LicensePage from './pages/LicensePage.vue'
import SettingsPage from './pages/SettingsPage.vue'
import { DS } from './demo-data'
import { buildWorkspaceView } from './workspace-view'
import { downloadDemoReport } from './report-export'

const pages = {
  dash: OverviewPage, sets: DatasetsPage, profile: ProfilePage,
  rules: RulesPage, checks: ChecksPage, sched: SchedulePage, audit: AuditPage,
  inc: IncidentsPage, reports: ReportsPage, lic: LicensePage, settings: SettingsPage
}
const paths = {
  dash: 'overview', sets: 'datasets', rules: 'rules', checks: 'checks',
  sched: 'schedule', audit: 'audit', inc: 'incidents', reports: 'reports',
  lic: 'license', settings: 'settings'
}
const defaultStatuses = {
  1: 'act', 2: 'act', 3: 'sug', 4: 'sug', 5: 'sug', 6: 'sug',
  7: 'sug', 8: 'sug', 9: 'sug', 10: 'rej', 11: 'act', 12: 'sug'
}
const defaultSettings = { weekly: true, auto: false, tg: true, mail: true, hook: false }

function readPreference(name, defaults, isValid) {
  try {
    const saved = JSON.parse(localStorage.getItem(name))
    return Object.fromEntries(Object.entries(defaults).map(([key, value]) => [
      key, isValid(saved?.[key]) ? saved[key] : value
    ]))
  } catch {
    return { ...defaults }
  }
}

const state = reactive({
  screen: 'dash', ds: 0, col: 2, rtab: 'sug', per: 1, inc: 'all', rep: 0,
  lic: 'active', sel: null, query: '', datasetFilter: 'all',
  p: 0, running: false, ran: false, toast: false, loading: false, gen: -1,
  rs: readPreference('autodq.demo.rules', defaultStatuses, value => ['sug', 'act', 'rej'].includes(value)),
  tg: readPreference('autodq.demo.settings', defaultSettings, value => typeof value === 'boolean')
})
const login = ref(false)
let generationTimer
let checkTimer
let toastTimer
let profileTimer

function syncRoute() {
  const [, path = '', dataset = ''] = location.hash.split('/')
  login.value = path === 'login'
  const selected = path === 'datasets' && dataset ? DS.findIndex(item => item.name === dataset) : -1
  clearTimeout(profileTimer)
  state.loading = false
  state.sel = null
  if (selected >= 0) {
    state.screen = 'profile'
    state.ds = selected
    state.col = 2
    state.loading = selected === 0
    profileTimer = setTimeout(() => { state.loading = false }, 400)
  } else {
    state.screen = Object.keys(paths).find(key => paths[key] === path) ?? 'dash'
  }
  window.scrollTo(0, 0)
}

syncRoute()
window.addEventListener('hashchange', syncRoute)
onUnmounted(() => {
  window.removeEventListener('hashchange', syncRoute)
  clearInterval(generationTimer)
  clearInterval(checkTimer)
  clearTimeout(toastTimer)
  clearTimeout(profileTimer)
})

watch(() => [state.rs, state.tg], ([rules, settings]) => {
  try {
    localStorage.setItem('autodq.demo.rules', JSON.stringify(rules))
    localStorage.setItem('autodq.demo.settings', JSON.stringify(settings))
  } catch {
    // Storage can be blocked by browser policy. Changes still apply in this tab.
  }
}, { deep: true })

function go(screen) {
  const target = '#/' + paths[screen]
  if (location.hash === target) state.sel = null
  else location.hash = target
}

function startRun() {
  if (state.lic === 'expired') return
  go('checks')
  if (state.running) return
  clearTimeout(toastTimer)
  Object.assign(state, { running: true, ran: true, p: 0, toast: false })
  const start = performance.now()
  checkTimer = setInterval(() => {
    state.p = Math.min(100, (performance.now() - start) / 60)
    if (state.p === 100) {
      clearInterval(checkTimer)
      state.running = false
      state.toast = true
      toastTimer = setTimeout(() => { state.toast = false }, 4500)
    }
  }, 200)
}

function startGen() {
  if (state.gen >= 0 || state.lic === 'expired') return
  state.gen = 0
  generationTimer = setInterval(() => {
    if (state.gen < 3) {
      state.gen += 1
      return
    }
    clearInterval(generationTimer)
    state.gen = -1
    state.rtab = 'sug'
    if (!login.value && state.screen === 'profile') go('rules')
  }, 400)
}

const actions = {
  update: patch => Object.assign(state, patch),
  go,
  openSet: index => { location.hash = '#/datasets/' + DS[index].name },
  startGen,
  startRun,
  search: event => {
    state.query = new FormData(event.currentTarget).get('query')?.trim() ?? ''
    state.datasetFilter = 'all'
    go('sets')
  }
}
const view = computed(() => {
  const vm = buildWorkspaceView(state, actions)
  const query = state.query.toLowerCase()
  return {
    ...vm,
    search: actions.search,
    hasProfile: state.ds === 0,
    datasetQuery: state.query,
    setFilters: [
      { id: 'all', label: 'Все · ' + DS.length },
      { id: 'issues', label: 'С нарушениями' },
      { id: 'new', label: 'Новые' }
    ].map(filter => ({
      ...filter,
      selected: filter.id === state.datasetFilter,
      activate: () => { state.datasetFilter = filter.id }
    })),
    clearSearch: () => { state.query = '' },
    sets: vm.sets.filter(dataset =>
      dataset.name.toLowerCase().includes(query) &&
      (state.datasetFilter === 'all' || (state.datasetFilter === 'new' ? dataset.st === 'run' : dataset.st === 'fail'))
    ),
    rulePending: state.rtab === 'sug' && vm.rulesView.length > 0,
    exportReport: format => downloadDemoReport(format, vm.rep, vm.repRules),
    printReport: () => window.print(),
  }
})
</script>

<template>
  <LoginPage v-if="login" />
  <WorkspaceShell v-else :vm="view">
    <component :is="pages[state.screen]" :vm="view" />
  </WorkspaceShell>
</template>
