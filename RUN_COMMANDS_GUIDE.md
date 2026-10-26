# ⚡ คู่มือรวมคำสั่งรันทุกโปรเจกต์ (Run Commands Master Cheat Sheet)
## วิชา IoT-App-2569 ครบทั้ง 13 สัปดาห์ (Week 01 – Week 13)

เอกสารนี้รวบรวม **คำสั่งที่ใช้รันจริงทุกสัปดาห์** ทั้งคำสั่งแฟลชบอร์ด ESP-IDF, คำสั่งรัน Kestrel Server (.NET C#), คำสั่งรัน Python Script / Benchmark, คำสั่งรัน MQTT Mosquitto mTLS, และคำสั่งรันแอปพลิเคชันมือถือ Flutter สามารถคัดลอกไปวางใน Terminal ได้ทันที

---

## 📌 ขั้นตอนเริ่มต้นก่อนรันคำสั่ง (Pre-requisites)

### 1. วิธีเช็กชื่อพอร์ตของบอร์ด ESP32
* **Windows (PowerShell):**
  ```powershell
  Get-CimInstance Win32_SerialPort | Select-Object DeviceID, Description
  # ตัวอย่างพอร์ต: COM3, COM4, COM5
  ```
* **macOS / Linux (Terminal):**
  ```bash
  ls /dev/cu.usbserial* /dev/cu.SLAB_USBtoUART /dev/ttyUSB* 2>/dev/null
  # ตัวอย่างพอร์ต: /dev/cu.usbserial-0001
  ```
* **ใช้เครื่องมือใน Master Kit ตรวจและเคลียร์พอร์ตค้างอัตโนมัติ:**
  ```bash
  python3 remote_doctor.py --fix-ports
  ```

### 2. วิธีโหลด Environment ของ ESP-IDF
* **macOS / Linux:**
  ```bash
  . $HOME/esp/esp-idf/export.sh
  ```
* **Windows (PowerShell):**
  ```powershell
  $env:IDF_PATH\export.ps1
  ```
*(หรือเปิดโปรแกรม **ESP-IDF 5.x PowerShell / Command Prompt** จาก Start Menu)*

---

## 🚀 สรุปคำสั่งรันแยกตามสัปดาห์ (Week 01 – Week 13)

---

### 🟢 Week 01: Introduction & Architecture (ทำเดี่ยว)
* **โฟลเดอร์:** `Week01_Intro/`
* **วัตถุประสงค์:** ตรวจสอบความพร้อมของ ESP-IDF Toolchain และดู Serial Boot Log
```bash
# เปิด Serial Monitor ดู Boot Log ชิป ESP32 (กด Ctrl + ] เพื่อออก)
idf.py -p <PORT> monitor
```

---

### 🟢 Week 02: Sensors and Calibration I (POT & LED) (ทำเดี่ยว)
* **โฟลเดอร์หลัก:** `Week02_POT_and_LED/ESP32_Project/`
* **อุปกรณ์:** บอร์ด ESP32 + Potentiometer (GPIO 34) + LED (GPIO 2)

#### 1. Lab 2.1: ควบคุมความสว่างหลอดไฟ LED หรี่แสง (PWM Breathing)
```bash
cd Week02_POT_and_LED/ESP32_Project/LED_Blink
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 2.2: อ่านค่าแอนะล็อกและแปลงเป็นมุมองศา (0° - 180°)
```bash
cd Week02_POT_and_LED/ESP32_Project/POT_Angle_Measure
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 2.3: ปรับมุม POT หรี่ความสว่างหลอดไฟ LED (Standard IoT Station)
```bash
cd Week02_POT_and_LED/ESP32_Project/POT_ADC_Read
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 03: Sensors and Calibration II (LDR Lux) (ทำเดี่ยว)
* **โฟลเดอร์หลัก:** `Week03_LDR_Calibration/67030183_template/`
* **อุปกรณ์:** บอร์ด ESP32 + LDR ไวแสง + ตัวต้านทาน 10kΩ ต่อแบบ Voltage Divider เข้าขา GPIO 34

#### 1. Lab 3.1: การอ่านค่าแอนะล็อกดิบจาก LDR (ADC Raw 12-bit)
```bash
cd Week03_LDR_Calibration/67030183_template/Lab3-1_LDR_ADC_Raw
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 3.2: การแปลงค่า ADC เป็นแรงดันไฟฟ้า (Voltage mV) สำหรับเก็บข้อมูลทำตาราง
```bash
cd Week03_LDR_Calibration/67030183_template/Lab3-2_LDR_Voltage
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 3.3: มิเตอร์วัดความสว่างเรียลไทม์ (Calibrated Lux) ด้วยสมการ Calibration
```bash
cd Week03_LDR_Calibration/67030183_template/Lab3-3_LDR_Lux_Calibrated
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 04: LED and RGB Color Sensing (ทำเดี่ยว)
* **โฟลเดอร์หลัก:** `Week04_RGB_Color_Sensing/`
* **อุปกรณ์:** บอร์ด ESP32 + RGB LED (GPIO 4, 5, 23) + LDR (GPIO 34)

#### 1. Lab 4.1: Hardware Timer Interrupts
```bash
cd Week04_RGB_Color_Sensing/Lab1
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 4.2: ขับไฟแม่สี RGB LED ผสมสี 7 เฉด
```bash
cd Week04_RGB_Color_Sensing/Lab2
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 4.3: ยิงแสงสะท้อนตรวจจับสีวัตถุด้วย LDR
```bash
cd Week04_RGB_Color_Sensing/Lab3
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 05: Wi-Fi Station Scan & Connection (ทำเดี่ยว)
* **โฟลเดอร์หลัก:** `Week05_WiFi_ESP32/67030183_template/`
* **อุปกรณ์:** บอร์ดเปล่าเสียบสาย USB

#### 1. Lab 5.1: สแกนโครงข่าย Wi-Fi รอบตัว (Scan All APs)
```bash
cd Week05_WiFi_ESP32/67030183_template/lab1
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 5.2 - 5.4: เชื่อมต่อ Wi-Fi และดักจับ Reason Codes
```bash
cd Week05_WiFi_ESP32/67030183_template/lab2
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 👥 Week 06: Wi-Fi SoftAP, TCP Throughput & FreeRTOS (ทำคู่)
* **โฟลเดอร์:** `Week06_SoftAP_FreeRTOS/67030183_template/codes/`
* **เครื่องที่ 1 (ESP32):** ปล่อย Wi-Fi SoftAP
```bash
cd Week06_SoftAP_FreeRTOS/67030183_template/codes
idf.py build
idf.py -p <PORT> flash monitor
# บอร์ดจะปล่อย Wi-Fi ชื่อ ESP32_AP_XXXX (IP: 192.168.4.1)
```

* **เครื่องที่ 2 (เพื่อน / โน้ตบุ๊ก / มือถือ):** ต่อ Wi-Fi ของเพื่อน แล้วยิงทดสอบ Throughput
```bash
# 1. ทดสอบปิงวัดค่าความหน่วง
ping 192.168.4.1

# 2. ยิง iperf วัด Bandwidth (TCP Throughput)
iperf -c 192.168.4.1 -i 1 -t 10
```

---

### 🟢 Week 07: Wi-Fi Provisioning (BLE & SoftAP) (ทำเดี่ยว/คู่)
* **โฟลเดอร์หลัก:** `Week07_WiFi_Provisioning/67030183_template/`
* **อุปกรณ์:** บอร์ด ESP32 + สมาร์ทโฟนเปิดแอป **ESP BLE Provisioning**

#### 1. Lab 7.1: Forensics ตรวจสอบ NVS Flash และล้างค่า
```bash
cd Week07_WiFi_Provisioning/67030183_template/Lab7-1-Reset-and-NVS-Forensics
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 7.3: ปล่อยบลูทูธ (BLE) ให้มือถือค้นพบและส่งค่า Wi-Fi
```bash
cd Week07_WiFi_Provisioning/67030183_template/Lab7-3-BLE-Provisioning
idf.py build
idf.py -p <PORT> flash monitor
# สแกน QR Code หรือเลือกชื่อบอร์ด PROV_XXXX บนมือถือ
```

---

### 🟢 Week 08: Kestrel C# Web Server & SVG Dashboard (ทำเดี่ยว)
* **โฟลเดอร์หลัก:** `Week08_Kestrel_and_SVG/`
* **โปรแกรมที่ต้องใช้:** .NET SDK 8.0+

#### 1. Lab 8.1: รัน Base Kestrel Server
```bash
cd Week08_Kestrel_and_SVG/Lab8-1
dotnet run
# เปิดดูหน้าเว็บที่: http://localhost:5000 หรือ http://localhost:5117
```

#### 2. Lab 8.3: Kestrel Serial Gateway ดึงค่าจาก ESP32
* **Terminal 1 (แฟลช ESP32 ส่งค่า ADC):**
  ```bash
  cd Week08_Kestrel_and_SVG/Lab8-3/ESP32_ADC_Stream
  idf.py build && idf.py -p <PORT> flash monitor
  ```
* **Terminal 2 (รัน Kestrel Gateway เชื่อมพอร์ต COMx):**
  ```bash
  cd Week08_Kestrel_and_SVG/Lab8-3/Kestrel_Serial_Gateway
  dotnet run
  ```

#### 3. Lab 8.5: Kestrel Dual Dashboard (หน้าปัด SVG Gauge มีรหัสและชื่อ)
```bash
cd Week08_Kestrel_and_SVG/Lab8-5/Kestrel_Dual_Dashboard
dotnet run
# เปิดดูหน้าเว็บแบบเรียลไทม์: http://localhost:5000
```

---

### 🟢 Week 09: SPI OLED SSD1306 (7-Pin) & Kestrel Web UI (ทำเดี่ยว)
* **โฟลเดอร์หลัก:** `Week09_SPI_OLED_and_UI/67030183_template/`
* **อุปกรณ์:** บอร์ด ESP32 + จอ OLED 7 ขา + POT 10k

#### 1. แฟลชโค้ดขับจอ OLED ขึ้น ESP32
```bash
cd Week09_SPI_OLED_and_UI/67030183_template/Lab9-1_OLED_BringUp
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. รัน Kestrel Web Server บนคอมพิวเตอร์
```bash
cd Week09_SPI_OLED_and_UI/67030183_template/ESP32.Kestrel.Webserver
dotnet run
```

#### 3. รัน Python Serial Bridge ส่งข้อมูลข้ามพอร์ต
```bash
cd Week09_SPI_OLED_and_UI/67030183_template
python3 serial_bridge.py --port <PORT> --baud 115200
```

#### 4. คำสั่งทดสอบยิงข้อความขึ้นจอ OLED ผ่าน API
```bash
# ส่งข้อความรหัสนักศึกษาขึ้นบรรทัดที่ 1 ของจอ OLED
curl -X POST "http://localhost:5000/api/oled" \
     -H "Content-Type: application/json" \
     -d '{"line1":"67030183","line2":"HELLO IOT"}'
```

---

### 👥 Week 10: Local Communication Benchmark (HTTP vs UDP vs CoAP) (ทำคู่)
* **โฟลเดอร์:** `Week10_HTTP_UDP_CoAP/`
* **อุปกรณ์:** บอร์ด ESP32 วงจรที่ 7 (POT + LED)

#### 1. ฝั่ง ESP32 (เครื่องที่ 1): เปิดเซิร์ฟเวอร์ทั้ง 3 โปรโตคอล
```bash
cd Week10_HTTP_UDP_CoAP/Example_ESP32_Project/Lab10-4_Protocol_Benchmark
idf.py build
idf.py -p <PORT> flash monitor
# สังเกตและจด IP ของ ESP32 เช่น 192.168.1.150
```

#### 2. ฝั่งคอมพิวเตอร์เพื่อน (เครื่องที่ 2): รันชุดทดสอบยิง Benchmark 50 รอบ
```bash
cd Week10_HTTP_UDP_CoAP
python3 benchmark_protocols.py --target-ip <ESP32_IP> --rounds 50
```

---

### 👥 Week 11: MQTT Broker, mTLS & ESP RainMaker (ทำคู่)
* **โฟลเดอร์:** `Week11_MQTT_and_RainMaker/`

#### 1. เปิด Mosquitto Broker โหมดความปลอดภัยสูง (mTLS Port 8883)
```bash
cd Week11_MQTT_and_RainMaker/mqtt_certs
mosquitto -c mosquitto_ssl.conf -v -p 8883
```

#### 2. ทดสอบรับ-ส่งสัญญาณ (Publish / Subscribe ข้ามเครื่อง)
* **เครื่องเพื่อน 1 (ผู้รับ - Subscriber):**
  ```bash
  cd Week11_MQTT_and_RainMaker/mqtt_certs
  mosquitto_sub -h <BROKER_IP> -p 8883 --cafile ca.crt --cert client.crt --key client.key -t "iot/67030183/telemetry" -v
  ```
* **เครื่องเพื่อน 2 (ผู้ส่ง - Publisher):**
  ```bash
  cd Week11_MQTT_and_RainMaker/mqtt_certs
  mosquitto_pub -h <BROKER_IP> -p 8883 --cafile ca.crt --cert client.crt --key client.key -t "iot/67030183/command" -m '{"led":1}'
  ```

#### 3. สคริปต์รันเดโมอัตโนมัติรวดเดียว (One-Click Demo)
```bash
cd Week11_MQTT_and_RainMaker
chmod +x lab11_2_demo.sh && ./lab11_2_demo.sh
```

#### 4. แฟลช ESP RainMaker Smart Light (ESP32)
```bash
cd Week11_MQTT_and_RainMaker/Example_project/Lab11-4_RainMaker_Light
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 👥 Week 12: Flutter Mobile IoT & MQTT Dashboard (ทำคู่)
* **โฟลเดอร์:** `Week12_Flutter_MQTT_App/67030183_template/Lab12-4/`
* **อุปกรณ์:** บอร์ด ESP32 รันโปรเจกต์ Week 11 + สมาร์ทโฟนหรือคอมพิวเตอร์รัน Flutter

#### 1. ดาวน์โหลดแพ็กเกจและรันแอปพลิเคชัน
```bash
cd Week12_Flutter_MQTT_App/67030183_template/Lab12-4
flutter pub get

# เลือกรันบนอุปกรณ์ที่สะดวก:
flutter run -d chrome     # แนะนำ: รันบนเว็บเบราว์เซอร์ เร็วที่สุด ไม่ต้องเสียบมือถือ
# หรือ
flutter run -d macos      # รันเป็นโปรแกรม Desktop บน Mac
# หรือ
flutter run -d windows    # รันเป็นโปรแกรม Desktop บน Windows
```

---


---

### 🟢 Week 13: The Ultimate Converged Edge Gateway (.NET 8 Kestrel & MQTTnet) (ทำเดี่ยว)
* **โฟลเดอร์หลัก:** `Week13_Kestrel_Edge_Gateway/67030183_template/`
* **อุปกรณ์:** บอร์ด ESP32 รันโปรเจกต์สตรีมเซนเซอร์ + คอมพิวเตอร์รัน Kestrel Converged Gateway

#### 1. Lab 13.1: รัน Embedded MQTT Broker (MQTTnet 4.x)
```bash
cd Week13_Kestrel_Edge_Gateway/67030183_template/Lab13-1-Embedded-Broker
dotnet restore
dotnet run
# ทดสอบเชื่อมต่อที่: mqtt://localhost:1883
```

#### 2. Lab 13.2: รัน Hardware Serial to MQTT Bridge
```bash
cd Week13_Kestrel_Edge_Gateway/67030183_template/Lab13-2-Serial-Bridge
dotnet run -- --port <PORT> --baud 115200
```

#### 3. Lab 13.3: รัน Realtime SignalR Hub & Web Dashboard
```bash
cd Week13_Kestrel_Edge_Gateway/67030183_template/Lab13-3-SignalR-Hub
dotnet run --urls="http://0.0.0.0:5123"
# เปิดแดชบอร์ดดูสด: http://localhost:5123
```

#### 4. Lab 13.4: The Grand Finale (All-in-One Converged Gateway)
```bash
cd Week13_Kestrel_Edge_Gateway/67030183_template/Lab13-4-Grand-Finale
dotnet run --urls="http://0.0.0.0:5123"
```

---

## 🛠️ คลินิกแก้ปัญหาและคำสั่งกู้คืน Environment ทั้งหมด (Troubleshooting Master Guide)

รวบรวมข้อผิดพลาด (Errors) ที่พบบ่อยที่สุดของนักศึกษา พร้อมสาเหตุ คำสั่งแก้ปัญหาสำหรับ Windows และ macOS/Linux ครบถ้วน:

---

### 🔴 Case 1: ESP-IDF Environment หาไม่เจอ / `idf.py: command not found`
* **อาการที่พบ:**
  * Windows: `The term 'idf.py' is not recognized as the name of a cmdlet...`
  * macOS / Linux: `zsh: command not found: idf.py` หรือ `bash: idf.py: command not found`
* **สาเหตุ:** เปิด Terminal ปกติที่ยังไม่ได้โหลดตัวแปร Environment ของ ESP-IDF
* **วิธีแก้ไข:**
  * **วิธีที่ 1 (Windows - แนะนำที่สุด):**
    * ปิด Terminal เดิม แล้วเปิดโปรแกรม **ESP-IDF 5.x PowerShell** หรือ **ESP-IDF 5.x CMD** จาก Start Menu โดยตรง (โปรแกรมนี้จะโหลด Environment ครบถ้วนตั้งแต่เปิด)
  * **วิธีที่ 2 (Windows - รันผ่าน PowerShell เดิม):**
    ```powershell
    # กรณีติดตั้งไว้ที่ User Profile มาตรฐาน:
    & "$env:USERPROFILE\esp\esp-idf\export.ps1"

    # กรณีติดตั้งไว้ที่โฟลเดอร์ Espressif:
    & "C:\Espressif\frameworks\esp-idf-v5.3\export.ps1"
    ```
  * **วิธีที่ 3 (macOS / Linux - Terminal):**
    ```bash
    # โหลด Environment ในเซสชันปัจจุบัน:
    . $HOME/esp/esp-idf/export.sh

    # เพิ่มเป็นคำสั่งถาวร (พิมพ์ get_idf เมื่อไหร่ก็พร้อมใช้ทันที):
    echo 'alias get_idf=". $HOME/esp/esp-idf/export.sh"' >> ~/.zshrc
    source ~/.zshrc
    get_idf
    ```
* **วิธีตรวจสอบ:**
  ```bash
  idf.py --version
  # ต้องแสดง: ESP-IDF v5.x.x
  ```

---

### 🔴 Case 2: Python / venv หาไม่เจอ หรือ `ModuleNotFoundError`
* **อาการที่พบ:**
  * `ModuleNotFoundError: No module named 'serial'` (ขาด pyserial)
  * `ModuleNotFoundError: No module named 'paho'` (ขาด paho-mqtt)
  * `error: externally-managed-environment` (บน macOS Homebrew หรือ Ubuntu 23+)
* **สาเหตุ:** ยังไม่ได้ติดตั้ง Python หรือรันข้าม Environment
* **วิธีแก้ไข:**
  * **ติดตั้งแพ็กเกจที่จำเป็นทั้งหมดในคำสั่งเดียว:**
    * **Windows (PowerShell/CMD):**
      ```powershell
      python -m pip install --upgrade pip
      python -m pip install pyserial paho-mqtt requests rich
      ```
    * **macOS / Linux:**
      ```bash
      python3 -m pip install --upgrade pip
      python3 -m pip install pyserial paho-mqtt requests rich
      ```
  * **กรณีติดปัญหา `externally-managed-environment` (สร้าง Virtual Environment):**
    ```bash
    python3 -m venv ~/iot-env
    source ~/iot-env/bin/activate
    pip install pyserial paho-mqtt requests rich
    ```
* **วิธีตรวจสอบ:**
  ```bash
  python3 -c "import serial, paho.mqtt.client, requests; print('✅ All Modules Ready!')"
  ```

---

### 🔴 Case 3: หาพอร์ตบอร์ด ESP32 ไม่เจอ / Port Busy / Access Denied
* **อาการที่พบ:**
  * `A fatal error occurred: Could not open port COMx: [Errno 13] Permission denied`
  * เสียบบอร์ดเข้าคอมแล้ว รัน `find_serial_ports` แต่ไม่ขึ้นชื่อพอร์ตใดๆ
* **สาเหตุ:**
  1. พอร์ตถูกโปรแกรมอื่นค้างเปิดใช้งานอยู่ (เช่น Serial Monitor ใน VS Code, Arduino IDE, PuTTY)
  2. สาย USB เป็นสายชาร์จอย่างเดียว (ไม่มีสายส่งข้อมูล Data)
  3. ยังไม่ได้ลงไดรเวอร์ชิป USB-to-UART (CP2102, CH340, หรือ CH9102)
* **วิธีแก้ไข:**
  * **ขั้นตอนที่ 1: ตรวจสอบและเคลียร์โปรเซสที่ค้างล็อกพอร์ต:**
    ```bash
    # รันสคริปต์หมอประจำโปรเจกต์เพื่อเคลียร์พอร์ตอัตโนมัติ:
    python3 remote_doctor.py --fix-ports
    ```
  * **ขั้นตอนที่ 2: ตรวจหาชื่อพอร์ตจริง:**
    * **Windows (PowerShell):**
      ```powershell
      Get-CimInstance Win32_SerialPort | Select-Object DeviceID, Description
      ```
    * **macOS:**
      ```bash
      ls /dev/cu.usbserial* /dev/cu.SLAB* /dev/cu.wch* 2>/dev/null
      ```
    * **Linux:**
      ```bash
      ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
      ```
  * **ขั้นตอนที่ 3: หากพอร์ตไม่ขึ้นเลย (ลงไดรเวอร์):**
    * ชิป CP2102 (บอร์ด NodeMCU/ESP32 ดำทั่วไป): [Silabs CP210x Driver](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers)
    * ชิป CH340/CH341: [WCH CH341SER Driver](http://www.wch-ic.com/downloads/CH341SER_ZIP.html)

---

### 🔴 Case 4: แฟลชไม่เข้า ค้าง `Connecting........_____.....` Timeout
* **อาการที่พบ:**
  * `Connecting........_____.....`
  * `A fatal error occurred: Failed to connect to ESP32: Timed out waiting for packet header`
* **สาเหตุ:** วงจร Auto-Reset ของบอร์ด ESP32 บางตัวไม่ดึงขา IO0 ลงกราวด์ ทำให้ชิปไม่เข้าสู่โหมด Bootloader
* **วิธีแก้ไข:**
  * **วิธี Manual (กดปุ่ม BOOT):**
    1. รันคำสั่งแฟลชตามปกติ `idf.py -p <PORT> flash monitor`
    2. ทันทีที่หน้าจอขึ้น `Connecting........` ให้ **กดปุ่ม `BOOT` (หรือ `IO0`) บนบอร์ด ESP32 ค้างไว้ 1-2 วินาที** แล้วปล่อย
    3. เมื่อเห็นข้อความ `Chip is ESP32... Writing at 0x00010000...` แสดงว่าแฟลชสำเร็จ
  * **วิธีลด Baud Rate เพื่อความเสถียร:**
    ```bash
    idf.py -p <PORT> -b 115200 flash monitor
    ```
  * **วิธีล้าง Flash ทั้งชิป (กรณี Memory เสียหรือขยะค้าง):**
    ```bash
    idf.py -p <PORT> erase-flash
    idf.py -p <PORT> flash monitor
    ```

---

### 🔴 Case 5: แฟลชผ่านแต่บอร์ดค้าง / Crash Loop (Guru Meditation Error)
* **อาการที่พบ:**
  * `Guru Meditation Error: Core 0 panic'ed`
  * บอร์ดรีสตาร์ทวนลูปเรื่อยๆ พร้อมข้อความ `rst:0x10 (RTCWDT_RTC_RESET)`
* **สาเหตุ:** ไฟเลี้ยงบอร์ดไม่พอ (USB จ่ายกระแสไม่ถึง 500mA โดยเฉพาะตอนเปิด Wi-Fi) หรือ NVS Flash เก็บค่า Wi-Fi เดิมที่ขัดแย้งกัน
* **วิธีแก้ไข:**
  * **วิธีที่ 1: ล้าง NVS Flash และ Erase ชิป:**
    ```bash
    idf.py -p <PORT> erase-flash
    idf.py -p <PORT> flash monitor
    ```
  * **วิธีที่ 2: เช็กสายไฟและพอร์ต USB:**
    * เสียบเข้าพอร์ต USB ด้านหลังของเครื่องคอมพิวเตอร์โดยตรง (หลีกเลี่ยง USB Hub ที่ไม่มีไฟเลี้ยง)
    * ปลดสายไฟที่ต่อกับขา GPIO 0, 2, 12, 15 ชั่วคราวขณะแฟลช (ขากลุ่มนี้เป็น Strapping Pins มีผลต่อการบูต)

---

### 🔴 Case 6: .NET 8 SDK / Kestrel หาไม่เจอ หรือพอร์ต 5000/5123 ชน
* **อาการที่พบ:**
  * `zsh: command not found: dotnet` หรือ `'dotnet' is not recognized...`
  * `System.IO.IOException: Failed to bind to address http://0.0.0.0:5000: address already in use.`
* **สาเหตุ:** ยังไม่ได้ติดตั้ง .NET SDK หรือมี Kestrel Server ตัวเก่ารันค้างอยู่
* **วิธีแก้ไข:**
  * **ติดตั้ง .NET 8 SDK:**
    * ดาวน์โหลดฟรี: [https://dotnet.microsoft.com/download/dotnet/8.0](https://dotnet.microsoft.com/download/dotnet/8.0)
    * ตรวจสอบ: `dotnet --version` (ต้องขึ้น 8.0.x)
  * **สั่งหยุดโปรเซสที่แย่งพอร์ต:**
    * **Windows (PowerShell):**
      ```powershell
      Get-Process -Name "dotnet", "*Kestrel*" -ErrorAction SilentlyContinue | Stop-Process -Force
      ```
    * **macOS / Linux:**
      ```bash
      pkill -f dotnet || sudo lsof -ti:5000,5117,5123 | xargs kill -9 2>/dev/null
      ```
  * **รัน Kestrel แบบระบุ Port เฉพาะกิจ:**
    ```bash
    dotnet run --urls="http://0.0.0.0:5999"
    ```

---

### 🔴 Case 7: Flutter หาไม่เจอ / รันบนเครื่องไม่ได้ (Week 12)
* **อาการที่พบ:**
  * `flutter: command not found`
  * `No connected devices found`
* **สาเหตุ:** ยังไม่ได้เพิ่ม Flutter ลง PATH หรือยังไม่ได้ติดตั้ง Android Emulator
* **วิธีแก้ไข:**
  * **วิธีที่ 1: เพิ่ม Flutter เข้า PATH:**
    * macOS/Linux: `export PATH="$PATH:$HOME/flutter/bin"`
    * Windows: เพิ่มโฟลเดอร์ `C:\src\flutter\bin` ใน Environment Variables
  * **วิธีที่ 2: รันบนเว็บเบราว์เซอร์ Chrome (แนะนำที่สุด — เร็ว ไม่ต้องลง Emulator):**
    ```bash
    cd Week12_Flutter_MQTT_App/67030183_template/Lab12-4
    flutter run -d chrome --web-port=8080
    ```
* **วิธีตรวจสอบ:**
  ```bash
  flutter doctor
  ```

---

### 🔴 Case 8: Mosquitto Broker รันไม่ขึ้น / Port 1883 ชน (Week 11)
* **อาการที่พบ:**
  * `Error: Address already in use` บนพอร์ต 1883 หรือ 8883
* **สาเหตุ:** Mosquitto Background Service ของ Windows หรือ Homebrew รันอยู่แล้ว
* **วิธีแก้ไข:**
  * **Windows (PowerShell):**
    ```powershell
    Stop-Service mosquitto
    taskkill /F /IM mosquitto.exe
    # รันพร้อมไฟล์ config ของวิชานี้:
    cd Week11_MQTT_and_RainMaker
    mosquitto -c mosquitto.conf -v
    ```
  * **macOS:**
    ```bash
    brew services stop mosquitto
    sudo lsof -ti:1883,8883 | xargs kill -9 2>/dev/null
    cd Week11_MQTT_and_RainMaker
    mosquitto -c mosquitto.conf -v
    ```
  * **Linux:**
    ```bash
    sudo systemctl stop mosquitto
    cd Week11_MQTT_and_RainMaker
    mosquitto -c mosquitto.conf -v
    ```

---

### 🔴 Case 9: สิทธิ์เปิดพอร์ตบน Linux ถูกปฏิเสธ (`Permission Denied: /dev/ttyUSB0`)
* **อาการที่พบ:**
  * `serial.serialutil.SerialException: [Errno 13] could not open port /dev/ttyUSB0: [Errno 13] Permission denied`
* **สาเหตุ:** บัญชีผู้ใช้บน Linux (Ubuntu/Debian) ยังไม่ได้อยู่ในกลุ่ม `dialout`
* **วิธีแก้ไข:**
  ```bash
  # 1. เพิ่ม User ปัจจุบันเข้ากลุ่ม dialout
  sudo usermod -a -G dialout $USER

  # 2. ปรับสิทธิ์พอร์ตชั่วคราวให้เขียนได้ทันที
  sudo chmod 666 /dev/ttyUSB0 /dev/ttyACM0 2>/dev/null || true

  # 3. โหลดสิทธิ์ใหม่ (หรือ Logout แล้ว Login ใหม่)
  newgrp dialout
  ```

---

### 🔴 Case 10: เชื่อมต่อ Wi-Fi SoftAP หรือเปิดเว็บข้ามเครื่องไม่ได้
* **อาการที่พบ:**
  * ปิงหา IP บอร์ด หรือ IP เครื่องเพื่อนไม่เจอ (`Request timed out`)
  * เปิดหน้าเว็บ Kestrel ข้ามเครื่องไม่ได้
* **สาเหตุ:** Firewall ของระบบปฏิบัติการปิดกั้น Inbound Traffic หรือเราเตอร์ของหอพัก/มหาวิทยาลัยเปิดโหมด **AP Client Isolation** (ไม่อนุญาตให้อุปกรณ์คุยกันเอง)
* **วิธีแก้ไข:**
  * **วิธีที่ 1 (แนะนำที่สุด): ให้คอมพิวเตอร์และมือถือต่อ Hotspot ส่วนตัวเดียวกัน** (แชร์จากมือถือ 1 เครื่อง จะไม่มีการบล็อกพอร์ตข้ามเครื่อง)
  * **วิธีที่ 2 (ปิด Firewall ชั่วคราวขณะทดสอบ):**
    * **Windows:** ตรวจสอบว่าประเภทเครือข่ายเป็น Private Network หรือสั่งอนุญาตพอร์ต:
      ```powershell
      New-NetFirewallRule -DisplayName "IoT Lab Ports" -Direction Inbound -LocalPort 1883,8883,5000,5117,5123 -Protocol TCP -Action Allow
      ```
    * **macOS:** System Settings -> Network -> Firewall -> อนุญาตโปรแกรม `dotnet` และ `mosquitto`

---
## 🛠️ สรุปเครื่องมือช่วยรันของ Master Kit

```bash
# 1. เปลี่ยนชื่อ, รหัสนักศึกษา, และค่า Wi-Fi ทั้งโปรเจกต์ให้เพื่อนในคำสั่งเดียว
python3 setup_friend.py --id 67030XXX --name-en "Friend Name" --name-th "ชื่อเพื่อน" --wifi "WiFi_Name" --pass "WiFi_Pass"

# 2. ตรวจสอบพอร์ต ซ่อมแซมสิทธิ์ และเคลียร์พอร์ตค้าง
python3 remote_doctor.py --fix-ports

# 3. โยนทั้ง Master Kit เข้าเครื่องเพื่อนผ่าน SSH
./ssh_deploy.sh <ชื่อผู้ใช้เพื่อน> <IP_เครื่องเพื่อน>
```
