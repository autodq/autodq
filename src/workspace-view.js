import { DS, COLS, RULES, REP } from "./demo-data.js";

function dotLine(vals, lo, hi, h, cls) {
    return vals.map((v, i) => ({ x: (i / (vals.length - 1) * 94).toFixed(1), y: Math.round((v - lo) / (hi - lo) * (h - 6)), c: cls ? cls(v, i) : 'd-ok', d: (0.3 + i * 0.03).toFixed(2) }));
  }

function buildCheckOrder() {
  let seed = 3;
  const keys = Array.from({ length: 184 }, (_, index) => {
    seed = (seed * 9301 + 49297) % 233280;
    return index + seed / 233280 * 70;
  });
  const order = keys.map((_, index) => index).sort((a, b) => keys[a] - keys[b]);
  const rank = [];
  order.forEach((cell, index) => { rank[cell] = index; });
  return rank;
}

const checkOrder = buildCheckOrder();

export function buildWorkspaceView(S, actions) {
  const scr = S.screen;
  const navOf = scr === 'profile' ? 'sets' : scr;
  let seed = 11; const rnd = () => { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
  const icons = {
    dash: 'M4 4h7v9H4zM13 4h7v5h-7zM13 11h7v9h-7zM4 15h7v5H4z',
    sets: 'M4 6c0-1.1 3.6-2 8-2s8 .9 8 2-3.6 2-8 2-8-.9-8-2zM4 6v12c0 1.1 3.6 2 8 2s8-.9 8-2V6M4 12c0 1.1 3.6 2 8 2s8-.9 8-2',
    rules: 'M10 6h10M10 12h10M10 18h10M4 6l1.2 1.2L7.5 5M4 12l1.2 1.2 2.3-2.2M4 18l1.2 1.2 2.3-2.2',
    checks: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM10 8.5l5 3.5-5 3.5z',
    sched: 'M4 6h16v14H4zM4 10h16M8 3v4M16 3v4M8 14h3M13 14h3M8 17h3',
    audit: 'M4 20V11M10 20V5M16 20v-6M21 20H3',
    inc: 'M12 4l9 15H3zM12 10v4M12 17h.01',
    reports: 'M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6',
    lic: 'M12 3l7 3v6c0 4-3 7.5-7 9-4-1.5-7-5-7-9V6zM9 12l2 2 4-4',
    settings: 'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19 12h2M3 12h2M12 3v2M12 19v2M17 7l1.4-1.4M5.6 18.4L7 17M17 17l1.4 1.4M5.6 5.6L7 7'
  };
  const sugCount = Object.values(S.rs).filter((status) => status === 'sug').length;
  const n1 = [['dash', 'Обзор'], ['sets', 'Наборы данных'], ['rules', 'Правила'], ['checks', 'Проверки'], ['sched', 'Регламент'], ['audit', 'Аудит'], ['inc', 'Инциденты'], ['reports', 'Отчёты']];
  const n2 = [['lic', 'Лицензия'], ['settings', 'Настройки']];
  const mk = (a) => ({ label: a[1], d: icons[a[0]], cls: navOf === a[0] ? 'on' : '', go: () => actions.go(a[0]),
    hasBadge: a[0] === 'rules' || a[0] === 'inc', badge: a[0] === 'rules' ? String(sugCount) : '13', bcls: a[0] === 'rules' ? 'hi' : '' });
  const all = n1.map((a) => a[0]).concat(n2.map((a) => a[0]));
  const idx = all.indexOf(navOf);
  const pillY = idx < 8 ? idx * 46 : 8 * 46 + 36 + (idx - 8) * 46;
  const titles = { dash: 'Обзор', sets: 'Наборы данных', profile: 'Профиль набора', rules: 'Правила качества', checks: 'Проверки', sched: 'Регламент проверок', audit: 'Аудит качества', inc: 'Инциденты', reports: 'Отчёты', lic: 'Лицензия', settings: 'Настройки' };

  const L = {
    active: { plan: 'Team', badge: 'Лицензия активна', cls: 'ok', short: '214 дн.', sideColor: '#C9EC5F', sidePct: 41, sideBar: '#C9EC5F', sideNote: 'до 17.05.2027 · 18 из 25 наборов', banner: false, dateLabel: 'Действует до', date: '17.05.2027', cta: 'Управление тарифом' },
    trial: { plan: 'Пробная', badge: 'Пробный период · 9 дн.', cls: 'sug', short: '9 дн.', sideColor: '#C9CBD1', sidePct: 64, sideBar: '#AEB4C2', sideNote: 'до 24.10.2026 · 5 из 5 наборов', banner: true, bBg: '#EDEFF3', bFg: '#2B3243', bTitle: 'Пробный период до 24.10.2026.', bText: 'Лимит в 5 наборов данных исчерпан.', dateLabel: 'Действует до', date: '24.10.2026', cta: 'Выбрать тариф' },
    expiring: { plan: 'Team', badge: 'Истекает через 12 дн.', cls: 'warn', short: '12 дн.', sideColor: '#E3A23B', sidePct: 96, sideBar: '#E3A23B', sideNote: 'до 27.10.2026 · 18 из 25 наборов', banner: true, bBg: '#FBF1DD', bFg: '#5A3C05', bTitle: 'Срок лицензии истекает 27.10.2026.', bText: 'После этой даты регламентные проверки будут остановлены.', dateLabel: 'Действует до', date: '27.10.2026', cta: 'Продлить' },
    expired: { plan: 'Team', badge: 'Лицензия истекла', cls: 'fail', short: 'истекла', sideColor: '#F08B73', sidePct: 100, sideBar: '#E0553A', sideNote: '13.10.2026 · режим чтения', banner: true, bBg: '#FBE7E2', bFg: '#6E1F0F', bTitle: 'Лицензия истекла 13.10.2026.', bText: 'Проверки и генерация правил недоступны, история и отчёты доступны для чтения.', dateLabel: 'Истекла', date: '13.10.2026', cta: 'Продлить' }
  }[S.lic];
  const licIds = ['active', 'trial', 'expiring', 'expired'];
  const licLabels = ['Активна', 'Пробная', 'Истекает', 'Истекла'];

  const sets = DS.map((d, i) => {
    const lo = Math.min.apply(null, d.t) - 1, hi = Math.max.apply(null, d.t) + 1;
    return Object.assign({}, d, { pts: d.st === 'run' ? [] : d.t.map((v, j) => ({ x: (j / 11 * 94).toFixed(1), y: Math.round((v - lo) / (hi - lo) * 16), c: v < 80 ? 'd-fail' : (v < 95 ? 'd-warn' : 'd-ok') })), open: () => actions.openSet(i) });
  });

  const heat = DS.map((d, r) => ({ name: d.name, score: d.score, cells: Array.from({ length: 28 }, (_, c) => {
    const x = rnd(); let cls = 'd-ok';
    if (d.name === 'finance.ledger') cls = c > 25 ? 'd-prof' : 'd-none';
    else if (d.name === 'logistics.shipments') cls = c > 18 ? (x < .55 ? 'd-fail' : 'd-warn') : (x < .15 ? 'd-warn' : 'd-ok');
    else if (d.st === 'warn') cls = x < .22 ? 'd-warn' : (x < .25 ? 'd-fail' : 'd-ok');
    else cls = x < .05 ? 'd-warn' : (x < .08 ? 'd-none' : 'd-ok');
    return { cls: cls, d: (c * 0.012 + r * 0.03).toFixed(3), t: d.name + ' · ' + (c + 18) + ' день' };
  }) }));

  const kp = (base, amp, n) => Array.from({ length: n }, (_, i) => base + Math.sin(i / 2) * amp + rnd() * amp);
  const kpis = [
    { l: 'Наборов данных', v: '8', d: '+1 за неделю', c: '#74777F', pts: dotLine([6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8], 5, 9, 30) },
    { l: 'Активных правил', v: '601', d: '+38 за неделю', c: '#4D6410', pts: dotLine([540, 548, 552, 560, 561, 566, 570, 572, 580, 584, 590, 596, 598, 601], 530, 610, 30) },
    { l: 'Проверок за сутки', v: '46', d: 'по регламенту 44', c: '#74777F', pts: dotLine(kp(44, 2, 14), 38, 52, 30) },
    { l: 'Открытых инцидентов', v: '13', d: '+4 за сутки', c: '#A8361E', pts: dotLine([7, 6, 8, 7, 6, 7, 9, 8, 8, 9, 10, 9, 11, 13], 4, 14, 30, (v) => v >= 11 ? 'd-fail' : 'd-ok') }
  ];

  // beeswarm of rule results
  const swarmVals = [];
  for (let i = 0; i < 96; i++) { const x = rnd(); swarmVals.push(x < .55 ? 99.2 + rnd() * .8 : x < .8 ? 97.5 + rnd() * 1.7 : x < .92 ? 95 + rnd() * 2.5 : 90 + rnd() * 5); }
  const binsS = {}; const swarm0 = swarmVals.map((v) => {
    const b = Math.min(79, Math.floor((v - 90) / 0.125)); binsS[b] = (binsS[b] || 0) + 1;
    return { b: b, n: binsS[b] - 1, v: v };
  });
  const maxS = Math.max.apply(null, Object.keys(binsS).map((q) => binsS[q]));
  const stepS = Math.min(11, 150 / maxS);
  const swarm = swarm0.map((o) => ({ x: ((o.b + 0.5) / 80 * 100).toFixed(2), y: (4 + o.n * stepS).toFixed(1), sz: Math.min(7, stepS - 1.5).toFixed(1), c: o.v < 95 ? 'd-fail' : (o.v < 99 ? 'd-warn' : 'd-ok'), d: (0.2 + (o.v - 90) * 0.05).toFixed(2), t: o.v.toFixed(2) + '%' }));

  const INC = [
    { title: 'Значения amount вне диапазона', cls: 'Диапазон', ds: 'sales.orders', col: 'amount', cnt: '37 строк', sev: 'fail', when: '12 мин', desc: 'Выше p99.5 профиля (2 450 000), максимум 18 900 000', owner: 'Д. Нуров', sla: 'до 13:12', slaC: '#4B4E57', state: 'Новый', stc: 'fail', k: 'range' },
    { title: 'Задержка поступления данных', cls: 'Своевременность', ds: 'sales.orders', col: 'created_at', cnt: '26 ч', sev: 'warn', when: '12 мин', desc: 'Последняя запись старше допуска 24 ч; обычная задержка 2–4 ч', owner: 'Д. Нуров', sla: 'до 17:12', slaC: '#4B4E57', state: 'В работе', stc: 'sug', k: 'time' },
    { title: 'Рост доли пропусков', cls: 'Полнота', ds: 'sales.orders', col: 'discount_pct', cnt: '12.4%', sev: 'warn', when: '12 мин', desc: 'Рост с 9.8% до 12.4% при допуске 15%, третья проверка подряд', owner: 'М. Ким', sla: 'до 17:12', slaC: '#4B4E57', state: 'Новый', stc: 'fail', k: 'null' },
    { title: 'Ключи без соответствия в справочнике', cls: 'Согласованность', ds: 'logistics.shipments', col: 'customer_id', cnt: '4 102 строки', sev: 'fail', when: '2 ч', desc: 'Нет соответствия в crm.customers.id после загрузки 14.10', owner: 'Т. Абенов', sla: 'просрочено', slaC: '#A8361E', state: 'В работе', stc: 'sug', k: 'fk' },
    { title: 'Дубликаты идентификатора', cls: 'Уникальность', ds: 'logistics.shipments', col: 'shipment_id', cnt: '918 строк', sev: 'fail', when: '2 ч', desc: 'Уникальность снизилась со 100% до 99.93%', owner: 'Т. Абенов', sla: 'до 11:30', slaC: '#4B4E57', state: 'В работе', stc: 'sug', k: 'uniq' },
    { title: 'Несоответствие формату номера', cls: 'Формат', ds: 'crm.customers', col: 'phone', cnt: '211 строк', sev: 'warn', when: '1 ч', desc: 'Не соответствуют шаблону +7XXXXXXXXXX', owner: 'М. Ким', sla: 'до 16:40', slaC: '#4B4E57', state: 'Новый', stc: 'fail', k: 'fmt' },
    { title: 'Смещение распределения', cls: 'Распределение', ds: 'marketing.events', col: 'session_len', cnt: 'PSI 0.22', sev: 'warn', when: '3 ч', desc: 'Медиана выросла с 41 до 58 с после обновления трекера 13.10', owner: 'А. Сейткали', sla: '—', slaC: '#4B4E57', state: 'Решён', stc: 'ok', k: 'dist' }
  ];
  const bars = { fail: '#E0553A', warn: '#E3A23B' };
  const incAll = INC.map((i) => Object.assign({}, i, { bar: bars[i.sev], when: i.when + ' назад' }));
  const fl0 = [['all', 'Все'], ['range', 'Диапазон'], ['null', 'Полнота'], ['uniq', 'Уникальность'], ['fk', 'Согласованность'], ['fmt', 'Формат'], ['time', 'Своевременность'], ['dist', 'Распределение']];
  const incFilters = fl0.map((f) => ({ label: f[1], n: f[0] === 'all' ? INC.length : INC.filter((i) => i.k === f[0]).length, cls: S.inc === f[0] ? 'ink' : 'ghost', go: () => actions.update({ inc: f[0] }) }));
  const incView = S.inc === 'all' ? incAll : incAll.filter((i) => i.k === S.inc);

  // profile
  const flagC = { fail: '#E0553A', warn: '#E3A23B' };
  const cols = COLS.map((c, i) => ({ name: c.name, type: c.type, nulls: c.nulls, uniq: c.uniq, on: S.col === i ? 'on' : '', pick: () => actions.update({ col: i }), hasFlag: !!c.flag, flagC: flagC[c.flag] || '#0E0F12' }));
  const cc = COLS[S.col];
  const interp = (a) => { const r = []; for (let i = 0; i < 16; i++) { r.push(a[i]); r.push(i < 15 ? Math.round((a[i] + a[i + 1]) / 2) : Math.round(a[i] * 0.6)); } return r; };
  const cur = interp(cc.h), exp = interp(cc.e || cc.h);
  const MAXD = 14;
  const col = {
    name: cc.name, min: cc.min, mid: cc.mid, max: cc.max, bandTxt: cc.bandTxt,
    bandL: (cc.band[0] / 32 * 100).toFixed(2), bandW: ((cc.band[1] - cc.band[0] + 1) / 32 * 100).toFixed(2),
    bins: cur.map((h, i) => {
      const n = Math.round(h / 100 * MAXD); const inBand = i >= cc.band[0] && i <= cc.band[1]; const isOut = (cc.out || []).indexOf(i) >= 0;
      const dots = []; for (let k = 0; k < Math.max(n, isOut ? 1 : 0); k++) dots.push({ c: isOut ? 'd-fail' : (inBand ? 'd-ok' : 'd-soft'), dl: (0.1 + i * 0.015 + k * 0.02).toFixed(3) });
      const en = Math.round(exp[i] / 100 * MAXD);
      return { dots: dots, tk: 3 + en * 11 - 2, to: en > 0 ? 1 : 0 };
    }),
    stats: cc.stats.map((s) => ({ k: s[0], v: s[1] })),
    rules: cc.rules.map((r) => ({ e: r[0], w: r[1], c: r[2], s: r[3], sl: r[4] }))
  };

  // rules
  const setR = (id, v) => { const rs = Object.assign({}, S.rs); rs[id] = v; actions.update({ rs: rs }); };
  const rulesView = RULES.filter((r) => S.rs[r.id] === S.rtab).map((r) => {
    const st = S.rs[r.id];
    return { expr: r.expr, why: r.why, dim: r.dim, conf: r.conf.toFixed(2), confW: Math.round(r.conf * 100),
      isSug: st === 'sug', isAct: st === 'act', isRej: st === 'rej', ckOn: st === 'act' ? 'on' : '',
      toggle: () => setR(r.id, st === 'act' ? 'sug' : 'act'), accept: () => setR(r.id, 'act'), reject: () => setR(r.id, 'rej'), open: () => actions.update({ sel: r.id }) };
  });
  const counts = { sug: 0, act: 0, rej: 0 };
  Object.keys(S.rs).forEach((k) => { counts[S.rs[k]]++; });
  const rt = [['sug', 'На рассмотрении · ' + counts.sug], ['act', 'Активные · ' + counts.act], ['rej', 'Отклонённые · ' + counts.rej]];
  const rti = rt.map((t) => t[0]).indexOf(S.rtab);
  const selR = RULES.filter((r) => r.id === S.sel)[0];
  const selSt = selR ? S.rs[selR.id] : 'sug';
  const sel = selR ? Object.assign({}, selR, { conf: selR.conf.toFixed(2), stCls: selSt === 'act' ? 'ok' : (selSt === 'rej' ? 'idle' : 'sug'), stl: selSt === 'act' ? 'Активно' : (selSt === 'rej' ? 'Отклонено' : 'Предложено системой') }) : {};

  // flow
  const k = 200 / 212, top0 = 20, gap = 10, xs = [0, 220, 440, 660];
  const node = (x, y, n) => ({ x: x, y: y.toFixed(1), h: (n * k).toFixed(1), yy: y, hh: n * k, lx: x + 22, ly: (y + Math.min(n * k, 60) / 2 + 6).toFixed(1) });
  const n0 = node(xs[0], top0, 212);
  const n1a = node(xs[1], top0, 148); const n1b = node(xs[1], top0 + 148 * k + gap, 64);
  const n2a = node(xs[2], top0, 112); const n2b = node(xs[2], top0 + 112 * k + gap, 15); const n2c = node(xs[2], top0 + 127 * k + gap * 2, 21);
  const n3a = node(xs[3], top0, 104); const n3b = node(xs[3], top0 + 104 * k + gap, 8);
  const band = (x0, a0, b0, x1, a1, b1) => { const xm = (x0 + x1) / 2; return 'M' + x0 + ' ' + a0 + ' C' + xm + ' ' + a0 + ' ' + xm + ' ' + a1 + ' ' + x1 + ' ' + a1 + ' L' + x1 + ' ' + b1 + ' C' + xm + ' ' + b1 + ' ' + xm + ' ' + b0 + ' ' + x0 + ' ' + b0 + ' Z'; };
  const fl = {
    n0: n0, n1a: n1a, n1b: n1b, n2a: n2a, n2b: n2b, n2c: n2c, n3a: n3a, n3b: n3b,
    b1: band(12, n0.yy, n0.yy + 148 * k, xs[1], n1a.yy, n1a.yy + n1a.hh),
    b2: band(12, n0.yy + 148 * k, n0.yy + 212 * k, xs[1], n1b.yy, n1b.yy + n1b.hh),
    b3: band(xs[1] + 12, n1a.yy, n1a.yy + 112 * k, xs[2], n2a.yy, n2a.yy + n2a.hh),
    b4: band(xs[1] + 12, n1a.yy + 112 * k, n1a.yy + 127 * k, xs[2], n2b.yy, n2b.yy + n2b.hh),
    b5: band(xs[1] + 12, n1a.yy + 127 * k, n1a.yy + 148 * k, xs[2], n2c.yy, n2c.yy + n2c.hh),
    b6: band(xs[2] + 12, n2a.yy, n2a.yy + 104 * k, xs[3], n3a.yy, n3a.yy + n3a.hh),
    b7: band(xs[2] + 12, n2a.yy + 104 * k, n2a.yy + 112 * k, xs[3], n3b.yy, n3b.yy + n3b.hh)
  };
  // confidence swarm
  const confBins = {}; const confSwarm = [];
  for (let i = 0; i < 148; i++) {
    const x = rnd(); const v = x < .5 ? 0.95 + rnd() * 0.05 : x < .8 ? 0.88 + rnd() * 0.07 : 0.75 + rnd() * 0.13;
    const b = Math.min(24, Math.floor((v - 0.75) / 0.01)); confBins[b] = (confBins[b] || 0) + 1;
    const r = rnd(); const c = v >= 0.9 ? (r < .82 ? 'd-ok' : 'd-sug') : (r < .45 ? 'd-ok' : r < .7 ? 'd-sug' : 'd-rej');
    confSwarm.push({ x: ((b + 0.5) / 25 * 100).toFixed(2), y: 4 + (confBins[b] - 1) * 9, c: c, d: (0.2 + b * 0.03).toFixed(2) });
  }
  const DIMS = [['Полнота', 38, 6], ['Уникальность', 14, 2], ['Диапазон', 31, 9], ['Допустимые значения', 19, 3], ['Формат', 12, 4], ['Своевременность', 9, 2], ['Согласованность', 11, 5], ['Распределение', 14, 6]];
  const dimStats = DIMS.map((d) => ({ name: d[0], a: d[1], s: d[2], total: d[1] + d[2], aw: (d[1] / 47 * 100).toFixed(1), sw: (d[2] / 47 * 100).toFixed(1) }));

  // checks
  const p = S.ran ? Math.floor(S.p) : 0;
  const doneN = Math.round(184 * (S.ran ? S.p : 0) / 100);
  const FAILS = [41, 122], WARNS = [29, 56, 77, 98, 141, 163];
  const res = (i) => FAILS.indexOf(i) >= 0 ? 'd-fail' : (WARNS.indexOf(i) >= 0 ? 'd-warn' : 'd-ok');
  const RK = checkOrder;
  const grid = Array.from({ length: 184 }, (_, i) => { const r = RK[i]; return { c: r < doneN ? res(r) : (S.running && r < doneN + 4 ? 'd-cur' : 'd-pend') }; });
  let fail = 0, warn = 0; for (let i = 0; i < doneN; i++) { if (FAILS.indexOf(i) >= 0) fail++; else if (WARNS.indexOf(i) >= 0) warn++; }
  const logAll = [
    [1, '09:41:02', 'Запуск проверки № 2815 · 184 правила', '#C9CBD1'],
    [6, '09:41:03', 'Профиль загружен · 24 колонки', '#C9CBD1'],
    [16, '09:41:05', 'WARN  null_share(discount_pct) = 12.4%', '#E3A23B'],
    [23, '09:41:07', 'FAIL  between(amount) · 37 строк вне диапазона', '#F08B73'],
    [40, '09:41:10', 'OK    unique(order_id) · 4 812 090 из 4 812 090', '#C9EC5F'],
    [54, '09:41:12', 'WARN  freshness(created_at) = 26 ч', '#E3A23B'],
    [67, '09:41:14', 'FAIL  psi(amount, profile) = 0.27', '#F08B73'],
    [100, '09:41:18', 'Завершено · 176 без нарушений · 6 предупр. · 2 нарушения', '#C9EC5F']
  ];
  const log = S.ran ? logAll.filter((l) => p >= l[0]).map((l) => ({ t: l[1], s: l[2], c: l[3] })) : [{ t: '—', s: 'Проверка не запущена', c: '#6E717A' }];
  const run = { p: p, grid: grid, done: doneN + ' / 184', pass: doneN - warn - fail, warn: warn, fail: fail, log: log,
    cls: S.running ? 'run' : (S.ran && p >= 100 ? 'fail' : 'idle'), label: S.running ? 'Выполняется' : (S.ran && p >= 100 ? 'Завершена с нарушениями' : 'Ожидает запуска') };
  const runs = [
    { id: '2814', ds: 'sales.orders', when: 'сегодня 09:12', p: 176, w: 6, f: 2, dur: '2 мин 14 с', trig: 'Регламент', st: 'fail', stl: '2 нарушения' },
    { id: '2813', ds: 'crm.customers', when: 'сегодня 08:40', p: 91, w: 3, f: 0, dur: '48 с', trig: 'Регламент', st: 'warn', stl: '3 предупреждения' },
    { id: '2812', ds: 'billing.payments', when: 'сегодня 08:00', p: 131, w: 1, f: 0, dur: '3 мин 02 с', trig: 'Airflow', st: 'ok', stl: 'Без нарушений' },
    { id: '2811', ds: 'logistics.shipments', when: 'сегодня 07:30', p: 43, w: 11, f: 7, dur: '1 мин 37 с', trig: 'Регламент', st: 'fail', stl: '7 нарушений' },
    { id: '2810', ds: 'marketing.events', when: 'сегодня 06:15', p: 47, w: 5, f: 0, dur: '6 мин 40 с', trig: 'М. Ким', st: 'warn', stl: '5 предупреждений' },
    { id: '2809', ds: 'hr.employees', when: 'вчера 23:00', p: 40, w: 0, f: 0, dur: '6 с', trig: 'Регламент', st: 'ok', stl: 'Без нарушений' },
    { id: '2808', ds: 'bi.dim_products', when: 'вчера 22:00', p: 37, w: 1, f: 0, dur: '9 с', trig: 'CI', st: 'ok', stl: 'Без нарушений' }
  ];

  // schedule
  const hx = (h) => (h / 24 * 100).toFixed(2);
  const PL = [
    ['billing.payments', [[2, 'd-ok'], [8, 'd-ok'], [14, 'd-pend'], [20, 'd-pend']]],
    ['sales.orders', [[3, 'd-ok'], [9.2, 'd-fail'], [15, 'd-pend'], [21, 'd-pend']]],
    ['crm.customers', [[8.67, 'd-warn'], [20.67, 'd-pend']]],
    ['logistics.shipments', [[7.5, 'd-fail'], [13.5, 'd-pend'], [19.5, 'd-pend']]],
    ['marketing.events', [[6.25, 'd-warn'], [18.25, 'd-pend']]],
    ['hr.employees', [[23, 'd-pend']]],
    ['bi.dim_products', [[10, 'd-pend'], [22, 'd-pend']]]
  ];
  const plan = PL.map((r, ri) => ({ name: r[0], pts: r[1].map((q, qi) => ({ x: hx(q[0]), c: q[1], d: (0.2 + ri * 0.05 + qi * 0.04).toFixed(2), t: r[0] + ' · ' + Math.floor(q[0]) + ':' + String(Math.round((q[0] % 1) * 60)).padStart(2, '0') })) }));
  const sched = [
    { ds: 'billing.payments', freq: 'Каждые 6 часов', cron: '0 */6 * * *', next: 'сегодня 14:00', sla: '30 мин', owner: 'А. Сейткали', notify: 'Telegram, почта', st: 'ok', stl: 'Активно' },
    { ds: 'sales.orders', freq: 'Каждые 6 часов', cron: '12 3/6 * * *', next: 'сегодня 15:12', sla: '1 ч', owner: 'Д. Нуров', notify: 'Telegram', st: 'ok', stl: 'Активно' },
    { ds: 'crm.customers', freq: 'Дважды в сутки', cron: '40 8,20 * * *', next: 'сегодня 20:40', sla: '2 ч', owner: 'М. Ким', notify: 'Почта', st: 'ok', stl: 'Активно' },
    { ds: 'logistics.shipments', freq: 'Каждые 6 часов', cron: '30 1/6 * * *', next: 'сегодня 13:30', sla: '1 ч', owner: 'Т. Абенов', notify: 'Telegram, webhook', st: 'warn', stl: 'SLA нарушен' },
    { ds: 'marketing.events', freq: 'Дважды в сутки', cron: '15 6,18 * * *', next: 'сегодня 18:15', sla: '4 ч', owner: 'М. Ким', notify: 'Почта', st: 'ok', stl: 'Активно' },
    { ds: 'hr.employees', freq: 'Ежедневно', cron: '0 23 * * *', next: 'сегодня 23:00', sla: '12 ч', owner: 'А. Сейткали', notify: 'Почта', st: 'ok', stl: 'Активно' },
    { ds: 'finance.ledger', freq: 'Не задано', cron: '—', next: '—', sla: '—', owner: '—', notify: '—', st: 'idle', stl: 'Черновик' }
  ];

  // audit
  let s2 = 5; const r2 = () => { s2 = (s2 * 9301 + 49297) % 233280; return s2 / 233280; };
  const N = 30, W = 900;
  const yv = (v) => 22 + (100 - v) / 30 * 165;
  const med = [], mn = [], mx = [];
  for (let i = 0; i < N; i++) {
    const base = 93 + Math.sin(i / 4) * 1.2 + i * 0.05;
    med.push(base + (r2() - 0.5)); mx.push(Math.min(100, base + 4 + r2() * 1.5));
    mn.push(Math.max(72, i > 18 ? 74 + (29 - i) * 0.4 + r2() * 3 - (i - 18) * 0.3 : 84 + r2() * 4));
  }
  const visibleDays = S.per === 0 ? 7 : N;
  const medianWindow = med.slice(-visibleDays);
  const upperWindow = mx.slice(-visibleDays);
  const lowerWindow = mn.slice(-visibleDays);
  const X = (i) => (i * W / (visibleDays - 1)).toFixed(1);
  const tl = {
    med: medianWindow.map((v, i) => (i ? 'L' : 'M') + X(i) + ' ' + yv(v).toFixed(1)).join(' '),
    band: upperWindow.map((v, i) => (i ? 'L' : 'M') + X(i) + ' ' + yv(v).toFixed(1)).join(' ') + ' ' +
      lowerWindow.slice().reverse().map((v, j) => 'L' + X(visibleDays - 1 - j) + ' ' + yv(v).toFixed(1)).join(' ') + ' Z',
    marks: lowerWindow.map((v, i) => ({ v, i })).filter((o) => o.v < 80).map((o) => ({
      x: (o.i / (visibleDays - 1) * 100).toFixed(2), y: Math.round(yv(o.v)), t: 'logistics.shipments · ' + o.v.toFixed(1)
    })),
    dates: S.per === 0 ? ['09.10', '11.10', '13.10', '15.10'] : ['16.09', '23.09', '30.09', '07.10', '15.10'],
  };
  const ruleNames = ['not_null(order_id)', 'unique(order_id)', 'between(amount)', 'null_share(discount)', 'in_set(status)', 'regex(phone)', 'freshness(created_at)', 'psi(amount)', 'fk(customer_id)', 'row_count ±15%'];
  const matrix = ruleNames.map((n, ri) => ({ name: n, cells: Array.from({ length: 24 }, (_, ci) => {
    const x = r2(); let s = 5, c = '#D6D6CF';
    const risky = ri === 2 || ri === 3 || ri === 6 || ri === 7 || ri === 8;
    if (risky && x < (ci > 16 ? 0.6 : 0.18)) { const big = x < 0.2; s = big ? 14 : 10; c = big ? '#E0553A' : '#E3A23B'; }
    else if (!risky && x < 0.04) { s = 9; c = '#E3A23B'; }
    return { s: s, c: c, d: (ci * 0.015 + ri * 0.03).toFixed(3) };
  }) }));
  const CL = [['Диапазон и выбросы', 58, '#0E0F12'], ['Полнота', 44, '#3E4659'], ['Согласованность', 37, '#6B7488'], ['Своевременность', 29, '#AEB4C2'], ['Уникальность', 21, '#8FB82A'], ['Формат', 14, '#C9EC5F'], ['Распределение', 10, '#E2E6D2']];
  const classes = CL.map((c, i) => ({ name: c[0], n: c[1], bg: c[2], d: (i * 0.06).toFixed(2) }));
  const DM = [['Полнота', 98.7], ['Уникальность', 99.9], ['Валидность', 94.2], ['Согласованность', 91.0], ['Своевременность', 86.5], ['Стабильность распределений', 92.3]];
  const dims = DM.map((d, i) => ({ name: d[0], v: d[1].toFixed(1), w: Math.max(2, Math.round((d[1] - 90) * 10)), dot: d[1] >= 95 ? '#C9EC5F' : (d[1] >= 90 ? '#E3A23B' : '#E0553A'), dl: (0.1 + i * 0.07).toFixed(2), dl2: (0.9 + i * 0.07).toFixed(2) }));
  const per = ['7 дней', '30 дней', '90 дней'];

  const reports = REP.map((r, i) => Object.assign({}, r, { bc: S.rep === i ? '#0E0F12' : '#E4E4DE', pick: () => actions.update({ rep: i }) }));
  const tgl = (key) => () => { const t = Object.assign({}, S.tg); t[key] = !t[key]; actions.update({ tg: t }); };
  const GS = ['Чтение профиля · 24 колонки', 'Поиск закономерностей', 'Расчёт порогов по квантилям', 'Оценка уверенности'];

  return {
    pillY: pillY, nav1: n1.map(mk), nav2: n2.map(mk), sugCount: sugCount,
    title: scr === 'profile' ? DS[S.ds].name : titles[scr],
    crumb: scr === 'profile' ? 'Analytics / Наборы данных / Профиль' : 'Analytics / ' + titles[scr],
    lic: L, licX: (licIds.indexOf(S.lic) * 100) + '%',
    licTabs: licIds.map((id, i) => ({ label: licLabels[i], cls: S.lic === id ? 'on' : '', go: () => actions.update({ lic: id }) })),
    runDisabled: S.lic === 'expired', genDisabled: S.lic === 'expired',
    runBusy: S.running ? 'busy' : '', isRunning: S.running, notRunning: !S.running,
    runLabel: S.running ? 'Выполняется · ' + Math.floor(S.p) + '%' : 'Запустить проверку',
    startRun: () => actions.startRun(), startGen: () => actions.startGen(),
    goLic: () => actions.go('lic'), goInc: () => actions.go('inc'), goRules: () => actions.go('rules'), goSets: () => actions.go('sets'), goReports: () => actions.go('reports'),
    kpis: kpis, heat: heat, swarm: swarm, incTop: incAll.slice(0, 4), sets: sets,
    ds: DS[S.ds], cols: cols, col: col, loading: S.loading, loaded: !S.loading,
    fl: fl, confSwarm: confSwarm, dimStats: dimStats,
    rtabs: rt.map((t) => ({ label: t[1], cls: S.rtab === t[0] ? 'on' : '', go: () => actions.update({ rtab: t[0] }) })), rtabX: (rti * 100) + '%',
    rulesView: rulesView, rulesEmpty: rulesView.length === 0,
    acceptAll: () => { const rs = Object.assign({}, S.rs); RULES.forEach((r) => { if (rs[r.id] === 'sug' && r.conf >= 0.9) rs[r.id] = 'act'; }); actions.update({ rs: rs }); },
    hasRule: !!selR, sel: sel,
    closeRule: () => actions.update({ sel: null }),
    acceptSel: () => { if (selR) setR(selR.id, 'act'); actions.update({ sel: null }); },
    rejectSel: () => { if (selR) setR(selR.id, 'rej'); actions.update({ sel: null }); },
    run: run, runs: runs, plan: plan, sched: sched,
    tl: tl, matrix: matrix, classes: classes, dims: dims,
    periods: per.map((l, i) => ({ label: l, cls: S.per === i ? 'on' : '', disabled: i === 2, go: () => actions.update({ per: i }) })), perX: (S.per * 100) + '%',
    incFilters: incFilters, incView: incView,
    reports: reports, rep: REP[S.rep],
    repRules: [{ e: 'between(amount, 0, 2 450 000)', s: 'fail', v: '37 строк' }, { e: 'psi(amount, profile) < 0.2', s: 'fail', v: 'PSI 0.27' }, { e: 'null_share(discount_pct) ≤ 15%', s: 'warn', v: '12.4%' }, { e: 'freshness(created_at) ≤ 24 ч', s: 'warn', v: '26 ч' }],
    tgWeekly: S.tg.weekly ? 'on' : '', toggleWeekly: tgl('weekly'), tgAuto: S.tg.auto ? 'on' : '', toggleAuto: tgl('auto'),
    tgTg: S.tg.tg ? 'on' : '', toggleTg: tgl('tg'), tgMail: S.tg.mail ? 'on' : '', toggleMail: tgl('mail'), tgHook: S.tg.hook ? 'on' : '', toggleHook: tgl('hook'),
    usage: [
      { name: 'Наборы данных', v: S.lic === 'trial' ? '5 из 5' : '18 из 25', p: S.lic === 'trial' ? 100 : 72, c: S.lic === 'trial' ? '#E3A23B' : '#0E0F12' },
      { name: 'Проверено строк за месяц', v: '1.24 из 2 млрд', p: 62, c: '#0E0F12' },
      { name: 'Пользователи', v: '6 из 10', p: 60, c: '#0E0F12' },
      { name: 'Регламентные задания', v: S.lic === 'expired' ? 'остановлены' : '14 из 50', p: S.lic === 'expired' ? 0 : 28, c: '#0E0F12' }
    ],
    plans: [
      { f: 'Наборы данных', a: '5', b: '25', c: 'без ограничений' },
      { f: 'Строк в месяц', a: '50 млн', b: '2 млрд', c: 'без ограничений' },
      { f: 'Генерация правил по профилю', a: 'есть', b: 'есть', c: 'есть' },
      { f: 'Регламентные проверки и Airflow', a: '—', b: 'есть', c: 'есть' },
      { f: 'SSO, журнал действий, роли', a: '—', b: 'роли', c: 'полностью' },
      { f: 'Хранение истории', a: '14 дней', b: '1 год', c: '3 года' }
    ],
    sources: [
      { ab: 'PG', name: 'PostgreSQL · DWH', host: 'dwh.internal:5432 · 5 наборов', st: 'ok', stl: 'Подключено' },
      { ab: 'CH', name: 'ClickHouse · события', host: 'ch.internal:8123 · 2 набора', st: 'ok', stl: 'Подключено' },
      { ab: 'S3', name: 'Объектное хранилище · Parquet', host: 's3://lake/logistics · 1 набор', st: 'warn', stl: 'Медленный ответ' },
      { ab: 'CSV', name: 'Загрузка файлов', host: 'вручную · 1 набор', st: 'idle', stl: 'Вручную' }
    ],
    team: [
      { ab: 'АС', name: 'Алия Сейткали', mail: 'aliya@company.kz', role: 'Администратор', bg: '#0E0F12', fg: '#C9EC5F' },
      { ab: 'ДН', name: 'Данияр Нуров', mail: 'daniyar@company.kz', role: 'Инженер данных', bg: '#EEEEE9', fg: '#0E0F12' },
      { ab: 'МК', name: 'Мария Ким', mail: 'maria@company.kz', role: 'Аналитик', bg: '#EEEEE9', fg: '#0E0F12' },
      { ab: 'ТА', name: 'Тимур Абенов', mail: 'timur@company.kz', role: 'Владелец данных', bg: '#EEEEE9', fg: '#0E0F12' }
    ],
    actlog: [
      { t: '15.10 09:20', u: 'Д. Нуров', a: 'Принял правило between(amount, 0, 2 450 000)' },
      { t: '15.10 09:14', u: 'Система', a: 'Сформирован отчёт по проверке № 2814' },
      { t: '15.10 08:02', u: 'А. Сейткали', a: 'Изменил порог дрейфа PSI с 0.25 на 0.20' },
      { t: '14.10 18:31', u: 'Т. Абенов', a: 'Назначил ответственного по инциденту INC-0412' },
      { t: '14.10 11:05', u: 'М. Ким', a: 'Добавила регламент для crm.customers' }
    ],
    genOn: S.gen >= 0,
    genSteps: GS.map((l, i) => ({ l: l, cls: i < S.gen ? 'on' : (i === S.gen ? 'cur' : '') })),
    toast: S.toast
  };
}
