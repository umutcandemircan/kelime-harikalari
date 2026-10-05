# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Audit locale usage in index.html
upper_tr_calls = html.count(".toLocaleUpperCase('tr-TR')")
lower_tr_calls = html.count(".toLocaleLowerCase('tr-TR')")
raw_upper_calls = html.count(".toUpperCase()")
raw_lower_calls = html.count(".toLowerCase()")

print(f"toLocaleUpperCase('tr-TR') calls: {upper_tr_calls}")
print(f"toLocaleLowerCase('tr-TR') calls: {lower_tr_calls}")
print(f"raw toUpperCase() calls: {raw_upper_calls}")
print(f"raw toLowerCase() calls: {raw_lower_calls}")

# Look for places where string comparison might be done without locale
import re
comparisons = re.findall(r'(\b[a-zA-Z0-9_.]+\s*(?:===|==)\s*[a-zA-Z0-9_.]+\b)', html)
print(f"Total comparisons in code: {len(comparisons)}")
