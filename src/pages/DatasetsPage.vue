<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center">
      <div class="seg filters" aria-label="Фильтр наборов">
        <button v-for="filter in vm.setFilters" :key="filter.id" type="button"
          :class="{ on: filter.selected }" :aria-pressed="filter.selected" @click="filter.activate">
          {{ filter.label }}
        </button>
      </div>
      <span style="font-size: 13px; color: #74777F; margin-left: auto">Наборов · {{ vm.sets.length }}</span>
      <button type="button" class="btn ghost" disabled title="Появится после подключения источников">Подключить источник</button>
    </div>
    <div v-if="vm.datasetQuery" class="demo-message">Поиск «{{ vm.datasetQuery }}»
      <button class="btn ghost sm" type="button" @click="vm.clearSearch">Сбросить</button>
    </div>
    <p v-if="!vm.sets.length" class="demo-message">Подходящих наборов нет.</p>
    <div v-else class="card tw">
      <div style="min-width: 980px">
        <div class="th" style="display: grid; grid-template-columns: minmax(200px, 1.8fr) 120px 110px 80px 80px 150px 130px 140px; gap: 16px; padding: 14px 20px">
          <span>Набор данных</span><span>Источник</span><span style="text-align: right">Строк</span><span style="text-align: right">Колонок</span><span style="text-align: right">Правил</span><span>Индекс · 12 проверок</span><span>Последняя проверка</span><span>Статус</span>
        </div>
        <template v-for="(s, sIndex) in vm.sets" :key="sIndex">
          <button type="button" class="rowbtn row" @click="s.open" style="display: grid; grid-template-columns: minmax(200px, 1.8fr) 120px 110px 80px 80px 150px 130px 140px; gap: 16px; align-items: center; padding: 13px 20px; border-top: 1px solid #EEEEE9">
            <span style="display: flex; flex-direction: column; gap: 2px; min-width: 0"><span class="m" style="font-size: 13px; font-weight: 600">{{ s.name }}</span><span style="font-size: 12px; color: #74777F">{{ s.owner }}</span></span>
            <span><span class="tag">{{ s.src }}</span></span>
            <span class="num" style="font-size: 13px; text-align: right">{{ s.rows }}</span>
            <span class="num" style="font-size: 13px; text-align: right">{{ s.cols }}</span>
            <span class="num" style="font-size: 13px; text-align: right">{{ s.rules }}</span>
            <span style="display: flex; align-items: center; gap: 10px"><span class="num" style="font-size: 13px; font-weight: 600; width: 36px">{{ s.score }}</span><span style="position: relative; width: 90px; height: 22px"><template v-for="(p, pIndex) in s.pts" :key="pIndex"><span :class="`dot ${p.c}`" :style="`position: absolute; left: ${p.x}%; bottom: ${p.y}px; width: 5px; height: 5px`"></span></template></span></span>
            <span style="font-size: 13px; color: #4B4E57">{{ s.last }}</span>
            <span><span :class="`st ${s.st}`"><i></i>{{ s.stl }}</span></span>
          </button>
        </template>
      </div>
    </div>
  </div>
</template>
