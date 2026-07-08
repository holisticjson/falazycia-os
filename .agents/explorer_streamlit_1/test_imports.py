import os
import sys
import importlib.util
import traceback

# Add workspace root to sys.path
sys.path.append(r"c:\Aplikacje MVP\Holistic Jason")

print("Python executable:", sys.executable)

src_dir = r"c:\Aplikacje MVP\Holistic Jason\01_src"
failed_imports = []

for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(".py") and not file.startswith("__"):
            full_path = os.path.join(root, file)
            # Get relative module name, e.g. 01_src.knowledge
            rel_path = os.path.relpath(full_path, r"c:\Aplikacje MVP\Holistic Jason")
            mod_name = rel_path[:-3].replace(os.sep, ".")
            print(f"Testing import of {mod_name}...")
            try:
                # Load module
                if mod_name.startswith("01_src"):
                    spec = importlib.util.spec_from_file_location(mod_name, full_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                else:
                    importlib.import_module(mod_name)
                print(f"SUCCESS: {mod_name}")
            except Exception as e:
                err_msg = traceback.format_exc()
                print(f"FAILED: {mod_name}")
                print(f"Error: {e}")
                failed_imports.append((mod_name, str(e), err_msg))

print("\n--- Summary ---")
if failed_imports:
    print(f"Found {len(failed_imports)} modules with import errors:")
    for mod, err, tb in failed_imports:
        print(f"- {mod}: {err}")
else:
    print("All modules imported successfully!")
