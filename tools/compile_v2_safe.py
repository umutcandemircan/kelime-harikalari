# -*- coding: utf-8 -*-
"""
Safe Compiler for Kelime Harikaları v2.0.0
Uses plain string replacements to avoid f-string syntax issues.
"""
import json

with open("credits.json", "r", encoding="utf-8") as f:
    credits_json = f.read()

with open("idioms.json", "r", encoding="utf-8") as f:
    idioms_json = f.read()

with open("levels_100.json", "r", encoding="utf-8") as f:
    levels_json = f.read()

# Read the HTML template
with open("compile_v2.py", "r", encoding="utf-8") as f:
    code = f.read()

# Let's extract HTML_CONTENT and JS_ENGINE cleanly
start_html = code.find('HTML_CONTENT = r\'\'\'') + len('HTML_CONTENT = r\'\'\'')
end_html = code.find('\'\'\'\n\n# Let\'s assemble')
html_template = code[start_html:end_html]

start_js = code.find('JS_ENGINE = f\'\'\'') + len('JS_ENGINE = f\'\'\'')
end_js = code.rfind('\'\'\'\n\nfull_html =')
js_engine_template = code[start_js:end_js]

# Replace double curly braces with single curly braces in js_engine_template
js_engine = js_engine_template.replace("{{", "{").replace("}}", "}")

# Replace data placeholders
js_engine = js_engine.replace("{json.dumps(credits_data, ensure_ascii=False)}", credits_json)
js_engine = js_engine.replace("{json.dumps(idioms_data, ensure_ascii=False)}", idioms_json)
js_engine = js_engine.replace("{json.dumps(levels_data, ensure_ascii=False)}", levels_json)

final_html = html_template.replace("__JS_ENGINE_INJECTION__", js_engine)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"SUCCESS: Compiled index.html! File size: {len(final_html)} bytes.")
