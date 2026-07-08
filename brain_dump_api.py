import os
import datetime
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Brain Dump API (Obsidian Sync)")

# Konfiguracja CORS dla hermes-web-ui
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Katalog docelowy w Obsidianie (Inbox)
# Dla systemów WSL/Linux można ustawić zmienną środowiskową OBSIDIAN_INBOX_PATH
INBOX_DIR = os.getenv("OBSIDIAN_INBOX_PATH", os.path.join(os.getenv("OBSIDIAN_VAULT_PATH", os.path.join(os.getcwd(), "Obsidian_Vault")), "Inbox"))

class DumpRequest(BaseModel):
    content: str
    tags: list[str] = []

@app.post("/api/dump")
async def save_brain_dump(req: DumpRequest):
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
        
    try:
        # Zapewnij, że folder Inbox istnieje
        os.makedirs(INBOX_DIR, exist_ok=True)
        
        # Generowanie unikalnej nazwy pliku
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:6]
        filename = f"Zrzut_{timestamp}_{unique_id}.md"
        filepath = os.path.join(INBOX_DIR, filename)
        
        # Formatowanie Frontmatter (YAML) dla Obsidiana
        tags_str = "\n  - ".join(["brain-dump"] + req.tags) if req.tags else "brain-dump"
        
        markdown_content = f"""---
aliases: []
tags:
  - {tags_str}
date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
status: "inbox"
---

# Zrzut z Hermesa (Brain Dump)
Data zrzutu: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{req.content}
"""
        
        # Zapisz plik MD do Obsidiana
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        return {"status": "success", "file": filename, "path": filepath}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Uruchamiamy na porcie 8085
    print(f"Uruchamianie Brain Dump API na porcie 8085. Ścieżka Inbox: {INBOX_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8085)
