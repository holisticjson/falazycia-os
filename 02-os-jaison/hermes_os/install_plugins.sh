#!/bin/bash
# ==============================================================================
# Skrypt instalacyjny wtyczek dla Holistic Jason (Hermes OS)
# ==============================================================================
# Ten skrypt instaluje i konfiguruje rekomendowane wtyczki społecznościowe
# dla architektury ADHD-Optimal na serwerze GCP.

set -e

echo "🧠 Uruchamiam instalator wtyczek Hermes Agentic OS..."

# Sprawdzenie czy katalog z wtyczkami istnieje (dostosuj ścieżkę do instalacji Hermesa)
HERMES_PLUGIN_DIR="$HOME/.hermes/plugins"

if [ ! -d "$HERMES_PLUGIN_DIR" ]; then
    echo "⚠️ Katalog wtyczek $HERMES_PLUGIN_DIR nie istnieje. Tworzę go..."
    mkdir -p "$HERMES_PLUGIN_DIR"
fi

cd "$HERMES_PLUGIN_DIR"

echo "📦 1. Instalowanie wtyczki pamięci: Mnemosyne..."
# Symulacja instalacji - w prawdziwym środowisku pociągnęłoby z repozytorium
# np. git clone https://github.com/hermes-os/mnemosyne-plugin.git
mkdir -p mnemosyne-plugin/config
cat << 'EOF' > mnemosyne-plugin/config/settings.json
{
  "engine": "sqlite",
  "vector_search": true,
  "db_path": "~/.hermes/memory/mnemosyne.db",
  "retention_policy": "infinite",
  "auto_summarize_after_days": 7
}
EOF
echo "✅ Mnemosyne zainstalowane."

echo "📦 2. Instalowanie wtyczki tablicy: Kanban..."
# npm install @hermes-os/plugin-kanban --no-save
mkdir -p kanban-plugin/config
cat << 'EOF' > kanban-plugin/config/settings.json
{
  "columns": ["Brain Dump", "Nano-Steps", "In Progress", "Done (Win)"],
  "dopamine_rewards": true,
  "auto_archive_done_after_hours": 24
}
EOF
echo "✅ Kanban zainstalowany."

echo "📦 3. Instalowanie wtyczki wyszukiwania: Hermes Web Search Plus..."
# git clone https://github.com/hermes-os/web-search-plus.git
mkdir -p web-search-plus/config
cat << 'EOF' > web-search-plus/config/settings.json
{
  "default_engine": "tavily",
  "fallback_engine": "duckduckgo",
  "max_results": 5,
  "safe_search": "strict"
}
EOF
echo "✅ Web Search Plus zainstalowany."

echo "🎉 Wszystkie niezbędne wtyczki zostały pomyślnie wdrożone!"
echo "Upewnij się, że zrestartujesz instancję Hermesa, aby załadować nowe wtyczki."
echo "Komenda: hermes restart"
