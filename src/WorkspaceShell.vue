<script setup>
import { ref, watch } from 'vue'
import WorkspaceOverlays from "./WorkspaceOverlays.vue"

const props = defineProps({ vm: { type: Object, required: true } })
const menuOpen = ref(false)
watch(() => props.vm.title, () => { menuOpen.value = false })
</script>

<template>
  <div class="app" style="min-height: 100vh; display: flex; flex-wrap: wrap; background: #F4F4F0">

    <aside class="side" :class="{ 'menu-open': menuOpen }">
      <div class="side-brand" style="display: flex; align-items: center; gap: 11px; padding: 4px 8px">
        <svg class="lg" viewBox="0 0 120 120" aria-hidden="true" style="width: 28px; height: 28px; margin: 3px 0 0 2px; overflow: visible">
          <g style="transform-box: view-box; transform-origin: 54px 54px; transform: rotate(-90deg)"><circle class="ring" cx="54" cy="54" r="30" pathLength="100"></circle></g>
          <path class="tail" d="M84 56 V104" pathLength="100"></path>
          <g class="orbit"><g class="drop"><circle class="core" cx="54" cy="24" r="4.5" fill="#C9EC5F"></circle></g></g>
        </svg>
        <span class="wm" style="font-size: 20px">autodq</span>
        <button type="button" class="mobile-menu" aria-controls="workspace-nav" :aria-expanded="menuOpen"
          @click="menuOpen = !menuOpen">{{ menuOpen ? 'Закрыть меню' : 'Разделы' }}</button>
      </div>

      <div style="display: flex; align-items: center; gap: 10px; height: 46px; padding: 0 12px; border-radius: 10px; border: 1px solid #24262C; background: #141519; color: #F4F4F0; cursor: pointer; text-align: left; font: inherit">
        <span class="m" style="width: 24px; height: 24px; border-radius: 6px; background: #F4F4F0; color: #0E0F12; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600">AN</span>
        <span style="display: flex; flex-direction: column; min-width: 0"><span style="font-size: 13px; font-weight: 600">Analytics</span><span style="font-size: 12px; color: #8C8F97">Демонстрация</span></span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8C8F97" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="margin-left: auto"><path d="M8 9l4-4 4 4M8 15l4 4 4-4"></path></svg>
      </div>

      <nav id="workspace-nav" class="nav" aria-label="Разделы">
        <div class="pill" :style="`transform: translateY(${vm.pillY}px)`"></div>
        <template v-for="(n, nIndex) in vm.nav1" :key="nIndex">
          <button type="button" :class="`nv ${n.cls}`" @click="n.go">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path :d="n.d"></path></svg>
            <span>{{ n.label }}</span>
            <template v-if="n.hasBadge"><span :class="`bd ${n.bcls}`">{{ n.badge }}</span></template>
          </button>
        </template>
        <div class="grp">Администрирование</div>
        <template v-for="(n, nIndex) in vm.nav2" :key="nIndex">
          <button type="button" :class="`nv ${n.cls}`" @click="n.go">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path :d="n.d"></path></svg>
            <span>{{ n.label }}</span>
          </button>
        </template>
      </nav>

      <div style="margin-top: auto; display: flex; flex-direction: column; gap: 12px">
        <button type="button" @click="vm.goLic" style="display: flex; flex-direction: column; gap: 10px; padding: 14px; border-radius: 12px; background: #141519; border: 1px solid #24262C; color: #F4F4F0; cursor: pointer; text-align: left; font: inherit">
          <span style="display: flex; justify-content: space-between; align-items: center"><span style="font-size: 13px; font-weight: 600">Лицензия {{ vm.lic.plan }}</span><span class="m" :style="`font-size: 11px; color: ${vm.lic.sideColor}`">{{ vm.lic.short }}</span></span>
          <span style="height: 3px; border-radius: 2px; background: #24262C; overflow: hidden"><span :style="`display: block; height: 100%; width: ${vm.lic.sidePct}%; background: ${vm.lic.sideBar}`"></span></span>
          <span style="font-size: 12px; color: #8C8F97">{{ vm.lic.sideNote }}</span>
        </button>
        <div style="display: flex; align-items: center; gap: 10px; padding: 4px 6px">
          <span class="m" style="width: 30px; height: 30px; border-radius: 50%; background: #24262C; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600">АС</span>
          <span style="display: flex; flex-direction: column; min-width: 0"><span style="font-size: 13px; font-weight: 600">Алия Сейткали</span><span style="font-size: 12px; color: #8C8F97">Администратор</span></span>
          <a href="#/login" aria-label="Выйти" style="margin-left: auto; color: #8C8F97; display: flex"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h10"></path></svg></a>
        </div>
      </div>
    </aside>

    <main class="main">
      <div class="top">
        <div style="display: flex; flex-direction: column; gap: 2px; min-width: 0; margin-right: auto">
          <span style="font-size: 12px; color: #74777F">{{ vm.crumb }}</span>
          <h1 style="font-size: 22px">{{ vm.title }}</h1>
        </div>
        <form class="search" @submit.prevent="vm.search"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg><input type="text" name="query" placeholder="Поиск по наборам данных" aria-label="Поиск по наборам данных"><button class="kbd" type="submit">Найти</button></form>
        <button type="button" :class="`st ${vm.lic.cls}`" @click="vm.goLic" style="border: 0; cursor: pointer; height: 30px"><i></i>{{ vm.lic.badge }}</button>
        <button type="button" :class="`btn ink ${vm.runBusy}`" @click="vm.startRun" :disabled="vm.runDisabled" style="min-width: 214px"><template v-if="vm.isRunning"><svg viewBox="0 0 120 120" aria-hidden="true" style="width: 14px; height: 14px; overflow: visible"><circle cx="60" cy="60" r="40" fill="none" stroke="#3A3C42" stroke-width="20"></circle><g class="spn"><circle cx="60" cy="20" r="16" fill="#C9EC5F"></circle></g></svg></template><template v-if="vm.notRunning"><i class="dot"></i></template><span style="font-variant-numeric: tabular-nums">{{ vm.runLabel }}</span></button>
      </div>

      <template v-if="vm.lic.banner">
        <div :style="`margin: 16px 32px 0; padding: 12px 16px; border-radius: 12px; display: flex; flex-wrap: wrap; align-items: center; gap: 10px 16px; background: ${vm.lic.bBg}; color: ${vm.lic.bFg}; animation: fadeUp .5s cubic-bezier(.22,1,.36,1) both`">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 8v5M12 16h.01"></path></svg>
          <span style="font-size: 14px; font-weight: 600">{{ vm.lic.bTitle }}</span>
          <span style="font-size: 14px">{{ vm.lic.bText }}</span>
          <button type="button" class="btn sm ink" @click="vm.goLic" style="margin-left: auto">{{ vm.lic.cta }}</button>
        </div>
      </template>

      <div class="body">

        <slot />
      </div>
    </main>
    <WorkspaceOverlays :vm="vm" />
  </div>
</template>
