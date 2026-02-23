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
    # Render utilise souvent le port 10000 par défaut
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. CONFIGURATION DU BOT ---
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True # Utile pour voir qui rejoint le serveur

bot = commands.Bot(command_prefix="!", intents=intents)

# --- 3. LES ÉVÉNEMENTS ---

@bot.event
async def on_ready():
    print(f"Le bot ZTV est prêt : {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Si le message arrive en MP (DM)
    if isinstance(message.channel, discord.DMChannel):
        reponse = f"""Salut {message.author.mention} ! Voici les informations :

📺 **ACCÈS STREAMS EN DIRECT**
➡️ [LIEN ICI]

⚠️ **LE SITE PEUT SAUTER À TOUT MOMENT** ⚠️

📱 **ZTV Telegram**: https://t.me/+4lh51n9igUhjN2I0

🔥 NOTRE !PTV – **À PARTIR DE 15€ ICI** 👇

ℹ️ Paiement sécurisé : 
# [Store](https://discord.gg/Z8XABGBBdk)

❓ Questions / Avis clients : 
# [Shop](https://discord.gg/Z8XABGBBdk)"""

        try:
            await message.channel.send(reponse)
        except discord.Forbidden:
            pass

    # IMPORTANT : Permet aux commandes (!test, !tarifs) de fonctionner
    await bot.process_commands(message)

# --- 4. EXEMPLE DE COMMANDE ---
@bot.command()
async def info(ctx):
    await ctx.send("ZTV est un service de streaming et d'IPTV de haute qualité ! Envoyez-moi un MP pour plus d'infos.")

# --- 5. LANCEMENT ---
keep_alive()

token = os.getenv('DISCORD_TOKEN') 
if token:
    bot.run(token)
else:
    print("ERREUR : DISCORD_TOKEN manquant dans les variables d'environnement Render.")
