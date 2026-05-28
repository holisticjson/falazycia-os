import os
import shutil

def sanitize_and_truncate(filename, max_length=100):
    name, ext = os.path.splitext(filename)
    if len(name) > max_length:
        name = name[:max_length].strip("_ ")
        # Also remove weird multiple underscores
        import re
        name = re.sub(r'_{2,}', '_', name)
    return name + ext

def fix_directory_recursively(root_dir):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for file in files:
            old_path = os.path.join(root, file)
            new_name = sanitize_and_truncate(file)
            if new_name != file:
                new_path = os.path.join(root, new_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Zmieniono: {file[:30]}... -> {new_name}")
                except Exception as e:
                    print(f"Błąd zmiany nazwy pliku {file}: {e}")

if __name__ == "__main__":
    target_dir = r"C:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\Adrian Kilar Motion"
    if os.path.exists(target_dir):
        print("Naprawiam nazwy plików w Adrian Kilar Motion...")
        fix_directory_recursively(target_dir)
        print("Gotowe!")
    else:
        print("Katalog nie istnieje.")
