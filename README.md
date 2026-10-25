# 🚀 IoT-2569-Master-Kit

ชุดเครื่องมือและโปรเจกต์รวมสำหรับวิชา **IoT-App-2569** ครบทั้ง 12 สัปดาห์ (Week 01 – Week 12)  
รวบรวมโค้ดที่ต้องรันจริง, Report Templates, ผังวงจร ESP32 (ครบ 38 ขา) ความละเอียดสูง, สคริปต์อัตโนมัติแปลงรหัส/ชื่อเพื่อน (`setup_friend.py`), สคริปต์ตรวจเครื่องและพอร์ต (`remote_doctor.py`), และระบบเชื่อมต่อผ่าน SSH (`ssh_deploy.sh`)

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
IoT-2569-Master-Kit/
├── circuits/                      # ผังวงจรเวกเตอร์ SVG (ครบ 38 ขา) และรูปภาพ PNG ทุกแล็บ
├── CIRCUITS_WIRING_GUIDE.md       # คู่มือผังวงจรฮาร์ดแวร์และการต่อสายไฟทุกแล็บ
├── MASTER_CHECKLIST.md            # Checklist ตรวจงาน + คำสั่ง SSH + สิ่งที่ต้องแคปใน Terminal
├── CHECKLIST_AND_DATA_COPY.md     # ตารางบันทึกค่าสำเร็จรูป (Copy-Paste) ครบ 12 สัปดาห์
├── setup_friend.py                # สคริปต์เปลี่ยนรหัสนักศึกษา/ชื่อ/Wi-Fi และสร้าง SVG Gauge Lab 8.5
├── remote_doctor.py               # สคริปต์ตรวจสอบ IP, พอร์ต ESP32 (COMx), และเคลียร์พอร์ตค้าง
├── ssh_deploy.sh                  # สคริปต์โยนชุดคิทเข้าเครื่องเพื่อนและเปิด SSH ทันที
│
├── Week01_Intro/                  # Week 01: Introduction & IoT Architecture
├── Week02_POT_and_LED/            # Week 02: Sensors and Calibration I (POT & LED PWM)
├── Week03_LDR_Calibration/        # Week 03: Sensors and Calibration II (LDR Lux)
├── Week04_RGB_Color_Sensing/      # Week 04: LED and RGB Color Sensing
├── Week05_WiFi_ESP32/             # Week 05: Wi-Fi ESP32 Station Scan & Reason Codes
├── Week06_SoftAP_FreeRTOS/        # Week 06: Wi-Fi SoftAP, TCP Throughput & FreeRTOS Stack
├── Week07_WiFi_Provisioning/      # Week 07: Wi-Fi Provisioning (BLE & SoftAP)
├── Week08_Kestrel_and_SVG/        # Week 08: Kestrel C# Web Server & SVG Dual Dashboard
├── Week09_SPI_OLED_and_UI/        # Week 09: SPI OLED SSD1306 (7-Pin) & Kestrel Web UI
├── Week10_HTTP_UDP_CoAP/          # Week 10: Local Communication (HTTP REST, UDP, CoAP)
├── Week11_MQTT_and_RainMaker/     # Week 11: MQTT Cloud Broker, mTLS & ESP RainMaker
└── Week12_Flutter_MQTT_App/       # Week 12: Flutter Mobile IoT & MQTT Dashboard
```

---

## ⚡ วิธีใช้งานหน้างาน (Quickstart)

### 1. ให้เพื่อนรันคำสั่งเปิด SSH ครั้งเดียว
* **Windows (PowerShell Admin):**
  ```powershell
  Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0; Start-Service sshd; Set-Service -Name sshd -StartupType 'Automatic'; New-NetFirewallRule -Name "IoT_SSH_Lab" -DisplayName "IoT Lab SSH & Ports" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22,1883,8883,5000,5117; ipconfig | findstr /i "IPv4"
  ```
* **macOS (Terminal):**
  ```bash
  sudo systemsetup -setremotelogin on && ifconfig | grep "inet " | grep -v 127.0.0.1
  ```

### 2. โยนชุด Master Kit เข้าเครื่องเพื่อนผ่าน SSH
```bash
./ssh_deploy.sh <Username_เพื่อน> <IP_เครื่องเพื่อน>
```

### 3. เมื่อล็อกอินเข้าเครื่องเพื่อนแล้ว สั่งแปลงข้อมูลและสร้างโค้ดให้เพื่อนทันที
```bash
cd ~/Desktop/IoT-2569-Master-Kit

# ตรวจสอบพอร์ต ESP32 และเคลียร์พอร์ตที่ค้าง
python3 remote_doctor.py --fix-ports

# เปลี่ยนชื่อ รหัส และสร้างหน้าปัด SVG Gauge Lab 8.5 ให้เพื่อนอัตโนมัติ
python3 setup_friend.py --id 67030XXX --name-en "Friend Name" --name-th "ชื่อเพื่อน" --wifi "WiFi_Name" --pass "WiFi_Pass"
```

---

## 🔌 สรุปการต่อวงจรฮาร์ดแวร์ (Speedrun Strategy)
* **Week 01, 05, 06, 07, 08:** ใช้ **บอร์ดเปล่า (Bare Board)** เสียบสาย Micro-USB อย่างเดียว ไม่ต้องต่อ Breadboard
* **Week 02 (Lab 3), 10, 11, 12:** ใช้ **วงจรที่ 7 (Standard IoT Station: POT GPIO 34 + LED GPIO 2)** ต่อครั้งเดียว ใช้ได้ถึง 4 สัปดาห์ ไม่ต้องรื้อวงจรเลย!
* **Week 03:** LDR + R 10kΩ
* **Week 04:** RGB LED + LDR
* **Week 09:** SPI OLED SSD1306 (7 ขา) + POT
