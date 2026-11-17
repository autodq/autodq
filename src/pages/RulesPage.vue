<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div style="display: flex; flex-wrap: wrap; gap: 16px">
      <div class="card" style="flex: 3 1 600px; min-width: 0">
        <div class="ch"><h3>Путь правил: от профиля до результата</h3><span style="font-size: 12px; color: #74777F">все наборы · 30 дней</span></div>
        <div class="cb">
          <svg class="flow" viewBox="0 0 900 250" aria-hidden="true" style="width: 100%; height: auto; display: block; overflow: visible">
            <path :d="vm.fl.b1" fill="#0E0F12" fill-opacity=".08"></path>
            <path :d="vm.fl.b2" fill="#AEB4C2" fill-opacity=".25"></path>
            <path :d="vm.fl.b3" fill="#0E0F12" fill-opacity=".08" style="animation-delay: .15s"></path>
            <path :d="vm.fl.b4" fill="#A6CC34" fill-opacity=".35" style="animation-delay: .15s"></path>
            <path :d="vm.fl.b5" fill="#AEB4C2" fill-opacity=".25" style="animation-delay: .15s"></path>
            <path :d="vm.fl.b6" fill="#0E0F12" fill-opacity=".08" style="animation-delay: .3s"></path>
            <path :d="vm.fl.b7" fill="#E0553A" fill-opacity=".3" style="animation-delay: .3s"></path>
            <rect :x="vm.fl.n0.x" :y="vm.fl.n0.y" width="12" :height="vm.fl.n0.h" rx="3" fill="#6B7488"></rect>
            <rect :x="vm.fl.n1a.x" :y="vm.fl.n1a.y" width="12" :height="vm.fl.n1a.h" rx="3" fill="#0E0F12"></rect>
            <rect :x="vm.fl.n1b.x" :y="vm.fl.n1b.y" width="12" :height="vm.fl.n1b.h" rx="3" fill="#AEB4C2"></rect>
            <rect :x="vm.fl.n2a.x" :y="vm.fl.n2a.y" width="12" :height="vm.fl.n2a.h" rx="3" fill="#0E0F12"></rect>
            <rect :x="vm.fl.n2b.x" :y="vm.fl.n2b.y" width="12" :height="vm.fl.n2b.h" rx="3" fill="#A6CC34"></rect>
            <rect :x="vm.fl.n2c.x" :y="vm.fl.n2c.y" width="12" :height="vm.fl.n2c.h" rx="3" fill="#AEB4C2"></rect>
            <rect :x="vm.fl.n3a.x" :y="vm.fl.n3a.y" width="12" :height="vm.fl.n3a.h" rx="3" fill="#0E0F12"></rect>
            <rect :x="vm.fl.n3b.x" :y="vm.fl.n3b.y" width="12" :height="vm.fl.n3b.h" rx="3" fill="#E0553A"></rect>
            <text :x="vm.fl.n0.lx" :y="vm.fl.n0.ly"><tspan class="n">212</tspan><tspan dx="8">колонок</tspan></text>
            <text :x="vm.fl.n1a.lx" :y="vm.fl.n1a.ly"><tspan class="n">148</tspan><tspan dx="8">предложено</tspan></text>
            <text :x="vm.fl.n1b.lx" :y="vm.fl.n1b.ly"><tspan class="n">64</tspan><tspan dx="8">без правил</tspan></text>
            <text :x="vm.fl.n2a.lx" :y="vm.fl.n2a.ly"><tspan class="n">112</tspan><tspan dx="8">принято</tspan></text>
            <text :x="vm.fl.n2b.lx" :y="vm.fl.n2b.ly"><tspan class="n">15</tspan><tspan dx="8">на рассмотрении</tspan></text>
            <text :x="vm.fl.n2c.lx" :y="vm.fl.n2c.ly"><tspan class="n">21</tspan><tspan dx="8">отклонено</tspan></text>
            <text :x="vm.fl.n3a.lx" :y="vm.fl.n3a.ly"><tspan class="n">104</tspan><tspan dx="8">без нарушений</tspan></text>
            <text :x="vm.fl.n3b.lx" :y="vm.fl.n3b.ly"><tspan class="n">8</tspan><tspan dx="8">с нарушениями</tspan></text>
          </svg>
        </div>
      </div>
      <div class="card" style="flex: 2 1 380px; min-width: 0">
        <div class="ch"><h3>Уверенность предложенных правил</h3><span style="font-size: 12px; color: #74777F">148 правил</span></div>
        <div class="cb">
          <div style="position: relative; height: 170px; border-bottom: 1px solid #E4E4DE">
            <div style="position: absolute; left: 60%; top: 0; bottom: 0; border-left: 1px dashed #C9C9C2"></div>
            <span style="position: absolute; left: 60%; top: 0; margin-left: 6px; font-size: 11px; color: #74777F">автопринятие ≥ 0.90</span>
            <template v-for="(s, sIndex) in vm.confSwarm" :key="sIndex"><span :class="`dot ${s.c}`" :style="`position: absolute; left: ${s.x}%; bottom: ${s.y}px; width: 7px; height: 7px; margin-left: -3.5px; animation-delay: ${s.d}s`"></span></template>
          </div>
          <div class="m" style="display: flex; justify-content: space-between; padding-top: 8px; font-size: 11px; color: #74777F"><span>0.75</span><span>0.80</span><span>0.85</span><span>0.90</span><span>0.95</span><span>1.00</span></div>
          <div style="display: flex; flex-wrap: wrap; gap: 14px; padding-top: 12px; font-size: 12px; color: #4B4E57">
            <span style="display: flex; align-items: center; gap: 6px"><i class="d-ok" style="width: 8px; height: 8px; border-radius: 50%"></i>принято</span>
            <span style="display: flex; align-items: center; gap: 6px"><i class="d-sug" style="width: 8px; height: 8px; border-radius: 50%"></i>на рассмотрении</span>
            <span style="display: flex; align-items: center; gap: 6px"><i class="d-rej" style="width: 8px; height: 8px; border-radius: 50%"></i>отклонено</span>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="cb" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(240px, 100%), 1fr)); gap: 16px 28px">
        <template v-for="(d, dIndex) in vm.dimStats" :key="dIndex">
          <div style="display: flex; flex-direction: column; gap: 7px">
            <div style="display: flex; justify-content: space-between; gap: 8px"><span style="font-size: 13px">{{ d.name }}</span><span class="num" style="font-size: 13px; font-weight: 600">{{ d.total }}</span></div>
            <div style="display: flex; height: 6px; gap: 2px; border-radius: 3px; overflow: hidden; background: #EEEEE9">
              <span class="hbar" :style="`width: ${d.aw}%; background: #0E0F12`"></span><span class="hbar" :style="`width: ${d.sw}%; background: #A6CC34; animation-delay: .2s`"></span>
            </div>
            <span style="font-size: 12px; color: #74777F">{{ d.a }} активно · {{ d.s }} на рассмотрении</span>
          </div>
        </template>
      </div>
    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center">
      <div class="seg">
        <div class="sp" :style="`width: 168px; transform: translateX(${vm.rtabX})`"></div>
        <template v-for="(t, tIndex) in vm.rtabs" :key="tIndex"><button type="button" :class="t.cls" @click="t.go" style="width: 168px">{{ t.label }}</button></template>
      </div>
      <span style="font-size: 13px; color: #74777F; margin-left: auto">sales.orders</span>
      <button type="button" class="btn ink" @click="vm.acceptAll" :disabled="!vm.rulePending">Принять с уверенностью ≥ 0.90</button>
    </div>
    <div class="card tw">
      <div style="min-width: 1000px">
        <div class="th rule" style="border-top: 0; padding-top: 14px; padding-bottom: 10px"><span></span><span>Правило</span><span>Измерение</span><span>Уверенность</span><span style="text-align: right">Действие</span></div>
        <template v-for="(r, rIndex) in vm.rulesView" :key="rIndex">
          <div class="rule">
            <button type="button" :class="`ck ${r.ckOn}`" @click="r.toggle" aria-label="Отметить правило"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#C9EC5F" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l5 5 9-10"></path></svg></button>
            <button type="button" class="rowbtn" @click="r.open" style="display: flex; flex-direction: column; gap: 3px; min-width: 0">
              <span class="m" style="font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{{ r.expr }}</span>
              <span style="font-size: 12px; color: #74777F; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">{{ r.why }}</span>
            </button>
            <span><span class="tag" style="font-family: 'Onest Variable', sans-serif">{{ r.dim }}</span></span>
            <span style="display: grid; grid-template-columns: 1fr 38px; gap: 10px; align-items: center"><span class="conf"><b class="hbar" :style="`width: ${r.confW}%`"></b></span><span class="num" style="font-size: 13px; font-weight: 600">{{ r.conf }}</span></span>
            <span style="display: flex; gap: 8px; justify-content: flex-end">
              <template v-if="r.isSug"><span style="display: flex; gap: 8px"><button type="button" class="btn sm ghost" @click="r.reject">Отклонить</button><button type="button" class="btn sm ink" @click="r.accept">Принять</button></span></template>
              <template v-if="r.isAct"><span style="display: flex; gap: 8px; align-items: center"><span class="st ok"><i></i>Активно</span><button type="button" class="btn sm ghost" @click="r.open">Изменить</button></span></template>
              <template v-if="r.isRej"><button type="button" class="btn sm ghost" @click="r.accept">Восстановить</button></template>
            </span>
          </div>
        </template>
        <template v-if="vm.rulesEmpty">
          <div style="padding: 40px 20px; text-align: center; border-top: 1px solid #EEEEE9; font-size: 14px; color: #74777F">Нет правил в этом статусе.</div>
        </template>
      </div>
    </div>
  </div>
</template>
