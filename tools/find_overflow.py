# -*- coding: utf-8 -*-
import json
import re
import subprocess

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

debug_snippet = '''
<script>
window.addEventListener('load', () => {
  const wide = [];
  document.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > 361) {
      wide.push({ tag: el.tagName, id: el.id, class: el.className, left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width) });
    }
  });
  const div = document.createElement('div');
  div.id = 'DEBUG_OVERFLOW';
  div.textContent = JSON.stringify(wide);
  document.body.appendChild(div);
});
</script>
'''

html_debug = html.replace('</body>', debug_snippet + '\n</body>')
with open('index_debug.html', 'w', encoding='utf-8') as f:
    f.write(html_debug)

res = subprocess.run([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--window-size=360,800',
    '--dump-dom',
    r'file:///C:/Users/umutc/.gemini/antigravity/scratch/kelime-avcisi/index_debug.html'
], capture_output=True)

out = res.stdout.decode('utf-8', errors='ignore')
m = re.search(r'<div id="DEBUG_OVERFLOW">(.*?)</div>', out)
if m:
    data = json.loads(m.group(1))
    print(f'Found {len(data)} overflowing elements:')
    for item in data[:20]:
        print(' ', item)
else:
    print('No debug overflow div found')
