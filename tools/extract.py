import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract CSS
start_css = html.find('<style>') + len('<style>')
end_css = html.find('</style>')
css_content = html[start_css:end_css].strip()
with open('src/css/main.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# Extract JS
start_js = html.find('<script>') + len('<script>')
end_js = html.find('</script>', start_js)
js_content = html[start_js:end_js].strip()
with open('src/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

# Extract HTML structure (Template)
html_template = html[:html.find('<style>')] + '<style>\n/* INJECT_CSS */\n</style>\n' + html[html.find('</style>')+8:html.find('<script>')] + '<script>\n/* INJECT_JS */\n</script>\n</body>\n</html>'
with open('src/template.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Extraction complete. CSS, JS, and HTML template separated.")
