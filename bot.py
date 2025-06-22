import discord
from discord.ext import commands
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# --- Configuración ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "etec/led"

# --- MQTT ---
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# --- Discord Bot ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.command()
async def encender(ctx):
    mqtt_client.publish(MQTT_TOPIC, "ON")
    await ctx.send("🔆 LED ENCENDIDO")

@bot.command()
async def apagar(ctx):
    mqtt_client.publish(MQTT_TOPIC, "OFF")
    await ctx.send("💤 LED APAGADO")

@bot.command()
async def habilitar(ctx):
    mqtt_client.publish(MQTT_TOPIC, "HABILITAR")
    await ctx.send("⚡ Interruptor habilitado")

@bot.command()
async def deshabilitar(ctx):
    mqtt_client.publish(MQTT_TOPIC, "DESHABILITAR")
    await ctx.send("🚫 Interruptor deshabilitado")

bot.run(DISCORD_TOKEN)
