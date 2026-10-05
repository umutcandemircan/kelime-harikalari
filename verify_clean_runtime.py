import subprocess
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

snippet = '''
<script>
window.ERRORS = [];
window.addEventListener('error', e => {
  window.ERRORS.push(e.message + ' at ' + e.filename + ':' + e.lineno);
});
window.addEventListener('load', () => {
  const d = document.createElement('div');
  d.id = 'JS_RUNTIME_ERRORS';
  d.textContent = JSON.stringify(window.ERRORS);
  document.body.appendChild(d);
});
</script>
'''

html_check = html.replace('</body>', snippet + '\n</body>')
with open('runtime_check.html', 'w', encoding='utf-8') as f:
    f.write(html_check)

res = subprocess.run([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--dump-dom',
    r'file:///C:/Users/umutc/.gemini/antigravity/scratch/kelime-avcisi/runtime_check.html'
], capture_output=True)

out = res.stdout.decode('utf-8', errors='ignore')
m = re.search(r'<div id="JS_RUNTIME_ERRORS">(.*?)</div>', out)
if m:
    errs = m.group(1)
    print("JS Errors:", errs)
else:
    print("No errors div found")
