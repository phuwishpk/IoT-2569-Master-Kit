# 📋 คู่มือ Master Checklist: ทำเดี่ยว vs ทำคู่ & สิ่งที่ต้องแคปใน Terminal ครบทั้ง 12 สัปดาห์

เอกสารนี้รวบรวม **การแบ่งประเภทแล็บ (ทำเดี่ยว vs ทำคู่รับ-ส่งสัญญาณ)**, **ข้อความและคำสั่งที่ต้องแคปใน Terminal / Serial Monitor แต่ละแล็บ**, และ **ตารางบันทึกค่าสำเร็จรูป (Copy-Paste)** สำหรับวิชา **IoT-App-2569** ครบทั้ง 12 สัปดาห์

---

## 👥 ส่วนที่ 1: สรุปภาพรวม "แล็บไหนทำเดี่ยว vs แล็บไหนทำคู่ (รับ-ส่งสัญญาณ)?"

| สัปดาห์ (Week) | รูปแบบการทำ | บทบาทและลักษณะการรับ-ส่งสัญญาณ | อุปกรณ์ที่ต้องใช้ |
| :---: | :---: | :--- | :--- |
| **Week 01** | 👤 **ทำเดี่ยว** | ต่อบอร์ด ESP32 รัน Serial Monitor และคุยกับ AI TA 3 หมวด | คอมพิวเตอร์ + ESP32 |
| **Week 02** | 👤 **ทำเดี่ยว** | หมุน Potentiometer และดูไฟกระพริบ LED บนบอร์ดของตัวเอง | บอร์ด ESP32 + POT + LED |
| **Week 03** | 👤 **ทำเดี่ยว** | ส่องไฟฉาย / ปิดมืด เซนเซอร์ LDR เพื่อสอบเทียบค่า Lux vs ADC | บอร์ด ESP32 + LDR + R 10k |
| **Week 04** | 👤 **ทำเดี่ยว** | วางกระดาษสีแดง เขียว น้ำเงิน จ่อเซนเซอร์เพื่อจำแนกสี | บอร์ด ESP32 + RGB LED + LDR |
| **Week 05** | 👤 **ทำเดี่ยว** | สแกนหา Wi-Fi และต่อเน็ต Hotspot ของตัวเอง | คอมพิวเตอร์ + ESP32 |
| ⭐ **Week 06** | 👥 **ทำคู่ (หรือ 2 เครื่อง)** | **เครื่องที่ 1 (ESP32):** ปล่อย Wi-Fi SoftAP `ESP32_AP_0073`<br>**เครื่องที่ 2 (เพื่อน / มือถือ / โน้ตบุ๊ก):** เชื่อมต่อเข้า AP ของเพื่อน แล้วยิง iperf / HTTP request วัด Throughput | ESP32 + โน้ตบุ๊กเพื่อน / สมาร์ทโฟน |
| **Week 07** | 👤 **ทำเดี่ยว (หรือคู่ช่วยกด)** | ESP32 ทำตัวเป็น BLE Peripheral / มือถือเปิดแอปส่งรหัส Wi-Fi | ESP32 + สมาร์ทโฟน |
| **Week 08** | 👤 **ทำเดี่ยว** | รัน Kestrel Web Server บนคอมพิวเตอร์ และเปิดดู Dashboard | คอมพิวเตอร์ |
| **Week 09** | 👤 **ทำเดี่ยว** | ESP32 ขับจอ OLED 7 ขา และรัน Kestrel UI ส่งข้อความผ่าน API | ESP32 + จอ OLED + POT |
| ⭐ **Week 10** | 👥 **ทำคู่ (หรือ 2 จอข้ามเครื่อง)** | **เครื่องที่ 1 (ESP32):** เปิดเซิร์ฟเวอร์ HTTP (80), UDP (3333), CoAP (5683)<br>**เครื่องที่ 2 (คอมพิวเตอร์เพื่อน):** ยิงคำสั่ง Benchmark 50 รอบ วัด RTT ข้ามเครื่อง | ESP32 + คอมพิวเตอร์ในวง LAN เดียวกัน |
| ⭐ **Week 11** | 👥 **ทำคู่ (รับ-ส่ง 3 ช่องทาง)** | **เครื่องที่ 1 (ESP32):** ส่ง Telemetry และรับคำสั่งเปิด-ปิดไฟ<br>**เครื่องที่ 2 (เพื่อน):** รัน Broker + Terminal `sub`/`pub` สลับกับแอปมือถือ RainMaker | ESP32 + คอมพิวเตอร์เพื่อน + สมาร์ทโฟน |
| ⭐ **Week 12** | 👥 **ทำคู่ (ควบคุมระยะไกล)** | **เครื่องที่ 1 (ESP32):** อ่านค่า POT ส่งขึ้น Cloud และรอคำสั่งเปิดไฟ<br>**เครื่องที่ 2 (เพื่อน):** เปิดแอป Flutter กดสวิตช์ไฟและดูกราฟ Real-time | ESP32 + สมาร์ทโฟน / คอมพิวเตอร์เพื่อน |

---

## 🖥️ ส่วนที่ 2: สิ่งที่ต้องแคปใน Terminal / Serial Monitor แต่ละแล็บ (ครบ 12 สัปดาห์)

> [!IMPORTANT]
> **กฎเหล็กการแคปหน้าจอ Terminal / Serial Monitor:**
> 1. ต้องเห็น **คำสั่งที่พิมพ์** (Command Line)
> 2. ต้องเห็น **ข้อความตอบกลับสำเร็จ (Success Logs / Output)**
> 3. สำหรับแล็บที่มีชื่อหรือรหัส (Week 06, 08, 09, 11, 12) **ต้องติดรหัสนักศึกษาของตัวเองชัดเจน**

---

### 🟢 Week 01: Introduction & IoT Architecture (ทำเดี่ยว)
* **สิ่งที่ต้องแคปใน Terminal / หน้าจอ:**
  1. **Terminal Serial Boot Log (1 รูป):** ตอนเสียบ ESP32 เปิด `idf.py monitor` ต้องเห็นข้อความ:
     * `Booting ESP32...`, `ESP-IDF v...`, `Chip is ESP32-D0WDQ6`, `Flash size: 4MB`
  2. **แคปหน้าจอคุยกับ AI TA (12 รูป):** บันทึกรูป `1.png` ถึง `12.png` ครบ 3 หมวด
     * **Category A (4 รูป):** สถาปัตยกรรม IoT, Perception/Network/Middleware Layer
     * **Category B (4 รูป):** ESP-IDF Project Structure, CMakeLists.txt, FreeRTOS Tasks
     * **Category C (4 รูป):** ปัญหา Serial Port Busy, Driver CP2102, Backtrace Analysis

---

### 🟢 Week 02: Sensors & Calibration I (POT & LED) (ทำเดี่ยว)
* **สิ่งที่ต้องแคปใน Terminal:**
  1. **Serial Monitor Lab 2.2 (1 รูป):** หมุนตัวต้านทานปรับค่าได้ (POT 10k) 
     * ต้องเห็นค่าล็อก: `ADC Raw = 2052`, `Voltage = 1.65 V`, `Angle = 90.2 deg`
  2. **Serial Monitor Lab 2.3 (1 รูป):** หมุน POT เพื่อหรี่แสง LED แบบ PWM
     * ต้องเห็นค่า: `POT ADC: 4095 -> PWM Duty: 8191 (100% Brightness)`

---

### 🟢 Week 03: Sensors & Calibration II (LDR Calibration) (ทำเดี่ยว)
* **สิ่งที่ต้องแคปใน Terminal:**
  1. **Serial Monitor วัดแสง LDR (1 รูป):** 
     * ต้องเห็นค่าดิบและแรงดัน: `Raw ADC: 1720`, `Vadc: 1386 mV (1.39 V)`, `Approx Lux: 260`
  2. **รูปกราฟใน Report (1 รูป):** `chart week3.png` พล็อตความสัมพันธ์ระหว่าง ADC Raw กับค่า Lux

---

### 🟢 Week 04: LED and RGB Color Sensing (ทำเดี่ยว)
* **สิ่งที่ต้องแคปใน Terminal:**
  1. **Serial Monitor จำแนกสี (`serial_monitor_log.png` หรือ `terminallab1.png`):**
     * ต้องเห็นการยิงไฟทีละสี:
       ```text
       [TX] RED ON -> LDR ADC: 2845
       [TX] GREEN ON -> LDR ADC: 1120
       [TX] BLUE ON -> LDR ADC: 975
       [CLASSIFIER] Target Color Matched: >> RED << (Confidence: 94.2%)
       ```
  2. **กราฟการทดลอง (4 รูป):** กราฟ Transient Response (สีแดง, สีเขียว, สีน้ำเงิน) + กราฟ Data Selection

---

### 🟡 Week 05: Wi-Fi ESP32 Station (ทำเดี่ยว)
* **สิ่งที่ต้องแคปใน Terminal (ใช้เป็นหลักฐานแทนรูปถ่ายบอร์ด):**
  1. **Terminal Lab 5.1 (Scan APs):** 
     * คำสั่งรันสแกน และผลลัพธ์รายชื่อ Wi-Fi:
       `[WIFI_SCAN] Found 14 Access Points` พร้อมตาราง `SSID | BSSID | RSSI | Channel | Auth`
  2. **Terminal Lab 5.2 (Station Connection):**
     * ต้องเห็นข้อความ: `WIFI_EVENT_STA_CONNECTED`, `got ip: 192.168.x.x`, `netmask: 255.255.255.0`
  3. **Terminal Lab 5.3 (Disconnect Reason Codes):**
     * **เคสที่ 1 (SSID ผิด):** ต้องเห็นข้อความ `WIFI_EVENT_STA_DISCONNECTED`, **`Reason: 201 (NO_AP_FOUND)`**
     * **เคสที่ 2 (รหัสผ่านผิด):** ต้องเห็นข้อความ `WIFI_EVENT_STA_DISCONNECTED`, **`Reason: 202 (AUTH_FAIL)`** หรือ **`Reason: 15 (4WAY_HANDSHAKE_TIMEOUT)`**

---

### ⭐ 🟡 Week 06: Wi-Fi SoftAP, Throughput & FreeRTOS (ทำคู่ / 2 เครื่อง)
* **สิ่งที่ต้องแคปใน Terminal และเบราว์เซอร์:**
  1. **Terminal บอร์ด ESP32 (Lab 6.1):** 
     * ต้องเห็นข้อความประกาศ SoftAP: `[AP_INIT] SSID: ESP32_AP_0073` *(ต้องมีเลขท้าย 4 ตัว)*
     * ตอนเพื่อนหรือมือถือเชื่อมต่อเข้ามา: `[WIFI_EVENT_AP_STACONNECTED] MAC: xx:xx:xx... AID: 1`
  2. **Terminal เครื่องเพื่อน / Client (Lab 6.2 TCP Throughput):**
     * รันสคริปต์วัดความเร็ว: `python3 throughput_test.py --ip 192.168.4.1`
     * ต้องเห็นผลลัพธ์: `Connected to ESP32 SoftAP`, `Transferred: 10.5 MB`, `Throughput: 14.65 Mbps` ที่กำลังส่งระดับต่างๆ
  3. **Terminal ESP32 (Lab 6.3 FreeRTOS Stack):**
     * พิมพ์ค่าหน่วยความจำ: `[TASK_MONITOR] sensor_task HighWaterMark: 2420 Bytes`, `http_task: 3180 Bytes`
  4. **แคปหน้าจอเว็บ Dashboard & API (3 รูป):**
     * `lab64_dashboard.png` (หน้าเว็บเชื่อมต่อ SoftAP)
     * `lab64_api.png` (หน้า JSON `/api/telemetry`)
     * `rssi_vs_throughput.png` (กราฟความเร็ว Throughput เทียบกับ RSSI 5 ระดับ)

---

### 🟡 Week 07: Wi-Fi Provisioning BLE & SoftAP (ทำเดี่ยว / คู่ช่วยกดแอป)
* **สิ่งที่ต้องแคปใน Terminal:**
  1. **Terminal เริ่มต้นทำ BLE Provisioning (Lab 7.2):**
     * ต้องเห็น: `[PROV_MGR] Provisioning service started`, `Device Name: PROV_0073XX`, `PoP: abcd1234`
  2. **Terminal ตอนใส่รหัส PoP ผิด (Security 1 Test):**
     * ต้องเห็นข้อความ Error ตัวแดง: `E (14520) security1: Invalid proof of possession!` / `Verification failed`
  3. **Terminal ตอนตั้งค่า Wi-Fi สำเร็จ & NVS Forensics (Lab 7.1):**
     * ต้องเห็น: `Wi-Fi Credentials received -> SSID: ...`, `Writing to NVS: sta.ssid, sta.pswd`
     * และเมื่อรีบูต: `Reading NVS: sta.ssid ... Auto-connected successfully!`

---

### 🔴 Week 08: Kestrel Web Server & SVG Dashboard (ทำเดี่ยว)
* **สิ่งที่ต้องแคปใน Terminal และเว็บเบราว์เซอร์:**
  1. **Terminal Kestrel Web Server (Lab 8.1):**
     * รันคำสั่ง `dotnet run`
     * ต้องเห็นข้อความ: `info: Microsoft.Hosting.Lifetime[14] Now listening on: http://0.0.0.0:5000`
     * เมื่อมีคำขอเปิด-ปิดไฟ: `[HTTP POST] /api/led/on - Status: 200 OK`
  2. **แคปหน้าเว็บและ API (Lab 8.1 รวม 6 รูป):**
     * `lab8-1_act2_welcome.png`: หน้าแรก `http://localhost:5000/` **ต้องแสดงชื่อ-นามสกุลตัวเอง**
     * `lab8-1_act3_status_json.png`: หน้า `http://localhost:5000/api/status` แสดง JSON สถานะระบบ
     * `lab8-1_act4_led_on.png`: หน้าสั่งเปิดไฟ LED
     * `lab8-1_act4_led_off.png`: หน้าสั่งปิดไฟ LED
     * `lab8-1_act4_terminal_log.png`: ข้อความบน Terminal ตอบรับคำขอ
     * `lab8-1_micro_challenge_student.png`: หน้า `http://localhost:5000/api/student` **ต้องแสดง `studentId: 67030073` และ `studentName` ของตัวเอง**
  3. **วิดีโอ 4 คลิป (Lab 8.2 - 8.5):**
     * Lab 8.5 ต้องโชว์หน้าปัดซ้าย-ขวาที่คำนวณตรงกับเลขท้าย 3 ตัวของรหัสนักศึกษาตัวเอง

---

### 🔴 Week 09: SPI OLED Display & Kestrel UI (ทำเดี่ยว)
* **สิ่งที่ต้องแคปใน Terminal และ API:**
  1. **Terminal Serial Monitor ของ ESP32 (Lab 9.1):**
     * พิมพ์ข้อมูล Framebuffer Hex Dump ของจอภาพ:
       `[OLED_PAGE0] 0x00 0x7F 0x08 0x08 0x08 0x7F ...` (แสดงค่า Hex ของตัวอักษร 'H')
  2. **Terminal รันคำสั่ง curl ทดสอบ Kestrel API (Lab 9.2 รวม 5 รูป):**
     * `lab9_2_curl_get_telemetry.png`: คำสั่ง `curl http://localhost:5117/api/oled/telemetry`
     * `lab9_2_browser_telemetry.png`: เปิดดู JSON บนเบราว์เซอร์
     * `lab9_2_network_devtools.png`: เปิด F12 ดู Network Request Headers
     * `lab9_2_curl_post_calibrate.png`: คำสั่ง `curl -X POST http://localhost:5117/api/oled/calibrate`
     * `lab9_2_curl_post_oled_message.png`: คำสั่ง `curl -X POST http://localhost:5117/api/oled/message -d "ID: 67030073"` **(ต้องส่งรหัสตัวเอง)**
  3. **รูปถ่ายจอจริง OLED (2 รูป):**
     * `lab9_1_oled_result.jpg`: ภาพจอจริงติดชัดเจน แสดงตัวหนังสือ **`HELLO WORLD`** และ **`ID: 67030073`**

---

### ⭐ 🔴 Week 10: HTTP, UDP, CoAP Local Control (ทำคู่ / 2 เครื่อง)
* **สิ่งที่ต้องแคปใน Terminal:**
  1. **Terminal บนบอร์ด ESP32 (เซิร์ฟเวอร์):**
     * ต้องเห็น: `HTTP Server listening on port 80`, `CoAP Server listening on port 5683`, `UDP Socket listening on port 3333`
     * และข้อความ Free Heap RAM (`images/free_heap_status.png`): `esp_get_free_heap_size() = 198420 Bytes`
  2. **Terminal บนเครื่องคอมพิวเตอร์ / เพื่อน (Client Benchmark):**
     * รันคำสั่ง: `python3 benchmark.py --ip <ESP32_IP> --rounds 50`
     * ต้องเห็น **ตารางเปรียบเทียบ RTT 50 รอบ**:
       ```text
       ================ PROTOCOL BENCHMARK SUMMARY (50 ROUNDS) ================
       Protocol      Mean RTT (ms)    Min (ms)    Max (ms)    SD (ms)    Success
       -------------------------------------------------------------------------
       HTTP REST         42.4 ms       29.5 ms     76.2 ms     6.3 ms     100%
       CoAP (CON)        11.8 ms        7.9 ms     23.4 ms     2.4 ms     100%
       Raw UDP            5.8 ms        3.7 ms     13.8 ms     1.2 ms     100%
       =========================================================================
       ```
  3. **Terminal ทดสอบ CoAP โดยเฉพาะ:**
     * รัน `python3 coap_test.py --ip <ESP32_IP>` แสดงการตอบกลับ `2.04 Changed (ACK)`
  4. **รูปถ่ายบอร์ดวงจรจริง (1 รูป):** `images/hardware_setup.jpg`

---

### ⭐ 🟣 Week 11: MQTT Broker, mTLS & ESP RainMaker (ทำคู่ / 2 เครื่อง)
* **สิ่งที่ต้องแคปใน Terminal (รวม 15 รูป):**
  1. **Terminal 1 (Broker Start):** `images/lab11_1_broker_start.png`
     * `mosquitto -c mosquitto_local.conf -v` ขึ้นข้อความ: `Opening ipv4 listen socket on port 1883`, `Opening ipv4 listen socket on port 8883`
  2. **Terminal 2 (MQTT Wildcards):** `images/lab11_1_wildcards.png`
     * `mosquitto_sub -t "iot/67030073/#" -v` ดักจับทุก Topic ย่อย
  3. **Terminal 3 (QoS Comparison):** `images/lab11_1_qos.png`
     * เทียบข้อความส่งแบบ QoS 0, QoS 1, QoS 2
  4. **Terminal 4 (Retained Message):** `images/lab11_1_retain.png`
     * สั่ง `-r` แล้วเปิด Sub ใหม่ได้รับข้อความล่าสุดทันที
  5. **Terminal 5 (LWT Notification):** `images/lab11_1_lwt.png`
     * ถอดสายไฟ ESP32 แล้ว Broker ส่ง `{"online": false}` อัตโนมัติ
  6. **Terminal 6 (Serial Telemetry):** `images/lab11_2_serial_telemetry.png`
     * ESP32 Serial Monitor พิมพ์ `Publishing Telemetry -> {"temp": 28.5, "pot": 2048}`
  7. **Terminal 7 (CLI Sub Telemetry):** `images/lab11_2_cli_telemetry.png`
     * หน้าจอฝั่งเพื่อนได้รับ JSON สตรีมเข้ามาต่อเนื่อง
  8. **Terminal 8 (LED Command):** `images/lab11_2_led_control.png`
     * สั่ง `mosquitto_pub -t "iot/67030073/led/cmd" -m '{"state": true}'` แล้วไฟบนบอร์ดติดทันที
  9. **Terminal 9 (OpenSSL Certs):** `images/lab11_3_openssl_certs.png`
     * แสดงไฟล์ `ca.crt`, `server.crt`, `client.crt`
  10. **Terminal 10 (mTLS Authorized vs Unauthorized):** `images/lab11_3_cli_mtls.png`
      * ลองเชื่อมต่อพอร์ต 8883 แบบไม่ใส่ Cert โดน Reject ทันที
  11. **Terminal 11 (ESP32 mTLS Handshake):** `images/lab11_3_esp32_mtls.png`
      * Serial Monitor ของ ESP32 แสดง `mTLS Handshake Successful! Cipher: TLS_AES_256_GCM_SHA384`
  12. **Terminal 12 (RainMaker QR Code):** `images/lab11_4_qrcode_provision.png`
      * Serial Monitor พิมพ์ ASCII QR Code และ URL ลิงก์สำหรับสแกนเข้าแอป RainMaker

---

### ⭐ 🟣 Week 12: Flutter Mobile IoT & MQTT Dashboard (ทำคู่ / 2 เครื่อง)
* **สิ่งที่ต้องแคปใน Terminal และแอปพลิเคชัน Flutter (รวม 11 รูป):**
  1. **Terminal บอร์ด ESP32 (1 รูป):**
     * ต้องเห็น: ต่อ Wi-Fi สำเร็จ & เชื่อมต่อ MQTT Broker พอร์ต 1883 ได้สำเร็จ
     * ต้องเห็น: ส่ง JSON Telemetry ออก Topic `iot/67030073/telemetry` ทุก 2 วินาที
     * ต้องเห็น: ตอบรับคำสั่งเปิด-ปิดไฟจากแอปมือถือ และส่ง ACK กลับ Topic `iot/67030073/led/state`
  2. **Terminal รัน Flutter (1 รูป):**
     * คำสั่ง `flutter run -d chrome` หรือรันบนเครื่องสมาร์ทโฟน
     * แสดงข้อความ: `Flutter run key commands. Syncing files to device... Connected to MQTT Broker!`
  3. **แคปหน้าจอแอป Flutter บนมือถือ / เบราว์เซอร์ (9 รูป):**
     * **รูปที่ 1 (Connection Screen):** ใส่ IP Broker และขึ้นแถบสีเขียว `Connected`
     * **รูปที่ 2 (Dashboard Telemetry):** ตัวเลขเซนเซอร์อุณหภูมิ, แรงดันไฟฟ้า, และค่ามุมหมุน POT
     * **รูปที่ 3 (Real-time Line Chart):** กราฟเส้นกำลังวาดคลื่นสัญญาณขยับไปทางซ้ายแบบ Real-time
     * **รูปที่ 4 (LED Toggle ON):** กดสวิตช์เปิดไฟ และหลอดไฟบนบอร์ด ESP32 สว่างขึ้นจริง
     * **รูปที่ 5 (LED Toggle OFF):** กดสวิตช์ปิดไฟ และหลอดไฟดับลง
     * **รูปที่ 6 (State Feedback ACK):** ปุ่มสวิตช์แสดงสถานะซิงค์สมบูรณ์เมื่อได้รับข้อความยืนยันจากบอร์ด
     * **รูปที่ 7 (LWT Offline Banner):** ถอดสาย ESP32 แล้วแอปขึ้นแบนเนอร์สีแดงแจ้งเตือน `Device Offline!` ภายใน 15 วินาที
     * **รูปที่ 8 (Message Log Screen):** หน้าแสดงตารางประวัติข้อความ JSON ย้อนหลัง (Timestamp, Topic, Payload)
     * **รูปที่ 9 (Settings Screen):** หน้าตั้งค่า Client ID และ Topic Prefix `iot/67030073` ของตัวเอง
  4. **รูปถ่ายบอร์ดวงจรจริงคู่กับหน้าจอแอป (1 รูป):** `images/hardware_circuit.jpg`

---

## 📊 ส่วนที่ 3: ตาราง Checklist หน้างาน (สำหรับก๊อปปี้ส่งให้เพื่อนติ๊ก)

```markdown
# 📋 แผนตรวจงานและ Checklist ส่งแล็บ IoT ครบ 12 สัปดาห์
ชื่อ-นามสกุล: _______________________ รหัสนักศึกษา: 67030____

### 👤 เฟส 1: แล็บเดี่ยว (บอร์ดเปล่าเสียบสาย USB ไม่ต้องต่อวงจร)
- [ ] **Week 01 (Intro & Architecture)** [เดี่ยว]
  - [ ] แคป Terminal Boot Log ESP32 1 รูป
  - [ ] แคปคุยกับ AI TA ครบ 3 หมวด (A, B, C) รวม 12 รูป
- [ ] **Week 05 (Wi-Fi ESP32 Station)** [เดี่ยว]
  - [ ] แคป Terminal Scan APs (พบ 14 เครือข่าย)
  - [ ] แคป Terminal ต่อ Wi-Fi ได้รับ IP 192.168.x.x
  - [ ] แคป Terminal Disconnect Reason Code 201 (SSID ผิด) และ 202/15 (รหัสผ่านผิด)
- [ ] **Week 07 (Wi-Fi Provisioning)** [เดี่ยว / คู่ช่วยกดมือถือ]
  - [ ] แคป Terminal เริ่มต้น BLE Advertising ชื่อ PROV_0073XX
  - [ ] แคป Terminal ตอนใส่ PoP ผิด (Invalid proof of possession!)
  - [ ] แคป Terminal บันทึก NVS และ Auto-reconnect หลังรีบูต
- [ ] **Week 08 (Kestrel Web Server)** [เดี่ยว]
  - [ ] แคป Terminal รัน dotnet run (Now listening on port 5000)
  - [ ] แคปหน้าแรกโชว์ชื่อตัวเอง + แคป API /api/student โชว์รหัสนักศึกษาตัวเอง (รวม 6 รูป)
  - [ ] อัดคลิปหน้าจอเว็บ 4 คลิป (Lab 8.2 - 8.5 โดย 8.5 ต้องตรงสูตรเลขท้าย 3 ตัว)

### 👤 เฟส 2: แล็บเดี่ยว (ต่อวงจรบน Breadboard)
- [ ] **Week 02 (POT & LED)** [เดี่ยว]
  - [ ] แคป Terminal หมุน POT ดูค่า ADC และ Angle 0°-180°
  - [ ] อัดวิดีโอ 3 คลิป: (1) ไฟกระพริบ, (2) หมุน POT ดูตัวเลข, (3) หมุน POT หรี่ไฟ LED
- [ ] **Week 03 (LDR Calibration)** [เดี่ยว]
  - [ ] แคป Terminal ค่าแสง ADC และแรงดัน 5 ระดับ
  - [ ] กราฟ Scatter chart week3.png + กรอกตาราง Rubric
- [ ] **Week 04 (RGB Color Sensing)** [เดี่ยว]
  - [ ] แคป Terminal ตรวจจับสี (Target Color Matched: RED/GREEN/BLUE)
  - [ ] กราฟ Transient 4 รูป + อัดคลิปส่องกระดาษสี 1 คลิป
- [ ] **Week 09 (SPI OLED & Kestrel UI)** [เดี่ยว]
  - [ ] ถ่ายรูปจอจริง OLED 2 รูป (เห็น HELLO WORLD และ ID: 67030073)
  - [ ] แคป Terminal Framebuffer Hex dump ('H' = 0x7F 0x08 0x08 0x08 0x7F)
  - [ ] แคปคำสั่ง curl ทดสอบ API 5 รูป (POST /api/oled/message ส่งรหัสตัวเอง)
  - [ ] อัดคลิป 1 คลิป หมุน POT เทียบหน้าเว็บคู่กับจอจริง

### 👥 เฟส 3: แล็บคู่ (รับ-ส่งสัญญาณข้ามเครื่องในวง Wi-Fi เดียวกัน)
- [ ] ⭐ **Week 06 (Wi-Fi SoftAP & Throughput)** [ทำคู่]
  - [ ] เครื่อง 1: แคป Terminal ปล่อย AP (ESP32_AP_0073 มีเลขท้าย 4 ตัว)
  - [ ] เครื่อง 2: เพื่อนเชื่อมต่อ AP สำเร็จ (AID: 1)
  - [ ] เครื่อง 2: แคป Terminal รันสคริปต์ Throughput ได้ความเร็ว 5 ระดับกำลังส่ง (กราฟ rssi_vs_throughput.png)
  - [ ] เครื่อง 1: แคป Terminal แสดง FreeRTOS Stack High Water Mark
  - [ ] แคปหน้าจอเว็บ Dashboard & JSON API 3 รูป
- [ ] ⭐ **Week 10 (HTTP, UDP, CoAP Local Control)** [ทำคู่ / 2 เครื่อง]
  - [ ] ถ่ายรูปบอร์ดจริง 1 รูป + แคป Terminal Free Heap RAM 1 รูป
  - [ ] เครื่องเพื่อน: แคป Terminal รัน benchmark.py ได้ตารางสรุป RTT 50 รอบ (HTTP, CoAP, UDP)
  - [ ] อัดวิดีโอ 5 คลิป: HTTP, UDP, CoAP, Benchmark 50 รอบ, จำลองเน็ตหลุด
- [ ] ⭐ **Week 11 (MQTT & ESP RainMaker)** [ทำคู่ / 2 เครื่อง]
  - [ ] ถ่ายรูปบอร์ดจริง 1 รูป + แคป Terminal รวม 15 รูป (Broker 1883/8883, Sub/Pub, mTLS OpenSSL, RainMaker QR)
  - [ ] อัดวิดีโอ 2 คลิป: CLI สั่งเปิดไฟ + 3-Way Synchronization (บอร์ด <-> แอป <-> CLI)
- [ ] ⭐ **Week 12 (Flutter Mobile IoT Dashboard)** [ทำคู่ / 2 เครื่อง]
  - [ ] ถ่ายรูปบอร์ดจริงคู่กับหน้าจอแอป 1 รูป
  - [ ] แคป Terminal ESP32 เชื่อมต่อ Wi-Fi & MQTT และแคป Terminal รัน Flutter 1 รูป
  - [ ] แคปหน้าจอแอป Flutter 9 รูป (Connect, Telemetry, Graph, LED ON/OFF, ACK sync, LWT Banner, Log, Settings)
  - [ ] กรอกตาราง Verification Test Matrix 4 เคส และตาราง Latency ลงใน Report
```
