#!/usr/bin/env python3
"""
Generate personalized run command guides and setup scripts for each student.
"""

import os
import re

STUDENTS = [
    {
        "id": "67030248",
        "name_th": "นายสุวิจักขณ์ ลาวัง",
        "name_en": "Suwijak Lawang",
        "folder_name": "67030248_Suwijak_Lawang"
    },
    {
        "id": "67030249",
        "name_th": "นางสาวสุวิมล ศรีประไหม",
        "name_en": "Suwimon Sripramai",
        "folder_name": "67030249_Suwimon_Sripramai"
    },
    {
        "id": "67030268",
        "name_th": "นายกร แดงทอง",
        "name_en": "Korn Daengthong",
        "folder_name": "67030268_Korn_Daengthong"
    },
    {
        "id": "67030270",
        "name_th": "นายกฤษฏิณัช สำราญกิจ",
        "name_en": "Kritsadinat Samrankit",
        "folder_name": "67030270_Kritsadinat_Samrankit"
    },
    {
        "id": "67030299",
        "name_th": "นางสาวธนพร พิศมัย",
        "name_en": "Thanaporn Pitsamai",
        "folder_name": "67030299_Thanaporn_Pitsamai"
    },
    {
        "id": "67030359",
        "name_th": "นายอัฐวุฒิ บัวเรียน",
        "name_en": "Attawut Bualian",
        "folder_name": "67030359_Attawut_Bualian"
    },
    {
        "id": "67030360",
        "name_th": "นายอิทธิพัทธิ์ สุทธินวล",
        "name_en": "Ittipat Sutthinuan",
        "folder_name": "67030360_Ittipat_Sutthinuan"
    },
    {
        "id": "67030181",
        "name_th": "นายภูมิพัฒน์ กุลด้วง",
        "name_en": "Phumipat Kulduang",
        "folder_name": "67030181_Phumipat_Kulduang"
    }
]

GAUGE_NAMES = {
    1: "Analog Speedometer (หน้าปัดไมล์อนาล็อก)",
    2: "Audio VU Meter (ไฟระดับเสียง 10 ระดับ)",
    3: "Retro 7-Segment (ตัวเลขดิจิทัล 7 ส่วน)",
    4: "Liquid Level Tank (แทงก์ระดับของเหลว)",
}

def calc_lab85_gauges(student_id: str):
    digits = re.sub(r"\D", "", student_id)
    n = int(digits[-3:]) if len(digits) >= 3 else 183
    left = (n % 4) + 1
    right = ((n // 4) % 4) + 1
    collision = False
    if left == right:
        collision = True
        right = (right % 4) + 1
    return n, left, right, collision

BASE_DIR = "/Users/phuwish/Downloads/fortest week1 week2/IoT-2569-Master-Kit/students"
ARTIFACT_DIR = "/Users/phuwish/.gemini/antigravity/brain/861fb457-eb55-478a-9ecd-4d4221975e10/students"

os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

for st in STUDENTS:
    sid = st["id"]
    nth = st["name_th"]
    nen = st["name_en"]
    folder = st["folder_name"]
    last4 = sid[-4:]
    
    n_code, g_left_id, g_right_id, col = calc_lab85_gauges(sid)
    g_left = GAUGE_NAMES[g_left_id]
    g_right = GAUGE_NAMES[g_right_id]
    
    st_dir = os.path.join(BASE_DIR, folder)
    st_art_dir = os.path.join(ARTIFACT_DIR, folder)
    os.makedirs(st_dir, exist_ok=True)
    os.makedirs(st_art_dir, exist_ok=True)
    
    content = f"""# ⚡ คำสั่งรันโปรเจกต์ประจำตัว (Run Commands Master Guide)
## สำหรับ: {sid} – {nth} ({nen})
### วิชา IoT-App-2569 (Week 01 – Week 12)

เอกสารนี้เป็น **คู่มือรันโปรเจกต์ฉบับเฉพาะบุคคล** ของ **{nth} (รหัส {sid})** โดยข้อมูลทุกสัปดาห์ (ชื่อ Wi-Fi, BLE Device, MQTT Topic, รหัสบนหน้าปัด Kestrel Dashboard และข้อความบนจอ OLED) ได้รับการผูกค่าเป็นของนักศึกษาเรียบร้อยแล้ว คัดลอกไปวางรันใน Terminal ได้ทันที

---

## 👤 ข้อมูลประจำตัวในระบบ IoT
* **รหัสนักศึกษา (Student ID):** `{sid}`
* **ชื่อ-นามสกุล (ไทย):** `{nth}`
* **ชื่อ-นามสกุล (อังกฤษ):** `{nen}`
* **ชื่อ Wi-Fi SoftAP (Week 06):** `ESP32_AP_{last4}` (รหัสผ่าน: `12345678`)
* **ชื่อบลูทูธ BLE Provisioning (Week 07):** `PROV_{last4}`
* **หัวข้อ MQTT Telemetry (Week 11 - 12):** `iot/{sid}/telemetry`
* **หัวข้อ MQTT Command (Week 11 - 12):** `iot/{sid}/command`
* **วิดเจ็ตหน้าปัดคู่ Kestrel Dashboard (Lab 8.5):**
  * **ด้านซ้าย (Left Widget):** Type {g_left_id} = **{g_left}**
  * **ด้านขวา (Right Widget):** Type {g_right_id} = **{g_right}**

---

## ⚡ คำสั่งแปลงโปรเจกต์ทั้ง 12 สัปดาห์เป็นของตนเองอัตโนมัติ (รันครั้งเดียว)
เมื่อเปิด Terminal ในโฟลเดอร์ `IoT-2569-Master-Kit` ให้พิมพ์คำสั่งนี้:
```bash
python3 setup_friend.py --id {sid} --name-en "{nen}" --name-th "{nth}" --wifi "IoT-Lab-{last4}" --pass "12345678"
```
*สคริปต์นี้จะเปลี่ยนรหัสนักศึกษา, ชื่อ, และสร้างหน้าปัด SVG Gauge ({g_left} + {g_right}) เข้าไปในโค้ด C# และ ESP-IDF ให้อัตโนมัติทันที*

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
cd Week02_POT_and_LED/ESP32_Project/LED_Blink
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 2.2: อ่านค่ามุมการหมุนของ Potentiometer 10k (0° ถึง 180°)
```bash
cd Week02_POT_and_LED/ESP32_Project/POT_Angle_Measure
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 2.3: ปรับมุม POT หรี่ไฟ LED แบบเรียลไทม์
```bash
cd Week02_POT_and_LED/ESP32_Project/POT_ADC_Read
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 03: Sensors & Calibration II (LDR Lux) (ทำเดี่ยว)
* **วงจร:** วงจรที่ 4 (เซนเซอร์แสง LDR + R 10kΩ บนขา GPIO 34)
* **คำสั่งรัน:**
```bash
cd Week03_LDR_Calibration/{sid}_template 2>/dev/null || cd Week03_LDR_Calibration/67030183_template
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 04: LED and RGB Color Sensing (ทำเดี่ยว)
* **วงจร:** วงจรที่ 5 (หลอดไฟแม่สี RGB LED บนขา GPIO 4, 5, 23 + LDR บนขา GPIO 34)

#### 1. Lab 4.1: Hardware Timer Interrupts
```bash
cd Week04_RGB_Color_Sensing/Lab1
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 4.2: ผสมสีแม่สี RGB LED 7 เฉดสี
```bash
cd Week04_RGB_Color_Sensing/Lab2
idf.py build
idf.py -p <PORT> flash monitor
```

#### 3. Lab 4.3: ตรวจจับสีวัตถุด้วยการวัดแสงสะท้อน LDR
```bash
cd Week04_RGB_Color_Sensing/Lab3
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 🟢 Week 05: Wi-Fi Station Scan & Connection (ทำเดี่ยว)
* **วงจร:** วงจรที่ 1 (บอร์ดเปล่าเสียบสาย USB)

#### 1. Lab 5.1: สแกนโครงข่าย Wi-Fi ทั้งหมด
```bash
cd Week05_WiFi_ESP32/{sid}_template/lab1 2>/dev/null || cd Week05_WiFi_ESP32/67030183_template/lab1
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. Lab 5.2 - 5.4: เชื่อมต่อ Wi-Fi และแสดง Reason Code ตอนหลุด
```bash
cd Week05_WiFi_ESP32/{sid}_template/lab2 2>/dev/null || cd Week05_WiFi_ESP32/67030183_template/lab2
idf.py build
idf.py -p <PORT> flash monitor
```

---

### 👥 Week 06: Wi-Fi SoftAP & TCP Throughput (ทำคู่ 2 เครื่อง)
* **วงจร:** วงจรที่ 1 (บอร์ดเปล่าเสียบสาย USB)

* **เครื่องที่ 1 (บอร์ด ESP32 ของ {nen}):** ปล่อย Wi-Fi Hotspot ชื่อ `ESP32_AP_{last4}`
  ```bash
  cd Week06_SoftAP_FreeRTOS/{sid}_template/codes 2>/dev/null || cd Week06_SoftAP_FreeRTOS/67030183_template/codes
  idf.py build
  idf.py -p <PORT> flash monitor
  ```
* **เครื่องที่ 2 (เพื่อน / โน้ตบุ๊ก):** ต่อ Wi-Fi `ESP32_AP_{last4}` แล้ววัด Bandwidth:
  ```bash
  ping 192.168.4.1
  iperf -c 192.168.4.1 -i 1 -t 10
  ```

---

### 🟢 Week 07: Wi-Fi Provisioning (BLE) (ทำเดี่ยว/คู่)
* **วงจร:** วงจรที่ 1 (บอร์ดเปล่าเสียบสาย USB)
```bash
cd Week07_WiFi_Provisioning/{sid}_template/Lab7-3-BLE-Provisioning 2>/dev/null || cd Week07_WiFi_Provisioning/67030183_template/Lab7-3-BLE-Provisioning
idf.py build
idf.py -p <PORT> flash monitor
```
*เปิดแอปมือถือ **ESP BLE Provisioning** แล้วเลือกเชื่อมต่อบลูทูธชื่อ `PROV_{last4}` เพื่อส่งค่ารหัส Wi-Fi เข้าบอร์ด*

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

#### 3. Lab 8.5: Kestrel Dual Dashboard (หน้าปัด SVG ประจำตัวของ {sid})
* *วิดเจ็ตที่กำหนด:* ซ้าย = **{g_left}** | ขวา = **{g_right}**
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
cd Week09_SPI_OLED_and_UI/{sid}_template/Lab9-1_OLED_BringUp 2>/dev/null || cd Week09_SPI_OLED_and_UI/67030183_template/Lab9-1_OLED_BringUp
idf.py set-target esp32
idf.py build
idf.py -p <PORT> flash monitor
```

#### 2. รัน Kestrel Web Server บนคอมพิวเตอร์
```bash
cd Week09_SPI_OLED_and_UI/{sid}_template/ESP32.Kestrel.Webserver 2>/dev/null || cd Week09_SPI_OLED_and_UI/67030183_template/ESP32.Kestrel.Webserver
dotnet run
```

#### 3. รัน Serial Bridge ส่งข้อมูลข้ามพอร์ต
```bash
cd Week09_SPI_OLED_and_UI/{sid}_template 2>/dev/null || cd Week09_SPI_OLED_and_UI/67030183_template
python3 serial_bridge.py --port <PORT> --baud 115200
```

#### 4. ส่งข้อความรหัสประจำตัวขึ้นบรรทัดแรกของจอ OLED ผ่าน API
```bash
curl -X POST "http://localhost:5000/api/oled" \\
     -H "Content-Type: application/json" \\
     -d '{{"line1":"{sid}","line2":"{nen[:12].upper()}"}}'
```

---

### 👥 Week 10: Local Communication Benchmark (HTTP vs UDP vs CoAP) (ทำคู่)
* **วงจร:** วงจรที่ 7 (POT 10k + LED)

* **เครื่องที่ 1 (ESP32 ของ {nen}):** เปิด Server HTTP, UDP, CoAP
  ```bash
  cd Week10_HTTP_UDP_CoAP/Example_ESP32_Project/Lab10-4_Protocol_Benchmark
  idf.py build
  idf.py -p <PORT> flash monitor
  # ดู IP ของ ESP32 บนหน้าจอ เช่น 192.168.1.150
  ```
* **เครื่องที่ 2 (คอมพิวเตอร์เพื่อน):** ยิงคำสั่ง Benchmark 50 รอบ วัด RTT
  ```bash
  cd Week10_HTTP_UDP_CoAP
  python3 benchmark_protocols.py --target-ip <ESP32_IP> --rounds 50
  ```

---

### 👥 Week 11: MQTT Broker, mTLS & ESP RainMaker (ทำคู่)
* **วงจร:** วงจรที่ 7 (POT 10k + LED)

#### 1. เปิด Mosquitto Broker โหมดความปลอดภัย mTLS (Port 8883)
```bash
cd Week11_MQTT_and_RainMaker/mqtt_certs
mosquitto -c mosquitto_ssl.conf -v -p 8883
```

#### 2. ทดสอบรับ-ส่งสัญญาณ Topic ประจำตัวของ {sid}
* **เครื่องผู้รับ (Subscriber):**
  ```bash
  mosquitto_sub -h <BROKER_IP> -p 8883 --cafile ca.crt --cert client.crt --key client.key -t "iot/{sid}/telemetry" -v
  ```
* **เครื่องผู้ส่ง (Publisher):**
  ```bash
  mosquitto_pub -h <BROKER_IP> -p 8883 --cafile ca.crt --cert client.crt --key client.key -t "iot/{sid}/command" -m '{{"led":1,"sender":"{sid}"}}'
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
* **โฟลเดอร์:** `Week12_Flutter_MQTT_App/{sid}_template/Lab12-4` (หรือ `67030183_template/Lab12-4`)
* **คำสั่งรันแอปพลิเคชันมือถือ:**
```bash
cd Week12_Flutter_MQTT_App/{sid}_template/Lab12-4 2>/dev/null || cd Week12_Flutter_MQTT_App/67030183_template/Lab12-4
flutter pub get

# เลือกรันบน Google Chrome (เร็วที่สุด ไม่ต้องเสียบมือถือ):
flutter run -d chrome

# หรือรันบนเครื่อง Mac โดยตรง:
flutter run -d macos
```
*แอปจะเชื่อมต่อเข้า Topic `iot/{sid}/telemetry` เพื่อแสดงกราฟ Real-time และกดสวิตช์ส่งคำสั่งไปยัง `iot/{sid}/command` อัตโนมัติ*

---
"""
    
    # Save student guide
    guide_path = os.path.join(st_dir, f"RUN_COMMANDS_{sid}.md")
    art_guide_path = os.path.join(st_art_dir, f"RUN_COMMANDS_{sid}.md")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(content)
    with open(art_guide_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    # Also save a 1-click bash setup script inside each student folder
    setup_sh = f"""#!/bin/bash
# 1-Click Environment Setup for {sid} ({nth})
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for {sid} - {nth}"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id {sid} --name-en "{nen}" --name-th "{nth}" --wifi "IoT-Lab-{last4}" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
"""
    sh_path = os.path.join(st_dir, "setup.sh")
    with open(sh_path, "w", encoding="utf-8") as f:
        f.write(setup_sh)
    os.chmod(sh_path, 0o755)

# Generate STUDENTS_INDEX.md
index_content = """# 🎓 ดัชนีโฟลเดอร์และคู่มือรันโปรเจกต์รายบุคคล (Students Run Directory)
## วิชา IoT-App-2569 ภาคเรียนที่ 2/2568

โฟลเดอร์นี้รวบรวม **ไฟล์คำสั่งรันและสคริปต์ประจำตัวนักศึกษาแต่ละคน** โดยแยกออกเป็นโฟลเดอร์เฉพาะบุคคล ทุกคำสั่งได้รับการผูกรหัสนักศึกษา, ชื่อ-นามสกุล, หัวข้อ MQTT, และวิดเจ็ตหน้าปัด SVG Gauge (Lab 8.5) ตามโจทย์เฉพาะตัวเรียบร้อยแล้ว

---

## 📋 รายชื่อนักศึกษาและลิงก์คู่มือประจำตัว

| รหัสนักศึกษา | ชื่อ - นามสกุล | ชื่อภาษาอังกฤษ | วิดเจ็ตหน้าปัด Lab 8.5 (ซ้าย + ขวา) | ลิงก์โฟลเดอร์และคู่มือคำสั่งรัน |
| :---: | :--- | :--- | :--- | :---: |
"""

for st in STUDENTS:
    sid = st["id"]
    nth = st["name_th"]
    nen = st["name_en"]
    folder = st["folder_name"]
    n_code, g_left_id, g_right_id, col = calc_lab85_gauges(sid)
    g_left = GAUGE_NAMES[g_left_id].split()[0]
    g_right = GAUGE_NAMES[g_right_id].split()[0]
    
    index_content += f"| **{sid}** | {nth} | {nen} | {g_left} + {g_right} | [📂 เปิดโฟลเดอร์ `{folder}`]({folder}/RUN_COMMANDS_{sid}.md) |\n"

index_content += """
---

## ⚡ วิธีใช้งานหน้างานสำหรับเพื่อนแต่ละคน
1. เข้าไปที่โฟลเดอร์ของตัวเอง เช่น `cd students/67030248_Suwijak_Lawang/`
2. เปิดไฟล์ `RUN_COMMANDS_<รหัส>.md`
3. คัดลอกคำสั่งในแต่ละ Week ไปวางใน Terminal ได้ทันที โค้ดและล็อกที่แสดงจะติดชื่อและรหัสของตัวเองถูกต้อง 100%!
"""

with open(os.path.join(BASE_DIR, "STUDENTS_INDEX.md"), "w", encoding="utf-8") as f:
    f.write(index_content)
with open(os.path.join(ARTIFACT_DIR, "STUDENTS_INDEX.md"), "w", encoding="utf-8") as f:
    f.write(index_content)

print(f"Generated personalized guides and setup scripts for all {len(STUDENTS)} students successfully!")
