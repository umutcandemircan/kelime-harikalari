import re

css_path = 'src/css/main.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Fix letter-node centering
old_letter = r"""        \.letter-node \{[\s\S]*?touch-action: none;
        \}"""
new_letter = """        .letter-node {
            position: absolute;
            width: 52px;
            height: 52px;
            transform: translate(-50%, -50%);
            border-radius: 50%;
            background: #ffffff;
            color: #0b132b;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-weight: 900;
            font-size: 22px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            transition: transform 0.15s ease, background 0.15s ease;
            user-select: none;
            touch-action: none;
        }"""
css = re.sub(r'        \.letter-node \{[\s\S]*?touch-action: none;\n        \}', new_letter, css)

# Fix letter-node selected transform
old_selected = r"""        \.letter-node\.selected \{
            background: var\(--gold-primary\);
            color: #ffffff;
            transform: scale\(1\.15\);
            box-shadow: 0 0 14px rgba\(245, 158, 11, 0\.8\);
        \}"""
new_selected = """        .letter-node.selected {
            background: var(--gold-primary);
            color: #ffffff;
            transform: translate(-50%, -50%) scale(1.15);
            box-shadow: 0 0 14px rgba(245, 158, 11, 0.8);
        }"""
css = re.sub(old_selected, new_selected, css)

# Fix word-preview-pill centering and wrapping
css = re.sub(
    r'\.word-preview-pill \{',
    r'.word-preview-pill {\n            white-space: nowrap;\n            max-width: 90%;\n            overflow: hidden;\n            text-overflow: ellipsis;',
    css
)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS patched.")
