<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center">
      <div class="seg">
        <div class="sp" :style="`width: 86px; transform: translateX(${vm.perX})`"></div>
        <template v-for="(t, tIndex) in vm.periods" :key="tIndex">
          <button type="button" :class="t.cls" @click="t.go" :disabled="t.disabled"
            :title="t.disabled ? 'В демо доступно 30 дней' : undefined" style="width: 86px">{{ t.label }}</button>
        </template>
      </div>
      <span style="font-size: 13px; color: #74777F; margin-left: auto">Все наборы · 601 активное правило</span>
      <button type="button" class="btn ghost" @click="vm.goReports">Сформировать отчёт</button>
    </div>

    <div class="card">
      <div class="ch"><h3>Индекс качества во времени</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 14px; font-size: 12px; color: #4B4E57">
          <span style="display: flex; align-items: center; gap: 6px"><i style="width: 16px; height: 2px; background: #0E0F12"></i>медиана по наборам</span>
          <span style="display: flex; align-items: center; gap: 6px"><i style="width: 14px; height: 10px; border-radius: 3px; background: #E7E9EE"></i>диапазон min–max</span>
          <span style="display: flex; align-items: center; gap: 6px"><i style="width: 9px; height: 9px; border-radius: 50%; background: #E0553A"></i>набор ниже 80</span>
        </div>
      </div>
      <div class="cb">
        <div style="position: relative; height: 240px">
          <svg viewBox="0 0 900 220" preserveAspectRatio="none" aria-hidden="true" style="position: absolute; inset: 0; width: 100%; height: 220px">
            <path d="M0 22 H900 M0 77 H900 M0 132 H900 M0 187 H900" stroke="#EEEEE9" stroke-width="1"></path>
            <path :d="vm.tl.band" fill="#E7E9EE"></path>
            <path :d="vm.tl.med" fill="none" stroke="#0E0F12" stroke-width="2.2" stroke-linejoin="round" style="animation: fade 1s ease .2s both"></path>
          </svg>
          <template v-for="(k, kIndex) in vm.tl.marks" :key="kIndex"><div class="marker" :style="`left: ${k.x}%; top: ${k.y}px`" :title="k.t"></div></template>
          <div class="m" style="position: absolute; left: 0; right: 0; bottom: 0; display: flex; justify-content: space-between; font-size: 11px; color: #74777F">
            <span v-for="date in vm.tl.dates" :key="date">{{ date }}</span>
          </div>
          <div class="m" style="position: absolute; right: 4px; top: 14px; display: flex; flex-direction: column; justify-content: space-between; height: 180px; font-size: 10px; color: #9C9FA7; text-align: right"><span>100</span><span>90</span><span>80</span><span>70</span></div>
        </div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(460px, 100%), 1fr)); gap: 16px">
      <div class="card">
        <div class="ch"><h3>Правила × проверки</h3><span style="font-size: 12px; color: #74777F">размер точки — число нарушений</span></div>
        <div class="cb tw">
          <div style="min-width: 520px; display: flex; flex-direction: column; gap: 8px">
            <template v-for="(r, rIndex) in vm.matrix" :key="rIndex">
              <div style="display: grid; grid-template-columns: 160px 1fr; gap: 12px; align-items: center">
                <span class="m" style="font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{{ r.name }}</span>
                <div style="display: grid; grid-template-columns: repeat(24, minmax(0, 1fr)); gap: 6px; align-items: center; justify-items: center">
                  <template v-for="(c, cIndex) in r.cells" :key="cIndex"><span class="dot" :style="`width: ${c.s}px; height: ${c.s}px; background: ${c.c}; animation-delay: ${c.d}s`"></span></template>
                </div>
              </div>
            </template>
            <div class="m" style="display: grid; grid-template-columns: 160px 1fr; gap: 12px; font-size: 11px; color: #74777F"><span></span><span style="display: flex; justify-content: space-between"><span>№ 2791</span><span>№ 2814</span></span></div>
          </div>
        </div>
      </div>

      <div style="display: flex; flex-direction: column; gap: 16px">
        <div class="card">
          <div class="ch"><h3>Классы нарушений</h3><span style="font-size: 12px; color: #74777F">213 за 30 дней</span></div>
          <div class="cb" style="display: flex; flex-direction: column; gap: 16px">
            <div style="display: flex; height: 28px; border-radius: 8px; overflow: hidden; gap: 2px">
              <template v-for="(c, cIndex) in vm.classes" :key="cIndex"><div class="hbar" :style="`flex: ${c.n}; background: ${c.bg}; animation-delay: ${c.d}s`" :title="c.name"></div></template>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(190px, 100%), 1fr)); gap: 10px 20px">
              <template v-for="(c, cIndex) in vm.classes" :key="cIndex">
                <div style="display: flex; align-items: center; gap: 10px"><i :style="`width: 10px; height: 10px; border-radius: 3px; background: ${c.bg}; flex-shrink: 0`"></i><span style="font-size: 13px">{{ c.name }}</span><span class="num" style="margin-left: auto; font-size: 13px; font-weight: 600">{{ c.n }}</span></div>
              </template>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="ch"><h3>Измерения качества</h3><span style="font-size: 12px; color: #74777F">шкала 90–100 · цель 95</span></div>
          <div class="cb" style="display: flex; flex-direction: column; gap: 14px">
            <template v-for="(d, dIndex) in vm.dims" :key="dIndex">
              <div style="display: grid; grid-template-columns: 180px 1fr 48px; gap: 14px; align-items: center">
                <span style="font-size: 13px">{{ d.name }}</span>
                <div style="position: relative; height: 18px">
                  <div style="position: absolute; left: 0; right: 0; top: 8px; height: 2px; background: #EEEEE9"></div>
                  <div class="hbar" :style="`position: absolute; left: 0; top: 8px; height: 2px; width: ${d.w}%; background: #0E0F12; animation-delay: ${d.dl}s`"></div>
                  <div style="position: absolute; left: 50%; top: 2px; width: 1.5px; height: 14px; background: #AEB4C2"></div>
                  <div class="dot" :style="`position: absolute; left: ${d.w}%; top: 2px; width: 14px; height: 14px; margin-left: -7px; background: ${d.dot}; box-shadow: 0 0 0 2.5px #0E0F12 inset; animation-delay: ${d.dl2}s`"></div>
                </div>
                <span class="num" style="font-size: 13px; font-weight: 600; text-align: right">{{ d.v }}</span>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
