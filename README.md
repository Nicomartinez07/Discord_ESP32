# 🔌 Bot de Discord para controlar ESP32 por MQTT

Este proyecto permite controlar dispositivos conectados a una **placa ESP32** (como un LED o un interruptor 220V) mediante comandos enviados desde un **bot de Discord**.

La comunicación se realiza a través de **MQTT**, utilizando un broker público (`broker.hivemq.com`). El bot es una forma sencilla para que cualquier usuario, incluso sin conocimientos técnicos, pueda interactuar con los dispositivos IoT.

---

## 🚀 Comandos disponibles

| Comando en Discord   | Acción que realiza                                 |
|----------------------|----------------------------------------------------|
| `/encender`          | Enciende el LED conectado a la ESP32               |
| `/apagar`            | Apaga el LED conectado a la ESP32                  |
| `/habilitar`         | Habilita el interruptor de 220V                    |
| `/deshabilitar`      | Deshabilita el interruptor de 220V                 |

---

## 🧠 Cómo funciona

1. La ESP32 está conectada al WiFi y suscrita al topic MQTT `etec/led`.
2. El bot de Discord publica mensajes (`ON`, `OFF`, `HABILITAR`, `DESHABILITAR`) en ese topic.
3. La ESP32 recibe el mensaje y actúa sobre los pines correspondientes.

---

## 🛠️ Instalación

### 1. Cloná el repositorio

```bash
git clone https://github.com/tu-usuario/discord-esp32-mqtt-bot.git
cd discord-esp32-mqtt-bot


pip3 install discord.py paho-mqtt
python3 bot.py
