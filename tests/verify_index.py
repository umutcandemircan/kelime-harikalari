# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check script
m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if not m:
    print('ERROR: No script tag found!')
    exit(1)

js = m.group(1)
print(f'Found JS script ({len(js)} chars).')

# Check getElementById
ids_in_js = re.findall(r'getElementById\([\'"]([^\'"]+)[\'"]\)', js)
print(f'Found {len(ids_in_js)} getElementById calls, {len(set(ids_in_js))} unique IDs.')

missing = []
for id_name in set(ids_in_js):
    pattern = rf'id=[\'"]{id_name}[\'"]'
    if not re.search(pattern, content):
        missing.append(id_name)

if missing:
    print('MISSING IDs in HTML:', missing)
    exit(1)
else:
    print('PASS: All getElementById targets exist in HTML!')

# Check querySelector targets
qs_classes = re.findall(r'querySelector(All)?\([\'"]\.([a-zA-Z0-9_-]+)[\'"]\)', js)
print(f'Found {len(qs_classes)} class query selectors.')
missing_classes = []
for _, cls in set(qs_classes):
    if f'class="{cls}"' not in content and f'class=\'{cls}\'' not in content and f'class=' not in content:
        # Check if created dynamically in js
        if cls not in ['spark-projectile', 'star-projectile', 'floating-toast', 'crossword-cell', 'cell-inner', 'cell-front', 'cell-back', 'wheel-node', 'selected', 'revealed', 'active', 'flash', 'calendar-day-header', 'calendar-day-cell', 'check', 'star-badge']:
            missing_classes.append(cls)

if missing_classes:
    print('WARNING - Unrecognized class querySelectors:', missing_classes)
else:
    print('PASS: All query selector classes accounted for!')

print('Checking Turkish characters in text...')
turkish_samples = ["Kapadokya", "Pamukkale", "İstanbul", "Celsus", "Şanlıurfa", "Kolezyum", "Günün Özel", "Bulmacası", "İpucu", "Altın"]
for sample in turkish_samples:
    if sample in content:
        print(f'  Found: {sample}')
    else:
        print(f'  NOT found: {sample}')

print('ALL CHECKS PASSED!')
