import os
import shutil
import glob

dirs_to_create = ['archive', 'tools', 'src', 'src/core', 'src/ui', 'src/game', 'src/data', 'docs', 'tests', 'assets']
for d in dirs_to_create:
    os.makedirs(d, exist_ok=True)

# Move pngs to archive
for f in glob.glob('*.png'):
    shutil.move(f, os.path.join('archive', f))

# Move htmls to archive (except index.html)
for f in glob.glob('*.html'):
    if f != 'index.html':
        shutil.move(f, os.path.join('archive', f))

# Move test scripts to tests
for f in glob.glob('test_*.py') + glob.glob('validate_*.py') + glob.glob('verify_*.py') + glob.glob('simulate_*.py'):
    shutil.move(f, os.path.join('tests', f))

# Move build/patch/compile/generate scripts to tools
for f in glob.glob('build_*.py') + glob.glob('patch_*.py') + glob.glob('compile_*.py') + glob.glob('generate_*.py') + glob.glob('write_*.py') + glob.glob('update_*.py') + glob.glob('resolve_*.py') + glob.glob('find_*.py') + glob.glob('clean_*.py') + glob.glob('inspect_*.py') + glob.glob('shots*.py') + glob.glob('take_*.py'):
    shutil.move(f, os.path.join('tools', f))

print("Cleanup complete.")
