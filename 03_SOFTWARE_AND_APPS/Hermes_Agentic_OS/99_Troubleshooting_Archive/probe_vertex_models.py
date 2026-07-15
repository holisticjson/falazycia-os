#!/usr/bin/env python3
"""Sprawdza dostepne modele Gemini/Imagen/Veo w projekcie holistic-broker"""
import os, json, urllib.request

# WYMUSZENIE pliku SA key dla projektu holistic-broker
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/holisticjson/gcp-sa-key.json"

import google.auth
import google.auth.transport.requests

creds, project = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
creds.refresh(google.auth.transport.requests.Request())
token = creds.token
print(f"[OK] Credentials z SA key | projekt w kluczu: {project}")

# ZAWSZE uzywamy holistic-broker (z SA key)
PROJECT = "holistic-broker"
LOCATION = "us-central1"

GEMINI_CANDIDATES = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro",
    "gemini-1.5-pro-002",
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-preview-05-20",
    "gemini-2.5-pro",
    "gemini-2.5-pro-preview-05-06",
    "gemini-2.5-pro-preview-06-05",
]

IMAGE_CANDIDATES = [
    "imagen-3.0-generate-001",
    "imagen-3.0-fast-generate-001",
    "imagen-4.0-generate-preview-05-20",
    "imagen-4.0-ultra-generate-preview-05-23",
    "imagegeneration@006",
]

VIDEO_CANDIDATES = [
    "veo-2.0-generate-001",
    "veo-001",
    "veo-2",
]

def test_text(model_name):
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}/publishers/google/models/{model_name}:generateContent"
    body = json.dumps({"contents": [{"role": "user", "parts": [{"text": "Say OK"}]}], "generationConfig": {"maxOutputTokens": 5}}).encode()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return "OK", r.status
    except urllib.error.HTTPError as e:
        return "FAIL", e.code
    except Exception as ex:
        return "ERR", str(ex)[:40]

def test_image(model_name):
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}/publishers/google/models/{model_name}:predict"
    body = json.dumps({"instances": [{"prompt": "a red ball"}], "parameters": {"sampleCount": 1}}).encode()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return "OK", r.status
    except urllib.error.HTTPError as e:
        return "FAIL", e.code
    except Exception as ex:
        return "ERR", str(ex)[:40]

def test_video(model_name):
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}/publishers/google/models/{model_name}:predictLongRunning"
    body = json.dumps({"instances": [{"prompt": "a cat walking"}], "parameters": {"durationSeconds": 5}}).encode()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return "OK", r.status
    except urllib.error.HTTPError as e:
        return "FAIL", e.code
    except Exception as ex:
        return "ERR", str(ex)[:40]

print(f"\n{'='*60}")
print(f"PROJEKT: {PROJECT} | REGION: {LOCATION}")
print(f"{'='*60}\n")

ok_gemini, ok_imagen, ok_video = [], [], []

print("--- MODELE GEMINI (TEKST) ---")
for m in GEMINI_CANDIDATES:
    s, c = test_text(m)
    icon = "✅" if s == "OK" else "❌"
    print(f"  {icon} {m:45s} {c}")
    if s == "OK":
        ok_gemini.append(m)

print("\n--- MODELE IMAGEN (OBRAZY) ---")
for m in IMAGE_CANDIDATES:
    s, c = test_image(m)
    icon = "✅" if s == "OK" else "❌"
    print(f"  {icon} {m:45s} {c}")
    if s == "OK":
        ok_imagen.append(m)

print("\n--- MODELE VEO (VIDEO) ---")
for m in VIDEO_CANDIDATES:
    s, c = test_video(m)
    icon = "✅" if s == "OK" else "❌"
    print(f"  {icon} {m:45s} {c}")
    if s == "OK":
        ok_video.append(m)

print(f"\n{'='*60}")
print("DOSTEPNE MODELE:")
for m in ok_gemini: print(f"  GEMINI:  {m}")
for m in ok_imagen: print(f"  IMAGEN:  {m}")
for m in ok_video:  print(f"  VEO:     {m}")
print(f"{'='*60}")
