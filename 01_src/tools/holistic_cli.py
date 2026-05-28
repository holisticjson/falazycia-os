import sys
import os
from pathlib import Path

# Dodaj root do path, aby importy działały
sys.path.append(os.getcwd())

from holistic_ceo import call_agent

def main():
    if len(sys.argv) < 2:
        print("Użycie: python holistic_cli.py \"Twoje zadanie dla CEO\"")
        sys.exit(1)

    task = sys.argv[1]
    print(f"🚀 [CLI] Przekazywanie zadania do CEO Jason (via AWS Bedrock)...")
    
    # Przykładowe wywołanie przez Bedrock (jeśli agent ma ustawiony model eu.anthropic...)
    # Możemy wymusić Bedrock tutaj dla CLI
    from holistic_ceo import call_bedrock_robust
    
    response, _ = call_bedrock_robust(task)
    
    print("\n" + "="*50)
    print("🧠 ODPOWIEDŹ CEO JASON (AWS Bedrock):")
    print("="*50)
    print(response)
    print("="*50)

if __name__ == "__main__":
    main()
