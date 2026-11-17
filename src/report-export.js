const escapeHtml = text => String(text).replace(/[&<>"']/g, char => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
})[char])

export function downloadDemoReport(format, report, rules) {
  const data = { demo: true, title: report.title, score: Number(report.score), rules }
  let content = JSON.stringify(data, null, 2)
  let mime = 'application/json'
  if (format === 'html') {
    const rows = rules.map(rule => '<li>' + escapeHtml(rule.e) + ' · ' + escapeHtml(rule.v) + '</li>').join('')
    content = '<!doctype html><html lang="ru"><meta charset="utf-8"><title>autodq</title>' +
      '<main><h1>' + escapeHtml(report.title) + '</h1><p>Демонстрационный отчёт</p>' +
      '<p>Индекс качества: ' + escapeHtml(report.score) + '</p><ul>' + rows + '</ul></main>'
    mime = 'text/html'
  }
  const url = URL.createObjectURL(new Blob([content], { type: mime + ';charset=utf-8' }))
  const link = document.createElement('a')
  link.href = url
  link.download = 'autodq-demo.' + format
  document.body.append(link)
  link.click()
  link.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
