import os
import shutil
import glob

dirs = ['src/data', 'src/css', 'src/js', 'src/assets', 'docs', 'tools', 'archive', 'tests']
for d in dirs:
    os.makedirs(d, exist_ok=True)

for f in glob.glob('*.json'):
    shutil.move(f, os.path.join('src/data', f))

if os.path.exists('config.js'):
    shutil.move('config.js', 'src/data/config.js')

if os.path.exists('debug_wide.js'):
    shutil.move('debug_wide.js', 'archive/debug_wide.js')

print("Restructured.")
