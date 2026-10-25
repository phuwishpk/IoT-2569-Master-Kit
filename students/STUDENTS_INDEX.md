# 🎓 ดัชนีโฟลเดอร์ใหญ่และชุดโปรเจกต์ประจำตัวรายบุคคล (Students Standalone Kits)
## วิชา IoT-App-2569 ภาคเรียนที่ 2/2568

ทุกโฟลเดอร์ในหน้านี้เป็น **โฟลเดอร์ใหญ่ฉบับสมบูรณ์ (Standalone Big Folder)** ของนักศึกษาแต่ละคน โดยบรรจุโค้ด, รายงาน, ผังวงจร ESP32 (ครบ 38 ขา), และคู่มือคำสั่งรันครบทั้ง 12 สัปดาห์ (Week 01 – Week 12) ที่ได้รับการผูกรหัสนักศึกษา, ชื่อ-นามสกุล, หัวข้อ MQTT, และวิดเจ็ตหน้าปัด SVG Gauge (Lab 8.5) เรียบร้อยแล้ว พร้อมส่งงานและรันได้ทันทีโดยไม่ต้องตั้งค่าใหม่

---

## 📋 รายชื่อนักศึกษาและโฟลเดอร์ใหญ่ประจำตัว

| รหัสนักศึกษา | ชื่อ - นามสกุล | ชื่อภาษาอังกฤษ | วิดเจ็ตหน้าปัด Lab 8.5 (ซ้าย + ขวา) | ลิงก์โฟลเดอร์ใหญ่ประจำตัว | ไฟล์ ZIP ดาวน์โหลด (8 MB) |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **67030248** | นายสุวิจักขณ์ ลาวัง | Suwijak Lawang | Analog Speedometer + 7-Segment | [📂 `67030248_Suwijak_Lawang`](67030248_Suwijak_Lawang/) | [📦 `67030248_Suwijak_Lawang.zip`](zips/67030248_Suwijak_Lawang.zip) |
| **67030249** | นางสาวสุวิมล ศรีประไหม | Suwimon Sripramai | Audio VU Meter + 7-Segment | [📂 `67030249_Suwimon_Sripramai`](67030249_Suwimon_Sripramai/) | [📦 `67030249_Suwimon_Sripramai.zip`](zips/67030249_Suwimon_Sripramai.zip) |
| **67030268** | นายกร แดงทอง | Korn Daengthong | Analog Speedometer + Liquid Tank | [📂 `67030268_Korn_Daengthong`](67030268_Korn_Daengthong/) | [📦 `67030268_Korn_Daengthong.zip`](zips/67030268_Korn_Daengthong.zip) |
| **67030270** | นายกฤษฏิณัช สำราญกิจ | Kritsadinat Samrankit | Retro 7-Segment + Liquid Tank | [📂 `67030270_Kritsadinat_Samrankit`](67030270_Kritsadinat_Samrankit/) | [📦 `67030270_Kritsadinat_Samrankit.zip`](zips/67030270_Kritsadinat_Samrankit.zip) |
| **67030299** | นางสาวธนพร พิศมัย | Thanaporn Pitsamai | Liquid Tank + Retro 7-Segment | [📂 `67030299_Thanaporn_Pitsamai`](67030299_Thanaporn_Pitsamai/) | [📦 `67030299_Thanaporn_Pitsamai.zip`](zips/67030299_Thanaporn_Pitsamai.zip) |
| **67030359** | นายอัฐวุฒิ บัวเรียน | Attawut Bualian | Liquid Tank + Audio VU Meter | [📂 `67030359_Attawut_Bualian`](67030359_Attawut_Bualian/) | [📦 `67030359_Attawut_Bualian.zip`](zips/67030359_Attawut_Bualian.zip) |
| **67030360** | นายอิทธิพัทธิ์ สุทธินวล | Ittipat Sutthinuan | Analog Speedometer + 7-Segment | [📂 `67030360_Ittipat_Sutthinuan`](67030360_Ittipat_Sutthinuan/) | [📦 `67030360_Ittipat_Sutthinuan.zip`](zips/67030360_Ittipat_Sutthinuan.zip) |

---

## 📂 โครงสร้างภายในโฟลเดอร์ของแต่ละคน

```text
67030xxx_FriendName/
├── README.md                  # แนะนำการใช้งานและโปรไฟล์ประจำตัว
├── RUN_COMMANDS.md            # รวมคำสั่งรันทุกแล็บ (ผูกรหัสของตนเองแล้ว)
├── circuits/                  # ผังวงจร ESP32 ครบ 38 ขา (SVG & PNG)
├── CIRCUITS_WIRING_GUIDE.md   # คู่มือต่อสายไฟ Breadboard
├── CHECKLIST_AND_DATA_COPY.md # ตารางบันทึกค่าสำเร็จรูป (Copy-Paste)
├── MASTER_CHECKLIST.md        # ข้อมูลการทำเดี่ยว vs ทำคู่
├── remote_doctor.py           # สคริปต์ตรวจพอร์ต COMx
│
├── Week01_Intro/              # โค้ดและรายงาน Week 01
├── Week02_POT_and_LED/        # โค้ดและรายงาน Week 02
├── Week03_LDR_Calibration/    # โค้ดและรายงาน Week 03 (โฟลเดอร์ <รหัส>_template)
├── Week04_RGB_Color_Sensing/  # โค้ดและรายงาน Week 04 (โฟลเดอร์ <รหัส>)
├── Week05_WiFi_ESP32/         # โค้ดและรายงาน Week 05
├── Week06_SoftAP_FreeRTOS/    # โค้ดและรายงาน Week 06 (SSID: ESP32_AP_<เลขท้าย>)
├── Week07_WiFi_Provisioning/  # โค้ดและรายงาน Week 07 (BLE: PROV_<เลขท้าย>)
├── Week08_Kestrel_and_SVG/    # Kestrel Server & Dual Gauge SVG ตามโจทย์ตนเอง
├── Week09_SPI_OLED_and_UI/    # SPI OLED SSD1306 (OLED Line 1: <รหัส>)
├── Week10_HTTP_UDP_CoAP/      # Benchmark HTTP, UDP, CoAP
├── Week11_MQTT_and_RainMaker/ # Mosquitto mTLS (Topic: iot/<รหัส>/...) & RainMaker
└── Week12_Flutter_MQTT_App/   # แอปพลิเคชันมือถือ Flutter ผูก Topic ตนเอง
```

---

## ⚡ วิธีการนำไปใช้งาน
1. **คัดลอกโฟลเดอร์ของตัวเอง** ไปไว้ที่หน้า Desktop หรือเครื่องของตัวเอง
2. **เปิดไฟล์ `RUN_COMMANDS.md`**
3. เสียบบอร์ด ESP32 แล้วคัดลอกคำสั่งในสัปดาห์นั้นไปวางใน Terminal เพื่อรันได้ทันที
