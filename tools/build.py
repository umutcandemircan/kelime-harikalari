import os
import sys

# Forwarding stub for backward compatibility
script_dir = os.path.dirname(os.path.abspath(__file__))
v2_build_script = os.path.join(script_dir, 'build', 'build.py')

if os.path.exists(v2_build_script):
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_v2", v2_build_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.build()
else:
    print(f"Error: {v2_build_script} not found.")
    sys.exit(1)
