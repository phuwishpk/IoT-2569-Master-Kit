#!/usr/bin/env python3
"""
Generate vector-perfect SVG diagrams for all 7 circuits of IoT-App-2569.
Native SVG text rendering ensures 100% flawless Thai font shaping (สระไม่ลอย ไม่ซ้อนทับ).
"""

import os

OUTPUT_DIR = "/Users/phuwish/Downloads/fortest week1 week2/IoT-2569-Master-Kit/circuits"
ARTIFACT_DIR = "/Users/phuwish/.gemini/antigravity/brain/861fb457-eb55-478a-9ecd-4d4221975e10/circuits"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

SVG_COMMON_HEADER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 680" width="1100" height="680" style="background:#f8f9fa; font-family: -apple-system, 'Thonburi', 'Sarabun', 'Segoe UI', Arial, sans-serif;">
<defs>
  <style>
    .title { font-size: 24px; font-weight: bold; fill: #0d6efd; }
    .subtitle { font-size: 15px; fill: #495057; }
    .badge-lab { font-size: 14px; font-weight: bold; fill: #6f42c1; }
    .card { fill: #ffffff; stroke: #dee2e6; stroke-width: 1.5; rx: 10; }
    .pcb { fill: #212529; stroke: #495057; stroke-width: 2; rx: 12; }
    .rf-shield { fill: #ced4da; stroke: #adb5bd; stroke-width: 1.5; rx: 4; }
    .pin-label { font-size: 12px; font-family: monospace; font-weight: bold; fill: #f8f9fa; }
    .text-head { font-size: 17px; font-weight: bold; fill: #212529; }
    .text-body { font-size: 14px; fill: #495057; }
    .text-note { font-size: 13px; fill: #6c757d; }
    .wire { stroke-linecap: round; stroke-linejoin: round; fill: none; }
  </style>
</defs>
"""

# ========================================================
# 1. CIRCUIT 1: BARE ESP32
# ========================================================
svg_c1 = SVG_COMMON_HEADER + """
<!-- Header Card -->
<rect x="25" y="20" width="1050" height="105" class="card" />
<text x="45" y="55" class="title">วงจรที่ 1: บอร์ดเปล่า ESP32 (Bare ESP32 Board)</text>
<text x="45" y="82" class="subtitle">เสียบสาย Micro-USB เข้าคอมพิวเตอร์อย่างเดียว ไม่ต้องต่ออุปกรณ์ภายนอกบน Breadboard</text>
<text x="45" y="106" class="badge-lab">📌 ใช้ใน: Week 01, Week 05, Week 06, Week 07, Week 08 (Lab 8.1, 8.2, 8.4, 8.5)</text>

<!-- ESP32 Board -->
<g transform="translate(180, 150)">
  <rect x="0" y="0" width="220" height="420" class="pcb" />
  <rect x="35" y="40" width="150" height="150" class="rf-shield" />
  <text x="50" y="110" font-size="14px" font-weight="bold" fill="#212529">ESP-WROOM-32</text>
  <text x="65" y="130" font-size="11px" fill="#6c757d">Wi-Fi &amp; Bluetooth</text>
  <!-- Buttons -->
  <rect x="20" y="360" width="25" height="20" fill="#dc3545" rx="2" />
  <text x="22" y="350" font-size="11px" fill="#ced4da">EN</text>
  <rect x="175" y="360" width="25" height="20" fill="#495057" rx="2" />
  <text x="170" y="350" font-size="11px" fill="#ced4da">BOOT</text>
  <!-- Micro USB Port -->
  <rect x="85" y="405" width="50" height="25" fill="#adb5bd" rx="3" />
  <text x="97" y="422" font-size="11px" font-weight="bold" fill="#212529">USB</text>
</g>

<!-- USB Cable & Computer -->
<path d="M 290 575 L 290 620 L 520 620 L 520 480" stroke="#343a40" stroke-width="8" class="wire" />
<g transform="translate(460, 240)">
  <!-- Laptop Screen -->
  <rect x="0" y="0" width="260" height="170" rx="8" fill="#e9ecef" stroke="#0d6efd" stroke-width="2" />
  <rect x="15" y="15" width="230" height="140" fill="#212529" rx="4" />
  <text x="35" y="70" font-size="16px" font-weight="bold" fill="#ffffff">Computer / Terminal</text>
  <text x="35" y="100" font-size="13px" font-family="monospace" fill="#20c997">$ idf.py monitor</text>
  <text x="35" y="125" font-size="12px" font-family="monospace" fill="#0dcaf0">ESP32 Connected: OK</text>
  <!-- Laptop Base -->
  <polygon points="-20,170 280,170 260,195 0,195" fill="#adb5bd" />
</g>

<!-- Info & Guidance Card -->
<rect x="760" y="150" width="315" height="420" class="card" />
<text x="785" y="185" class="text-head" fill="#0d6efd">📝 สรุปการใช้งานวงจรนี้</text>
<text x="785" y="220" class="text-head" font-size="14px">1. Week 01 (Intro &amp; Architecture)</text>
<text x="800" y="240" class="text-body">• ทดสอบคอมไพล์และเปิดดู Serial Monitor</text>
<text x="785" y="275" class="text-head" font-size="14px">2. Week 05 (Wi-Fi ESP32 Station)</text>
<text x="800" y="295" class="text-body">• สแกนคลื่นสัญญาณ Wi-Fi รอบตัว 2.4 GHz</text>
<text x="785" y="330" class="text-head" font-size="14px">3. Week 06 (SoftAP &amp; Throughput)</text>
<text x="800" y="350" class="text-body">• ปล่อย SSID: ESP32_AP_XXXX ในตัว</text>
<text x="785" y="385" class="text-head" font-size="14px">4. Week 07 (Wi-Fi Provisioning)</text>
<text x="800" y="405" class="text-body">• ทำ BLE / SoftAP Provisioning ผ่านมือถือ</text>
<text x="785" y="440" class="text-head" font-size="14px">5. Week 08 (Kestrel Web Server)</text>
<text x="800" y="460" class="text-body">• รันเซิร์ฟเวอร์บนคอมพิวเตอร์จำลองค่า</text>

<rect x="780" y="495" width="275" height="55" rx="6" fill="#e7f1ff" stroke="#b6d4fe" />
<text x="795" y="520" font-size="12px" font-weight="bold" fill="#0d6efd">💡 เทคนิคหน้างาน:</text>
<text x="795" y="538" font-size="12px" fill="#495057">ใช้สาย Micro-USB Data (ไม่ใช่สายชาร์จ)</text>
</svg>
"""

# ========================================================
# 7. CIRCUIT 7: STANDARD IOT STATION (POT + LED) - MASTER!
# ========================================================
svg_c7 = SVG_COMMON_HEADER + """
<!-- Header Card -->
<rect x="25" y="20" width="1050" height="105" class="card" />
<text x="45" y="55" class="title">วงจรที่ 7: สถานี IoT มาตรฐาน (Standard IoT Station: POT 10k + LED)</text>
<text x="45" y="82" class="subtitle">เซนเซอร์วัดค่าแอนะล็อก Potentiometer (GPIO 34) และหลอดไฟ LED ผ่าน R 220Ω (GPIO 2)</text>
<text x="45" y="106" class="badge-lab" fill="#198754">⭐⭐ วงจรมาสเตอร์ยอดฮิต! ใช้วงจรเดียวกัน 100% สำหรับ: Week 02 (Lab 3), Week 10, Week 11, Week 12</text>

<!-- ESP32 Board -->
<g transform="translate(60, 150)">
  <rect x="0" y="0" width="200" height="420" class="pcb" />
  <rect x="30" y="40" width="140" height="140" class="rf-shield" />
  <text x="42" y="110" font-size="13px" font-weight="bold" fill="#212529">ESP-WROOM-32</text>
  <text x="50" y="130" font-size="11px" fill="#6c757d">NodeMCU-32S</text>
  <!-- Pins Left -->
  <circle cx="0" cy="80" r="4" fill="#ffc107" /><text x="12" y="84" class="pin-label">3V3</text>
  <circle cx="0" cy="180" r="4" fill="#ffc107" /><text x="12" y="184" class="pin-label" fill="#0dcaf0">G34 (ADC)</text>
  <circle cx="0" cy="380" r="4" fill="#ffc107" /><text x="12" y="384" class="pin-label">GND</text>
  <!-- Pins Right -->
  <circle cx="200" cy="80" r="4" fill="#ffc107" /><text x="160" y="84" class="pin-label">GND</text>
  <circle cx="200" cy="320" r="4" fill="#ffc107" /><text x="145" y="324" class="pin-label" fill="#ffc107">G2 (LED)</text>
</g>

<!-- Breadboard Container -->
<g transform="translate(340, 150)">
  <rect x="0" y="0" width="360" height="420" rx="10" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="130" y="25" font-size="13px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- Potentiometer 10k -->
  <g transform="translate(40, 60)">
    <rect x="0" y="0" width="120" height="160" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="60" cy="65" r="40" fill="#0d6efd" opacity="0.85" />
    <circle cx="60" cy="65" r="22" fill="#e9ecef" />
    <line x1="60" y1="65" x2="80" y2="45" stroke="#0d6efd" stroke-width="4" stroke-linecap="round" />
    <text x="15" y="125" font-size="12px" font-weight="bold" fill="#212529">Potentiometer</text>
    <text x="40" y="145" font-size="12px" fill="#0d6efd">10 kΩ</text>
    <!-- 3 Pins -->
    <circle cx="25" cy="175" r="5" fill="#dc3545" /><text x="15" y="195" font-size="11px" fill="#dc3545">3.3V</text>
    <circle cx="60" cy="175" r="5" fill="#0d6efd" /><text x="48" y="210" font-size="12px" font-weight="bold" fill="#0d6efd">GPIO 34</text>
    <circle cx="95" cy="175" r="5" fill="#212529" /><text x="85" y="195" font-size="11px" fill="#212529">GND</text>
  </g>

  <!-- LED & Resistor 220 Ohm -->
  <g transform="translate(200, 60)">
    <rect x="0" y="0" width="120" height="160" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <!-- LED Bulb -->
    <circle cx="60" cy="55" r="25" fill="#dc3545" opacity="0.9" />
    <polygon points="45,75 75,75 60,95" fill="#dc3545" />
    <text x="35" y="125" font-size="12px" font-weight="bold" fill="#212529">LED Red</text>
    <!-- Resistor 220 Ohm -->
    <rect x="35" y="145" width="50" height="16" rx="3" fill="#e2d9cc" stroke="#8b7355" stroke-width="1.5" />
    <line x1="45" y1="145" x2="45" y2="161" stroke="#dc3545" stroke-width="3" />
    <line x1="55" y1="145" x2="55" y2="161" stroke="#dc3545" stroke-width="3" />
    <line x1="65" y1="145" x2="65" y2="161" stroke="#8b4513" stroke-width="3" />
    <!-- LED Pins -->
    <circle cx="45" cy="180" r="5" fill="#fd7e14" /><text x="25" y="200" font-size="11px" fill="#fd7e14">R 220Ω</text>
    <text x="30" y="215" font-size="10px" fill="#fd7e14">(Anode +)</text>
    <circle cx="85" cy="180" r="5" fill="#212529" /><text x="75" y="200" font-size="11px" fill="#212529">GND</text>
    <text x="70" y="215" font-size="10px" fill="#212529">(Cathode -)</text>
  </g>
</g>

<!-- Wires -->
<!-- 1. 3.3V (Red) -> POT Pin 1 -->
<path d="M 60 230 L 25 230 L 25 400 L 365 400 L 365 325" stroke="#dc3545" stroke-width="4" class="wire" />
<!-- 2. GPIO 34 (Blue) -> POT Wiper -->
<path d="M 60 330 L 40 330 L 40 430 L 400 430 L 400 325" stroke="#0d6efd" stroke-width="4" class="wire" />
<!-- 3. GND (Black) -> POT Pin 3 -->
<path d="M 60 530 L 15 530 L 15 460 L 435 460 L 435 325" stroke="#212529" stroke-width="4" class="wire" />

<!-- 4. GPIO 2 (Orange) -> Resistor 220 Ohm -->
<path d="M 260 470 L 305 470 L 305 490 L 585 490 L 585 325" stroke="#fd7e14" stroke-width="4" class="wire" />
<!-- 5. GND (Black) -> LED Cathode -->
<path d="M 260 230 L 315 230 L 315 520 L 625 520 L 625 325" stroke="#212529" stroke-width="4" class="wire" />

<!-- Pinout & Instruction Table (Right Side) -->
<rect x="735" y="150" width="340" height="420" class="card" />
<text x="755" y="185" class="text-head" fill="#0d6efd">📋 ตารางการต่อสาย (Pinout Table)</text>

<g transform="translate(755, 205)">
  <rect x="0" y="0" width="300" height="35" fill="#f8f9fa" rx="4" />
  <circle cx="15" cy="18" r="6" fill="#dc3545" />
  <text x="35" y="16" font-size="13px" font-weight="bold" fill="#dc3545">3.3V (VCC)</text>
  <text x="125" y="16" font-size="12px" fill="#495057">ต่อเข้า ขา 1 ของ POT</text>
  <text x="35" y="30" font-size="11px" fill="#6c757d">สายสีแดง (ห้ามต่อ 5V)</text>
</g>

<g transform="translate(755, 250)">
  <rect x="0" y="0" width="300" height="35" fill="#f8f9fa" rx="4" />
  <circle cx="15" cy="18" r="6" fill="#0d6efd" />
  <text x="35" y="16" font-size="13px" font-weight="bold" fill="#0d6efd">GPIO 34</text>
  <text x="125" y="16" font-size="12px" fill="#495057">ต่อเข้า ขากลาง (Wiper)</text>
  <text x="35" y="30" font-size="11px" fill="#6c757d">สายสีน้ำเงิน (ADC1_CH6)</text>
</g>

<g transform="translate(755, 295)">
  <rect x="0" y="0" width="300" height="35" fill="#f8f9fa" rx="4" />
  <circle cx="15" cy="18" r="6" fill="#fd7e14" />
  <text x="35" y="16" font-size="13px" font-weight="bold" fill="#fd7e14">GPIO 2</text>
  <text x="125" y="16" font-size="12px" fill="#495057">ต่อ R 220Ω &gt; Anode (+)</text>
  <text x="35" y="30" font-size="11px" fill="#6c757d">สายสีส้ม (สัญญาณสั่งเปิดไฟ)</text>
</g>

<g transform="translate(755, 340)">
  <rect x="0" y="0" width="300" height="35" fill="#f8f9fa" rx="4" />
  <circle cx="15" cy="18" r="6" fill="#212529" />
  <text x="35" y="16" font-size="13px" font-weight="bold" fill="#212529">GND (กราวด์)</text>
  <text x="125" y="16" font-size="12px" fill="#495057">ต่อ ขา 3 POT &amp; Cathode</text>
  <text x="35" y="30" font-size="11px" fill="#6c757d">สายสีดำ (กราวด์ร่วม)</text>
</g>

<rect x="750" y="395" width="310" height="155" rx="6" fill="#d1e7dd" stroke="#a3cfbb" />
<text x="765" y="420" font-size="13px" font-weight="bold" fill="#0f5132">🎯 ข้อดีของการต่อวงจรนี้:</text>
<text x="765" y="445" font-size="12px" fill="#0f5132">• ต่อครั้งเดียวที่สัปดาห์ 2 (Lab 2.3)</text>
<text x="765" y="468" font-size="12px" fill="#0f5132">• สัปดาห์ 10 (HTTP/UDP/CoAP) ใช้บอร์ดเดิมได้เลย</text>
<text x="765" y="491" font-size="12px" fill="#0f5132">• สัปดาห์ 11 (MQTT / RainMaker) ใช้บอร์ดเดิม</text>
<text x="765" y="514" font-size="12px" fill="#0f5132">• สัปดาห์ 12 (Flutter Mobile) ใช้บอร์ดเดิม</text>
<text x="765" y="537" font-size="12px" font-weight="bold" fill="#0f5132">✨ สรุป: ไม่ต้องรื้อวงจรใหม่ถึง 4 สัปดาห์!</text>
</svg>
"""

# ========================================================
# 6. CIRCUIT 6: SPI OLED + POT (Week 09)
# ========================================================
svg_c6 = SVG_COMMON_HEADER + """
<!-- Header Card -->
<rect x="25" y="20" width="1050" height="105" class="card" />
<text x="45" y="55" class="title">วงจรที่ 6: จอแสดงผล SPI OLED SSD1306 (7 ขา) ร่วมกับ Potentiometer</text>
<text x="45" y="82" class="subtitle">ควบคุมจอแสดงผล 128x64 ผ่านบัสความเร็วสูง SPI2 (10 MHz) พร้อมอ่านค่า Potentiometer (GPIO 34)</text>
<text x="45" y="106" class="badge-lab">📌 ใช้ใน: Week 09 (SPI OLED and Kestrel UI)</text>

<!-- ESP32 Board -->
<g transform="translate(60, 150)">
  <rect x="0" y="0" width="200" height="420" class="pcb" />
  <rect x="30" y="40" width="140" height="140" class="rf-shield" />
  <text x="42" y="110" font-size="13px" font-weight="bold" fill="#212529">ESP-WROOM-32</text>
  <text x="50" y="130" font-size="11px" fill="#6c757d">NodeMCU-32S</text>
  <!-- Pins Left -->
  <circle cx="0" cy="80" r="4" fill="#ffc107" /><text x="12" y="84" class="pin-label">3V3</text>
  <circle cx="0" cy="180" r="4" fill="#ffc107" /><text x="12" y="184" class="pin-label" fill="#0dcaf0">G34 (POT)</text>
  <circle cx="0" cy="380" r="4" fill="#ffc107" /><text x="12" y="384" class="pin-label">GND</text>
  <!-- Pins Right (SPI) -->
  <circle cx="200" cy="110" r="4" fill="#ffc107" /><text x="140" y="114" class="pin-label" fill="#a370f7">G23 (D1)</text>
  <circle cx="200" cy="230" r="4" fill="#ffc107" /><text x="140" y="234" class="pin-label" fill="#20c997">G18 (D0)</text>
  <circle cx="200" cy="260" r="4" fill="#ffc107" /><text x="145" y="264" class="pin-label" fill="#fd7e14">G5 (CS)</text>
  <circle cx="200" cy="290" r="4" fill="#ffc107" /><text x="145" y="294" class="pin-label" fill="#0dcaf0">G4 (RES)</text>
  <circle cx="200" cy="320" r="4" fill="#ffc107" /><text x="145" y="324" class="pin-label" fill="#d63384">G2 (DC)</text>
</g>

<!-- OLED Module 128x64 -->
<g transform="translate(360, 150)">
  <rect x="0" y="0" width="310" height="230" rx="10" fill="#212529" stroke="#495057" stroke-width="2" />
  <!-- Display Glass -->
  <rect x="25" y="65" width="260" height="140" rx="4" fill="#050811" stroke="#343a40" />
  <text x="55" y="115" font-size="18px" font-weight="bold" fill="#0dcaf0" font-family="monospace">HELLO WORLD</text>
  <text x="55" y="145" font-size="16px" font-weight="bold" fill="#ffc107" font-family="monospace">ID: 67030XXX</text>
  <text x="55" y="175" font-size="14px" fill="#20c997" font-family="monospace">ADC: 2048 (1.65V)</text>
  
  <!-- 7 Pins Header -->
  <g transform="translate(20, 10)">
    <text x="10" y="15" font-size="11px" font-family="monospace" fill="#ced4da">GND VCC D0  D1 RES  DC  CS</text>
    <circle cx="20" cy="30" r="4" fill="#ffc107" />
    <circle cx="50" cy="30" r="4" fill="#dc3545" />
    <circle cx="80" cy="30" r="4" fill="#20c997" />
    <circle cx="110" cy="30" r="4" fill="#a370f7" />
    <circle cx="145" cy="30" r="4" fill="#0dcaf0" />
    <circle cx="180" cy="30" r="4" fill="#d63384" />
    <circle cx="215" cy="30" r="4" fill="#fd7e14" />
  </g>
</g>

<!-- Potentiometer Container -->
<g transform="translate(360, 410)">
  <rect x="0" y="0" width="310" height="160" rx="8" fill="#ffffff" stroke="#dee2e6" />
  <circle cx="80" cy="80" r="40" fill="#0d6efd" opacity="0.85" />
  <circle cx="80" cy="80" r="22" fill="#e9ecef" />
  <line x1="80" y1="80" x2="100" y2="60" stroke="#0d6efd" stroke-width="4" stroke-linecap="round" />
  <text x="140" y="70" font-size="14px" font-weight="bold" fill="#212529">Potentiometer 10k</text>
  <text x="140" y="95" font-size="12px" fill="#0d6efd">ขากลาง -&gt; GPIO 34</text>
  <text x="140" y="118" font-size="12px" fill="#6c757d">ขาข้าง -&gt; 3.3V และ GND</text>
</g>

<!-- Pinout Table -->
<rect x="710" y="150" width="365" height="420" class="card" />
<text x="730" y="185" class="text-head" fill="#0d6efd">📌 ตารางการต่อขา OLED 7 ขา (SSD1306)</text>

<g transform="translate(730, 205)" font-size="12px">
  <text x="0" y="18" font-weight="bold" fill="#212529">1. GND</text><text x="120" y="18" fill="#495057">-&gt; ขา GND บนบอร์ด (กราวด์)</text>
  <text x="0" y="46" font-weight="bold" fill="#dc3545">2. VCC</text><text x="120" y="46" fill="#495057">-&gt; ขา 3.3V (ไฟเลี้ยงจอภาพ)</text>
  <text x="0" y="74" font-weight="bold" fill="#20c997">3. D0 (SCK)</text><text x="120" y="74" fill="#495057">-&gt; GPIO 18 (SPI Clock)</text>
  <text x="0" y="102" font-weight="bold" fill="#a370f7">4. D1 (MOSI)</text><text x="120" y="102" fill="#495057">-&gt; GPIO 23 (SPI Data Out)</text>
  <text x="0" y="130" font-weight="bold" fill="#0dcaf0">5. RES (Reset)</text><text x="120" y="130" fill="#495057">-&gt; GPIO 4 (Active Low)</text>
  <text x="0" y="158" font-weight="bold" fill="#d63384">6. DC (Data/Cmd)</text><text x="120" y="158" fill="#495057">-&gt; GPIO 2 (0=Cmd, 1=Data)</text>
  <text x="0" y="186" font-weight="bold" fill="#fd7e14">7. CS (Chip Select)</text><text x="120" y="186" fill="#495057">-&gt; GPIO 5 (Active Low)</text>
</g>

<rect x="725" y="415" width="335" height="135" rx="6" fill="#fff3cd" stroke="#ffecb5" />
<text x="740" y="440" font-size="13px" font-weight="bold" fill="#664d03">⚠️ ข้อควรระวังหน้างาน:</text>
<text x="740" y="465" font-size="12px" fill="#664d03">• ห้ามสลับสาย DC (GPIO 2) กับ RES (GPIO 4)</text>
<text x="740" y="488" font-size="12px" fill="#664d03">• หากหน้าจอมืด ให้เช็คสาย SCK (GPIO 18)</text>
<text x="740" y="511" font-size="12px" fill="#664d03">• ถ่ายรูปจอจริง ต้องเห็นตัวหนังสือชัดเจน</text>
<text x="755" y="532" font-size="11px" font-weight="bold" fill="#0d6efd">"HELLO WORLD" และ "ID: 67030XXX"</text>
</svg>
"""

# ========================================================
# 4. CIRCUIT 4: LDR VOLTAGE DIVIDER (Week 03)
# ========================================================
svg_c4 = SVG_COMMON_HEADER + """
<!-- Header Card -->
<rect x="25" y="20" width="1050" height="105" class="card" />
<text x="45" y="55" class="title">วงจรที่ 4: วงจรแบ่งแรงดันเซนเซอร์แสง LDR ร่วมกับ R 10kΩ</text>
<text x="45" y="82" class="subtitle">ต่อตัวต้านทานไวแสง (LDR) อนุกรมกับตัวต้านทานคงที่ 10kΩ ดึงแรงดันตกคร่อมเข้าขา GPIO 34 (ADC1)</text>
<text x="45" y="106" class="badge-lab">📌 ใช้ใน: Week 03 (Sensors &amp; Calibration II)</text>

<!-- ESP32 Board -->
<g transform="translate(80, 150)">
  <rect x="0" y="0" width="200" height="420" class="pcb" />
  <rect x="30" y="40" width="140" height="140" class="rf-shield" />
  <text x="42" y="110" font-size="13px" font-weight="bold" fill="#212529">ESP-WROOM-32</text>
  <!-- Pins Left -->
  <circle cx="0" cy="80" r="4" fill="#ffc107" /><text x="12" y="84" class="pin-label">3V3</text>
  <circle cx="0" cy="180" r="4" fill="#ffc107" /><text x="12" y="184" class="pin-label" fill="#0dcaf0">G34 (ADC)</text>
  <circle cx="0" cy="380" r="4" fill="#ffc107" /><text x="12" y="384" class="pin-label">GND</text>
</g>

<!-- Breadboard Voltage Divider -->
<g transform="translate(380, 150)">
  <rect x="0" y="0" width="310" height="420" rx="10" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="110" y="30" font-size="13px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- LDR Component -->
  <g transform="translate(95, 60)">
    <circle cx="60" cy="50" r="30" fill="#ffeaa7" stroke="#fdcb6e" stroke-width="3" />
    <path d="M 45 40 Q 55 30 65 50 T 75 60" fill="none" stroke="#d63031" stroke-width="3" />
    <text x="25" y="105" font-size="13px" font-weight="bold" fill="#212529">LDR (Photoresistor)</text>
    <circle cx="40" cy="120" r="4" fill="#dc3545" /><text x="25" y="140" font-size="11px" fill="#dc3545">3.3V</text>
    <circle cx="80" cy="120" r="4" fill="#0d6efd" /><text x="70" y="140" font-size="11px" fill="#0d6efd">Node</text>
  </g>

  <!-- Central Tie Node -->
  <circle cx="175" cy="240" r="8" fill="#0d6efd" />
  <text x="195" y="245" font-size="13px" font-weight="bold" fill="#0d6efd">Vout (Node กลาง) -&gt; GPIO 34</text>

  <!-- Fixed Resistor 10k -->
  <g transform="translate(95, 270)">
    <rect x="35" y="20" width="50" height="20" rx="3" fill="#e2d9cc" stroke="#8b7355" stroke-width="1.5" />
    <!-- Bands: Brown, Black, Orange -->
    <line x1="45" y1="20" x2="45" y2="40" stroke="#8b4513" stroke-width="3" />
    <line x1="55" y1="20" x2="55" y2="40" stroke="#000000" stroke-width="3" />
    <line x1="65" y1="20" x2="65" y2="40" stroke="#ff7f50" stroke-width="3" />
    <text x="20" y="65" font-size="13px" font-weight="bold" fill="#212529">Resistor 10 kΩ</text>
    <circle cx="60" cy="85" r="4" fill="#212529" /><text x="50" y="105" font-size="11px" fill="#212529">GND</text>
  </g>
</g>

<!-- Right Side Formulas & Notes -->
<rect x="730" y="150" width="345" height="420" class="card" />
<text x="750" y="185" class="text-head" fill="#0d6efd">📐 หลักการคำนวณและพฤติกรรม</text>

<g transform="translate(750, 210)">
  <rect x="0" y="0" width="305" height="60" rx="6" fill="#f8f9fa" />
  <text x="15" y="25" font-size="12px" font-weight="bold" fill="#212529">สูตรคำนวณแรงดัน Vout:</text>
  <text x="15" y="48" font-size="13px" font-family="monospace" fill="#0d6efd">Vout = (R10k / (R_ldr + R10k)) × 3.3V</text>
</g>

<g transform="translate(750, 285)">
  <text x="0" y="20" font-size="13px" font-weight="bold" fill="#212529">พฤติกรรมของเซนเซอร์:</text>
  <text x="0" y="45" font-size="13px" fill="#495057">• เมื่อมืดสนิท: R_ldr สูงมาก (&gt; 200 kΩ)</text>
  <text x="15" y="68" font-size="12px" fill="#6c757d">-&gt; Vout ต่ำ (~0.1V), ADC อ่านได้ ~3900+</text>
  <text x="0" y="98" font-size="13px" fill="#495057">• เมื่อแสงจ้า: R_ldr ลดต่ำลง (&lt; 1 kΩ)</text>
  <text x="15" y="121" font-size="12px" fill="#6c757d">-&gt; Vout สูง (~3.0V), ADC ลดลงเหลือ ~200-700</text>
</g>

<rect x="745" y="440" width="315" height="110" rx="6" fill="#e7f1ff" stroke="#b6d4fe" />
<text x="760" y="465" font-size="13px" font-weight="bold" fill="#0d6efd">💡 เคล็ดลับการทดลอง:</text>
<text x="760" y="490" font-size="12px" fill="#495057">• ปิดหัวเซนเซอร์ด้วยนิ้วเพื่อวัดค่าตอนมืด</text>
<text x="760" y="512" font-size="12px" fill="#495057">• เปิดไฟฉายมือถือส่องเพื่อวัดค่าแสงสว่าง</text>
<text x="760" y="534" font-size="12px" fill="#495057">• นำค่าที่ได้ไปพล็อตกราฟใน Excel / Python</text>
</svg>
"""

# ========================================================
# 5. CIRCUIT 5: RGB COLOR SENSING (Week 04)
# ========================================================
svg_c5 = SVG_COMMON_HEADER + """
<!-- Header Card -->
<rect x="25" y="20" width="1050" height="105" class="card" />
<text x="45" y="55" class="title">วงจรที่ 5: ตรวจจับสีวัตถุด้วย RGB LED (GPIO 4, 5, 23) และ LDR (GPIO 34)</text>
<text x="45" y="82" class="subtitle">ส่องแสงแม่สีทีละสี (แดง, เขียว, น้ำเงิน) กระทบวัตถุ และวัดความเข้มแสงสะท้อนผ่านเซนเซอร์ LDR</text>
<text x="45" y="106" class="badge-lab">📌 ใช้ใน: Week 04 (LED and RGB Color Sensing)</text>

<!-- ESP32 Board -->
<g transform="translate(60, 150)">
  <rect x="0" y="0" width="200" height="420" class="pcb" />
  <rect x="30" y="40" width="140" height="140" class="rf-shield" />
  <text x="42" y="110" font-size="13px" font-weight="bold" fill="#212529">ESP-WROOM-32</text>
  <!-- Pins Left -->
  <circle cx="0" cy="80" r="4" fill="#ffc107" /><text x="12" y="84" class="pin-label">3V3</text>
  <circle cx="0" cy="180" r="4" fill="#ffc107" /><text x="12" y="184" class="pin-label" fill="#0dcaf0">G34 (LDR)</text>
  <circle cx="0" cy="380" r="4" fill="#ffc107" /><text x="12" y="384" class="pin-label">GND</text>
  <!-- Pins Right -->
  <circle cx="200" cy="110" r="4" fill="#ffc107" /><text x="140" y="114" class="pin-label" fill="#0d6efd">G23 (B)</text>
  <circle cx="200" cy="260" r="4" fill="#ffc107" /><text x="140" y="264" class="pin-label" fill="#198754">G5 (G)</text>
  <circle cx="200" cy="290" r="4" fill="#ffc107" /><text x="140" y="294" class="pin-label" fill="#dc3545">G4 (R)</text>
</g>

<!-- Breadboard Layout -->
<g transform="translate(340, 150)">
  <rect x="0" y="0" width="360" height="420" rx="10" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="130" y="25" font-size="13px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- RGB LED (Common Cathode) -->
  <g transform="translate(30, 60)">
    <rect x="0" y="0" width="140" height="220" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="70" cy="50" r="30" fill="#f8f9fa" stroke="#ced4da" stroke-width="2" />
    <circle cx="58" cy="45" r="8" fill="#dc3545" />
    <circle cx="82" cy="45" r="8" fill="#198754" />
    <circle cx="70" cy="62" r="8" fill="#0d6efd" />
    <text x="25" y="105" font-size="12px" font-weight="bold" fill="#212529">RGB LED (Cathode)</text>
    
    <!-- 4 Pins -->
    <g transform="translate(15, 125)" font-size="11px">
      <text x="0" y="15" fill="#dc3545">R (ขาแดง) -&gt; R 220Ω -&gt; G4</text>
      <text x="0" y="38" fill="#212529">Cathode (ขายาว) -&gt; GND</text>
      <text x="0" y="61" fill="#198754">G (ขาเขียว) -&gt; R 220Ω -&gt; G5</text>
      <text x="0" y="84" fill="#0d6efd">B (ขาน้ำเงิน) -&gt; R 220Ω -&gt; G23</text>
    </g>
  </g>

  <!-- LDR Reflection Sensor -->
  <g transform="translate(190, 60)">
    <rect x="0" y="0" width="140" height="220" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="70" cy="50" r="25" fill="#ffeaa7" stroke="#fdcb6e" stroke-width="2" />
    <path d="M 58 45 Q 65 38 72 52 T 80 60" fill="none" stroke="#d63031" stroke-width="2" />
    <text x="20" y="105" font-size="12px" font-weight="bold" fill="#212529">LDR Rx Sensor</text>
    <text x="15" y="130" font-size="11px" fill="#495057">• ขา 1 ต่อ 3.3V</text>
    <text x="15" y="152" font-size="11px" fill="#0d6efd">• Node กลาง -&gt; G34</text>
    <text x="15" y="174" font-size="11px" fill="#495057">• R 10k ต่อลง GND</text>
    <text x="15" y="202" font-size="10px" fill="#6c757d">(วางคู่ขนานกับ RGB LED)</text>
  </g>
</g>

<!-- Right Side Pinout Table -->
<rect x="740" y="150" width="335" height="420" class="card" />
<text x="760" y="185" class="text-head" fill="#0d6efd">📋 ตารางการต่อขา Week 04</text>

<g transform="translate(760, 210)" font-size="13px">
  <text x="0" y="18" font-weight="bold" fill="#dc3545">GPIO 4</text><text x="90" y="18" fill="#495057">-&gt; LED ขาแดง (R 220Ω)</text>
  <text x="0" y="48" font-weight="bold" fill="#198754">GPIO 5</text><text x="90" y="48" fill="#495057">-&gt; LED ขาเขียว (R 220Ω)</text>
  <text x="0" y="78" font-weight="bold" fill="#0d6efd">GPIO 23</text><text x="90" y="78" fill="#495057">-&gt; LED ขาน้ำเงิน (R 220Ω)</text>
  <text x="0" y="108" font-weight="bold" fill="#212529">GND</text><text x="90" y="108" fill="#495057">-&gt; ขา Common Cathode</text>
  <text x="0" y="138" font-weight="bold" fill="#0dcaf0">GPIO 34</text><text x="90" y="138" fill="#495057">-&gt; Node เซนเซอร์ LDR</text>
</g>

<rect x="750" y="380" width="315" height="170" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
<text x="765" y="405" font-size="13px" font-weight="bold" fill="#212529">📦 เทคนิคการจัดมุมทดสอบสี:</text>
<text x="765" y="430" font-size="12px" fill="#495057">• ติดตั้งหลอด RGB LED และ LDR ชี้ไปข้างหน้า</text>
<text x="765" y="452" font-size="12px" fill="#495057">• วางวัตถุทดสอบ (กระดาษ แดง/เขียว/น้ำเงิน)</text>
<text x="765" y="474" font-size="12px" fill="#495057">  ห่างจากหัวเซนเซอร์ประมาณ 1 - 2 cm</text>
<text x="765" y="496" font-size="12px" fill="#495057">• ใช้กระดาษสีดำหรือกล่องครอบกันแสงรบกวน</text>
<text x="765" y="520" font-size="12px" font-weight="bold" fill="#198754">✅ ระบบจะจำแนกสีวัตถุได้อย่างแม่นยำ!</text>
</svg>
"""

# Write all SVGs
circuits_svg = {
    "circuit_01_bare_esp32.svg": svg_c1,
    "circuit_04_ldr_divider.svg": svg_c4,
    "circuit_05_rgb_color_sensing.svg": svg_c5,
    "circuit_06_spi_oled_pot.svg": svg_c6,
    "circuit_07_standard_iot_station.svg": svg_c7,
}

for fname, content in circuits_svg.items():
    p1 = os.path.join(OUTPUT_DIR, fname)
    p2 = os.path.join(ARTIFACT_DIR, fname)
    with open(p1, "w", encoding="utf-8") as f:
        f.write(content.strip())
    with open(p2, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated Vector SVG: {p1}")

print("All vector SVGs written successfully!")
