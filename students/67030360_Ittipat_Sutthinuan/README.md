# 🚀 IoT-App-2569: ชุดโปรเจกต์ประจำตัวฉบับสมบูรณ์ (Standalone Kit)
## นักศึกษา: นายอิทธิพัทธิ์ สุทธินวล (Ittipat Sutthinuan)
### รหัสนักศึกษา: `67030360` | Sec: IoT-App-2569

โฟลเดอร์นี้เป็น **ชุดโปรเจกต์ฉบับสมบูรณ์ที่พร้อมรันและส่งงานได้ทันที** ครบทั้ง 12 สัปดาห์ (Week 01 – Week 12) โดยโค้ด, รายงาน, หัวข้อ MQTT, ชื่อ Wi-Fi/BLE, และหน้าปัด SVG Gauge ได้รับการผูกค่าเป็นของ **นายอิทธิพัทธิ์ สุทธินวล (67030360)** เรียบร้อยแล้ว 100%

---

## 📂 โครงสร้างโฟลเดอร์ของ 67030360

```text
67030360_Ittipat_Sutthinuan/
├── RUN_COMMANDS.md            # ⭐ รวมคำสั่งรันทุกสัปดาห์ ผูกรหัส 67030360 เรียบร้อย
├── circuits/                  # ผังวงจรฮาร์ดแวร์ ESP32 (ครบ 38 ขา) เวกเตอร์และรูปภาพ
├── CIRCUITS_WIRING_GUIDE.md   # คู่มือผังวงจรฮาร์ดแวร์ภาษาไทย
├── CHECKLIST_AND_DATA_COPY.md # ตารางบันทึกค่าสำเร็จรูป (Copy-Paste) ครบ 12 สัปดาห์
├── MASTER_CHECKLIST.md        # Checklist ตรวจงาน + ข้อมูลทำเดี่ยว vs ทำคู่
├── remote_doctor.py           # สคริปต์ตรวจพอร์ต COMx และแก้พอร์ตค้าง
│
├── Week01_Intro/              # Week 01: Introduction & Architecture
├── Week02_POT_and_LED/        # Week 02: Sensors & Calibration I (POT 10k + LED PWM)
├── Week03_LDR_Calibration/    # Week 03: Sensors & Calibration II (LDR Lux)
├── Week04_RGB_Color_Sensing/  # Week 04: RGB LED & Color Sensing
├── Week05_WiFi_ESP32/         # Week 05: Wi-Fi ESP32 Station Scan
├── Week06_SoftAP_FreeRTOS/    # Week 06: SoftAP (ESP32_AP_0360) & TCP Throughput
├── Week07_WiFi_Provisioning/  # Week 07: BLE Provisioning (PROV_0360)
├── Week08_Kestrel_and_SVG/    # Week 08: Kestrel C# Server & Gauge Dashboard
├── Week09_SPI_OLED_and_UI/    # Week 09: SPI OLED (7 ขา) & Kestrel Web UI
├── Week10_HTTP_UDP_CoAP/      # Week 10: Local Communication Benchmark (HTTP/UDP/CoAP)
├── Week11_MQTT_and_RainMaker/ # Week 11: MQTT Broker mTLS (iot/67030360/...) & RainMaker
└── Week12_Flutter_MQTT_App/   # Week 12: Flutter Mobile IoT Dashboard
```

---

## ⚡ เริ่มต้นใช้งานทันที (Quick Start)
1. เปิดไฟล์ [`RUN_COMMANDS.md`](RUN_COMMANDS.md) ในโฟลเดอร์นี้
2. เสียบบอร์ด ESP32 เข้าคอมพิวเตอร์
3. คัดลอกคำสั่งในสัปดาห์ที่ต้องการรันไปวางใน Terminal ได้ทันที!
