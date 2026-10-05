import re

with open('src/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the provinces layer and replace its contents
html = re.sub(r'<g id="provinces-layer">.*?</g>', '<g id="provinces-layer">\n                        {{ INJECT_MAP_PATHS }}\n                    </g>', html, flags=re.DOTALL)
html = html.replace('/* INJECT_CSS */', '{{ INJECT_CSS }}')
html = html.replace('/* INJECT_JS */', '{{ INJECT_JS }}')

with open('src/template.html', 'w', encoding='utf-8') as f:
    f.write(html)
