<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center">
      <span style="font-size: 13px; color: #74777F">Демонстрация состояний:</span>
      <div class="seg">
        <div class="sp" :style="`width: 116px; transform: translateX(${vm.licX})`"></div>
        <template v-for="(t, tIndex) in vm.licTabs" :key="tIndex"><button type="button" :class="t.cls" @click="t.go" style="width: 116px">{{ t.label }}</button></template>
      </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(380px, 100%), 1fr)); gap: 16px">
      <div class="card" style="padding: 24px; display: flex; flex-direction: column; gap: 22px; background: #0E0F12; color: #F4F4F0; border-color: #0E0F12">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 16px">
          <div style="display: flex; flex-direction: column; gap: 4px"><span style="font-size: 12px; color: #8C8F97">Тариф</span><span style="font-size: 30px; font-weight: 600; letter-spacing: -0.02em">{{ vm.lic.plan }}</span></div>
          <span :class="`st ${vm.lic.cls}`"><i></i>{{ vm.lic.badge }}</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px">
          <div style="display: flex; flex-direction: column; gap: 3px"><span style="font-size: 12px; color: #8C8F97">{{ vm.lic.dateLabel }}</span><span class="num" style="font-size: 17px; font-weight: 600">{{ vm.lic.date }}</span></div>
          <div style="display: flex; flex-direction: column; gap: 3px"><span style="font-size: 12px; color: #8C8F97">Лицензионный ключ</span><span class="num" style="font-size: 17px; font-weight: 600">ADQ-••••-••••-T3LP</span></div>
          <div style="display: flex; flex-direction: column; gap: 3px"><span style="font-size: 12px; color: #8C8F97">Организация</span><span style="font-size: 15px; font-weight: 600">[Название организации]</span></div>
          <div style="display: flex; flex-direction: column; gap: 3px"><span style="font-size: 12px; color: #8C8F97">Тип размещения</span><span style="font-size: 15px; font-weight: 600">On-premise</span></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px"><div style="height: 4px; border-radius: 2px; background: #24262C; overflow: hidden"><div class="hbar" :style="`height: 100%; width: ${vm.lic.sidePct}%; background: ${vm.lic.sideBar}`"></div></div><span style="font-size: 12px; color: #8C8F97">{{ vm.lic.sideNote }}</span></div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap">
          <button type="button" class="btn paper" disabled title="Недоступно в деморежиме">{{ vm.lic.cta }}</button>
          <a class="btn" href="#/login" style="background: #1C1D22; color: #F4F4F0">Экран входа</a>
        </div>
      </div>
      <div class="card">
        <div class="ch"><h3>Использование лимитов</h3><span style="font-size: 12px; color: #74777F">до {{ vm.lic.date }}</span></div>
        <div class="cb" style="display: flex; flex-direction: column; gap: 18px">
          <template v-for="(u, uIndex) in vm.usage" :key="uIndex">
            <div style="display: flex; flex-direction: column; gap: 8px">
              <div style="display: flex; justify-content: space-between; gap: 12px"><span style="font-size: 14px">{{ u.name }}</span><span class="num" style="font-size: 13px; font-weight: 600">{{ u.v }}</span></div>
              <div class="meter" style="height: 6px; border-radius: 3px"><b :style="`width: ${u.p}%; background: ${u.c}`"></b></div>
            </div>
          </template>
        </div>
      </div>
    </div>
    <div class="card tw">
      <div style="min-width: 720px">
        <div class="th" style="display: grid; grid-template-columns: minmax(220px, 1.6fr) repeat(3, 1fr); gap: 16px; padding: 14px 20px"><span>Возможности</span><span>Пробная</span><span>Team</span><span>Enterprise</span></div>
        <template v-for="(p, pIndex) in vm.plans" :key="pIndex">
          <div class="row" style="display: grid; grid-template-columns: minmax(220px, 1.6fr) repeat(3, 1fr); gap: 16px; padding: 12px 20px; border-top: 1px solid #EEEEE9; font-size: 14px"><span>{{ p.f }}</span><span style="font-size: 13px; color: #4B4E57">{{ p.a }}</span><span style="font-size: 13px; font-weight: 600">{{ p.b }}</span><span style="font-size: 13px; color: #4B4E57">{{ p.c }}</span></div>
        </template>
      </div>
    </div>
  </div>
</template>
