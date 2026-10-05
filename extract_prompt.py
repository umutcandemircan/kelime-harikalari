import json
p = r'C:\Users\umutc\.gemini\antigravity\brain\0c0e0ce6-6c4b-4ec4-a3bc-da3cdcfce2fc\.system_generated\logs\transcript_full.jsonl'
ui = []
for l in open(p, encoding='utf-8'):
    try:
        d = json.loads(l)
    except Exception:
        continue
    if d.get('type') == 'USER_INPUT':
        ui.append(d.get('content', ''))
target = [c for c in ui if '81 ile' in c]
c = target[-1] if target else ui[-2]
open('last_prompt.txt', 'w', encoding='utf-8').write(c)
print(len(c))
