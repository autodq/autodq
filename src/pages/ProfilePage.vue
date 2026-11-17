<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div class="card" style="padding: 18px 20px; display: flex; flex-wrap: wrap; align-items: center; gap: 14px 32px">
      <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Набор данных</span><span class="m" style="font-size: 16px; font-weight: 600">{{ vm.ds.name }}</span></div>
      <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Строк</span><span class="num" style="font-size: 16px; font-weight: 600">{{ vm.ds.rows }}</span></div>
      <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Колонок</span><span class="num" style="font-size: 16px; font-weight: 600">{{ vm.ds.cols }}</span></div>
      <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Профиль построен</span><span class="num" style="font-size: 16px; font-weight: 600">15.10.2026 09:12</span></div>
      <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Выборка</span><span class="num" style="font-size: 16px; font-weight: 600">100%</span></div>
      <div style="margin-left: auto; display: flex; gap: 8px; flex-wrap: wrap">
        <button type="button" class="btn ghost" @click="vm.goSets">Назад к наборам</button>
        <button type="button" class="btn ink" @click="vm.startGen" :disabled="vm.genDisabled || !vm.hasProfile"><i class="dot"></i>Сгенерировать правила</button>
      </div>
    </div>

    <p v-if="!vm.hasProfile" class="demo-message">В демо доступен подробный профиль sales.orders.</p>
    <template v-if="vm.hasProfile && vm.loading">
      <div style="display: flex; flex-wrap: wrap; gap: 16px">
        <div class="card" style="flex: 1 1 320px; padding: 16px; display: flex; flex-direction: column; gap: 12px">
          <div class="sk" style="height: 18px; width: 40%"></div>
          <div class="sk" style="height: 46px"></div><div class="sk" style="height: 46px"></div><div class="sk" style="height: 46px"></div><div class="sk" style="height: 46px"></div><div class="sk" style="height: 46px"></div><div class="sk" style="height: 46px"></div>
        </div>
        <div class="card" style="flex: 2 1 560px; padding: 20px; display: flex; flex-direction: column; gap: 16px">
          <div style="display: flex; align-items: center; gap: 12px">
            <svg viewBox="0 0 120 120" aria-hidden="true" style="width: 20px; height: 20px; overflow: visible"><circle cx="60" cy="60" r="36" fill="none" stroke="#EEEEE9" stroke-width="18"></circle><g class="spin"><g style="transform-box: view-box; transform-origin: 60px 60px; transform: rotate(-90deg)"><circle cx="60" cy="60" r="36" fill="none" stroke="#0E0F12" stroke-width="18" stroke-linecap="round" pathLength="100" style="stroke-dasharray: 22 78; stroke-dashoffset: 22"></circle></g><circle cx="60" cy="24" r="11" fill="#C9EC5F"></circle></g></svg>
            <span style="font-size: 14px; font-weight: 500">Загрузка профиля · 24 колонки, 4.8 млн строк</span>
          </div>
          <div class="sk" style="height: 180px"></div>
          <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px"><div class="sk" style="height: 48px"></div><div class="sk" style="height: 48px"></div><div class="sk" style="height: 48px"></div><div class="sk" style="height: 48px"></div></div>
        </div>
      </div>
    </template>

    <template v-if="vm.hasProfile && vm.loaded">
      <div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-start">
        <div class="card" style="flex: 1 1 320px; overflow: hidden">
          <div class="th" style="display: flex; justify-content: space-between; padding: 14px 16px; border-bottom: 1px solid #EEEEE9"><span>Колонка</span><span>Пропуски · уникальность</span></div>
          <template v-for="(c, cIndex) in vm.cols" :key="cIndex">
            <button type="button" :class="`colr ${c.on}`" @click="c.pick">
              <span style="display: flex; align-items: center; gap: 8px; min-width: 0"><span class="m" style="font-size: 13px; font-weight: 600">{{ c.name }}</span><span class="tag">{{ c.type }}</span><template v-if="c.hasFlag"><span :style="`width: 7px; height: 7px; border-radius: 50%; background: ${c.flagC}`"></span></template></span>
              <span class="num" style="font-size: 12px; color: #4B4E57">{{ c.nulls }} · {{ c.uniq }}%</span>
              <span class="meter" style="grid-column: 1 / -1"><b :style="`width: ${c.uniq}%; background: #0E0F12`"></b></span>
            </button>
          </template>
        </div>

        <div style="flex: 2 1 560px; min-width: 0; display: flex; flex-direction: column; gap: 16px">
          <div class="card">
            <div class="ch"><h3><span class="m">{{ vm.col.name }}</span> · распределение значений</h3>
              <div style="display: flex; flex-wrap: wrap; gap: 14px; font-size: 12px; color: #4B4E57">
                <span style="display: flex; align-items: center; gap: 6px"><i class="d-ok" style="width: 8px; height: 8px; border-radius: 50%"></i>текущие данные</span>
                <span style="display: flex; align-items: center; gap: 6px"><i style="width: 12px; height: 2px; background: #6B7488"></i>профиль</span>
                <span style="display: flex; align-items: center; gap: 6px"><i class="d-fail" style="width: 8px; height: 8px; border-radius: 50%"></i>вне диапазона</span>
              </div>
            </div>
            <div class="cb">
              <div style="position: relative; height: 200px; display: flex; align-items: flex-end; gap: 3px; padding-top: 22px; border-bottom: 1px solid #E4E4DE">
                <div :style="`position: absolute; top: 0; bottom: 0; left: ${vm.col.bandL}%; width: ${vm.col.bandW}%; background: #F6F8EE; border-left: 1px dashed #A6CC34; border-right: 1px dashed #A6CC34`"></div>
                <span :style="`position: absolute; top: 3px; left: ${vm.col.bandL}%; margin-left: 8px; font-size: 11px; color: #4D6410`">ожидаемый диапазон · {{ vm.col.bandTxt }}</span>
                <template v-for="(b, bIndex) in vm.col.bins" :key="bIndex">
                  <div style="position: relative; flex: 1; display: flex; flex-direction: column-reverse; align-items: center; gap: 3px; padding-bottom: 3px">
                    <template v-for="(d, dIndex) in b.dots" :key="dIndex"><span :class="`dot ${d.c}`" :style="`width: 8px; height: 8px; animation-delay: ${d.dl}s`"></span></template>
                    <span class="tick" :style="`bottom: ${b.tk}px; opacity: ${b.to}`"></span>
                  </div>
                </template>
              </div>
              <div class="m" style="display: flex; justify-content: space-between; padding-top: 8px; font-size: 11px; color: #74777F"><span>{{ vm.col.min }}</span><span>{{ vm.col.mid }}</span><span>{{ vm.col.max }}</span></div>
            </div>
          </div>
          <div class="card">
            <div class="cb" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(150px, 100%), 1fr)); gap: 14px 20px">
              <template v-for="(t, tIndex) in vm.col.stats" :key="tIndex">
                <div style="display: flex; flex-direction: column; gap: 3px"><span class="lbl">{{ t.k }}</span><span class="num" style="font-size: 15px; font-weight: 600">{{ t.v }}</span></div>
              </template>
            </div>
          </div>
          <div class="card">
            <div class="ch"><h3>Правила, предложенные по колонке</h3><button type="button" class="btn sm ghost" @click="vm.goRules">Все правила</button></div>
            <div class="cb" style="display: flex; flex-direction: column; padding-top: 6px">
              <template v-for="(r, rIndex) in vm.col.rules" :key="rIndex">
                <div style="display: grid; grid-template-columns: minmax(0, 1fr) 90px auto; gap: 16px; align-items: center; padding: 11px 0; border-bottom: 1px solid #EEEEE9">
                  <span style="display: flex; flex-direction: column; gap: 2px; min-width: 0"><span class="m" style="font-size: 13px; font-weight: 600">{{ r.e }}</span><span style="font-size: 12px; color: #74777F">{{ r.w }}</span></span>
                  <span class="num" style="font-size: 13px">{{ r.c }}</span>
                  <span :class="`st ${r.s}`"><i></i>{{ r.sl }}</span>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
