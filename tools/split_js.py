import os
import re

with open('src/js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# We will split manually based on known comments
parts = {
    "utils": js[:js.find('// DATASETS')],
    "SaveManager": js[js.find('// 1. SAVE MANAGER (LOCALSTORAGE)'):js.find('// 2. PROCEDURAL WEB AUDIO SYNTHESIZER')],
    "AudioEngine": js[js.find('// 2. PROCEDURAL WEB AUDIO SYNTHESIZER'):js.find('// 3. INTERACTIVE 81-PROVINCE MAP ENGINE')],
    "MapEngine": js[js.find('// 3. INTERACTIVE 81-PROVINCE MAP ENGINE'):js.find('// 4. CROSSWORD & GAMEPLAY ENGINE')],
    "GameEngine": js[js.find('// 4. CROSSWORD & GAMEPLAY ENGINE'):js.find('// 5. DEYİM AVCISI MINI-MODE')],
    "IdiomEngine": js[js.find('// 5. DEYİM AVCISI MINI-MODE'):js.find('// 6. MAIN APPLICATION STATE MACHINE')],
    "App": js[js.find('// 6. MAIN APPLICATION STATE MACHINE'):]
}

os.makedirs('src/js/core', exist_ok=True)
os.makedirs('src/js/game', exist_ok=True)

with open('src/js/core/utils.js', 'w', encoding='utf-8') as f: f.write(parts['utils'])
with open('src/js/core/SaveManager.js', 'w', encoding='utf-8') as f: f.write(parts['SaveManager'])
with open('src/js/core/AudioEngine.js', 'w', encoding='utf-8') as f: f.write(parts['AudioEngine'])
with open('src/js/game/MapEngine.js', 'w', encoding='utf-8') as f: f.write(parts['MapEngine'])
with open('src/js/game/GameEngine.js', 'w', encoding='utf-8') as f: f.write(parts['GameEngine'])
with open('src/js/game/IdiomEngine.js', 'w', encoding='utf-8') as f: f.write(parts['IdiomEngine'])
with open('src/js/App.js', 'w', encoding='utf-8') as f: f.write(parts['App'])

print("JS split successfully.")
