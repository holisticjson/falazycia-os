"""
Jaison OS — Dual-Identity Discord Bot Daemon
Handles multi-personality AI advisory in Discord:
- Channel #jaison-agency: Agency OS B2B Advisor & Interactive Proposal Generator
- Channel #lifewave-builder: LifeWave MLM Cellular Health & Biohacking Coach
Uses Google GenAI SDK (Gemini 2.5 Flash on Vertex AI / GCP).
"""

import os
import sys
import json
import logging
import asyncio
import discord
from discord.ext import commands
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Load environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "jaison-os").strip()
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1").strip()

# Initialize Gemini Client via GenAI SDK
try:
    gemini_client = genai.Client(vertexai=True, project=GCP_PROJECT_ID, location=GCP_LOCATION)
    logging.info(f"Connected to Vertex AI Gemini 2.5 on GCP Project: {GCP_PROJECT_ID}")
except Exception as e:
    logging.warning(f"Could not connect to Vertex AI Gemini: {e}")
    gemini_client = None

# System Prompts for Dual Identity
PROMPT_JAISON_AGENCY = """
Jesteś Jaison Agentic OS — Głównym Architektem i Co-Pilotem Agencji Jaison (jaison.pl).
Twoje motto: "Robimy to co ważne. Resztę robi kod."
Zasada: Mów bezpośrednio ("Ty"), krótko (ADHD-friendly, max 1-2 akapity), z empatią.
Pogrubienia pisz WYŁĄCZNIE tagami <strong>tekst</strong>. BEZWZGLĘDNY ZAKAZ UŻYWANIA podwójnych gwiazdek ** w wiadomościach.
Twój cel: Pomagać Tomaszowi zarządzać klientami B2B, automatyzacjami n8n, kreacjami Remotion i ofertami.
"""

PROMPT_LIFEWAVE_BUILDER = """
Jesteś LifeWave MLM Builder — Doradcą ds. Bioregeneracji Komórkowej i Budowniczym Zespołu MLM.
Twoje motto: "Automatyzuj to, co powtarzalne. Twórz to, co unikalne."
Zasada: Mów bezpośrednio ("Ty"), z pasją do zdrowia komórkowego, regeneracji X39 i fototerapii komórkowej.
Pogrubienia pisz WYŁĄCZNIE tagami <strong>tekst</strong>. BEZWZGLĘDNY ZAKAZ UŻYWANIA podwójnych gwiazdek ** w wiadomościach.
Twój cel: Wspierać kwalifikację partnerów MLM, generować posty biohackingowe i budować zautomatyzowaną strukturę.
"""

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"🟢 Jaison OS Discord Bot is online! Logged in as: {bot.user.name} ({bot.user.id})")

@bot.event
async def on_message(message):
    # Ignore self messages
    if message.author == bot.user:
        return

    # Route message by channel name or parent category
    channel_name = str(message.channel.name).lower()
    user_prompt = message.content.strip()

    if not user_prompt:
        return

    # Select identity prompt
    if "lifewave" in channel_name or "mlm" in channel_name:
        sys_prompt = PROMPT_LIFEWAVE_BUILDER
        identity_tag = "🔵 [LifeWave MLM Builder]"
    else:
        sys_prompt = PROMPT_JAISON_AGENCY
        identity_tag = "🟢 [Jaison Agency OS]"

    async with message.channel.typing():
        try:
            if gemini_client:
                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=sys_prompt,
                        temperature=0.7,
                    )
                )
                reply_text = response.text.replace("**", "<strong>").replace("**", "</strong>")
            else:
                reply_text = f"Odbrałem Twoją wiadomość: '{user_prompt}'. (Podepnij klucz DISCORD_BOT_TOKEN i poświadczenia GCP w .env aby aktywować pełny silnik LLM)."

            # Send reply to Discord channel
            formatted_reply = f"{identity_tag}\n{reply_text}"
            await message.channel.send(formatted_reply[:1900])
        except Exception as err:
            logging.error(f"Error processing Discord message: {err}")
            await message.channel.send(f"⚠️ Błąd silnika AI: {err}")

    await bot.process_commands(message)

if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN:
        print("⚠️ UWAGA: Brak klucza DISCORD_BOT_TOKEN w środowisku .env!")
        print("Postępuj zgodnie z przewodnikiem budowy bota Discord, aby wkleić token.")
    else:
        bot.run(DISCORD_BOT_TOKEN)
