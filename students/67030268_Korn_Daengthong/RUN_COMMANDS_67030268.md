# ⚡ คำสั่งรันโปรเจกต์ประจำตัว (Run Commands Master Guide)
## สำหรับ: 67030268 – นายกร แดงทอง (Korn Daengthong)
### วิชา IoT-App-2569 (Week 01 – Week 12)

เอกสารนี้เป็น **คู่มือรันโปรเจกต์ฉบับเฉพาะบุคคล** ของ **นายกร แดงทอง (รหัส 67030268)** โดยข้อมูลทุกสัปดาห์ (ชื่อ Wi-Fi, BLE Device, MQTT Topic, รหัสบนหน้าปัด Kestrel Dashboard และข้อความบนจอ OLED) ได้รับการผูกค่าเป็นของนักศึกษาเรียบร้อยแล้ว คัดลอกไปวางรันใน Terminal ได้ทันที

---

## 👤 ข้อมูลประจำตัวในระบบ IoT
* **รหัสนักศึกษา (Student ID):** `67030268`
* **ชื่อ-นามสกุล (ไทย):** `นายกร แดงทอง`
* **ชื่อ-นามสกุล (อังกฤษ):** `Korn Daengthong`
* **ชื่อ Wi-Fi SoftAP (Week 06):** `ESP32_AP_0268` (รหัสผ่าน: `12345678`)
* **ชื่อบลูทูธ BLE Provisioning (Week 07):** `PROV_0268`
* **หัวข้อ MQTT Telemetry (Week 11 - 12):** `iot/67030268/telemetry`
* **หัวข้อ MQTT Command (Week 11 - 12):** `iot/67030268/command`
* **วิดเจ็ตหน้าปัดคู่ Kestrel Dashboard (Lab 8.5):**
  * **ด้านซ้าย (Left Widget):** Type 1 = **Analog Speedometer (หน้าปัดไมล์อนาล็อก)**
  * **ด้านขวา (Right Widget):** Type 4 = **Liquid Level Tank (แทงก์ระดับของเหลว)**

---

## ⚡ คำสั่งแปลงโปรเจกต์ทั้ง 12 สัปดาห์เป็นของตนเองอัตโนมัติ (รันครั้งเดียว)
เมื่อเปิด Terminal ในโฟลเดอร์ `IoT-2569-Master-Kit` ให้พิมพ์คำสั่งนี้:
```bash
python3 setup_friend.py --id 67030268 --name-en "Korn Daengthong" --name-th "นายกร แดงทอง" --wifi "IoT-Lab-0268" --pass "12345678"
```
*สคริปต์นี้จะเปลี่ยนรหัสนักศึกษา, ชื่อ, และสร้างหน้าปัด SVG Gauge (Analog Speedometer (หน้าปัดไมล์อนาล็อก) + Liquid Level Tank (แทงก์ระดับของเหลว)) เข้าไปในโค้ด C# และ ESP-IDF ให้อัตโนมัติทันที*

---

## 🔌 การตรวจสอบและเตรียมพอร์ตเชื่อมต่อ ESP32
* **ตรวจสอบและเคลียร์พอร์ตที่ค้างอัตโนมัติ:**
  ```bash
  python3 remote_doctor.py --fix-ports
  ```
* **พอร์ตบนเครื่อง Windows:** เช่น `COM3`, `COM4`
* **พอร์ตบนเครื่อง macOS:** เช่น `/dev/cu.usbserial-0001`

---

## 🚀 สรุปคำสั่งรันทุกแล็บ (คัดลอกไปวางได้เลย)

---

### 🟢 Week 01: Introduction & IoT Architecture (ทำเดี่ยว)
* **วงจร:** วงจรที่ 1 (บอร์ดเปล่าเสียบสาย USB ไม่ต้องต่อ Breadboard)
* **คำสั่งรัน:** เปิด Serial Monitor ดู Boot Log ตรวจสอบชิป ESP32
  ```bash
  idf.py -p <PORT> monitor
  ```
  *(กด `Ctrl + ]` เพื่อออกจากหน้าจอ Monitor)*

---

### 🟢 Week 02: Sensors & Calibration I (POT & LED) (ทำเดี่ยว)
* **วงจร:** วงจรที่ 7 (POT 10k ขา GPIO 34 + หลอดไฟ LED ขา GPIO 2)

#### 1. Lab 2.1: ควบคุมไฟ LED หรี่แสง (PWM Breathing)
```bash
cd Week02_POT_and_LED/ESP32_Project/Lab2-1_LED_Blink 2>/dev/null || cd Week02_POT_and_LED/ESP32_Project/LED_Blink
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 2.2: อ่านค่าแรงดันไฟฟ้าและ ADC Raw จาก Potentiometer 10k
```bash
cd Week02_POT_and_LED/ESP32_Project/Lab2-2_POT_ADC_Read 2>/dev/null || cd Week02_POT_and_LED/ESP32_Project/POT_ADC_Read
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 2.3: อ่านค่ามุมการหมุน (0° ถึง 180°) และหรี่ไฟ LED
```bash
cd Week02_POT_and_LED/ESP32_Project/Lab2-3_POT_Angle_Measure 2>/dev/null || cd Week02_POT_and_LED/ESP32_Project/POT_Angle_Measure
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 03: Sensors & Calibration II (LDR Lux) (ทำเดี่ยว)
* **วงจร:** วงจรที่ 4 (เซนเซอร์แสง LDR + R 10kΩ บนขา GPIO 34)
#### 1. Lab 3.1: อ่านค่าแอนะล็อกดิบจาก LDR (ADC Raw 12-bit)
```bash
cd Week03_LDR_Calibration/67030268_template/Lab3-1_LDR_ADC_Raw 2>/dev/null || cd Week03_LDR_Calibration/67030183_template/Lab3-1_LDR_ADC_Raw
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 3.2: อ่านค่าแรงดันไฟฟ้า (Voltage mV) บันทึกตารางเทียบ Lux
```bash
cd Week03_LDR_Calibration/67030268_template/Lab3-2_LDR_Voltage 2>/dev/null || cd Week03_LDR_Calibration/67030183_template/Lab3-2_LDR_Voltage
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 3.3: มิเตอร์วัดความสว่างเรียลไทม์ (Calibrated Lux)
```bash
cd Week03_LDR_Calibration/67030268_template/Lab3-3_LDR_Lux_Calibrated 2>/dev/null || cd Week03_LDR_Calibration/67030183_template/Lab3-3_LDR_Lux_Calibrated
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 04: LED and RGB Color Sensing (ทำเดี่ยว)
* **วงจร:** วงจรที่ 5 (หลอดไฟแม่สี RGB LED บนขา GPIO 4, 5, 23 + LDR บนขา GPIO 34)

#### 1. Lab 4.1: Hardware Timer Interrupts
```bash
cd Week04_RGB_Color_Sensing/Lab4-1_Hardware_Timer 2>/dev/null || cd Week04_RGB_Color_Sensing/Lab1
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 4.2: ผสมสีแม่สี RGB LED 7 เฉดสี
```bash
cd Week04_RGB_Color_Sensing/Lab4-2_RGB_Color_Mixing 2>/dev/null || cd Week04_RGB_Color_Sensing/Lab2
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 4.3: ตรวจจับสีวัตถุด้วยการวัดแสงสะท้อน LDR
```bash
cd Week04_RGB_Color_Sensing/Lab4-3_Color_Classifier 2>/dev/null || cd Week04_RGB_Color_Sensing/Lab3
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 05: Wi-Fi Station Scan & Connection (ทำเดี่ยว)
* **วงจร:** วงจรที่ 1 (บอร์ดเปล่าเสียบสาย USB)

#### 1. Lab 5.1: สแกนโครงข่าย Wi-Fi ทั้งหมด
```bash
cd Week05_WiFi_ESP32/67030268_template/Lab5-1_WiFi_Scan 2>/dev/null || cd Week05_WiFi_ESP32/67030268_template/lab1
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 5.2: เชื่อมต่อสถานี Wi-Fi Station
```bash
cd Week05_WiFi_ESP32/67030268_template/Lab5-2_WiFi_STA_Connect 2>/dev/null || cd Week05_WiFi_ESP32/67030268_template/lab2
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 5.3: ตรวจสอบ Reason Code ตอนสัญญาณหลุด
```bash
cd Week05_WiFi_ESP32/67030268_template/Lab5-3_WiFi_Disconnect_Reason 2>/dev/null || cd Week05_WiFi_ESP32/67030268_template/lab3
idf.py build
idf.py -p <PORT> flash monitor
```

#### 4. Lab 5.4: ระบบเชื่อมต่อใหม่อัตโนมัติ (Smart Reconnect)
```bash
cd Week05_WiFi_ESP32/67030268_template/Lab5-4_WiFi_Smart_Reconnect 2>/dev/null || cd Week05_WiFi_ESP32/67030268_template/lab4
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 👥 Week 06: Wi-Fi SoftAP & TCP Throughput (ทำคู่ 2 เครื่อง)
* **วงจร:** วงจรที่ 1 (บอร์ดเปล่าเสียบสาย USB)

* **เครื่องที่ 1 (บอร์ด ESP32 ของ Korn Daengthong):** ปล่อย Wi-Fi Hotspot ชื่อ `ESP32_AP_0268`
  ```bash
  cd Week06_SoftAP_FreeRTOS/67030268_template/codes 2>/dev/null || cd Week06_SoftAP_FreeRTOS/67030183_template/codes
  idf.py build
  idf.py -p <PORT> flash monitor
  ```
* **เครื่องที่ 2 (เพื่อน / โน้ตบุ๊ก):** ต่อ Wi-Fi `ESP32_AP_0268` แล้ววัด Bandwidth:
  ```bash
  ping 192.168.4.1
  iperf -c 192.168.4.1 -i 1 -t 10
  ```

---

### 🟢 Week 07: Wi-Fi Provisioning (BLE) (ทำเดี่ยว/คู่)
* **วงจร:** วงจรที่ 1 (บอร์ดเปล่าเสียบสาย USB)
```bash
cd Week07_WiFi_Provisioning/67030268_template/Lab7-3-BLE-Provisioning 2>/dev/null || cd Week07_WiFi_Provisioning/67030183_template/Lab7-3-BLE-Provisioning
idf.py build
idf.py -p <PORT> flash monitor
```
*เปิดแอปมือถือ **ESP BLE Provisioning** แล้วเลือกเชื่อมต่อบลูทูธชื่อ `PROV_0268` เพื่อส่งค่ารหัส Wi-Fi เข้าบอร์ด*

---

### 🟢 Week 08: Kestrel C# Web Server & SVG Dual Dashboard (ทำเดี่ยว)
* **วงจร:** วงจรที่ 1 (บอร์ดเปล่า) หรือ วงจรที่ 3 (POT 10k)

#### 1. Lab 8.1: รัน Kestrel Base Web Server
```bash
cd Week08_Kestrel_and_SVG/Lab8-1
dotnet run
# เปิดดูหน้าเว็บ: http://localhost:5000
```

#### 2. Lab 8.3: Kestrel Serial Gateway ดึงค่าจาก ESP32
* *Terminal 1 (ESP32 ADC Stream):*
  ```bash
  cd Week08_Kestrel_and_SVG/Lab8-3/ESP32_ADC_Stream
  idf.py build && idf.py -p <PORT> flash monitor
  ```
* *Terminal 2 (C# Kestrel Gateway):*
  ```bash
  cd Week08_Kestrel_and_SVG/Lab8-3/Kestrel_Serial_Gateway
  dotnet run
  ```

#### 3. Lab 8.5: Kestrel Dual Dashboard (หน้าปัด SVG ประจำตัวของ 67030268)
* *วิดเจ็ตที่กำหนด:* ซ้าย = **Analog Speedometer (หน้าปัดไมล์อนาล็อก)** | ขวา = **Liquid Level Tank (แทงก์ระดับของเหลว)**
```bash
cd Week08_Kestrel_and_SVG/Lab8-5/Kestrel_Dual_Dashboard
dotnet run
# เปิดดูหน้าจอ Gauge เรียลไทม์: http://localhost:5000
```

---

### 🟢 Week 09: SPI OLED SSD1306 (7-Pin) & Kestrel Web UI (ทำเดี่ยว)
* **วงจร:** วงจรที่ 6 (จอแสดงผล SPI OLED 7 ขา + POT 10k)

#### 1. แฟลชโค้ดขับจอ OLED ลง ESP32
```bash
cd Week09_SPI_OLED_and_UI/67030268_template/Lab9-1_OLED_BringUp 2>/dev/null || cd Week09_SPI_OLED_and_UI/67030183_template/Lab9-1_OLED_BringUp
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. รัน Kestrel Web Server บนคอมพิวเตอร์
```bash
cd Week09_SPI_OLED_and_UI/67030268_template/ESP32.Kestrel.Webserver 2>/dev/null || cd Week09_SPI_OLED_and_UI/67030183_template/ESP32.Kestrel.Webserver
dotnet run
```

#### 3. รัน Serial Bridge ส่งข้อมูลข้ามพอร์ต
```bash
cd Week09_SPI_OLED_and_UI/67030268_template 2>/dev/null || cd Week09_SPI_OLED_and_UI/67030183_template
python3 serial_bridge.py --port <PORT> --baud 115200
```

#### 4. ส่งข้อความรหัสประจำตัวขึ้นบรรทัดแรกของจอ OLED ผ่าน API
```bash
curl -X POST "http://localhost:5000/api/oled" \
     -H "Content-Type: application/json" \
     -d '{"line1":"67030268","line2":"KORN DAENGTH"}'
```

---

### 👥 Week 10: Local Communication Benchmark (HTTP vs UDP vs CoAP) (ทำคู่)
* **วงจร:** วงจรที่ 7 (POT 10k + LED)

#### 1. Lab 10.1: HTTP REST Server & API ควบคุมหลอดไฟ
```bash
cd Week10_HTTP_UDP_CoAP/67030268_template/Lab10-1_HTTP_REST_Server 2>/dev/null || cd Week10_HTTP_UDP_CoAP/Example_ESP32_Project/Lab10-1_HTTP_REST_Server
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 10.2: UDP Telemetry Socket Server (พอร์ต 3333)
```bash
cd Week10_HTTP_UDP_CoAP/67030268_template/Lab10-2_UDP_Telemetry_Socket 2>/dev/null || cd Week10_HTTP_UDP_CoAP/Example_ESP32_Project/Lab10-2_UDP_Telemetry_Socket
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 10.3: CoAP Server สำหรับ IoT มาตรฐาน RFC 7252 (พอร์ต 5683)
```bash
cd Week10_HTTP_UDP_CoAP/67030268_template/Lab10-3_CoAP_Server 2>/dev/null || cd Week10_HTTP_UDP_CoAP/Example_ESP32_Project/Lab10-3_CoAP_Server
idf.py build
idf.py -p <PORT> flash monitor
```

#### 4. Lab 10.4: สคริปต์ Benchmark เปรียบเทียบ RTT และ RAM Footprint
```bash
cd Week10_HTTP_UDP_CoAP/67030268_template 2>/dev/null || cd Week10_HTTP_UDP_CoAP
python3 benchmark_protocols.py --target <ESP32_IP> --rounds 50
```

---

### 👥 Week 11: MQTT Broker, mTLS & ESP RainMaker (ทำคู่)
* **วงจร:** วงจรที่ 7 (POT 10k + LED)

#### 1. เปิด Mosquitto Broker โหมดความปลอดภัย mTLS (Port 8883)
```bash
cd Week11_MQTT_and_RainMaker/mqtt_certs
mosquitto -c mosquitto_ssl.conf -v -p 8883
```

#### 2. ทดสอบรับ-ส่งสัญญาณ Topic ประจำตัวของ 67030268
* **เครื่องผู้รับ (Subscriber):**
  ```bash
  mosquitto_sub -h <BROKER_IP> -p 8883 --cafile ca.crt --cert client.crt --key client.key -t "iot/67030268/telemetry" -v
  ```
* **เครื่องผู้ส่ง (Publisher):**
  ```bash
  mosquitto_pub -h <BROKER_IP> -p 8883 --cafile ca.crt --cert client.crt --key client.key -t "iot/67030268/command" -m '{"led":1,"sender":"67030268"}'
  ```

#### 3. รันสคริปต์เดโมอัตโนมัติรวดเดียว (One-Click)
```bash
cd Week11_MQTT_and_RainMaker
chmod +x lab11_2_demo.sh && ./lab11_2_demo.sh
```

#### 4. แฟลช ESP RainMaker Smart Light
```bash
cd Week11_MQTT_and_RainMaker/Example_project/Lab11-4_RainMaker_Light
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 👥 Week 12: Flutter Mobile IoT & MQTT Dashboard (ทำคู่)
* **โฟลเดอร์:** `Week12_Flutter_MQTT_App/67030268_template/Lab12-4` (หรือ `67030183_template/Lab12-4`)
* **คำสั่งรันแอปพลิเคชันมือถือ:**
```bash
cd Week12_Flutter_MQTT_App/67030268_template/Lab12-4 2>/dev/null || cd Week12_Flutter_MQTT_App/67030183_template/Lab12-4
flutter pub get

# เลือกรันบน Google Chrome (เร็วที่สุด ไม่ต้องเสียบมือถือ):
flutter run -d chrome

# หรือรันบนเครื่อง Mac โดยตรง:
flutter run -d macos
```
*แอปจะเชื่อมต่อเข้า Topic `iot/67030268/telemetry` เพื่อแสดงกราฟ Real-time และกดสวิตช์ส่งคำสั่งไปยัง `iot/67030268/command` อัตโนมัติ*

---
