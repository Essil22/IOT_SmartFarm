import paho.mqtt.client as mqtt
import sqlite3
import json
from datetime import datetime
import requests

# ---------------- MQTT ----------------
BROKER  = 'localhost'
PORT    = 1883
TOPICS  = ['farm/temperature', 'farm/humidity', 'farm/moisture', 'farm/light']
DB_PATH = 'C:/Users/essil/Downloads/project/project/smartfarm.db'

# ---------------- TELEGRAM ----------------
BOT_TOKEN = "8803374284:AAGGgXXyO1elaMjYHtkDOaJU1PjhKWZYnaU"
CHAT_ID   = "8010590881"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram error:", e)

# ---------------- THRESHOLDS (same as dashboard) ----------------
THRESHOLDS = {
    "temperature": {"high": 35, "low": 5},
    "humidity":    {"low": 30, "high": 95},
    "moisture":    {"low": 25},
    "light":       {"high": 1200}
}

# ---------------- MQTT CONNECT ----------------
def on_connect(client, userdata, flags, rc):
    print(f"Connected (rc={rc})")
    for topic in TOPICS:
        client.subscribe(topic)
        print(f"Subscribed to {topic}")

# ---------------- MQTT MESSAGE ----------------
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        value = float(payload.get('value', 0))

        # -------- SAVE TO DB --------
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            INSERT INTO sensor_data (topic, value, timestamp)
            VALUES (?, ?, ?)
        ''', (msg.topic, str(value), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        print(f"[{datetime.now()}] {msg.topic} = {value}")

        topic = msg.topic.split('/')[-1]

        # -------- ALERT LOGIC --------
        alert_msg = None

        if topic == "temperature":
            if value > THRESHOLDS["temperature"]["high"]:
                alert_msg = f"🔥 HIGH TEMPERATURE: {value}°C → Irrigation needed"
            elif value < THRESHOLDS["temperature"]["low"]:
                alert_msg = f"❄ LOW TEMPERATURE: {value}°C"

        elif topic == "humidity":
            if value < THRESHOLDS["humidity"]["low"]:
                alert_msg = f"💧 LOW HUMIDITY: {value}%"

        elif topic == "moisture":
            if value < THRESHOLDS["moisture"]["low"]:
                alert_msg = f"🌱 SOIL DRY → Irrigation needed ({value}%)"

        elif topic == "light":
            if value > THRESHOLDS["light"]["high"]:
                alert_msg = f"☀ HIGH LIGHT INTENSITY: {value}"

        # -------- SEND TELEGRAM ALERT --------
        if alert_msg:
            print("ALERT:", alert_msg)
            send_telegram(alert_msg)

    except Exception as e:
        print("Error:", e)

# ---------------- START MQTT CLIENT ----------------
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()