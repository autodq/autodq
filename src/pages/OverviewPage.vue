<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div style="display: flex; flex-wrap: wrap; gap: 16px">
      <div class="card" style="flex: 2 1 460px; padding: 22px; display: flex; flex-wrap: wrap; gap: 24px; align-items: center">
        <svg class="ringv" viewBox="0 0 140 140" aria-hidden="true" style="width: 148px; height: 148px; flex-shrink: 0; overflow: visible">
          <circle cx="70" cy="70" r="54" fill="none" stroke="#EEEEE9" stroke-width="12"></circle>
          <g style="transform-box: view-box; transform-origin: 70px 70px; transform: rotate(-90deg)"><circle class="arc" cx="70" cy="70" r="54" fill="none" stroke="#0E0F12" stroke-width="12" stroke-linecap="round" pathLength="100" style="stroke-dasharray: 94.6 100"></circle></g>
          <g class="tip" style="transform: rotate(340.6deg)"><circle cx="70" cy="16" r="8" fill="#C9EC5F" stroke="#0E0F12" stroke-width="3"></circle></g>
          <text x="70" y="76" text-anchor="middle" style="font: 600 28px 'JetBrains Mono Variable', monospace; fill: #0E0F12">94.6</text>
          <text x="70" y="96" text-anchor="middle" style="font: 500 11px 'Onest Variable', sans-serif; fill: #74777F">из 100</text>
        </svg>
        <div style="flex: 1 1 220px; display: flex; flex-direction: column; gap: 14px">
          <div style="display: flex; flex-direction: column; gap: 4px"><span style="font-size: 15px; font-weight: 600">Индекс качества данных</span><span class="t3" style="font-size: 13px">Доля пройденных проверок с учётом критичности правил, все наборы</span></div>
          <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; padding-top: 14px; border-top: 1px solid #EEEEE9">
            <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">За 7 дней</span><span class="num" style="font-size: 16px; font-weight: 600; color: #4D6410">+1.2</span></div>
            <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Проверено строк</span><span class="num" style="font-size: 16px; font-weight: 600">78.1 млн</span></div>
            <div style="display: flex; flex-direction: column; gap: 2px"><span class="lbl">Соблюдение SLA</span><span class="num" style="font-size: 16px; font-weight: 600">97.8%</span></div>
          </div>
        </div>
      </div>
      <div style="flex: 3 1 520px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(230px, 100%), 1fr)); gap: 16px">
        <template v-for="(k, kIndex) in vm.kpis" :key="kIndex">
          <div class="card lift" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 8px">
            <div style="display: flex; justify-content: space-between; gap: 8px"><span class="lbl">{{ k.l }}</span><span class="num" :style="`font-size: 12px; color: ${k.c}`">{{ k.d }}</span></div>
            <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 14px">
              <span class="num" style="font-size: 28px; font-weight: 600; letter-spacing: -0.02em; line-height: 1">{{ k.v }}</span>
              <div style="position: relative; width: 112px; height: 30px">
                <template v-for="(p, pIndex) in k.pts" :key="pIndex"><span :class="`dot ${p.c}`" :style="`position: absolute; left: ${p.x}%; bottom: ${p.y}px; width: 5px; height: 5px; animation-delay: ${p.d}s`"></span></template>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <div class="card">
      <div class="ch"><h3>Состояние наборов данных · 28 дней</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 14px; font-size: 12px; color: #4B4E57">
          <span style="display: flex; align-items: center; gap: 6px"><i class="d-ok" style="width: 9px; height: 9px; border-radius: 50%"></i>пройдено</span>
          <span style="display: flex; align-items: center; gap: 6px"><i class="d-warn" style="width: 9px; height: 9px; border-radius: 50%"></i>предупреждения</span>
          <span style="display: flex; align-items: center; gap: 6px"><i class="d-fail" style="width: 9px; height: 9px; border-radius: 50%"></i>нарушения</span>
          <span style="display: flex; align-items: center; gap: 6px"><i class="d-none" style="width: 9px; height: 9px; border-radius: 50%"></i>не запускалось</span>
          <span style="display: flex; align-items: center; gap: 6px"><i class="d-prof" style="width: 9px; height: 9px; border-radius: 50%"></i>профилирование</span>
        </div>
      </div>
      <div class="cb tw">
        <div style="min-width: 760px; display: flex; flex-direction: column; gap: 6px">
          <template v-for="(h, hIndex) in vm.heat" :key="hIndex">
            <div class="row" style="display: grid; grid-template-columns: 180px 1fr 60px; gap: 16px; align-items: center; padding: 3px 0; border-radius: 6px">
              <span class="m" style="font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{{ h.name }}</span>
              <div style="display: grid; grid-template-columns: repeat(28, minmax(0, 1fr)); gap: 4px; justify-items: center">
                <template v-for="(c, cIndex) in h.cells" :key="cIndex"><span :class="`dot ${c.cls}`" :style="`width: 12px; height: 12px; animation-delay: ${c.d}s`" :title="c.t"></span></template>
              </div>
              <span class="num" style="font-size: 13px; text-align: right; font-weight: 600">{{ h.score }}</span>
            </div>
          </template>
          <div style="display: grid; grid-template-columns: 180px 1fr 60px; gap: 16px; font-size: 11px; color: #74777F"><span></span><span class="m" style="display: flex; justify-content: space-between"><span>18.09</span><span>01.10</span><span>15.10</span></span><span class="m" style="text-align: right">индекс</span></div>
        </div>
      </div>
    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 16px">
      <div class="card" style="flex: 3 1 520px">
        <div class="ch"><h3>Результаты правил последней проверки</h3><span style="font-size: 12px; color: #74777F">одна точка — одно правило · 96 из 601</span></div>
        <div class="cb">
          <div style="position: relative; height: 180px; border-bottom: 1px solid #E4E4DE">
            <div style="position: absolute; left: 50%; top: 0; bottom: 0; border-left: 1px dashed #C9C9C2"></div>
            <span style="position: absolute; left: 50%; top: 0; margin-left: 6px; font-size: 11px; color: #74777F">порог 95%</span>
            <template v-for="(s, sIndex) in vm.swarm" :key="sIndex"><span :class="`dot ${s.c}`" :style="`position: absolute; left: ${s.x}%; bottom: ${s.y}px; width: ${s.sz}px; height: ${s.sz}px; margin-left: -4px; animation-delay: ${s.d}s`" :title="s.t"></span></template>
          </div>
          <div class="m" style="display: flex; justify-content: space-between; padding-top: 8px; font-size: 11px; color: #74777F"><span>90%</span><span>92.5%</span><span>95%</span><span>97.5%</span><span>100% пройдено строк</span></div>
        </div>
      </div>
      <div class="card" style="flex: 2 1 360px">
        <div class="ch"><h3>Открытые инциденты</h3><button type="button" class="btn sm ghost" @click="vm.goInc">Все 13</button></div>
        <div class="cb" style="display: flex; flex-direction: column; padding-top: 8px">
          <template v-for="(i, iIndex) in vm.incTop" :key="iIndex">
            <div style="display: grid; grid-template-columns: 8px 1fr auto; gap: 12px; align-items: center; padding: 12px 0; border-bottom: 1px solid #EEEEE9">
              <span :style="`width: 8px; height: 8px; border-radius: 50%; background: ${i.bar}`"></span>
              <div style="display: flex; flex-direction: column; gap: 2px; min-width: 0"><span style="font-size: 14px; font-weight: 500">{{ i.title }}</span><span class="m t3" style="font-size: 12px">{{ i.ds }} · {{ i.col }}</span></div>
              <span style="font-size: 12px; color: #74777F">{{ i.when }}</span>
            </div>
          </template>
        </div>
      </div>
    </div>

    <div class="card" style="padding: 18px 20px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px 20px; background: #0E0F12; color: #F4F4F0; border-color: #0E0F12">
      <span style="width: 8px; height: 8px; border-radius: 50%; background: #C9EC5F"></span>
      <span style="font-size: 15px; font-weight: 600">{{ vm.sugCount }} правил предложено по обновлённым профилям</span>
      <span class="m" style="font-size: 12px; color: #8C8F97">sales.orders · crm.customers · finance.ledger</span>
      <button type="button" class="btn paper" @click="vm.goRules" style="margin-left: auto">Рассмотреть</button>
    </div>
  </div>
</template>
