# ⚡ คู่มือรวมคำสั่งรันทุกโปรเจกต์ (Run Commands Master Cheat Sheet)
## วิชา IoT-App-2569 ครบทั้ง 12 สัปดาห์ (Week 01 – Week 12)

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

## 🚀 สรุปคำสั่งรันแยกตามสัปดาห์ (Week 01 – Week 12)

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

## 🛠️ สรุปเครื่องมือช่วยรันของ Master Kit

```bash
# 1. เปลี่ยนชื่อ, รหัสนักศึกษา, และค่า Wi-Fi ทั้งโปรเจกต์ให้เพื่อนในคำสั่งเดียว
python3 setup_friend.py --id 67030XXX --name-en "Friend Name" --name-th "ชื่อเพื่อน" --wifi "WiFi_Name" --pass "WiFi_Pass"

# 2. ตรวจสอบพอร์ต ซ่อมแซมสิทธิ์ และเคลียร์พอร์ตค้าง
python3 remote_doctor.py --fix-ports

# 3. โยนทั้ง Master Kit เข้าเครื่องเพื่อนผ่าน SSH
./ssh_deploy.sh <ชื่อผู้ใช้เพื่อน> <IP_เครื่องเพื่อน>
```
