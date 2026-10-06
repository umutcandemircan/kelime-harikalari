import re

js_path = 'src/js/game/GameEngine.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Remove pcStars logic for Daily
daily_regex = r"let pcStars = document\.getElementById\('post-stars'\);.*?pcStars\.style\.color = '#f59e0b';"
js = re.sub(daily_regex, '', js, flags=re.DOTALL)

# Remove pcStars logic for Regular
regular_regex = r"let pcStars = document\.getElementById\('post-stars'\);.*?pcStars\.style\.color = '#f59e0b';"
js = re.sub(regular_regex, '', js, flags=re.DOTALL)

# Remove calculateStars and reference
js = re.sub(r'calculateStars\(\) \{[\s\S]*?\},', '', js)
js = js.replace('const stars = this.calculateStars();', 'const stars = 3;')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("GameEngine cleaned")
