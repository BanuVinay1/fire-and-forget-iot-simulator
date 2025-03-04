import paho.mqtt.client as mqtt
import time
import json
import ssl
import random
import uuid
import socket
import os

# Azure IoT Hub Configuration
IOT_HUB_HOSTNAME = "<YOUR_IOT_HUB_NAME>.azure-devices.net"  # Update with your IoT Hub hostname
MQTT_PORT = 8883  # Secure MQTT Port
DEVICE_ID = "<YOUR_DEVICE_ID>"  
USERNAME = f"{IOT_HUB_HOSTNAME}/{DEVICE_ID}/?api-version=2021-04-12"
PASSWORD = "<YOUR_SAS_KEY>"

# Validate IoT Hub Hostname Before Connecting
try:
    resolved_ip = socket.gethostbyname(IOT_HUB_HOSTNAME)
    print(f"Resolved IoT Hub Hostname: {IOT_HUB_HOSTNAME} -> {resolved_ip}")
except socket.gaierror:
    print(f"ERROR: Cannot resolve hostname {IOT_HUB_HOSTNAME}. Check DNS or use the IP address instead.")
    exit(1)  # Exit script if the hostname cannot be resolved

# MQTT Connection Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Connected to Azure IoT Hub as {DEVICE_ID}")
    else:
        print(f"Connection failed with error code {rc}")

def on_disconnect(client, userdata, rc):
    print("🔄 Disconnected! Attempting reconnect...")
    try:
        client.reconnect()
    except Exception as e:
        print(f"Reconnection failed: {e}")

# Initialize MQTT Client
client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
#client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv5)

client.username_pw_set(USERNAME, PASSWORD)

# Proper TLS Configuration
try:
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)  # Enforce proper SSL security
except Exception as e:
    print(f"TLS Setup Failed: {e}, trying with CERT_NONE...")
    client.tls_set(cert_reqs=ssl.CERT_NONE)  # Temporary bypass SSL validation (not recommended for production)

client.on_connect = on_connect
client.on_disconnect = on_disconnect  

# Attempt to Connect to Azure IoT Hub
try:
    client.connect(IOT_HUB_HOSTNAME, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"ERROR: Failed to connect to Azure IoT Hub: {e}")
    exit(1)  # Exit if connection fails

# Failure Simulation Persistence (Downtime Memory)
LAST_FAILURE_FILE = "last_failure.json"

def load_last_failure():
    """Loads last recorded failure time."""
    if os.path.exists(LAST_FAILURE_FILE):
        with open(LAST_FAILURE_FILE, "r") as file:
            return json.load(file).get("last_failure_time", 0)
    return 0

def save_last_failure(timestamp):
    """Saves last failure timestamp."""
    with open(LAST_FAILURE_FILE, "w") as file:
        json.dump({"last_failure_time": timestamp}, file)

last_failure_time = load_last_failure()

def simulate_downtime():
    """Randomly introduces downtime with cooldown to mimic real-world failures."""
    global last_failure_time
    current_time = time.time()

    if current_time - last_failure_time < 900:  # 15 min cooldown
        return  

    if random.random() < 0.01:  # 1% chance per loop (~every few hours)
        downtime_duration = random.randint(60, 300)  # 1-5 min downtime
        last_failure_time = current_time
        save_last_failure(current_time)  

        print(f"SYSTEM FAILURE! No data for {downtime_duration} seconds... Cooling down.")
        time.sleep(downtime_duration)
        print("System Recovered. Resuming data transmission.")

# Generate IoT Sensor Data
def generate_sensor_data():
    """Generates sensor readings with temperature-humidity correlation."""
    base_temp = round(random.uniform(18, 35), 2)
    humidity = round(random.uniform(30, 55) if base_temp > 28 else random.uniform(55, 80), 2)

    return {
        "deviceId": DEVICE_ID,
        "temperature": base_temp,
        "humidity": humidity,
        "status": "ON",
        "timestamp": time.time(),
        "eventId": str(uuid.uuid4())  # Unique event ID
    }

# Main Loop: Publish Sensor Data
while True:
    simulate_downtime()  # Randomly trigger downtime
    
    sensor_data = generate_sensor_data()
    message = json.dumps(sensor_data)

    print(f"📤 Publishing: {message}")
    result = client.publish(f"devices/{DEVICE_ID}/messages/events/", message, qos=1)

    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Publish failed: {result.rc}")

    time.sleep(1)  # Adjust data rate
