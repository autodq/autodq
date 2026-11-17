<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(440px, 100%), 1fr)); gap: 16px">
      <div class="card">
        <div class="ch"><h3>Источники данных</h3><button type="button" class="btn sm ink" disabled title="Недоступно в деморежиме">Добавить источник</button></div>
        <div class="cb" style="display: flex; flex-direction: column; padding-top: 8px">
          <template v-for="(s, sIndex) in vm.sources" :key="sIndex">
            <div style="display: grid; grid-template-columns: 38px 1fr auto; gap: 14px; align-items: center; padding: 11px 0; border-bottom: 1px solid #EEEEE9">
              <span class="m" style="width: 38px; height: 38px; border-radius: 9px; background: #F4F4F0; border: 1px solid #E4E4DE; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600">{{ s.ab }}</span>
              <span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 600">{{ s.name }}</span><span class="m" style="font-size: 12px; color: #74777F">{{ s.host }}</span></span>
              <span :class="`st ${s.st}`"><i></i>{{ s.stl }}</span>
            </div>
          </template>
        </div>
      </div>
      <div class="card">
        <div class="ch"><h3>Генерация правил</h3></div>
        <div class="cb" style="display: flex; flex-direction: column; gap: 18px">
          <div style="display: flex; flex-direction: column; gap: 8px"><div style="display: flex; justify-content: space-between"><label for="r1" style="font-size: 14px">Минимальная уверенность для предложения</label><span class="num" style="font-size: 13px; font-weight: 600">0.75</span></div><input id="r1" type="range" min="0" max="100" value="75" disabled></div>
          <div style="display: flex; flex-direction: column; gap: 8px"><div style="display: flex; justify-content: space-between"><label for="r2" style="font-size: 14px">Границы диапазонов по квантилям</label><span class="num" style="font-size: 13px; font-weight: 600">p0.5 – p99.5</span></div><input id="r2" type="range" min="0" max="100" value="90" disabled></div>
          <div style="display: flex; flex-direction: column; gap: 8px"><div style="display: flex; justify-content: space-between"><label for="r3" style="font-size: 14px">Порог дрейфа распределения, PSI</label><span class="num" style="font-size: 13px; font-weight: 600">0.20</span></div><input id="r3" type="range" min="0" max="100" value="40" disabled></div>
          <div style="display: flex; align-items: center; gap: 14px"><span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 600">Автоматически принимать при уверенности ≥ 0.98</span><span style="font-size: 13px; color: #74777F">Остальные правила требуют подтверждения</span></span><button type="button" :class="`tg ${vm.tgAuto}`" @click="vm.toggleAuto" aria-label="Автопринятие" style="margin-left: auto"></button></div>
        </div>
      </div>
      <div class="card">
        <div class="ch"><h3>Уведомления</h3></div>
        <div class="cb" style="display: flex; flex-direction: column; gap: 14px">
          <div style="display: flex; align-items: center; gap: 14px"><span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 600">Telegram</span><span style="font-size: 12px; color: #74777F">нарушения критичных правил</span></span><button type="button" :class="`tg ${vm.tgTg}`" @click="vm.toggleTg" aria-label="Telegram" style="margin-left: auto"></button></div>
          <div style="display: flex; align-items: center; gap: 14px"><span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 600">Электронная почта</span><span style="font-size: 12px; color: #74777F">ежедневная сводка в 09:00</span></span><button type="button" :class="`tg ${vm.tgMail}`" @click="vm.toggleMail" aria-label="Почта" style="margin-left: auto"></button></div>
          <div style="display: flex; align-items: center; gap: 14px"><span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 600">Webhook</span><span style="font-size: 12px; color: #74777F">интеграция с Airflow и CI</span></span><button type="button" :class="`tg ${vm.tgHook}`" @click="vm.toggleHook" aria-label="Webhook" style="margin-left: auto"></button></div>
        </div>
      </div>
      <div class="card">
        <div class="ch"><h3>Пользователи и роли</h3><button type="button" class="btn sm ghost" disabled title="Недоступно в деморежиме">Пригласить</button></div>
        <div class="cb" style="display: flex; flex-direction: column; padding-top: 8px">
          <template v-for="(t, tIndex) in vm.team" :key="tIndex">
            <div style="display: grid; grid-template-columns: 32px 1fr auto; gap: 12px; align-items: center; padding: 10px 0; border-bottom: 1px solid #EEEEE9">
              <span class="m" :style="`width: 32px; height: 32px; border-radius: 50%; background: ${t.bg}; color: ${t.fg}; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600`">{{ t.ab }}</span>
              <span style="display: flex; flex-direction: column; gap: 1px"><span style="font-size: 14px; font-weight: 600">{{ t.name }}</span><span style="font-size: 12px; color: #74777F">{{ t.mail }}</span></span>
              <span class="tag" style="font-family: 'Onest Variable', sans-serif">{{ t.role }}</span>
            </div>
          </template>
        </div>
      </div>
    </div>
    <div class="card tw">
      <div class="ch"><h3>Журнал действий</h3><span style="font-size: 12px; color: #74777F">хранится 1 год</span></div>
      <div style="min-width: 760px; padding: 8px 0 6px">
        <template v-for="(a, aIndex) in vm.actlog" :key="aIndex">
          <div class="row" style="display: grid; grid-template-columns: 140px 160px 1fr; gap: 16px; padding: 10px 20px; border-top: 1px solid #EEEEE9; font-size: 13px"><span class="num" style="color: #74777F">{{ a.t }}</span><span>{{ a.u }}</span><span>{{ a.a }}</span></div>
        </template>
      </div>
    </div>
  </div>
</template>
