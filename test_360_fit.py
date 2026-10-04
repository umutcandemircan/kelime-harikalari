import subprocess
import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

test_snippet = '''
<script>
window.addEventListener('load', () => {
  const container = document.getElementById('app-container');
  container.style.width = '360px';
  container.style.maxWidth = '360px';
  container.style.marginLeft = '0';
  container.style.marginRight = '0';
  container.style.boxSizing = 'border-box';

  const wide = [];
  document.querySelectorAll('#app-container *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > 360.5) {
      wide.push({
        tag: el.tagName,
        id: el.id,
        cls: el.className,
        left: Math.round(r.left),
        right: Math.round(r.right),
        w: Math.round(r.width)
      });
    }
  });

  const out = document.createElement('div');
  out.id = 'TEST_RESULT';
  out.textContent = JSON.stringify(wide);
  document.body.appendChild(out);
});
</script>
'''

html_test = html.replace('</body>', test_snippet + '\n</body>')
with open('test_fit_360.html', 'w', encoding='utf-8') as f:
    f.write(html_test)

res = subprocess.run([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--dump-dom',
    r'file:///C:/Users/umutc/.gemini/antigravity/scratch/kelime-avcisi/test_fit_360.html'
], capture_output=True)

stdout_str = res.stdout.decode('utf-8', errors='ignore')
m = re.search(r'<div id="TEST_RESULT">(.*?)</div>', stdout_str)
if m:
    data = json.loads(m.group(1))
    print(f"Total elements overflowing 360px width: {len(data)}")
    for item in data[:25]:
        print(" ", item)
else:
    print("Could not find TEST_RESULT")
