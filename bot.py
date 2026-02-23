import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# --- 1. LE SERVEUR POUR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot ztv en ligne !"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. CONFIGURATION DU BOT DISCORD (DOIT ÊTRE AVANT LES EVENTS) ---
intents = discord.Intents.default()
intents.message_content = True 

# C'est cette ligne qui définit "bot"
bot = commands.Bot(command_prefix="!", intents=intents)

# --- 3. LES ÉVÉNEMENTS (ON_READY ET ON_MESSAGE) ---

@bot.event
async def on_ready():
    print(f"Le bot est prêt et connecté sous : {bot.user}")

@bot.event
async def on_message(message):
    # Ignore les messages du bot lui-même
    if message.author == bot.user:
        return

    # RÉPOND UNIQUEMENT SI C'EST UN MESSAGE PRIVÉ (DM)
    if isinstance(message.channel, discord.DMChannel):
        
        reponse = f"""Salut {message.author.mention} ! Voici les informations :

:tv: **ACCÈS STREAMS EN DIRECT**
:arrow_right: 

:warning: **LE SITE PEUT SAUTER À TOUT MOMENT** :warning:

:mobile_phone: **ZTV Telegram**: https://t.me/+4lh51n9igUhjN2I0

:fire: NOTRE !PTV – **À PARTIR DE 15€ ICI** :arrow_down:

:information_source: Paiement sécurisé : 
# [Store](https://discord.gg/Z8XABGBBdk)

:question: Questions / Avis clients : 
# [Shop ](https://discord.gg/Z8XABGBBdk)"""

        try:
            await message.channel.send(reponse)
            print(f"Réponse envoyée en MP à {message.author}")
        except discord.Forbidden:
            print(f"Impossible de répondre à {message.author}")

    # Permet au bot de continuer à traiter les commandes si besoin
    await bot.process_commands(message)

# --- 4. LANCEMENT ---
keep_alive()

token = os.getenv('DISCORD_TOKEN') 

if token:
    bot.run(token)
else:
    print("ERREUR : La variable DISCORD_TOKEN n'a pas été trouvée sur Render.")