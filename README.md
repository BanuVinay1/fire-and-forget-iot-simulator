 📌 Fire-and-Forget IoT Simulator
🚀 Simulate IoT Device Data Streaming to Azure IoT Hub
This Python-based simulator mimics an IoT device by generating real-time sensor data (temperature, humidity) and publishing it to Azure IoT Hub using MQTT.

🔹 No physical IoT device needed – Just run and stream data!
🔹 Ideal for testing IoT pipelines, load testing, and real-time analytics.

🔧 Features
✅ Fire-and-Forget Streaming – No retry logic, just send and move on!
✅ Sends Real Sensor Data – Randomized temperature & humidity values.
✅ Uses MQTT Protocol – Communicates with Azure IoT Hub securely.
✅ Can be Extended – Easily modify for multiple devices, AI, or edge computing.


📦 Installation
1️⃣ Clone the Repository

git clone https://github.com/yourusername/fire-and-forget-iot-simulator.git
cd fire-and-forget-iot-simulator

2️⃣ Create a Virtual Environment
python -m venv iot_env
iot_env\Scripts\activate 

3️⃣ Install Dependencies
pip install -r requirements.txt

⚙️ Configuration
Before running the simulator, update your Azure IoT Hub details in the script:

IoT Hub Hostname → "iot-hub-<yourname>.azure-devices.net"
Device ID → "your-device-id"
SAS Token → "Your pre-generated SAS token" (Update the generate_sas.py with device details and run the script to get SAS token)

Run the script to start streaming real-time IoT data to Azure:
python Simulator.py
You'll see live messages being published to Azure IoT Hub.

🔍 Monitor Messages in Azure
To verify data is reaching Azure IoT Hub, use:
az iot hub monitor-events --hub-name <your-iot-hub-name>

OR you can monitor using Overview in your iot hub

📌 Future Enhancements
✅ Multi-Device Support

💡 Contributing
🔥 Feel free to fork this repo, submit PRs, or suggest new features! 🚀

📜 License
This project is licensed under the MIT License.

🚀 Like This? Give It a Star ⭐ on GitHub!
If this project helped you, consider giving it a ⭐ on GitHub & sharing on LinkedIn! 🎉