<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <div class="scr">
    <div class="rbar"></div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr)); gap: 16px">
      <div class="card" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Регламентных заданий</span><span class="num" style="font-size: 26px; font-weight: 600">14</span></div>
      <div class="card" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Выполнено сегодня</span><span class="num" style="font-size: 26px; font-weight: 600">9 / 14</span></div>
      <div class="card" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Соблюдение SLA · 30 дней</span><span class="num" style="font-size: 26px; font-weight: 600">97.8%</span></div>
      <div class="card" style="padding: 16px 18px; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Следующее задание</span><span class="num" style="font-size: 26px; font-weight: 600">10:00</span></div>
    </div>
    <div class="card">
      <div class="ch"><h3>План на 15 октября</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 14px; font-size: 12px; color: #4B4E57">
          <span style="display: flex; align-items: center; gap: 6px"><i class="d-ok" style="width: 9px; height: 9px; border-radius: 50%"></i>выполнено</span>
          <span style="display: flex; align-items: center; gap: 6px"><i class="d-fail" style="width: 9px; height: 9px; border-radius: 50%"></i>с нарушениями</span>
          <span style="display: flex; align-items: center; gap: 6px"><i class="d-pend" style="width: 9px; height: 9px; border-radius: 50%"></i>запланировано</span>
        </div>
      </div>
      <div class="cb tw">
        <div style="min-width: 760px; position: relative">
          <div style="position: absolute; left: calc(180px + 16px + (100% - 196px) * 0.404); top: 0; bottom: 22px; border-left: 1.5px solid #C9EC5F; z-index: 1"></div>
          <span class="m" style="position: absolute; left: calc(180px + 22px + (100% - 196px) * 0.404); top: -2px; font-size: 11px; color: #4D6410">09:41</span>
          <div style="display: flex; flex-direction: column; gap: 4px; padding-top: 16px">
            <template v-for="(r, rIndex) in vm.plan" :key="rIndex">
              <div class="row" style="display: grid; grid-template-columns: 180px 1fr; gap: 16px; align-items: center; height: 34px; border-radius: 6px">
                <span class="m" style="font-size: 12px">{{ r.name }}</span>
                <div style="position: relative; height: 34px; background-image: repeating-linear-gradient(90deg, #EEEEE9 0 1px, transparent 1px calc(100% / 24))">
                  <template v-for="(p, pIndex) in r.pts" :key="pIndex"><span :class="`dot ${p.c}`" :style="`position: absolute; left: ${p.x}%; top: 11px; width: 12px; height: 12px; margin-left: -6px; animation-delay: ${p.d}s`" :title="p.t"></span></template>
                </div>
              </div>
            </template>
          </div>
          <div class="m" style="display: grid; grid-template-columns: 180px 1fr; gap: 16px; padding-top: 6px; font-size: 11px; color: #74777F"><span></span><span style="display: flex; justify-content: space-between"><span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span></span></div>
        </div>
      </div>
    </div>
    <div class="card tw">
      <div style="min-width: 940px">
        <div class="th" style="display: grid; grid-template-columns: minmax(180px, 1.4fr) 1.2fr 150px 100px 130px 150px 120px; gap: 16px; padding: 14px 20px"><span>Набор данных</span><span>Периодичность</span><span>Следующий запуск</span><span>SLA</span><span>Ответственный</span><span>Уведомления</span><span>Статус</span></div>
        <template v-for="(s, sIndex) in vm.sched" :key="sIndex">
          <div class="row" style="display: grid; grid-template-columns: minmax(180px, 1.4fr) 1.2fr 150px 100px 130px 150px 120px; gap: 16px; align-items: center; padding: 12px 20px; border-top: 1px solid #EEEEE9">
            <span class="m" style="font-size: 13px; font-weight: 600">{{ s.ds }}</span>
            <span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 13px">{{ s.freq }}</span><span class="m" style="font-size: 11px; color: #74777F">{{ s.cron }}</span></span>
            <span class="num" style="font-size: 13px">{{ s.next }}</span>
            <span class="num" style="font-size: 13px">{{ s.sla }}</span>
            <span style="font-size: 13px; color: #4B4E57">{{ s.owner }}</span>
            <span style="font-size: 13px; color: #4B4E57">{{ s.notify }}</span>
            <span><span :class="`st ${s.st}`"><i></i>{{ s.stl }}</span></span>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
