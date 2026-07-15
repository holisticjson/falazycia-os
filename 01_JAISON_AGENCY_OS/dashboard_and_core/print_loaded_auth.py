import os

def check():
    env_paths = [
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    ]
    
    print("Sprawdzam ścieżki .env:")
    for path in env_paths:
        print(f"Path: {path} - exists: {os.path.exists(path)}")

    for env_path in env_paths:
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line and not line.strip().startswith("#"):
                            k, v = line.split("=", 1)
                            val = v.strip()
                            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                                val = val[1:-1]
                            os.environ[k.strip()] = val
            except Exception as e:
                print("Błąd podczas odczytu pliku:", e)
            break

    u = os.environ.get("HERMES_DASHBOARD_BASIC_AUTH_USERNAME")
    p = os.environ.get("HERMES_DASHBOARD_BASIC_AUTH_PASSWORD")
    print("USERNAME:", repr(u), "Długość:", len(u) if u else 0)
    print("PASSWORD:", repr(p), "Długość:", len(p) if p else 0)

if __name__ == "__main__":
    check()
