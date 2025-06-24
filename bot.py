import discord
from discord.ext import commands
import paho.mqtt.client as mqtt
import os
import ssl
from dotenv import load_dotenv
import time

# --- Configuración ---
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 8883  
MQTT_TOPIC = "etec/led"


# --- MQTT Client Setup ---
mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Especificamos versión del protocolo

# Configuración SSL 
mqtt_client.tls_set(
    ca_certs=None,
    certfile=None,
    keyfile=None,
    cert_reqs=ssl.CERT_NONE,
    tls_version=ssl.PROTOCOL_TLS,
    ciphers=None
)
mqtt_client.tls_insecure_set(True)  # Necesario para HiveMQ público

# --- Discord Bot ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents) #configuro el bot

def on_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conexión MQTT establecida correctamente")
    else:
        print(f"❌ Error al conectar MQTT. Código: {rc}")

def on_mqtt_disconnect(client, userdata, rc):
    print(f"⚠️ Desconectado de MQTT. Código: {rc}")
    if rc != 0:
        print("Intentando reconexión...")
        time.sleep(5)
        reconnect_mqtt()

def reconnect_mqtt():
    try:
        mqtt_client.reconnect()
        print("♻️ Reconexión MQTT intentada")
    except Exception as e:
        print(f"❌ Error en reconexión: {e}")

mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_disconnect = on_mqtt_disconnect

@bot.event
async def on_ready():
    print(f"✅ Bot de Discord conectado como {bot.user}")
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"❌ Error inicial al conectar a MQTT: {e}")

@bot.command()
async def encender(ctx):
    try:
        mqtt_client.publish(MQTT_TOPIC, "ON")
        await ctx.send("🔆 LED ENCENDIDO")
    except Exception as e:
        await ctx.send(f"❌ Error al enviar comando: {e}")

@bot.command()
async def apagar(ctx):
    try:
        mqtt_client.publish(MQTT_TOPIC, "OFF")
        await ctx.send("💤 LED APAGADO")
    except Exception as e:
        await ctx.send(f"❌ Error al enviar comando: {e}")

@bot.command()
async def habilitar(ctx):
    try:
        mqtt_client.publish(MQTT_TOPIC, "HABILITAR")
        await ctx.send("⚡ Interruptor habilitado (220V ON)")
    except Exception as e:
        await ctx.send(f"❌ Error al enviar comando: {e}")

@bot.command()
async def deshabilitar(ctx):
    try:
        mqtt_client.publish(MQTT_TOPIC, "DESHABILITAR")
        await ctx.send("🚫 Interruptor deshabilitado (220V OFF)")
    except Exception as e:
        await ctx.send(f"❌ Error al enviar comando: {e}")

@bot.command()
async def estado(ctx):
    await ctx.send("ℹ️ Comandos disponibles:\n"
                  "/encender - Enciende el LED\n"
                  "/apagar - Apaga el LED\n"
                  "/habilitar - Activa interruptor 220V\n"
                  "/deshabilitar - Desactiva interruptor 220V")

if __name__ == "__main__":
    try:
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\nApagando bot...")
        mqtt_client.disconnect()
        mqtt_client.loop_stop()