<script setup>
defineProps({ vm: { type: Object, required: true } })
</script>

<template>
  <template v-if="vm.hasRule">
    <button type="button" class="ovl" @click="vm.closeRule" aria-label="Закрыть панель"></button>
    <aside class="drawer" aria-label="Правило">
      <div style="padding: 18px 22px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #EEEEE9">
        <span :class="`st ${vm.sel.stCls}`"><i></i>{{ vm.sel.stl }}</span>
        <button type="button" class="btn sm ghost" @click="vm.closeRule">Закрыть</button>
      </div>
      <div style="padding: 22px; display: flex; flex-direction: column; gap: 20px">
        <div style="display: flex; flex-direction: column; gap: 6px"><span class="lbl">Правило</span><span class="m" style="font-size: 16px; font-weight: 600; line-height: 1.45">{{ vm.sel.expr }}</span></div>
        <div style="display: flex; gap: 6px; flex-wrap: wrap"><span class="tag" style="font-family: 'Onest', sans-serif">{{ vm.sel.dim }}</span><span class="tag">{{ vm.sel.col }}</span><span class="tag">уверенность {{ vm.sel.conf }}</span></div>
        <div style="padding: 14px 16px; border-radius: 10px; background: #F9F9F6; display: flex; flex-direction: column; gap: 6px"><span class="lbl">Основание</span><span style="font-size: 14px; line-height: 1.55">{{ vm.sel.why }}</span></div>
        <div style="display: flex; flex-direction: column; gap: 8px"><label for="thr" style="font-size: 13px; font-weight: 600">Порог</label><input id="thr" type="text" :value="vm.sel.thr" :readOnly="true" class="m" style="height: 42px; border-radius: 9px; border: 1px solid #DCDCD5; padding: 0 12px; font-size: 13px"></div>
        <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">
          <div style="padding: 12px 14px; border-radius: 10px; border: 1px solid #EEEEE9; display: flex; flex-direction: column; gap: 3px"><span class="lbl">На данных профиля</span><span class="num" style="font-size: 16px; font-weight: 600">{{ vm.sel.onProf }}</span></div>
          <div style="padding: 12px 14px; border-radius: 10px; border: 1px solid #EEEEE9; display: flex; flex-direction: column; gap: 3px"><span class="lbl">Критичность</span><span style="font-size: 16px; font-weight: 600">{{ vm.sel.crit }}</span></div>
        </div>
        <div style="display: flex; gap: 8px">
          <button type="button" class="btn ghost" @click="vm.rejectSel" style="flex: 1">Отклонить</button>
          <button type="button" class="btn ink" @click="vm.acceptSel" style="flex: 1"><i class="dot"></i>Принять</button>
        </div>
      </div>
    </aside>
  </template>

  <template v-if="vm.genOn">
    <div class="ovl" style="cursor: default"></div>
    <div class="modal" role="dialog" aria-label="Генерация правил">
      <div style="display: flex; align-items: center; gap: 14px">
        <svg viewBox="0 0 120 120" aria-hidden="true" style="width: 36px; height: 36px; overflow: visible"><circle cx="60" cy="60" r="36" fill="none" stroke="#24262C" stroke-width="16"></circle><g class="spin"><g style="transform-box: view-box; transform-origin: 60px 60px; transform: rotate(-90deg)"><circle cx="60" cy="60" r="36" fill="none" stroke="#F4F4F0" stroke-width="16" stroke-linecap="round" pathLength="100" style="stroke-dasharray: 22 78; stroke-dashoffset: 22"></circle></g><circle cx="60" cy="24" r="10" fill="#C9EC5F"></circle></g></svg>
        <span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 16px; font-weight: 600">Генерация правил</span><span class="m" style="font-size: 12px; color: #8C8F97">{{ vm.ds.name }} · 24 колонки</span></span>
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px">
        <template v-for="(g, gIndex) in vm.genSteps" :key="gIndex"><div :class="`stp ${g.cls}`"><i></i>{{ g.l }}</div></template>
      </div>
    </div>
  </template>

  <template v-if="vm.toast">
    <div class="toast" role="status">
      <span style="width: 8px; height: 8px; border-radius: 50%; background: #C9EC5F"></span>
      <span style="display: flex; flex-direction: column; gap: 1px"><span style="font-size: 14px; font-weight: 600">Проверка № 2815 завершена</span><span style="font-size: 12px; color: #8C8F97">176 без нарушений · 6 предупреждений · 2 нарушения</span></span>
      <button type="button" class="btn sm paper" @click="vm.goInc">Инциденты</button>
    </div>
  </template>
</template>
