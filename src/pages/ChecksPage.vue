<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div class="card">
      <div class="ch">
        <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Проверка № 2815</span><h3 style="font-size: 17px">sales.orders · 184 правила</h3></div>
        <div style="display: flex; gap: 10px; align-items: center"><span :class="`st ${vm.run.cls}`"><i></i>{{ vm.run.label }}</span><button type="button" :class="`btn ink ${vm.runBusy}`" @click="vm.startRun" :disabled="vm.runDisabled" style="min-width: 214px"><template v-if="vm.isRunning"><svg viewBox="0 0 120 120" aria-hidden="true" style="width: 14px; height: 14px; overflow: visible"><circle cx="60" cy="60" r="40" fill="none" stroke="#3A3C42" stroke-width="20"></circle><g class="spn"><circle cx="60" cy="20" r="16" fill="#C9EC5F"></circle></g></svg></template><template v-if="vm.notRunning"><i class="dot"></i></template><span style="font-variant-numeric: tabular-nums">{{ vm.runLabel }}</span></button></div>
      </div>
      <div class="cb" style="display: flex; flex-wrap: wrap; gap: 24px">
        <div style="flex: 3 1 460px; display: flex; flex-direction: column; gap: 16px">
          <div style="display: grid; grid-template-columns: 1fr 56px; gap: 14px; align-items: center"><div class="prog"><b :style="`width: ${vm.run.p}%`"></b></div><span class="num" style="font-size: 14px; font-weight: 600; text-align: right">{{ vm.run.p }}%</span></div>
          <div style="display: grid; grid-template-columns: repeat(23, minmax(0, 1fr)); gap: 7px; justify-items: center">
            <template v-for="(g, gIndex) in vm.run.grid" :key="gIndex"><span :class="`cg ${g.c}`" style="display: block; width: 11px; height: 11px"></span></template>
          </div>
          <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px">
            <div style="padding: 12px 14px; border-radius: 10px; background: #F9F9F6; display: flex; flex-direction: column; gap: 4px"><span class="lbl">Выполнено</span><span class="num" style="font-size: 20px; font-weight: 600">{{ vm.run.done }}</span></div>
            <div style="padding: 12px 14px; border-radius: 10px; background: #F9F9F6; display: flex; flex-direction: column; gap: 4px"><span class="lbl">Без нарушений</span><span class="num" style="font-size: 20px; font-weight: 600">{{ vm.run.pass }}</span></div>
            <div style="padding: 12px 14px; border-radius: 10px; background: #FBF1DD; display: flex; flex-direction: column; gap: 4px"><span class="lbl" style="color: #7A5208">Предупреждения</span><span class="num" style="font-size: 20px; font-weight: 600">{{ vm.run.warn }}</span></div>
            <div style="padding: 12px 14px; border-radius: 10px; background: #FBE7E2; display: flex; flex-direction: column; gap: 4px"><span class="lbl" style="color: #A8361E">Нарушения</span><span class="num" style="font-size: 20px; font-weight: 600">{{ vm.run.fail }}</span></div>
          </div>
        </div>
        <div class="m" style="flex: 2 1 320px; display: flex; flex-direction: column; gap: 5px; padding: 14px 16px; border-radius: 10px; background: #0E0F12; color: #C9CBD1; font-size: 12px; min-height: 240px">
          <span style="font-family: 'Onest Variable', sans-serif; font-size: 12px; color: #6E717A; padding-bottom: 6px">Журнал выполнения</span>
          <template v-for="(l, lIndex) in vm.run.log" :key="lIndex"><div class="logline"><span style="color: #5F626A">{{ l.t }}</span>  <span :style="`color: ${l.c}`">{{ l.s }}</span></div></template>
        </div>
      </div>
    </div>
    <div class="card tw">
      <div class="ch"><h3>История проверок</h3><span style="font-size: 12px; color: #74777F">последние 7 из 2 815</span></div>
      <div style="min-width: 900px; padding-top: 8px">
        <div class="th" style="display: grid; grid-template-columns: 90px minmax(180px, 1.5fr) 1fr 110px 120px 140px; gap: 16px; padding: 10px 20px"><span>№</span><span>Набор данных</span><span>Результат правил</span><span>Длительность</span><span>Инициатор</span><span>Статус</span></div>
        <template v-for="(r, rIndex) in vm.runs" :key="rIndex">
          <div class="row" style="display: grid; grid-template-columns: 90px minmax(180px, 1.5fr) 1fr 110px 120px 140px; gap: 16px; align-items: center; padding: 12px 20px; border-top: 1px solid #EEEEE9">
            <span class="num" style="font-size: 13px">{{ r.id }}</span>
            <span style="display: flex; flex-direction: column; gap: 2px"><span class="m" style="font-size: 13px">{{ r.ds }}</span><span style="font-size: 12px; color: #74777F">{{ r.when }}</span></span>
            <span style="display: flex; height: 6px; border-radius: 3px; overflow: hidden; gap: 2px"><span class="hbar" :style="`flex: ${r.p}; background: #0E0F12`"></span><span class="hbar" :style="`flex: ${r.w}; background: #E3A23B`"></span><span class="hbar" :style="`flex: ${r.f}; background: #E0553A`"></span></span>
            <span class="num" style="font-size: 13px">{{ r.dur }}</span>
            <span style="font-size: 13px; color: #4B4E57">{{ r.trig }}</span>
            <span><span :class="`st ${r.st}`"><i></i>{{ r.stl }}</span></span>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
