<script setup>
import LocalReport from './LocalReport.vue'

defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <LocalReport />
    <div class="rbar"></div>
    <div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-start">
      <div style="flex: 1 1 300px; display: flex; flex-direction: column; gap: 10px">
        <template v-for="(r, rIndex) in vm.reports" :key="rIndex">
          <button type="button" class="card lift" @click="r.pick" :style="`padding: 14px 16px; text-align: left; font: inherit; color: inherit; cursor: pointer; display: flex; flex-direction: column; gap: 4px; border-color: ${r.bc}`">
            <span style="display: flex; justify-content: space-between; gap: 10px"><span style="font-size: 14px; font-weight: 600">{{ r.title }}</span><span class="num" style="font-size: 13px; font-weight: 600">{{ r.score }}</span></span>
            <span style="font-size: 12px; color: #74777F">{{ r.meta }}</span>
          </button>
        </template>
        <div class="card" style="padding: 14px 16px; display: flex; align-items: center; gap: 14px">
          <span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 600">Еженедельная рассылка</span><span style="font-size: 12px; color: #74777F">понедельник 09:00 · PDF · группа data-quality</span></span>
          <button type="button" :class="`tg ${vm.tgWeekly}`" @click="vm.toggleWeekly" aria-label="Еженедельная рассылка" style="margin-left: auto"></button>
        </div>
      </div>
      <div style="flex: 999 1 520px; min-width: 0; display: flex; flex-direction: column; gap: 12px">
        <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end">
          <button type="button" class="btn ghost" @click="vm.exportReport('json')">JSON</button>
          <button type="button" class="btn ghost" @click="vm.exportReport('html')">HTML</button>
          <button type="button" class="btn ink" @click="vm.printReport"><i class="dot"></i>Печать / PDF</button>
        </div>
        <div class="doc">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; padding-bottom: 22px; border-bottom: 1px solid #EEEEE9">
            <div style="display: flex; flex-direction: column; gap: 4px"><span class="lbl">Отчёт о качестве данных</span><span style="font-size: 24px; font-weight: 600; letter-spacing: -0.02em">{{ vm.rep.title }}</span><span style="font-size: 12px; color: #74777F">{{ vm.rep.meta }}</span></div>
            <div style="width: 42px; height: 42px; border-radius: 11px; background: #0E0F12; display: flex; align-items: center; justify-content: center; flex-shrink: 0"><svg viewBox="0 0 120 120" aria-hidden="true" style="width: 28px; height: 28px; margin: 3px 0 0 3px"><circle cx="54" cy="54" r="30" fill="none" stroke="#F4F4F0" stroke-width="16"></circle><path d="M84 56 V104" stroke="#F4F4F0" stroke-width="16" stroke-linecap="round"></path><circle cx="54" cy="54" r="12" fill="#C9EC5F"></circle></svg></div>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(110px, 100%), 1fr)); gap: 16px; padding: 22px 0; border-bottom: 1px solid #EEEEE9">
            <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Индекс</span><span class="num" style="font-size: 26px; font-weight: 600">{{ vm.rep.score }}</span></div>
            <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Правил</span><span class="num" style="font-size: 26px; font-weight: 600">184</span></div>
            <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">С нарушениями</span><span class="num" style="font-size: 26px; font-weight: 600">8</span></div>
            <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Строк</span><span class="num" style="font-size: 26px; font-weight: 600">4.8 млн</span></div>
          </div>
          <div style="display: flex; flex-direction: column; gap: 10px; padding: 22px 0; border-bottom: 1px solid #EEEEE9">
            <span style="font-size: 15px; font-weight: 600">Заключение</span>
            <span style="font-size: 14px; line-height: 1.6; color: #3A3C42">37 значений <span class="m">amount</span> выходят за ожидаемый диапазон профиля (p99.5 = 2 450 000). Доля пропусков <span class="m">discount_pct</span> выросла с 9.8% до 12.4% при допуске 15%. Данные <span class="m">created_at</span> поступили с задержкой 26 ч при допуске 24 ч. Остальные 176 правил выполнены без нарушений.</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px; padding-top: 22px">
            <span style="font-size: 15px; font-weight: 600; padding-bottom: 6px">Правила с нарушениями</span>
            <template v-for="(r, rIndex) in vm.repRules" :key="rIndex">
              <div style="display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: center; padding: 9px 0; border-bottom: 1px solid #F4F4F0"><span class="m" style="font-size: 13px">{{ r.e }}</span><span :class="`st ${r.s}`"><i></i>{{ r.v }}</span></div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
