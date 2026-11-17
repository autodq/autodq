<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr)); gap: 16px">
      <div class="card" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Открыто</span><span class="num" style="font-size: 26px; font-weight: 600">13</span></div>
      <div class="card" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Критичных</span><span class="num" style="font-size: 26px; font-weight: 600; color: #A8361E">4</span></div>
      <div class="card" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Среднее время решения</span><span class="num" style="font-size: 26px; font-weight: 600">6 ч 20 мин</span></div>
      <div class="card" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Просрочено по SLA</span><span class="num" style="font-size: 26px; font-weight: 600">1</span></div>
    </div>
    <div style="display: flex; flex-wrap: wrap; gap: 8px">
      <template v-for="(f, fIndex) in vm.incFilters" :key="fIndex">
        <button type="button" :class="`btn sm ${f.cls}`" @click="f.go">{{ f.label }} <span class="num" style="opacity: .55">{{ f.n }}</span></button>
      </template>
    </div>
    <div class="card tw">
      <div style="min-width: 980px">
        <div class="th" style="display: grid; grid-template-columns: 4px minmax(280px, 2fr) 150px 1fr 130px 110px 120px; gap: 16px; padding: 14px 20px"><span></span><span>Инцидент</span><span>Класс</span><span>Набор · колонка</span><span>Ответственный</span><span>SLA</span><span>Статус</span></div>
        <template v-for="(i, iIndex) in vm.incView" :key="iIndex">
          <div class="row" style="display: grid; grid-template-columns: 4px minmax(280px, 2fr) 150px 1fr 130px 110px 120px; gap: 16px; align-items: center; padding: 14px 20px; border-top: 1px solid #EEEEE9">
            <span :style="`align-self: stretch; border-radius: 2px; background: ${i.bar}`"></span>
            <span style="display: flex; flex-direction: column; gap: 3px; min-width: 0"><span style="font-size: 14px; font-weight: 600">{{ i.title }}</span><span style="font-size: 12px; color: #4B4E57; line-height: 1.45">{{ i.desc }}</span></span>
            <span><span class="tag" style="font-family: 'Onest Variable', sans-serif">{{ i.cls }}</span></span>
            <span style="display: flex; flex-direction: column; gap: 2px"><span class="m" style="font-size: 12px">{{ i.ds }}</span><span class="m" style="font-size: 12px; color: #74777F">{{ i.col }} · {{ i.cnt }}</span></span>
            <span style="font-size: 13px; color: #4B4E57">{{ i.owner }}</span>
            <span class="num" :style="`font-size: 12px; color: ${i.slaC}`">{{ i.sla }}</span>
            <span><span :class="`st ${i.stc}`"><i></i>{{ i.state }}</span></span>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
