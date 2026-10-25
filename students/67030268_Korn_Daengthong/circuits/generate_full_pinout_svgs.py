#!/usr/bin/env python3
"""
Generate complete, professional SVG and PNG wiring diagrams showing ALL ESP32 pins.
Includes exact pin numbers, color-coded solder pads, and clean wire routing.
"""

import os

OUTPUT_DIR = "/Users/phuwish/Downloads/fortest week1 week2/IoT-2569-Master-Kit/circuits"
ARTIFACT_DIR = "/Users/phuwish/.gemini/antigravity/brain/861fb457-eb55-478a-9ecd-4d4221975e10/circuits"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# Standard 30-Pin ESP32 DevKit / NodeMCU Pinout (15 pins per side)
LEFT_PINS = [
    ("3V3", "3.3V Power Out"),
    ("EN", "Enable / Reset"),
    ("VP", "GPIO 36 (ADC1_0)"),
    ("VN", "GPIO 39 (ADC1_3)"),
    ("G34", "GPIO 34 (ADC1_6)"),
    ("G35", "GPIO 35 (ADC1_7)"),
    ("G32", "GPIO 32 (ADC1_4)"),
    ("G33", "GPIO 33 (ADC1_5)"),
    ("G25", "GPIO 25 (DAC1)"),
    ("G26", "GPIO 26 (DAC2)"),
    ("G27", "GPIO 27 (ADC2_7)"),
    ("G14", "GPIO 14 (HSPI_CLK)"),
    ("G12", "GPIO 12 (HSPI_MISO)"),
    ("G13", "GPIO 13 (HSPI_MOSI)"),
    ("GND", "Ground (0V)")
]

RIGHT_PINS = [
    ("VIN", "5V Power In"),
    ("GND", "Ground (0V)"),
    ("G13_2", "GPIO 13"),
    ("G12_2", "GPIO 12"),
    ("G14_2", "GPIO 14"),
    ("G27_2", "GPIO 27"),
    ("G23", "GPIO 23 (MOSI)"),
    ("G22", "GPIO 22 (I2C_SCL)"),
    ("TX0", "GPIO 1 (UART_TX)"),
    ("RX0", "GPIO 3 (UART_RX)"),
    ("G21", "GPIO 21 (I2C_SDA)"),
    ("G19", "GPIO 19 (MISO)"),
    ("G18", "GPIO 18 (SCK)"),
    ("G5", "GPIO 5 (CS)"),
    ("TX2", "GPIO 17"),
    ("RX2", "GPIO 16"),
    ("G4", "GPIO 4"),
    ("G2", "GPIO 2 (LED)"),
    ("G15", "GPIO 15"),
    ("GND_2", "Ground (0V)")
]

# Let's use the full 38-pin NodeMCU-32S (19 pins per side) for absolute completeness!
FULL_LEFT_PINS = [
    ("3V3", "Power 3.3V"),
    ("EN", "Reset Button"),
    ("VP", "GPIO 36"),
    ("VN", "GPIO 39"),
    ("G34", "GPIO 34 (ADC1)"),
    ("G35", "GPIO 35"),
    ("G32", "GPIO 32"),
    ("G33", "GPIO 33"),
    ("G25", "GPIO 25"),
    ("G26", "GPIO 26"),
    ("G27", "GPIO 27"),
    ("G14", "GPIO 14"),
    ("G12", "GPIO 12"),
    ("GND", "Ground"),
    ("G13", "GPIO 13"),
    ("D2", "GPIO 9 (SD2)"),
    ("D3", "GPIO 10 (SD3)"),
    ("CMD", "GPIO 11 (CMD)"),
    ("5V", "Power 5V / VIN")
]

FULL_RIGHT_PINS = [
    ("GND", "Ground"),
    ("G23", "GPIO 23 (MOSI)"),
    ("G22", "GPIO 22 (SCL)"),
    ("TX", "GPIO 1 (TX0)"),
    ("RX", "GPIO 3 (RX0)"),
    ("G21", "GPIO 21 (SDA)"),
    ("GND", "Ground"),
    ("G19", "GPIO 19 (MISO)"),
    ("G18", "GPIO 18 (SCK)"),
    ("G5", "GPIO 5 (CS)"),
    ("TX2", "GPIO 17"),
    ("RX2", "GPIO 16"),
    ("G4", "GPIO 4"),
    ("G2", "GPIO 2 (LED)"),
    ("G15", "GPIO 15"),
    ("D1", "GPIO 8 (SD1)"),
    ("D0", "GPIO 7 (SD0)"),
    ("CLK", "GPIO 6 (CLK)"),
    ("GND", "Ground")
]

def render_esp32_board(x, y, active_left=None, active_right=None):
    """
    Renders an ESP32 NodeMCU-32S with ALL 38 pins clearly labeled and numbered.
    active_left / active_right: dict of pin_name -> (fill_color, text_color)
    """
    active_left = active_left or {}
    active_right = active_right or {}
    
    board_w = 260
    pin_spacing = 30
    board_h = len(FULL_LEFT_PINS) * pin_spacing + 100
    
    svg = []
    # Main PCB
    svg.append(f'<g transform="translate({x}, {y})">')
    svg.append(f'  <rect x="0" y="0" width="{board_w}" height="{board_h}" rx="14" fill="#1e222b" stroke="#3e4451" stroke-width="2.5" />')
    
    # Metal RF Shield (ESP-WROOM-32)
    svg.append(f'  <rect x="45" y="45" width="{board_w - 90}" height="190" rx="6" fill="#ced4da" stroke="#adb5bd" stroke-width="2" />')
    svg.append(f'  <text x="{board_w//2}" y="115" text-anchor="middle" font-size="14px" font-weight="bold" fill="#212529">ESP-WROOM-32</text>')
    svg.append(f'  <text x="{board_w//2}" y="138" text-anchor="middle" font-size="11px" fill="#495057">Wi-Fi &amp; Bluetooth</text>')
    svg.append(f'  <text x="{board_w//2}" y="158" text-anchor="middle" font-size="10px" font-family="monospace" fill="#6c757d">240MHz DUAL CORE</text>')
    
    # Micro-USB Port
    svg.append(f'  <rect x="{board_w//2 - 28}" y="{board_h - 22}" width="56" height="26" rx="4" fill="#adb5bd" stroke="#6c757d" stroke-width="1.5" />')
    svg.append(f'  <text x="{board_w//2}" y="{board_h - 6}" text-anchor="middle" font-size="10px" font-weight="bold" fill="#212529">USB</text>')
    
    # Reset (EN) & Boot Buttons
    svg.append(f'  <rect x="25" y="{board_h - 65}" width="24" height="20" rx="3" fill="#dc3545" />')
    svg.append(f'  <text x="37" y="{board_h - 72}" text-anchor="middle" font-size="10px" font-weight="bold" fill="#adb5bd">EN</text>')
    svg.append(f'  <rect x="{board_w - 49}" y="{board_h - 65}" width="24" height="20" rx="3" fill="#495057" />')
    svg.append(f'  <text x="{board_w - 37}" y="{board_h - 72}" text-anchor="middle" font-size="10px" font-weight="bold" fill="#adb5bd">BOOT</text>')
    
    # Onboard Blue LED (GPIO 2)
    svg.append(f'  <rect x="{board_w - 60}" y="{board_h - 110}" width="12" height="8" rx="2" fill="#0d6efd" stroke="#0b5ed7" />')
    svg.append(f'  <text x="{board_w - 54}" y="{board_h - 118}" text-anchor="middle" font-size="9px" fill="#0dcaf0">LED:D2</text>')
    
    # Left Pins (19 pins)
    pin_y_start = 55
    left_pin_coords = {}
    for i, (pname, pdesc) in enumerate(FULL_LEFT_PINS):
        py = pin_y_start + i * pin_spacing
        is_active = pname in active_left
        pad_fill = active_left[pname] if is_active else "#ffc107"
        text_fill = "#ffffff" if is_active else "#adb5bd"
        font_weight = "bold" if is_active else "normal"
        
        # Solder pad / pin hole
        svg.append(f'  <circle cx="8" cy="{py}" r="5" fill="{pad_fill}" stroke="#212529" stroke-width="1.5" />')
        svg.append(f'  <text x="20" y="{py + 4}" font-size="12px" font-family="monospace" font-weight="{font_weight}" fill="{text_fill}">{pname}</text>')
        left_pin_coords[pname] = (x + 8, y + py)
        
    # Right Pins (19 pins)
    right_pin_coords = {}
    for i, (pname, pdesc) in enumerate(FULL_RIGHT_PINS):
        py = pin_y_start + i * pin_spacing
        is_active = pname in active_right
        pad_fill = active_right[pname] if is_active else "#ffc107"
        text_fill = "#ffffff" if is_active else "#adb5bd"
        font_weight = "bold" if is_active else "normal"
        
        svg.append(f'  <circle cx="{board_w - 8}" cy="{py}" r="5" fill="{pad_fill}" stroke="#212529" stroke-width="1.5" />')
        svg.append(f'  <text x="{board_w - 20}" y="{py + 4}" text-anchor="end" font-size="12px" font-family="monospace" font-weight="{font_weight}" fill="{text_fill}">{pname}</text>')
        right_pin_coords[pname] = (x + board_w - 8, y + py)
        
    svg.append('</g>')
    return "".join(svg), left_pin_coords, right_pin_coords, board_h

# ========================================================
# 1. BUILD COMPLETE CIRCUIT 7: STANDARD IOT STATION (POT + LED)
# ========================================================
def build_circuit_7_svg():
    esp_x, esp_y = 60, 140
    active_l = {"3V3": "#dc3545", "G34": "#0d6efd", "GND": "#212529"}
    active_r = {"G2": "#fd7e14", "GND": "#212529"}
    
    board_markup, l_coords, r_coords, b_h = render_esp32_board(esp_x, esp_y, active_l, active_r)
    
    # Exact Pin Coordinates
    p_3v3 = l_coords["3V3"]
    p_g34 = l_coords["G34"]
    p_gnd_l = l_coords["GND"]
    
    p_g2 = r_coords["G2"]
    p_gnd_r = r_coords["GND"]
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="1280" height="880" style="background:#f8f9fa; font-family: -apple-system, 'Thonburi', 'Sarabun', 'Segoe UI', Arial, sans-serif;">
<defs>
  <style>
    .title {{ font-size: 24px; font-weight: bold; fill: #0d6efd; }}
    .subtitle {{ font-size: 15px; fill: #495057; }}
    .badge-lab {{ font-size: 14px; font-weight: bold; fill: #198754; }}
    .card {{ fill: #ffffff; stroke: #dee2e6; stroke-width: 1.5; rx: 10; }}
    .wire {{ stroke-linecap: round; stroke-linejoin: round; fill: none; }}
  </style>
</defs>

<!-- Header Card -->
<rect x="25" y="20" width="1230" height="100" class="card" />
<text x="45" y="52" class="title">วงจรที่ 7: สถานี IoT มาตรฐาน (Standard IoT Station: POT 10k + LED)</text>
<text x="45" y="78" class="subtitle">แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงเส้นสัญญาณไปยัง Potentiometer (GPIO 34) และหลอดไฟ LED (GPIO 2)</text>
<text x="45" y="102" class="badge-lab">⭐⭐ วงจรหลักยอดฮิต: ใช้วงจรเดียวกัน 100% สำหรับ Week 02 (Lab 3), Week 10, Week 11, Week 12 (ไม่ต้องรื้อวงจรใหม่)</text>

<!-- ESP32 Board (Full 38 Pins) -->
{board_markup}

<!-- Breadboard Layout -->
<g transform="translate(420, 160)">
  <rect x="0" y="0" width="450" height="580" rx="12" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="180" y="30" font-size="14px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- Left Side: Potentiometer 10k -->
  <g transform="translate(40, 60)">
    <rect x="0" y="0" width="160" height="230" rx="8" fill="#ffffff" stroke="#dee2e6" stroke-width="1.5" />
    <circle cx="80" cy="85" r="50" fill="#0d6efd" opacity="0.85" />
    <circle cx="80" cy="85" r="28" fill="#e9ecef" />
    <line x1="80" y1="85" x2="105" y2="60" stroke="#0d6efd" stroke-width="5" stroke-linecap="round" />
    
    <text x="80" y="155" text-anchor="middle" font-size="13px" font-weight="bold" fill="#212529">Potentiometer</text>
    <text x="80" y="175" text-anchor="middle" font-size="14px" font-weight="bold" fill="#0d6efd">10 kΩ</text>
    <text x="80" y="195" text-anchor="middle" font-size="11px" fill="#6c757d">เซนเซอร์แอนะล็อก</text>
    
    <!-- 3 Pins of Potentiometer -->
    <!-- Pin 1: 3.3V -->
    <circle cx="35" cy="245" r="6" fill="#dc3545" stroke="#212529" stroke-width="1.5" />
    <text x="35" y="270" text-anchor="middle" font-size="12px" font-weight="bold" fill="#dc3545">ขา 1</text>
    <text x="35" y="285" text-anchor="middle" font-size="11px" fill="#dc3545">(3.3V)</text>
    
    <!-- Pin 2: Wiper (GPIO 34) -->
    <circle cx="80" cy="245" r="7" fill="#0d6efd" stroke="#212529" stroke-width="2" />
    <text x="80" y="270" text-anchor="middle" font-size="13px" font-weight="bold" fill="#0d6efd">ขากลาง</text>
    <text x="80" y="288" text-anchor="middle" font-size="12px" font-weight="bold" fill="#0d6efd">(GPIO 34)</text>
    
    <!-- Pin 3: GND -->
    <circle cx="125" cy="245" r="6" fill="#212529" stroke="#6c757d" stroke-width="1.5" />
    <text x="125" y="270" text-anchor="middle" font-size="12px" font-weight="bold" fill="#212529">ขา 3</text>
    <text x="125" y="285" text-anchor="middle" font-size="11px" fill="#212529">(GND)</text>
  </g>

  <!-- Right Side: LED + Resistor 220 Ohm -->
  <g transform="translate(240, 60)">
    <rect x="0" y="0" width="170" height="230" rx="8" fill="#ffffff" stroke="#dee2e6" stroke-width="1.5" />
    
    <!-- LED Bulb -->
    <circle cx="85" cy="70" r="32" fill="#dc3545" opacity="0.9" />
    <polygon points="65,95 105,95 85,120" fill="#dc3545" />
    <text x="85" y="145" text-anchor="middle" font-size="13px" font-weight="bold" fill="#212529">LED (Red / Blue)</text>
    <text x="85" y="165" text-anchor="middle" font-size="11px" fill="#6c757d">หลอดไฟ Actuator</text>
    
    <!-- Resistor 220 Ohm -->
    <rect x="50" y="180" width="70" height="22" rx="4" fill="#e2d9cc" stroke="#8b7355" stroke-width="2" />
    <line x1="62" y1="180" x2="62" y2="202" stroke="#dc3545" stroke-width="3.5" />
    <line x1="75" y1="180" x2="75" y2="202" stroke="#dc3545" stroke-width="3.5" />
    <line x1="88" y1="180" x2="88" y2="202" stroke="#8b4513" stroke-width="3.5" />
    <line x1="105" y1="180" x2="105" y2="202" stroke="#d4af37" stroke-width="3.5" />
    
    <text x="85" y="218" text-anchor="middle" font-size="11px" font-weight="bold" fill="#8b4513">R 220Ω (แดง-แดง-น้ำตาล)</text>
    
    <!-- LED Connection Points -->
    <!-- Point 1: Anode via Resistor -->
    <circle cx="60" cy="245" r="7" fill="#fd7e14" stroke="#212529" stroke-width="2" />
    <text x="60" y="270" text-anchor="middle" font-size="12px" font-weight="bold" fill="#fd7e14">Anode (+)</text>
    <text x="60" y="288" text-anchor="middle" font-size="11px" fill="#fd7e14">ผ่าน R 220Ω</text>
    
    <!-- Point 2: Cathode -->
    <circle cx="110" cy="245" r="6" fill="#212529" stroke="#6c757d" stroke-width="1.5" />
    <text x="110" y="270" text-anchor="middle" font-size="12px" font-weight="bold" fill="#212529">Cathode (-)</text>
    <text x="110" y="288" text-anchor="middle" font-size="11px" fill="#212529">ขาสั้น (GND)</text>
  </g>

  <!-- Summary Card inside Breadboard Bottom -->
  <g transform="translate(30, 380)">
    <rect x="0" y="0" width="390" height="170" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <text x="20" y="30" font-size="14px" font-weight="bold" fill="#198754">📌 หน้าที่ของวงจรในแต่ละสัปดาห์:</text>
    <text x="20" y="60" font-size="13px" fill="#212529">• <tspan font-weight="bold">Week 02 (Lab 2.3):</tspan> หมุน POT หรี่ไฟ LED แบบ PWM</text>
    <text x="20" y="88" font-size="13px" fill="#212529">• <tspan font-weight="bold">Week 10 (HTTP/UDP/CoAP):</tspan> อ่านค่า POT และรับคำสั่งเปิด-ปิดไฟ</text>
    <text x="20" y="116" font-size="13px" fill="#212529">• <tspan font-weight="bold">Week 11 (MQTT / RainMaker):</tspan> ส่ง Telemetry และซิงค์ไฟผ่าน Cloud</text>
    <text x="20" y="144" font-size="13px" fill="#212529">• <tspan font-weight="bold">Week 12 (Flutter App):</tspan> กราฟบนแอปมือถือ + สวิตช์ควบคุมไฟ LED</text>
  </g>
</g>

<!-- Wires Routing (From exact ESP32 solder pads to Breadboard components) -->

<!-- 1. Wire Red: 3V3 Pad -> POT Pin 1 (3.3V) -->
<!-- Start: ({p_3v3[0]}, {p_3v3[1]}) -->
<path d="M {p_3v3[0]} {p_3v3[1]} L 30 {p_3v3[1]} L 30 760 L 455 760 L 455 405" stroke="#dc3545" stroke-width="4.5" class="wire" />
<circle cx="{p_3v3[0]}" cy="{p_3v3[1]}" r="3" fill="#ffffff" />
<circle cx="455" cy="405" r="3" fill="#ffffff" />

<!-- 2. Wire Blue: GPIO 34 Pad -> POT Pin 2 Wiper (ขากลาง) -->
<!-- Start: ({p_g34[0]}, {p_g34[1]}) -->
<path d="M {p_g34[0]} {p_g34[1]} L 45 {p_g34[1]} L 45 785 L 500 785 L 500 405" stroke="#0d6efd" stroke-width="4.5" class="wire" />
<circle cx="{p_g34[0]}" cy="{p_g34[1]}" r="3" fill="#ffffff" />
<circle cx="500" cy="405" r="3" fill="#ffffff" />

<!-- 3. Wire Black: GND Pad (Left) -> POT Pin 3 (GND) -->
<!-- Start: ({p_gnd_l[0]}, {p_gnd_l[1]}) -->
<path d="M {p_gnd_l[0]} {p_gnd_l[1]} L 15 {p_gnd_l[1]} L 15 810 L 545 810 L 545 405" stroke="#212529" stroke-width="4.5" class="wire" />
<circle cx="{p_gnd_l[0]}" cy="{p_gnd_l[1]}" r="3" fill="#ffffff" />
<circle cx="545" cy="405" r="3" fill="#ffffff" />

<!-- 4. Wire Orange: GPIO 2 Pad -> LED Anode via Resistor 220 Ohm -->
<!-- Start: ({p_g2[0]}, {p_g2[1]}) -->
<path d="M {p_g2[0]} {p_g2[1]} L 340 {p_g2[1]} L 340 760 L 720 760 L 720 405" stroke="#fd7e14" stroke-width="4.5" class="wire" />
<circle cx="{p_g2[0]}" cy="{p_g2[1]}" r="3" fill="#ffffff" />
<circle cx="720" cy="405" r="3" fill="#ffffff" />

<!-- 5. Wire Black: GND Pad (Right) -> LED Cathode -->
<!-- Start: ({p_gnd_r[0]}, {p_gnd_r[1]}) -->
<path d="M {p_gnd_r[0]} {p_gnd_r[1]} L 360 {p_gnd_r[1]} L 360 785 L 770 785 L 770 405" stroke="#212529" stroke-width="4.5" class="wire" />
<circle cx="{p_gnd_r[0]}" cy="{p_gnd_r[1]}" r="3" fill="#ffffff" />
<circle cx="770" cy="405" r="3" fill="#ffffff" />

<!-- Right Side Legend Table -->
<g transform="translate(900, 160)">
  <rect x="0" y="0" width="355" height="580" rx="12" class="card" />
  <text x="25" y="35" font-size="16px" font-weight="bold" fill="#0d6efd">📋 ตารางสรุปการต่อสายทุกเส้น</text>
  
  <!-- Item 1: 3.3V -->
  <g transform="translate(25, 60)">
    <rect x="0" y="0" width="305" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <line x1="12" y1="25" x2="35" y2="25" stroke="#dc3545" stroke-width="5" stroke-linecap="round" />
    <text x="45" y="20" font-size="13px" font-weight="bold" fill="#dc3545">ขา 3V3 (ESP32 ซ้ายบน)</text>
    <text x="45" y="38" font-size="12px" fill="#495057">→ ต่อเข้า ขา 1 ของ POT (สายสีแดง)</text>
  </g>

  <!-- Item 2: GPIO 34 -->
  <g transform="translate(25, 120)">
    <rect x="0" y="0" width="305" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <line x1="12" y1="25" x2="35" y2="25" stroke="#0d6efd" stroke-width="5" stroke-linecap="round" />
    <text x="45" y="20" font-size="13px" font-weight="bold" fill="#0d6efd">ขา G34 (ESP32 ซ้ายแถว 5)</text>
    <text x="45" y="38" font-size="12px" fill="#495057">→ ต่อเข้า ขากลาง Wiper (สายสีน้ำเงิน)</text>
  </g>

  <!-- Item 3: GND Left -->
  <g transform="translate(25, 180)">
    <rect x="0" y="0" width="305" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <line x1="12" y1="25" x2="35" y2="25" stroke="#212529" stroke-width="5" stroke-linecap="round" />
    <text x="45" y="20" font-size="13px" font-weight="bold" fill="#212529">ขา GND (ESP32 ซ้ายแถว 14)</text>
    <text x="45" y="38" font-size="12px" fill="#495057">→ ต่อเข้า ขา 3 ของ POT (สายสีดำ)</text>
  </g>

  <!-- Item 4: GPIO 2 -->
  <g transform="translate(25, 240)">
    <rect x="0" y="0" width="305" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <line x1="12" y1="25" x2="35" y2="25" stroke="#fd7e14" stroke-width="5" stroke-linecap="round" />
    <text x="45" y="20" font-size="13px" font-weight="bold" fill="#fd7e14">ขา G2 (ESP32 ขวาแถว 14)</text>
    <text x="45" y="38" font-size="12px" fill="#495057">→ ต่อเข้า R 220Ω &gt; Anode (+) (สายสีส้ม)</text>
  </g>

  <!-- Item 5: GND Right -->
  <g transform="translate(25, 300)">
    <rect x="0" y="0" width="305" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <line x1="12" y1="25" x2="35" y2="25" stroke="#212529" stroke-width="5" stroke-linecap="round" />
    <text x="45" y="20" font-size="13px" font-weight="bold" fill="#212529">ขา GND (ESP32 ขวาแถว 1)</text>
    <text x="45" y="38" font-size="12px" fill="#495057">→ ต่อเข้า Cathode (-) ของ LED (สายสีดำ)</text>
  </g>

  <!-- Important Speedrun Advice -->
  <rect x="20" y="375" width="315" height="180" rx="8" fill="#d1e7dd" stroke="#a3cfbb" />
  <text x="35" y="405" font-size="14px" font-weight="bold" fill="#0f5132">💡 เคล็ดลับการทำแล็บให้เร็วที่สุด:</text>
  <text x="35" y="432" font-size="12px" fill="#0f5132">1. เสียบบอร์ด ESP32 ค่อมร่องกลาง Breadboard</text>
  <text x="35" y="456" font-size="12px" fill="#0f5132">2. เสียบ Potentiometer และ LED ตามผังนี้</text>
  <text x="35" y="480" font-size="12px" fill="#0f5132">3. ต่อสายไฟทั้ง 5 เส้นตามสีที่ระบุ</text>
  <text x="35" y="504" font-size="12px" font-weight="bold" fill="#0f5132">4. แฟลชโค้ดได้ทั้ง Week 02, 10, 11, 12 ทันที!</text>
  <text x="35" y="528" font-size="12px" fill="#0f5132">5. เพื่อนมีหน้าที่แค่หมุน POT และกดแคปจอ</text>
</g>
</svg>
"""
    return svg

# Save Circuit 7 SVG
c7_content = build_circuit_7_svg()
with open(os.path.join(OUTPUT_DIR, "circuit_07_standard_iot_station.svg"), "w", encoding="utf-8") as f:
    f.write(c7_content)
with open(os.path.join(ARTIFACT_DIR, "circuit_07_standard_iot_station.svg"), "w", encoding="utf-8") as f:
    f.write(c7_content)

print("Generated Complete 38-Pin Circuit 7 SVG!")
#!/usr/bin/env python3
"""
Generate complete, professional SVG wiring diagrams showing ALL 38 ESP32 pins.
For every single circuit, all 38 pins (19 left + 19 right) are completely displayed,
and wires are cleanly routed directly from the exact pin pads to the components.
"""

import os

OUTPUT_DIR = "/Users/phuwish/Downloads/fortest week1 week2/IoT-2569-Master-Kit/circuits"
ARTIFACT_DIR = "/Users/phuwish/.gemini/antigravity/brain/861fb457-eb55-478a-9ecd-4d4221975e10/circuits"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# Full 38-Pin NodeMCU-32S Pinout (19 pins left, 19 pins right)
FULL_LEFT_PINS = [
    ("3V3", "Power 3.3V"),
    ("EN", "Reset Button"),
    ("VP", "GPIO 36 (ADC1_0)"),
    ("VN", "GPIO 39 (ADC1_3)"),
    ("G34", "GPIO 34 (ADC1_6)"),
    ("G35", "GPIO 35 (ADC1_7)"),
    ("G32", "GPIO 32 (ADC1_4)"),
    ("G33", "GPIO 33 (ADC1_5)"),
    ("G25", "GPIO 25 (DAC1)"),
    ("G26", "GPIO 26 (DAC2)"),
    ("G27", "GPIO 27 (ADC2_7)"),
    ("G14", "GPIO 14 (HSPI_CLK)"),
    ("G12", "GPIO 12 (HSPI_MISO)"),
    ("GND", "Ground (0V)"),
    ("G13", "GPIO 13 (HSPI_MOSI)"),
    ("D2", "GPIO 9 (SD2)"),
    ("D3", "GPIO 10 (SD3)"),
    ("CMD", "GPIO 11 (CMD)"),
    ("5V", "Power 5V / VIN")
]

FULL_RIGHT_PINS = [
    ("GND", "Ground (0V)"),
    ("G23", "GPIO 23 (VSPI_MOSI)"),
    ("G22", "GPIO 22 (I2C_SCL)"),
    ("TX", "GPIO 1 (UART0_TX)"),
    ("RX", "GPIO 3 (UART0_RX)"),
    ("G21", "GPIO 21 (I2C_SDA)"),
    ("GND", "Ground (0V)"),
    ("G19", "GPIO 19 (VSPI_MISO)"),
    ("G18", "GPIO 18 (VSPI_CLK)"),
    ("G5", "GPIO 5 (VSPI_CS)"),
    ("TX2", "GPIO 17 (UART2_TX)"),
    ("RX2", "GPIO 16 (UART2_RX)"),
    ("G4", "GPIO 4 (ADC2_0)"),
    ("G2", "GPIO 2 (Onboard LED)"),
    ("G15", "GPIO 15 (ADC2_3)"),
    ("D1", "GPIO 8 (SD1)"),
    ("D0", "GPIO 7 (SD0)"),
    ("CLK", "GPIO 6 (CLK)"),
    ("GND", "Ground (0V)")
]

def render_esp32_board(x, y, active_left=None, active_right=None):
    active_left = active_left or {}
    active_right = active_right or {}
    
    board_w = 260
    pin_spacing = 30
    board_h = len(FULL_LEFT_PINS) * pin_spacing + 100
    
    svg = []
    svg.append(f'<g transform="translate({x}, {y})">')
    # Main PCB
    svg.append(f'  <rect x="0" y="0" width="{board_w}" height="{board_h}" rx="14" fill="#1e222b" stroke="#3e4451" stroke-width="2.5" />')
    # Metal RF Shield
    svg.append(f'  <rect x="45" y="45" width="{board_w - 90}" height="190" rx="6" fill="#ced4da" stroke="#adb5bd" stroke-width="2" />')
    svg.append(f'  <text x="{board_w//2}" y="115" text-anchor="middle" font-size="14px" font-weight="bold" fill="#212529">ESP-WROOM-32</text>')
    svg.append(f'  <text x="{board_w//2}" y="138" text-anchor="middle" font-size="11px" fill="#495057">Wi-Fi &amp; Bluetooth</text>')
    svg.append(f'  <text x="{board_w//2}" y="158" text-anchor="middle" font-size="10px" font-family="monospace" fill="#6c757d">240MHz DUAL CORE</text>')
    
    # Micro USB Port
    svg.append(f'  <rect x="{board_w//2 - 28}" y="{board_h - 22}" width="56" height="26" rx="4" fill="#adb5bd" stroke="#6c757d" stroke-width="1.5" />')
    svg.append(f'  <text x="{board_w//2}" y="{board_h - 6}" text-anchor="middle" font-size="10px" font-weight="bold" fill="#212529">USB</text>')
    
    # Buttons
    svg.append(f'  <rect x="25" y="{board_h - 65}" width="24" height="20" rx="3" fill="#dc3545" />')
    svg.append(f'  <text x="37" y="{board_h - 72}" text-anchor="middle" font-size="10px" font-weight="bold" fill="#adb5bd">EN</text>')
    svg.append(f'  <rect x="{board_w - 49}" y="{board_h - 65}" width="24" height="20" rx="3" fill="#495057" />')
    svg.append(f'  <text x="{board_w - 37}" y="{board_h - 72}" text-anchor="middle" font-size="10px" font-weight="bold" fill="#adb5bd">BOOT</text>')
    
    # Blue LED
    svg.append(f'  <rect x="{board_w - 60}" y="{board_h - 110}" width="12" height="8" rx="2" fill="#0d6efd" stroke="#0b5ed7" />')
    svg.append(f'  <text x="{board_w - 54}" y="{board_h - 118}" text-anchor="middle" font-size="9px" fill="#0dcaf0">LED:D2</text>')
    
    # Left Pins (19 pins)
    pin_y_start = 55
    left_pin_coords = {}
    for i, (pname, pdesc) in enumerate(FULL_LEFT_PINS):
        py = pin_y_start + i * pin_spacing
        is_active = pname in active_left
        pad_fill = active_left[pname] if is_active else "#ffc107"
        text_fill = "#ffffff" if is_active else "#adb5bd"
        font_weight = "bold" if is_active else "normal"
        
        svg.append(f'  <circle cx="8" cy="{py}" r="5" fill="{pad_fill}" stroke="#212529" stroke-width="1.5" />')
        svg.append(f'  <text x="20" y="{py + 4}" font-size="12px" font-family="monospace" font-weight="{font_weight}" fill="{text_fill}">{pname}</text>')
        left_pin_coords[pname] = (x + 8, y + py)
        
    # Right Pins (19 pins)
    right_pin_coords = {}
    for i, (pname, pdesc) in enumerate(FULL_RIGHT_PINS):
        py = pin_y_start + i * pin_spacing
        is_active = pname in active_right
        pad_fill = active_right[pname] if is_active else "#ffc107"
        text_fill = "#ffffff" if is_active else "#adb5bd"
        font_weight = "bold" if is_active else "normal"
        
        svg.append(f'  <circle cx="{board_w - 8}" cy="{py}" r="5" fill="{pad_fill}" stroke="#212529" stroke-width="1.5" />')
        svg.append(f'  <text x="{board_w - 20}" y="{py + 4}" text-anchor="end" font-size="12px" font-family="monospace" font-weight="{font_weight}" fill="{text_fill}">{pname}</text>')
        right_pin_coords[pname] = (x + board_w - 8, y + py)
        
    svg.append('</g>')
    return "".join(svg), left_pin_coords, right_pin_coords, board_h

# ========================================================
# 6. CIRCUIT 6: SPI OLED (7 Pins) + POTENTIOMETER (Week 09)
# ========================================================
def build_circuit_6_svg():
    esp_x, esp_y = 60, 140
    active_l = {"3V3": "#dc3545", "G34": "#0d6efd", "GND": "#212529"}
    active_r = {
        "G23": "#a370f7",  # D1 (MOSI)
        "G18": "#198754",  # D0 (SCK)
        "G5":  "#fd7e14",  # CS
        "G4":  "#0dcaf0",  # RES
        "G2":  "#d63384",  # DC
        "GND": "#212529"   # GND
    }
    
    board_markup, l_coords, r_coords, b_h = render_esp32_board(esp_x, esp_y, active_l, active_r)
    
    p_3v3 = l_coords["3V3"]
    p_g34 = l_coords["G34"]
    p_gnd_l = l_coords["GND"]
    
    p_g23 = r_coords["G23"]
    p_g18 = r_coords["G18"]
    p_g5  = r_coords["G5"]
    p_g4  = r_coords["G4"]
    p_g2  = r_coords["G2"]
    p_gnd_r = r_coords["GND"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="1280" height="880" style="background:#f8f9fa; font-family: -apple-system, 'Thonburi', 'Sarabun', 'Segoe UI', Arial, sans-serif;">
<defs>
  <style>
    .title {{ font-size: 24px; font-weight: bold; fill: #0d6efd; }}
    .subtitle {{ font-size: 15px; fill: #495057; }}
    .badge-lab {{ font-size: 14px; font-weight: bold; fill: #6f42c1; }}
    .card {{ fill: #ffffff; stroke: #dee2e6; stroke-width: 1.5; rx: 10; }}
    .wire {{ stroke-linecap: round; stroke-linejoin: round; fill: none; }}
  </style>
</defs>

<!-- Header Card -->
<rect x="25" y="20" width="1230" height="100" class="card" />
<text x="45" y="52" class="title">วงจรที่ 6: จอแสดงผลกราฟิก SPI OLED SSD1306 (7 ขา) ร่วมกับ Potentiometer</text>
<text x="45" y="78" class="subtitle">แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายบัส SPI2 (10 MHz) 5 ขา + ไฟเลี้ยง 2 ขา + Potentiometer บนขา GPIO 34</text>
<text x="45" y="102" class="badge-lab">📌 ใช้ใน: Week 09 (SPI OLED and Kestrel UI) — ถ่ายรูปจอจริงต้องเห็นคำว่า "HELLO WORLD" และ "ID: 67030XXX"</text>

<!-- ESP32 Board (Full 38 Pins) -->
{board_markup}

<!-- Breadboard Layout -->
<g transform="translate(380, 150)">
  <rect x="0" y="0" width="480" height="600" rx="12" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="190" y="28" font-size="14px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- OLED Display Module (7 Pins Header) -->
  <g transform="translate(30, 45)">
    <rect x="0" y="0" width="420" height="260" rx="10" fill="#212529" stroke="#495057" stroke-width="2" />
    
    <!-- Screen Glass -->
    <rect x="35" y="75" width="350" height="165" rx="4" fill="#050811" stroke="#343a40" stroke-width="2" />
    <text x="65" y="130" font-size="20px" font-weight="bold" fill="#0dcaf0" font-family="monospace">HELLO WORLD</text>
    <text x="65" y="165" font-size="18px" font-weight="bold" fill="#ffc107" font-family="monospace">ID: 67030XXX</text>
    <text x="65" y="200" font-size="15px" fill="#20c997" font-family="monospace">ADC: 2048 (1.65V)</text>
    
    <!-- 7 Header Pins (Top Edge of OLED) -->
    <!-- Pin 1: GND -->
    <circle cx="45" cy="35" r="6" fill="#212529" stroke="#adb5bd" stroke-width="1.5" />
    <text x="45" y="20" text-anchor="middle" font-size="11px" font-weight="bold" fill="#ced4da">GND</text>
    <text x="45" y="55" text-anchor="middle" font-size="10px" fill="#adb5bd">Pin 1</text>
    
    <!-- Pin 2: VCC (3.3V) -->
    <circle cx="100" cy="35" r="6" fill="#dc3545" stroke="#212529" stroke-width="1.5" />
    <text x="100" y="20" text-anchor="middle" font-size="11px" font-weight="bold" fill="#dc3545">VCC</text>
    <text x="100" y="55" text-anchor="middle" font-size="10px" fill="#dc3545">(3.3V)</text>
    
    <!-- Pin 3: D0 (SCK / GPIO 18) -->
    <circle cx="155" cy="35" r="6" fill="#198754" stroke="#212529" stroke-width="1.5" />
    <text x="155" y="20" text-anchor="middle" font-size="11px" font-weight="bold" fill="#198754">D0</text>
    <text x="155" y="55" text-anchor="middle" font-size="10px" fill="#198754">(SCK:18)</text>
    
    <!-- Pin 4: D1 (MOSI / GPIO 23) -->
    <circle cx="210" cy="35" r="6" fill="#a370f7" stroke="#212529" stroke-width="1.5" />
    <text x="210" y="20" text-anchor="middle" font-size="11px" font-weight="bold" fill="#a370f7">D1</text>
    <text x="210" y="55" text-anchor="middle" font-size="10px" fill="#a370f7">(MOSI:23)</text>
    
    <!-- Pin 5: RES (Reset / GPIO 4) -->
    <circle cx="265" cy="35" r="6" fill="#0dcaf0" stroke="#212529" stroke-width="1.5" />
    <text x="265" y="20" text-anchor="middle" font-size="11px" font-weight="bold" fill="#0dcaf0">RES</text>
    <text x="265" y="55" text-anchor="middle" font-size="10px" fill="#0dcaf0">(RST:4)</text>
    
    <!-- Pin 6: DC (Data/Cmd / GPIO 2) -->
    <circle cx="320" cy="35" r="6" fill="#d63384" stroke="#212529" stroke-width="1.5" />
    <text x="320" y="20" text-anchor="middle" font-size="11px" font-weight="bold" fill="#d63384">DC</text>
    <text x="320" y="55" text-anchor="middle" font-size="10px" fill="#d63384">(D/C:2)</text>
    
    <!-- Pin 7: CS (Chip Select / GPIO 5) -->
    <circle cx="375" cy="35" r="6" fill="#fd7e14" stroke="#212529" stroke-width="1.5" />
    <text x="375" y="20" text-anchor="middle" font-size="11px" font-weight="bold" fill="#fd7e14">CS</text>
    <text x="375" y="55" text-anchor="middle" font-size="10px" fill="#fd7e14">(CS:5)</text>
  </g>

  <!-- Potentiometer 10k (Bottom of Breadboard) -->
  <g transform="translate(130, 335)">
    <rect x="0" y="0" width="220" height="230" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="110" cy="85" r="50" fill="#0d6efd" opacity="0.85" />
    <circle cx="110" cy="85" r="28" fill="#e9ecef" />
    <line x1="110" y1="85" x2="135" y2="60" stroke="#0d6efd" stroke-width="5" stroke-linecap="round" />
    <text x="110" y="155" text-anchor="middle" font-size="13px" font-weight="bold" fill="#212529">Potentiometer 10 kΩ</text>
    <text x="110" y="175" text-anchor="middle" font-size="12px" fill="#0d6efd">หมุนเทียบหน้าเว็บ Kestrel กับจอ OLED</text>
    
    <!-- POT Pins -->
    <circle cx="60" cy="205" r="6" fill="#dc3545" /><text x="60" y="224" text-anchor="middle" font-size="11px" fill="#dc3545">3.3V</text>
    <circle cx="110" cy="205" r="7" fill="#0d6efd" /><text x="110" y="224" text-anchor="middle" font-size="12px" font-weight="bold" fill="#0d6efd">GPIO 34</text>
    <circle cx="160" cy="205" r="6" fill="#212529" /><text x="160" y="224" text-anchor="middle" font-size="11px" fill="#212529">GND</text>
  </g>
</g>

<!-- Wire Routing: From Exact ESP32 Pins to OLED & POT -->

<!-- OLED Wires: -->
<!-- 1. VCC: 3V3 Pad -> OLED Pin 2 (100+380=480, 35+195=230) -->
<path d="M {p_3v3[0]} {p_3v3[1]} L 40 {p_3v3[1]} L 40 135 L 480 135 L 480 230" stroke="#dc3545" stroke-width="4" class="wire" />
<circle cx="{p_3v3[0]}" cy="{p_3v3[1]}" r="3" fill="#ffffff" />

<!-- 2. D0 (SCK): GPIO 18 Pad -> OLED Pin 3 (155+380=535, 230) -->
<path d="M {p_g18[0]} {p_g18[1]} L 335 {p_g18[1]} L 335 150 L 535 150 L 535 230" stroke="#198754" stroke-width="4" class="wire" />
<circle cx="{p_g18[0]}" cy="{p_g18[1]}" r="3" fill="#ffffff" />

<!-- 3. D1 (MOSI): GPIO 23 Pad -> OLED Pin 4 (210+380=590, 230) -->
<path d="M {p_g23[0]} {p_g23[1]} L 350 {p_g23[1]} L 350 165 L 590 165 L 590 230" stroke="#a370f7" stroke-width="4" class="wire" />
<circle cx="{p_g23[0]}" cy="{p_g23[1]}" r="3" fill="#ffffff" />

<!-- 4. RES: GPIO 4 Pad -> OLED Pin 5 (265+380=645, 230) -->
<path d="M {p_g4[0]} {p_g4[1]} L 365 {p_g4[1]} L 365 180 L 645 180 L 645 230" stroke="#0dcaf0" stroke-width="4" class="wire" />
<circle cx="{p_g4[0]}" cy="{p_g4[1]}" r="3" fill="#ffffff" />

<!-- 5. DC: GPIO 2 Pad -> OLED Pin 6 (320+380=700, 230) -->
<path d="M {p_g2[0]} {p_g2[1]} L 380 {p_g2[1]} L 380 195 L 700 195 L 700 230" stroke="#d63384" stroke-width="4" class="wire" />
<circle cx="{p_g2[0]}" cy="{p_g2[1]}" r="3" fill="#ffffff" />

<!-- 6. CS: GPIO 5 Pad -> OLED Pin 7 (375+380=755, 230) -->
<path d="M {p_g5[0]} {p_g5[1]} L 370 {p_g5[1]} L 370 210 L 755 210 L 755 230" stroke="#fd7e14" stroke-width="4" class="wire" />
<circle cx="{p_g5[0]}" cy="{p_g5[1]}" r="3" fill="#ffffff" />

<!-- 7. GND: Right GND Pad -> OLED Pin 1 (45+380=425, 230) -->
<path d="M {p_gnd_r[0]} {p_gnd_r[1]} L 320 {p_gnd_r[1]} L 320 120 L 425 120 L 425 230" stroke="#212529" stroke-width="4" class="wire" />
<circle cx="{p_gnd_r[0]}" cy="{p_gnd_r[1]}" r="3" fill="#ffffff" />

<!-- POT Wires: -->
<!-- POT Wiper: GPIO 34 Pad -> POT Middle Pin (110+130+380=620, 205+335+150=690) -->
<path d="M {p_g34[0]} {p_g34[1]} L 25 {p_g34[1]} L 25 780 L 620 780 L 620 690" stroke="#0d6efd" stroke-width="4" class="wire" />
<circle cx="{p_g34[0]}" cy="{p_g34[1]}" r="3" fill="#ffffff" />

<!-- POT 3.3V: From 3V3 Pad -->
<path d="M 30 {p_3v3[1]} L 15 {p_3v3[1]} L 15 805 L 570 805 L 570 690" stroke="#dc3545" stroke-width="3" class="wire" />

<!-- POT GND: From Left GND Pad -->
<path d="M {p_gnd_l[0]} {p_gnd_l[1]} L 35 {p_gnd_l[1]} L 35 830 L 670 830 L 670 690" stroke="#212529" stroke-width="3" class="wire" />

<!-- Pinout Table (Right Side) -->
<g transform="translate(890, 150)">
  <rect x="0" y="0" width="365" height="600" rx="12" class="card" />
  <text x="25" y="35" font-size="16px" font-weight="bold" fill="#0d6efd">📋 ตารางการต่อสาย OLED 7 ขา</text>
  
  <g transform="translate(20, 60)" font-size="12px">
    <!-- Pin 1 -->
    <rect x="0" y="0" width="325" height="36" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="18" r="5" fill="#212529" />
    <text x="30" y="16" font-weight="bold" fill="#212529">1. GND</text>
    <text x="100" y="16" fill="#495057">→ GND บนบอร์ด (กราวด์)</text>
    <text x="30" y="30" font-size="10px" fill="#6c757d">สายสีดำ</text>

    <!-- Pin 2 -->
    <rect x="0" y="44" width="325" height="36" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="62" r="5" fill="#dc3545" />
    <text x="30" y="60" font-weight="bold" fill="#dc3545">2. VCC</text>
    <text x="100" y="60" fill="#495057">→ ขา 3.3V (ไฟเลี้ยงจอภาพ)</text>
    <text x="30" y="74" font-size="10px" fill="#6c757d">สายสีแดง (ห้ามต่อ 5V)</text>

    <!-- Pin 3 -->
    <rect x="0" y="88" width="325" height="36" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="106" r="5" fill="#198754" />
    <text x="30" y="104" font-weight="bold" fill="#198754">3. D0 (SCK)</text>
    <text x="100" y="104" fill="#495057">→ GPIO 18 (SPI2 Clock)</text>
    <text x="30" y="118" font-size="10px" fill="#6c757d">สายสีเขียว</text>

    <!-- Pin 4 -->
    <rect x="0" y="132" width="325" height="36" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="150" r="5" fill="#a370f7" />
    <text x="30" y="148" font-weight="bold" fill="#a370f7">4. D1 (MOSI)</text>
    <text x="100" y="148" fill="#495057">→ GPIO 23 (SPI2 Data)</text>
    <text x="30" y="162" font-size="10px" fill="#6c757d">สายสีม่วง</text>

    <!-- Pin 5 -->
    <rect x="0" y="176" width="325" height="36" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="194" r="5" fill="#0dcaf0" />
    <text x="30" y="192" font-weight="bold" fill="#0dcaf0">5. RES (Reset)</text>
    <text x="100" y="192" fill="#495057">→ GPIO 4 (Active Low)</text>
    <text x="30" y="206" font-size="10px" fill="#6c757d">สายสีฟ้า</text>

    <!-- Pin 6 -->
    <rect x="0" y="220" width="325" height="36" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="238" r="5" fill="#d63384" />
    <text x="30" y="236" font-weight="bold" fill="#d63384">6. DC (Data/Cmd)</text>
    <text x="100" y="236" fill="#495057">→ GPIO 2 (0=Cmd, 1=Data)</text>
    <text x="30" y="250" font-size="10px" fill="#6c757d">สายสีชมพู</text>

    <!-- Pin 7 -->
    <rect x="0" y="264" width="325" height="36" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="282" r="5" fill="#fd7e14" />
    <text x="30" y="280" font-weight="bold" fill="#fd7e14">7. CS (Chip Sel)</text>
    <text x="100" y="280" fill="#495057">→ GPIO 5 (Active Low)</text>
    <text x="30" y="294" font-size="10px" fill="#6c757d">สายสีส้ม</text>

    <!-- POT Pin -->
    <rect x="0" y="308" width="325" height="36" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="326" r="5" fill="#0d6efd" />
    <text x="30" y="324" font-weight="bold" fill="#0d6efd">POT Wiper</text>
    <text x="100" y="324" fill="#495057">→ GPIO 34 (ADC1_CH6)</text>
    <text x="30" y="338" font-size="10px" fill="#6c757d">สายสีน้ำเงิน</text>
  </g>

  <!-- Speedrun Fault Clinic Alert -->
  <g transform="translate(20, 420)">
    <rect x="0" y="0" width="325" height="150" rx="8" fill="#fff3cd" stroke="#ffecb5" />
    <text x="15" y="25" font-size="13px" font-weight="bold" fill="#664d03">⚠️ การแก้ไขปัญหาหน้างาน (Fault Clinic):</text>
    <text x="15" y="50" font-size="12px" fill="#664d03">• <tspan font-weight="bold">จอมืดสนิท:</tspan> ตรวจสอบสาย SCK (GPIO 18) หลุด</text>
    <text x="15" y="73" font-size="12px" fill="#664d03">• <tspan font-weight="bold">จอขึ้นเส้นขยะ:</tspan> สลับสาย DC (GPIO 2) กับ RES</text>
    <text x="15" y="96" font-size="12px" fill="#664d03">• <tspan font-weight="bold">บัฟเฟอร์ค้าง:</tspan> สั่งรีเซ็ตผ่านปุ่ม EN บนตัวบอร์ด</text>
    <text x="15" y="125" font-size="12px" font-weight="bold" fill="#0d6efd">📷 ถ่ายรูปจอจริง 2 รูปให้เห็นชื่อ/รหัสชัดเจน</text>
  </g>
</g>
</svg>
"""
    return svg

# Save Circuit 6 SVG
c6_content = build_circuit_6_svg()
with open(os.path.join(OUTPUT_DIR, "circuit_06_spi_oled_pot.svg"), "w", encoding="utf-8") as f:
    f.write(c6_content)
with open(os.path.join(ARTIFACT_DIR, "circuit_06_spi_oled_pot.svg"), "w", encoding="utf-8") as f:
    f.write(c6_content)

print("Generated Complete 38-Pin Circuit 6 SVG!")

# ========================================================
# 5. CIRCUIT 5: RGB COLOR SENSING (Week 04)
# ========================================================
def build_circuit_5_svg():
    esp_x, esp_y = 60, 140
    active_l = {"3V3": "#dc3545", "G34": "#0dcaf0", "GND": "#212529"}
    active_r = {
        "G23": "#0d6efd",  # Blue LED
        "G5":  "#198754",  # Green LED
        "G4":  "#dc3545",  # Red LED
        "GND": "#212529"   # GND
    }
    board_markup, l_coords, r_coords, b_h = render_esp32_board(esp_x, esp_y, active_l, active_r)
    
    p_3v3 = l_coords["3V3"]
    p_g34 = l_coords["G34"]
    p_gnd_l = l_coords["GND"]
    
    p_g23 = r_coords["G23"]
    p_g5  = r_coords["G5"]
    p_g4  = r_coords["G4"]
    p_gnd_r = r_coords["GND"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="1280" height="880" style="background:#f8f9fa; font-family: -apple-system, 'Thonburi', 'Sarabun', 'Segoe UI', Arial, sans-serif;">
<defs>
  <style>
    .title {{ font-size: 24px; font-weight: bold; fill: #0d6efd; }}
    .subtitle {{ font-size: 15px; fill: #495057; }}
    .badge-lab {{ font-size: 14px; font-weight: bold; fill: #6f42c1; }}
    .card {{ fill: #ffffff; stroke: #dee2e6; stroke-width: 1.5; rx: 10; }}
    .wire {{ stroke-linecap: round; stroke-linejoin: round; fill: none; }}
  </style>
</defs>

<!-- Header Card -->
<rect x="25" y="20" width="1230" height="100" class="card" />
<text x="45" y="52" class="title">วงจรที่ 5: ตรวจจับสีวัตถุด้วย RGB LED (GPIO 4, 5, 23) และ LDR (GPIO 34)</text>
<text x="45" y="78" class="subtitle">แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมต่อหลอดไฟแม่สี 3 สี (ผ่าน R 220Ω) และรับแสงสะท้อนผ่านเซนเซอร์ LDR</text>
<text x="45" y="102" class="badge-lab">📌 ใช้ใน: Week 04 (LED and RGB Color Sensing) — วัตถุสีแดง เขียว น้ำเงิน</text>

<!-- ESP32 Board (Full 38 Pins) -->
{board_markup}

<!-- Breadboard Layout -->
<g transform="translate(380, 150)">
  <rect x="0" y="0" width="480" height="600" rx="12" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="190" y="28" font-size="14px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- RGB LED Unit (Common Cathode) -->
  <g transform="translate(35, 60)">
    <rect x="0" y="0" width="190" height="280" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="95" cy="65" r="45" fill="#f8f9fa" stroke="#ced4da" stroke-width="2" />
    <circle cx="80" cy="55" r="12" fill="#dc3545" />
    <circle cx="110" cy="55" r="12" fill="#198754" />
    <circle cx="95" cy="80" r="12" fill="#0d6efd" />
    <text x="95" y="130" text-anchor="middle" font-size="13px" font-weight="bold" fill="#212529">RGB LED</text>
    <text x="95" y="148" text-anchor="middle" font-size="11px" fill="#6c757d">(Common Cathode)</text>
    
    <!-- 4 Terminals of RGB LED -->
    <g transform="translate(20, 165)" font-size="11px">
      <!-- R -->
      <circle cx="15" cy="15" r="5" fill="#dc3545" /><text x="28" y="19" fill="#dc3545" font-weight="bold">R (แดง)</text><text x="80" y="19" fill="#6c757d">→ R 220Ω &gt; G4</text>
      <!-- Cathode -->
      <circle cx="15" cy="40" r="5" fill="#212529" /><text x="28" y="44" fill="#212529" font-weight="bold">Cathode (-)</text><text x="95" y="44" fill="#6c757d">→ GND</text>
      <!-- G -->
      <circle cx="15" cy="65" r="5" fill="#198754" /><text x="28" y="69" fill="#198754" font-weight="bold">G (เขียว)</text><text x="80" y="69" fill="#6c757d">→ R 220Ω &gt; G5</text>
      <!-- B -->
      <circle cx="15" cy="90" r="5" fill="#0d6efd" /><text x="28" y="94" fill="#0d6efd" font-weight="bold">B (น้ำเงิน)</text><text x="85" y="94" fill="#6c757d">→ R 220Ω &gt; G23</text>
    </g>
  </g>

  <!-- LDR Reflection Sensor Unit -->
  <g transform="translate(255, 60)">
    <rect x="0" y="0" width="190" height="280" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="95" cy="65" r="40" fill="#ffeaa7" stroke="#fdcb6e" stroke-width="2.5" />
    <path d="M 75 55 Q 85 45 95 65 T 115 75" fill="none" stroke="#d63031" stroke-width="3" />
    <text x="95" y="130" text-anchor="middle" font-size="13px" font-weight="bold" fill="#212529">LDR Sensor (Rx)</text>
    <text x="95" y="148" text-anchor="middle" font-size="11px" fill="#6c757d">รับแสงสะท้อนจากวัตถุ</text>
    
    <g transform="translate(15, 175)" font-size="11px">
      <circle cx="15" cy="15" r="5" fill="#dc3545" /><text x="28" y="19" fill="#dc3545">ขา 1 → 3.3V (ไฟเลี้ยง)</text>
      <circle cx="15" cy="45" r="6" fill="#0dcaf0" /><text x="28" y="49" font-weight="bold" fill="#0dcaf0">Node กลาง → GPIO 34</text>
      <circle cx="15" cy="75" r="5" fill="#212529" /><text x="28" y="79" fill="#212529">R 10kΩ → GND (กราวด์)</text>
    </g>
  </g>

  <!-- Setup Instruction inside Breadboard Bottom -->
  <g transform="translate(30, 365)">
    <rect x="0" y="0" width="420" height="205" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <text x="20" y="30" font-size="14px" font-weight="bold" fill="#0d6efd">🔬 ขั้นตอนการทดลองจำแนกสี (Week 04):</text>
    <text x="20" y="58" font-size="13px" fill="#212529">1. วางหลอดไฟ RGB LED และเซนเซอร์ LDR หันหน้าขนานไปข้างหน้า</text>
    <text x="20" y="84" font-size="13px" fill="#212529">2. นำวัตถุสีแดง สีเขียว สีน้ำเงิน วางจ่อข้างหน้าห่าง ~1 - 2 cm</text>
    <text x="20" y="110" font-size="13px" fill="#212529">3. บอร์ด ESP32 จะเปิดไฟทีละสี (R → G → B) เพื่อวัดค่าการสะท้อน</text>
    <text x="20" y="136" font-size="13px" fill="#212529">4. วัตถุสีใดจะสะท้อนแสงสีนั้นได้มากที่สุด ทำให้ค่า ADC เปลี่ยนแปลงเด่นชัด</text>
    <text x="20" y="165" font-size="13px" font-weight="bold" fill="#198754">✅ คำนวณ Trimmed Mean 10% และส่วนเบี่ยงเบนมาตรฐาน (SD) ลงตาราง</text>
  </g>
</g>

<!-- Wires Routing: From Exact ESP32 Pins -->
<!-- 1. G4 Pad -> RGB Red (55+380=435, 180+60+150=390) -->
<path d="M {p_g4[0]} {p_g4[1]} L 350 {p_g4[1]} L 350 240 L 450 240 L 450 390" stroke="#dc3545" stroke-width="4" class="wire" />
<circle cx="{p_g4[0]}" cy="{p_g4[1]}" r="3" fill="#ffffff" />

<!-- 2. G5 Pad -> RGB Green -->
<path d="M {p_g5[0]} {p_g5[1]} L 340 {p_g5[1]} L 340 260 L 470 260 L 470 440" stroke="#198754" stroke-width="4" class="wire" />
<circle cx="{p_g5[0]}" cy="{p_g5[1]}" r="3" fill="#ffffff" />

<!-- 3. G23 Pad -> RGB Blue -->
<path d="M {p_g23[0]} {p_g23[1]} L 330 {p_g23[1]} L 330 280 L 490 280 L 490 465" stroke="#0d6efd" stroke-width="4" class="wire" />
<circle cx="{p_g23[0]}" cy="{p_g23[1]}" r="3" fill="#ffffff" />

<!-- 4. GND Right Pad -> Common Cathode -->
<path d="M {p_gnd_r[0]} {p_gnd_r[1]} L 320 {p_gnd_r[1]} L 320 220 L 460 220 L 460 415" stroke="#212529" stroke-width="4" class="wire" />
<circle cx="{p_gnd_r[0]}" cy="{p_gnd_r[1]}" r="3" fill="#ffffff" />

<!-- 5. 3V3 Pad -> LDR Pin 1 (255+15+380=650, 60+175+15+150=400) -->
<path d="M {p_3v3[0]} {p_3v3[1]} L 30 {p_3v3[1]} L 30 790 L 650 790 L 650 400" stroke="#dc3545" stroke-width="4" class="wire" />
<circle cx="{p_3v3[0]}" cy="{p_3v3[1]}" r="3" fill="#ffffff" />

<!-- 6. G34 Pad -> LDR Node (650, 430) -->
<path d="M {p_g34[0]} {p_g34[1]} L 45 {p_g34[1]} L 45 815 L 670 815 L 670 430" stroke="#0dcaf0" stroke-width="4" class="wire" />
<circle cx="{p_g34[0]}" cy="{p_g34[1]}" r="3" fill="#ffffff" />

<!-- 7. GND Left Pad -> LDR Resistor (650, 460) -->
<path d="M {p_gnd_l[0]} {p_gnd_l[1]} L 15 {p_gnd_l[1]} L 15 840 L 690 840 L 690 460" stroke="#212529" stroke-width="4" class="wire" />
<circle cx="{p_gnd_l[0]}" cy="{p_gnd_l[1]}" r="3" fill="#ffffff" />

<!-- Right Side Pinout Table -->
<g transform="translate(890, 150)">
  <rect x="0" y="0" width="365" height="600" rx="12" class="card" />
  <text x="25" y="35" font-size="16px" font-weight="bold" fill="#0d6efd">📋 ตารางการต่อขา Week 04</text>
  
  <g transform="translate(20, 60)" font-size="12px">
    <rect x="0" y="0" width="325" height="42" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="21" r="5" fill="#dc3545" />
    <text x="30" y="18" font-weight="bold" fill="#dc3545">GPIO 4 (ESP32 ขวาแถว 13)</text>
    <text x="30" y="34" fill="#495057">→ LED ขาแดง R (ต่อผ่าน R 220Ω)</text>

    <rect x="0" y="52" width="325" height="42" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="73" r="5" fill="#198754" />
    <text x="30" y="70" font-weight="bold" fill="#198754">GPIO 5 (ESP32 ขวาแถว 10)</text>
    <text x="30" y="86" fill="#495057">→ LED ขาเขียว G (ต่อผ่าน R 220Ω)</text>

    <rect x="0" y="104" width="325" height="42" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="125" r="5" fill="#0d6efd" />
    <text x="30" y="122" font-weight="bold" fill="#0d6efd">GPIO 23 (ESP32 ขวาแถว 2)</text>
    <text x="30" y="138" fill="#495057">→ LED ขาน้ำเงิน B (ต่อผ่าน R 220Ω)</text>

    <rect x="0" y="156" width="325" height="42" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="177" r="5" fill="#212529" />
    <text x="30" y="174" font-weight="bold" fill="#212529">GND (ESP32 ขวาแถว 1)</text>
    <text x="30" y="190" fill="#495057">→ ขา Common Cathode (ขายาวสุด)</text>

    <rect x="0" y="208" width="325" height="42" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="229" r="5" fill="#dc3545" />
    <text x="30" y="226" font-weight="bold" fill="#dc3545">3V3 (ESP32 ซ้ายแถว 1)</text>
    <text x="30" y="242" fill="#495057">→ ไฟเลี้ยงเซนเซอร์ LDR (ขา 1)</text>

    <rect x="0" y="260" width="325" height="42" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="281" r="5" fill="#0dcaf0" />
    <text x="30" y="278" font-weight="bold" fill="#0dcaf0">GPIO 34 (ESP32 ซ้ายแถว 5)</text>
    <text x="30" y="294" fill="#495057">→ Node กลาง LDR + R 10k (ADC1)</text>

    <rect x="0" y="312" width="325" height="42" rx="4" fill="#f8f9fa" />
    <circle cx="15" cy="333" r="5" fill="#212529" />
    <text x="30" y="330" font-weight="bold" fill="#212529">GND (ESP32 ซ้ายแถว 14)</text>
    <text x="30" y="346" fill="#495057">→ ขาตัวต้านทานคงที่ 10kΩ</text>
  </g>

  <!-- Light shielding tip -->
  <g transform="translate(20, 430)">
    <rect x="0" y="0" width="325" height="140" rx="8" fill="#e7f1ff" stroke="#b6d4fe" />
    <text x="15" y="25" font-size="13px" font-weight="bold" fill="#0d6efd">💡 ทริคเพิ่มความแม่นยำตอนอัดคลิป:</text>
    <text x="15" y="50" font-size="12px" fill="#495057">• ใช้กระดาษแข็งสีดำม้วนเป็นท่อครอบกั้น</text>
    <text x="15" y="72" font-size="12px" fill="#495057">  ระหว่าง LED กับ LDR เพื่อไม่ให้แสงตรงเข้า</text>
    <text x="15" y="94" font-size="12px" fill="#495057">• ให้รับเฉพาะ "แสงสะท้อนจากวัตถุ" เท่านั้น</text>
    <text x="15" y="118" font-size="12px" font-weight="bold" fill="#198754">ผลการแยกสี RED / GREEN / BLUE จะชัดเจน 100%</text>
  </g>
</g>
</svg>
"""
    return svg

# Save Circuit 5 SVG
c5_content = build_circuit_5_svg()
with open(os.path.join(OUTPUT_DIR, "circuit_05_rgb_color_sensing.svg"), "w", encoding="utf-8") as f:
    f.write(c5_content)
with open(os.path.join(ARTIFACT_DIR, "circuit_05_rgb_color_sensing.svg"), "w", encoding="utf-8") as f:
    f.write(c5_content)

print("Generated Complete 38-Pin Circuit 5 SVG!")

# ========================================================
# 4. CIRCUIT 4: LDR VOLTAGE DIVIDER (Week 03)
# ========================================================
def build_circuit_4_svg():
    esp_x, esp_y = 60, 140
    active_l = {"3V3": "#dc3545", "G34": "#0d6efd", "GND": "#212529"}
    board_markup, l_coords, r_coords, b_h = render_esp32_board(esp_x, esp_y, active_l, {})
    
    p_3v3 = l_coords["3V3"]
    p_g34 = l_coords["G34"]
    p_gnd_l = l_coords["GND"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="1280" height="880" style="background:#f8f9fa; font-family: -apple-system, 'Thonburi', 'Sarabun', 'Segoe UI', Arial, sans-serif;">
<defs>
  <style>
    .title {{ font-size: 24px; font-weight: bold; fill: #0d6efd; }}
    .subtitle {{ font-size: 15px; fill: #495057; }}
    .badge-lab {{ font-size: 14px; font-weight: bold; fill: #6f42c1; }}
    .card {{ fill: #ffffff; stroke: #dee2e6; stroke-width: 1.5; rx: 10; }}
    .wire {{ stroke-linecap: round; stroke-linejoin: round; fill: none; }}
  </style>
</defs>

<!-- Header Card -->
<rect x="25" y="20" width="1230" height="100" class="card" />
<text x="45" y="52" class="title">วงจรที่ 4: วงจรแบ่งแรงดันเซนเซอร์แสง LDR ร่วมกับตัวต้านทาน 10kΩ</text>
<text x="45" y="78" class="subtitle">แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายไฟ 3.3V, GND และจุดแยกแรงดัน (Node) เข้าขา GPIO 34 (ADC1)</text>
<text x="45" y="102" class="badge-lab">📌 ใช้ใน: Week 03 (Sensors &amp; Calibration II) — วัดค่าความสว่างแสง Lux vs ค่าดิจิทัล ADC</text>

<!-- ESP32 Board (Full 38 Pins) -->
{board_markup}

<!-- Breadboard Layout -->
<g transform="translate(420, 150)">
  <rect x="0" y="0" width="450" height="600" rx="12" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="180" y="30" font-size="14px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- LDR Component Box -->
  <g transform="translate(115, 60)">
    <rect x="0" y="0" width="220" height="170" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="110" cy="55" r="35" fill="#ffeaa7" stroke="#fdcb6e" stroke-width="3" />
    <path d="M 90 45 Q 100 35 110 55 T 130 65" fill="none" stroke="#d63031" stroke-width="3" />
    
    <text x="110" y="115" text-anchor="middle" font-size="14px" font-weight="bold" fill="#212529">LDR (Photoresistor)</text>
    <text x="110" y="135" text-anchor="middle" font-size="12px" fill="#6c757d">ตัวต้านทานปรับค่าตามแสง</text>
    
    <!-- LDR Pins -->
    <circle cx="65" cy="180" r="6" fill="#dc3545" /><text x="65" y="202" text-anchor="middle" font-size="11px" fill="#dc3545">ขา 1 (3.3V)</text>
    <circle cx="155" cy="180" r="7" fill="#0d6efd" /><text x="155" y="202" text-anchor="middle" font-size="11px" font-weight="bold" fill="#0d6efd">ขา 2 (Node)</text>
  </g>

  <!-- Central Tie Node -->
  <g transform="translate(225, 290)">
    <circle cx="45" cy="0" r="10" fill="#0d6efd" stroke="#212529" stroke-width="2" />
    <text x="70" y="6" font-size="13px" font-weight="bold" fill="#0d6efd">Vout (Node กลาง) → ส่งเข้า GPIO 34</text>
  </g>

  <!-- Resistor 10k Box -->
  <g transform="translate(115, 340)">
    <rect x="0" y="0" width="220" height="170" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <!-- Resistor Body -->
    <rect x="75" y="45" width="70" height="24" rx="4" fill="#e2d9cc" stroke="#8b7355" stroke-width="2" />
    <!-- Bands: Brown, Black, Orange -->
    <line x1="88" y1="45" x2="88" y2="69" stroke="#8b4513" stroke-width="4" />
    <line x1="100" y1="45" x2="100" y2="69" stroke="#000000" stroke-width="4" />
    <line x1="112" y1="45" x2="112" y2="69" stroke="#ff7f50" stroke-width="4" />
    <line x1="130" y1="45" x2="130" y2="69" stroke="#d4af37" stroke-width="4" />
    
    <text x="110" y="95" text-anchor="middle" font-size="14px" font-weight="bold" fill="#212529">Resistor 10 kΩ</text>
    <text x="110" y="115" text-anchor="middle" font-size="11px" fill="#8b4513">(น้ำตาล-ดำ-ส้ม)</text>
    
    <circle cx="155" cy="0" r="6" fill="#0d6efd" />
    <circle cx="110" cy="150" r="6" fill="#212529" /><text x="110" y="168" text-anchor="middle" font-size="11px" fill="#212529">GND (กราวด์)</text>
  </g>
</g>

<!-- Wires Routing: From Exact ESP32 Pins -->
<!-- 1. 3V3 Pad -> LDR Pin 1 (115+65+420=600, 60+180+150=390) -->
<path d="M {p_3v3[0]} {p_3v3[1]} L 30 {p_3v3[1]} L 30 780 L 600 780 L 600 390" stroke="#dc3545" stroke-width="4.5" class="wire" />
<circle cx="{p_3v3[0]}" cy="{p_3v3[1]}" r="3" fill="#ffffff" />

<!-- 2. G34 Pad -> Central Node (225+45+420=690, 290+150=440) -->
<path d="M {p_g34[0]} {p_g34[1]} L 45 {p_g34[1]} L 45 805 L 690 805 L 690 440" stroke="#0d6efd" stroke-width="4.5" class="wire" />
<circle cx="{p_g34[0]}" cy="{p_g34[1]}" r="3" fill="#ffffff" />

<!-- 3. GND Pad -> Resistor Bottom Pin (115+110+420=645, 340+150+150=640) -->
<path d="M {p_gnd_l[0]} {p_gnd_l[1]} L 15 {p_gnd_l[1]} L 15 830 L 645 830 L 645 640" stroke="#212529" stroke-width="4.5" class="wire" />
<circle cx="{p_gnd_l[0]}" cy="{p_gnd_l[1]}" r="3" fill="#ffffff" />

<!-- Right Side Formulas & Table -->
<g transform="translate(900, 150)">
  <rect x="0" y="0" width="355" height="600" rx="12" class="card" />
  <text x="25" y="35" font-size="16px" font-weight="bold" fill="#0d6efd">📋 ตารางการต่อขา Week 03</text>
  
  <g transform="translate(20, 60)" font-size="12px">
    <rect x="0" y="0" width="315" height="46" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <circle cx="15" cy="23" r="5" fill="#dc3545" />
    <text x="30" y="19" font-weight="bold" fill="#dc3545">3V3 (ESP32 ซ้ายแถว 1)</text>
    <text x="30" y="36" fill="#495057">→ ขาที่ 1 ของ LDR (สายสีแดง)</text>

    <rect x="0" y="58" width="315" height="46" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <circle cx="15" cy="81" r="5" fill="#0d6efd" />
    <text x="30" y="77" font-weight="bold" fill="#0d6efd">GPIO 34 (ESP32 ซ้ายแถว 5)</text>
    <text x="30" y="94" fill="#495057">→ Node กึ่งกลาง LDR + R 10k (สายสีน้ำเงิน)</text>

    <rect x="0" y="116" width="315" height="46" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <circle cx="15" cy="139" r="5" fill="#212529" />
    <text x="30" y="135" font-weight="bold" fill="#212529">GND (ESP32 ซ้ายแถว 14)</text>
    <text x="30" y="152" fill="#495057">→ ขาอีกข้างของ R 10kΩ (สายสีดำ)</text>
  </g>

  <!-- Formula Box -->
  <g transform="translate(20, 240)">
    <rect x="0" y="0" width="315" height="150" rx="8" fill="#f8f9fa" stroke="#dee2e6" />
    <text x="15" y="25" font-size="13px" font-weight="bold" fill="#212529">📐 สูตรคำนวณวงจรแบ่งแรงดัน:</text>
    <text x="15" y="55" font-size="13px" font-family="monospace" fill="#0d6efd">Vout = (R10k / (R_ldr + R10k)) × 3.3V</text>
    <text x="15" y="85" font-size="12px" fill="#495057">• มืดสนิท: R_ldr &gt; 200kΩ → ADC สูง ~3900+</text>
    <text x="15" y="108" font-size="12px" fill="#495057">• แสงห้อง: R_ldr ~7kΩ → ADC ~1700 (1.4V)</text>
    <text x="15" y="131" font-size="12px" fill="#495057">• ไฟฉายจ่อ: R_ldr &lt; 1kΩ → ADC ลดเหลือ &lt; 200</text>
  </g>

  <!-- Self-assessment tip -->
  <g transform="translate(20, 410)">
    <rect x="0" y="0" width="315" height="165" rx="8" fill="#d1e7dd" stroke="#a3cfbb" />
    <text x="15" y="25" font-size="13px" font-weight="bold" fill="#0f5132">📝 สิ่งที่ต้องส่งใน Report Week 03:</text>
    <text x="15" y="50" font-size="12px" fill="#0f5132">1. วิธีคำนวณแรงดัน Vadc = (ADC/4095) × 3.3V</text>
    <text x="15" y="73" font-size="12px" fill="#0f5132">2. ตารางเทียบแสง 5 ระดับ (มืดสนิท → ไฟฉายจ่อ)</text>
    <text x="15" y="96" font-size="12px" fill="#0f5132">3. รูปกราฟ Scatter Trendline (chart week3.png)</text>
    <text x="15" y="120" font-size="12px" fill="#0f5132">4. กรอกตาราง Rubric ประเมินตนเอง</text>
    <text x="15" y="145" font-size="12px" font-weight="bold" fill="#0f5132">✨ ข้อมูลสำเร็จรูปมีอยู่ใน CHECKLIST_AND_DATA_COPY.md</text>
  </g>
</g>
</svg>
"""
    return svg

# Save Circuit 4 SVG
c4_content = build_circuit_4_svg()
with open(os.path.join(OUTPUT_DIR, "circuit_04_ldr_divider.svg"), "w", encoding="utf-8") as f:
    f.write(c4_content)
with open(os.path.join(ARTIFACT_DIR, "circuit_04_ldr_divider.svg"), "w", encoding="utf-8") as f:
    f.write(c4_content)

print("Generated Complete 38-Pin Circuit 4 SVG!")

# ========================================================
# 1. CIRCUIT 1: BARE ESP32 WITH FULL 38-PIN LABELS & PERIPHERALS
# ========================================================
def build_circuit_1_svg():
    esp_x, esp_y = 100, 140
    board_markup, l_coords, r_coords, b_h = render_esp32_board(esp_x, esp_y, {}, {})

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="1280" height="880" style="background:#f8f9fa; font-family: -apple-system, 'Thonburi', 'Sarabun', 'Segoe UI', Arial, sans-serif;">
<defs>
  <style>
    .title {{ font-size: 24px; font-weight: bold; fill: #0d6efd; }}
    .subtitle {{ font-size: 15px; fill: #495057; }}
    .badge-lab {{ font-size: 14px; font-weight: bold; fill: #198754; }}
    .card {{ fill: #ffffff; stroke: #dee2e6; stroke-width: 1.5; rx: 10; }}
  </style>
</defs>

<!-- Header Card -->
<rect x="25" y="20" width="1230" height="100" class="card" />
<text x="45" y="52" class="title">วงจรที่ 1: ผังขาบอร์ด ESP32 ฉบับสมบูรณ์ (Full 38-Pin Master Reference)</text>
<text x="45" y="78" class="subtitle">แสดงขาทั้งหมดของ ESP32 NodeMCU-32S ครบทั้ง 38 ขา (ฝั่งซ้าย 19 ขา + ฝั่งขวา 19 ขา) พร้อมกลุ่มหน้าที่และฟังก์ชันพิเศษ</text>
<text x="45" y="102" class="badge-lab">📌 ใช้งานแบบบอร์ดเปล่า (เสียบสาย USB ไม่ต้องต่อ Breadboard) สำหรับ: Week 01, Week 05, Week 06, Week 07, Week 08</text>

<!-- ESP32 Board (Full 38 Pins) -->
{board_markup}

<!-- Right Side Pin Function Explanations -->
<g transform="translate(420, 140)">
  <rect x="0" y="0" width="835" height="700" rx="12" class="card" />
  <text x="30" y="38" font-size="18px" font-weight="bold" fill="#0d6efd">📖 คู่มือหน้าที่ของแต่ละขาบนบอร์ด ESP32 (Pin Function Reference)</text>
  
  <g transform="translate(30, 65)">
    <!-- Group 1: Power & Reset -->
    <rect x="0" y="0" width="775" height="85" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <text x="15" y="25" font-size="14px" font-weight="bold" fill="#dc3545">1. ไฟเลี้ยงและรีเซ็ต (Power &amp; Control Pins):</text>
    <text x="15" y="48" font-size="13px" fill="#212529">• <tspan font-weight="bold">3V3:</tspan> แรงดันเอาต์พุต 3.3V จากรกูเลเตอร์บนบอร์ด (ใช้จ่ายไฟให้เซนเซอร์และจอภาพ OLED)</text>
    <text x="15" y="70" font-size="13px" fill="#212529">• <tspan font-weight="bold">5V / VIN:</tspan> ไฟเลี้ยงหลัก 5V จากพอร์ต USB | <tspan font-weight="bold">GND:</tspan> กราวด์ระบบ (มี 4 ตำแหน่งบนบอร์ด) | <tspan font-weight="bold">EN:</tspan> สั่งรีเซ็ตฮาร์ดแวร์</text>

    <!-- Group 2: ADC1 vs ADC2 -->
    <rect x="0" y="100" width="775" height="115" rx="6" fill="#e7f1ff" stroke="#b6d4fe" />
    <text x="15" y="25" font-size="14px" font-weight="bold" fill="#0d6efd">2. ขาแอนะล็อกอินพุต (Analog-to-Digital Converter - ADC):</text>
    <text x="15" y="48" font-size="13px" fill="#0d6efd">• <tspan font-weight="bold">ADC1 (GPIO 32, 33, 34, 35, 36/VP, 39/VN):</tspan> **ปลอดภัยสูงสุด** ใช้งานได้ตลอดเวลา ไม่กวน Wi-Fi</text>
    <text x="25" y="70" font-size="12px" fill="#495057">→ แล็บในวิชานี้กำหนดให้ใช้ <tspan font-weight="bold" fill="#0d6efd">GPIO 34 (ADC1_CH6)</tspan> เป็นหลักสำหรับ Potentiometer และ LDR</text>
    <text x="15" y="95" font-size="13px" fill="#6c757d">• <tspan font-weight="bold">ADC2 (GPIO 0, 2, 4, 12-15, 25-27):</tspan> ห้ามใช้อ่านแอนะล็อกขณะเปิด Wi-Fi (Wi-Fi Driver จะจองบล็อก ADC2)</text>

    <!-- Group 3: High-speed SPI Buses -->
    <rect x="0" y="230" width="775" height="95" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <text x="15" y="25" font-size="14px" font-weight="bold" fill="#198754">3. บัสสื่อสารความเร็วสูง SPI2 (VSPI) สำหรับจอภาพกราฟิก (Week 09):</text>
    <text x="15" y="48" font-size="13px" fill="#212529">• <tspan font-weight="bold">GPIO 18 (VSPI_CLK):</tspan> สัญญาณนาฬิกา D0 | <tspan font-weight="bold">GPIO 23 (VSPI_MOSI):</tspan> ข้อมูลส่งออก D1</text>
    <text x="15" y="70" font-size="13px" fill="#212529">• <tspan font-weight="bold">GPIO 5 (VSPI_CS):</tspan> Chip Select | <tspan font-weight="bold">GPIO 4:</tspan> Hardware Reset (RES) | <tspan font-weight="bold">GPIO 2:</tspan> Data/Command (DC)</text>

    <!-- Group 4: Actuator GPIO 2 -->
    <rect x="0" y="340" width="775" height="80" rx="6" fill="#fff3cd" stroke="#ffecb5" />
    <text x="15" y="25" font-size="14px" font-weight="bold" fill="#664d03">4. ขาควบคุม Actuator (GPIO 2 - Onboard Blue LED):</text>
    <text x="15" y="48" font-size="13px" fill="#212529">• เป็นขาต่อขนานอยู่กับหลอดไฟสีน้ำเงินบนบอร์ด NodeMCU-32S ใช้ทดสอบไฟกระพริบใน Week 02</text>
    <text x="15" y="68" font-size="13px" fill="#212529">• ใช้เป็น Actuator สั่งเปิด-ปิดไฟผ่านเครือข่ายใน Week 10 (HTTP/CoAP), Week 11 (MQTT), และ Week 12 (Flutter)</text>

    <!-- Group 5: Strapping Pins Warning -->
    <rect x="0" y="435" width="775" height="85" rx="6" fill="#f8d7da" stroke="#f5c2c7" />
    <text x="15" y="25" font-size="14px" font-weight="bold" fill="#842029">⚠️ ขาต้องห้ามระวังพิเศษ (Strapping Pins):</text>
    <text x="15" y="48" font-size="13px" fill="#842029">• <tspan font-weight="bold">GPIO 0, GPIO 2, GPIO 12, GPIO 15:</tspan> เป็นขาตั้งค่าโหมดบูตของชิป ESP32</text>
    <text x="15" y="70" font-size="13px" fill="#842029">• ห้ามต่อดึงลอจิกค้างลงกราวด์ตอนบูต เพราะอาจทำให้บอร์ดเข้าโหมดแฟลชไม่สำเร็จ หรือรีบูตวนซ้ำ</text>

    <!-- Group 6: Summary for Friends -->
    <rect x="0" y="535" width="775" height="80" rx="6" fill="#d1e7dd" stroke="#a3cfbb" />
    <text x="15" y="25" font-size="14px" font-weight="bold" fill="#0f5132">🚀 กฎเหล็กจำง่ายในการต่อวงจรทั้ง 12 สัปดาห์:</text>
    <text x="15" y="48" font-size="13px" font-weight="bold" fill="#0f5132">1. จำแค่ 2 ขาหลัก: เซนเซอร์แอนะล็อกต่อ "GPIO 34" เสมอ | สวิตช์หลอดไฟต่อ "GPIO 2" เสมอ</text>
    <text x="15" y="68" font-size="13px" fill="#0f5132">2. จ่ายไฟให้เซนเซอร์จากขา "3.3V" เท่านั้น (ห้ามต่อขา 5V เข้าเซนเซอร์เด็ดขาด)</text>
  </g>
</g>
</svg>
"""
    return svg

# Save Circuit 1 SVG
c1_content = build_circuit_1_svg()
with open(os.path.join(OUTPUT_DIR, "circuit_01_bare_esp32.svg"), "w", encoding="utf-8") as f:
    f.write(c1_content)
with open(os.path.join(ARTIFACT_DIR, "circuit_01_bare_esp32.svg"), "w", encoding="utf-8") as f:
    f.write(c1_content)

print("Generated Complete 38-Pin Circuit 1 SVG!")

# ========================================================
# 2. CIRCUIT 2: LED BLINK & PWM (GPIO 2)
# ========================================================
def build_circuit_2_svg():
    esp_x, esp_y = 60, 140
    active_l = {}
    active_r = {"G2": "#fd7e14", "GND": "#212529"}
    board_markup, l_coords, r_coords, b_h = render_esp32_board(esp_x, esp_y, active_l, active_r)
    
    p_g2 = r_coords["G2"]
    p_gnd_r = r_coords["GND"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="1280" height="880" style="background:#f8f9fa; font-family: -apple-system, 'Thonburi', 'Sarabun', 'Segoe UI', Arial, sans-serif;">
<defs>
  <style>
    .title {{ font-size: 24px; font-weight: bold; fill: #0d6efd; }}
    .subtitle {{ font-size: 15px; fill: #495057; }}
    .badge-lab {{ font-size: 14px; font-weight: bold; fill: #6f42c1; }}
    .card {{ fill: #ffffff; stroke: #dee2e6; stroke-width: 1.5; rx: 10; }}
    .wire {{ stroke-linecap: round; stroke-linejoin: round; fill: none; }}
  </style>
</defs>

<!-- Header Card -->
<rect x="25" y="20" width="1230" height="100" class="card" />
<text x="45" y="52" class="title">วงจรที่ 2: ควบคุมหลอดไฟ LED ผ่านขา GPIO 2 (LED Blink &amp; PWM)</text>
<text x="45" y="78" class="subtitle">แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมต่อหลอดไฟ LED ผ่านตัวต้านทาน 220Ω เข้าขา GPIO 2 (หรือใช้ Onboard Blue LED)</text>
<text x="45" y="102" class="badge-lab">📌 ใช้ใน: Week 02 (Lab 2.1) — ทดสอบไฟกระพริบและการหรี่แสงไฟ LED</text>

<!-- ESP32 Board (Full 38 Pins) -->
{board_markup}

<!-- Breadboard Layout -->
<g transform="translate(420, 150)">
  <rect x="0" y="0" width="450" height="600" rx="12" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="180" y="30" font-size="14px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- LED + Resistor Box -->
  <g transform="translate(125, 100)">
    <rect x="0" y="0" width="200" height="300" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="100" cy="80" r="40" fill="#dc3545" opacity="0.9" />
    <polygon points="75,115 125,115 100,145" fill="#dc3545" />
    <text x="100" y="180" text-anchor="middle" font-size="15px" font-weight="bold" fill="#212529">LED (Red / Blue)</text>
    
    <!-- Resistor 220 Ohm -->
    <rect x="65" y="200" width="70" height="24" rx="4" fill="#e2d9cc" stroke="#8b7355" stroke-width="2" />
    <line x1="77" y1="200" x2="77" y2="224" stroke="#dc3545" stroke-width="3.5" />
    <line x1="90" y1="200" x2="90" y2="224" stroke="#dc3545" stroke-width="3.5" />
    <line x1="103" y1="200" x2="103" y2="224" stroke="#8b4513" stroke-width="3.5" />
    <text x="100" y="245" text-anchor="middle" font-size="12px" font-weight="bold" fill="#8b4513">R 220Ω (แดง-แดง-น้ำตาล)</text>
    
    <!-- Terminals -->
    <circle cx="75" cy="275" r="7" fill="#fd7e14" /><text x="75" y="295" text-anchor="middle" font-size="11px" fill="#fd7e14">Anode (+)</text>
    <circle cx="125" cy="275" r="6" fill="#212529" /><text x="125" y="295" text-anchor="middle" font-size="11px" fill="#212529">Cathode (-)</text>
  </g>
</g>

<!-- Wire Routing -->
<!-- GPIO 2 Pad -> Resistor Anode -->
<path d="M {p_g2[0]} {p_g2[1]} L 350 {p_g2[1]} L 350 525 L 620 525 L 620 425" stroke="#fd7e14" stroke-width="4.5" class="wire" />
<circle cx="{p_g2[0]}" cy="{p_g2[1]}" r="3" fill="#ffffff" />

<!-- GND Right Pad -> LED Cathode -->
<path d="M {p_gnd_r[0]} {p_gnd_r[1]} L 330 {p_gnd_r[1]} L 330 550 L 670 550 L 670 425" stroke="#212529" stroke-width="4.5" class="wire" />
<circle cx="{p_gnd_r[0]}" cy="{p_gnd_r[1]}" r="3" fill="#ffffff" />

<!-- Right Side Info Box -->
<g transform="translate(900, 150)">
  <rect x="0" y="0" width="355" height="600" rx="12" class="card" />
  <text x="25" y="35" font-size="16px" font-weight="bold" fill="#0d6efd">📋 รายละเอียดการต่อวงจร</text>
  
  <g transform="translate(20, 60)" font-size="13px">
    <rect x="0" y="0" width="315" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <circle cx="15" cy="25" r="6" fill="#fd7e14" />
    <text x="32" y="22" font-weight="bold" fill="#fd7e14">GPIO 2 (ESP32 ขวาแถว 14)</text>
    <text x="32" y="40" font-size="12px" fill="#495057">→ ต่อผ่าน R 220Ω เข้าขาขายาว (Anode +)</text>

    <rect x="0" y="65" width="315" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <circle cx="15" cy="90" r="6" fill="#212529" />
    <text x="32" y="87" font-weight="bold" fill="#212529">GND (ESP32 ขวาแถว 1)</text>
    <text x="32" y="105" font-size="12px" fill="#495057">→ ต่อเข้าขาสั้น (Cathode -) ของ LED</text>
  </g>

  <g transform="translate(20, 200)">
    <rect x="0" y="0" width="315" height="200" rx="8" fill="#d1e7dd" stroke="#a3cfbb" />
    <text x="15" y="25" font-size="14px" font-weight="bold" fill="#0f5132">💡 ทริคเด็ดไม่ต้องต่อวงจรภายนอก:</text>
    <text x="15" y="52" font-size="12px" fill="#0f5132">• บอร์ด ESP32 NodeMCU-32S มีหลอดไฟ LED</text>
    <text x="15" y="74" font-size="12px" fill="#0f5132">  สีน้ำเงิน (Onboard Blue LED) เชื่อมอยู่กับ</text>
    <text x="15" y="96" font-size="12px" font-weight="bold" fill="#0f5132">  ขา GPIO 2 อยู่แล้วบนตัวบอร์ด!</text>
    <text x="15" y="122" font-size="12px" fill="#0f5132">• ถ้าไม่มี Breadboard หรือหลอดไฟ</text>
    <text x="15" y="144" font-size="12px" fill="#0f5132">  สามารถสั่งรันโค้ดแล้วดูไฟสีน้ำเงินกระพริบ</text>
    <text x="15" y="166" font-size="12px" fill="#0f5132">  บนตัวบอร์ดเพื่ออัดคลิปส่งได้ทันที 100%</text>
  </g>
</g>
</svg>
"""
    return svg

# Save Circuit 2 SVG
c2_content = build_circuit_2_svg()
with open(os.path.join(OUTPUT_DIR, "circuit_02_led_pwm.svg"), "w", encoding="utf-8") as f:
    f.write(c2_content)
with open(os.path.join(ARTIFACT_DIR, "circuit_02_led_pwm.svg"), "w", encoding="utf-8") as f:
    f.write(c2_content)

print("Generated Complete 38-Pin Circuit 2 SVG!")

# ========================================================
# 3. CIRCUIT 3: POTENTIOMETER ONLY (GPIO 34)
# ========================================================
def build_circuit_3_svg():
    esp_x, esp_y = 60, 140
    active_l = {"3V3": "#dc3545", "G34": "#0d6efd", "GND": "#212529"}
    board_markup, l_coords, r_coords, b_h = render_esp32_board(esp_x, esp_y, active_l, {})
    
    p_3v3 = l_coords["3V3"]
    p_g34 = l_coords["G34"]
    p_gnd_l = l_coords["GND"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 880" width="1280" height="880" style="background:#f8f9fa; font-family: -apple-system, 'Thonburi', 'Sarabun', 'Segoe UI', Arial, sans-serif;">
<defs>
  <style>
    .title {{ font-size: 24px; font-weight: bold; fill: #0d6efd; }}
    .subtitle {{ font-size: 15px; fill: #495057; }}
    .badge-lab {{ font-size: 14px; font-weight: bold; fill: #6f42c1; }}
    .card {{ fill: #ffffff; stroke: #dee2e6; stroke-width: 1.5; rx: 10; }}
    .wire {{ stroke-linecap: round; stroke-linejoin: round; fill: none; }}
  </style>
</defs>

<!-- Header Card -->
<rect x="25" y="20" width="1230" height="100" class="card" />
<text x="45" y="52" class="title">วงจรที่ 3: ตัวต้านทานปรับค่าได้ (Potentiometer 10kΩ บนขา GPIO 34)</text>
<text x="45" y="78" class="subtitle">แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายไฟ 3.3V, GND และขากลาง (Wiper) เข้าสู่วงจรแปลงสัญญาณ ADC1 Channel 6 บนขา GPIO 34</text>
<text x="45" y="102" class="badge-lab">📌 ใช้ใน: Week 02 (Lab 2.2: วัดมุม 0°-180°), Week 08 (Lab 8.3: สตรีมค่า ADC ไป Kestrel Server)</text>

<!-- ESP32 Board (Full 38 Pins) -->
{board_markup}

<!-- Breadboard Layout -->
<g transform="translate(420, 150)">
  <rect x="0" y="0" width="450" height="600" rx="12" fill="#f1f3f5" stroke="#ced4da" stroke-width="2" />
  <text x="180" y="30" font-size="14px" font-weight="bold" fill="#adb5bd">BREADBOARD</text>
  
  <!-- Potentiometer Component Box -->
  <g transform="translate(115, 100)">
    <rect x="0" y="0" width="220" height="280" rx="8" fill="#ffffff" stroke="#dee2e6" />
    <circle cx="110" cy="95" r="55" fill="#0d6efd" opacity="0.85" />
    <circle cx="110" cy="95" r="30" fill="#e9ecef" />
    <line x1="110" y1="95" x2="138" y2="67" stroke="#0d6efd" stroke-width="5" stroke-linecap="round" />
    
    <text x="110" y="175" text-anchor="middle" font-size="15px" font-weight="bold" fill="#212529">Potentiometer</text>
    <text x="110" y="198" text-anchor="middle" font-size="15px" font-weight="bold" fill="#0d6efd">10 kΩ</text>
    <text x="110" y="218" text-anchor="middle" font-size="11px" fill="#6c757d">หมุนปรับมุม 0° ถึง 180°</text>
    
    <!-- 3 Pins -->
    <circle cx="50" cy="255" r="6" fill="#dc3545" /><text x="50" y="275" text-anchor="middle" font-size="11px" fill="#dc3545">ขา 1 (3.3V)</text>
    <circle cx="110" cy="255" r="7" fill="#0d6efd" /><text x="110" y="275" text-anchor="middle" font-size="12px" font-weight="bold" fill="#0d6efd">Wiper (G34)</text>
    <circle cx="170" cy="255" r="6" fill="#212529" /><text x="170" y="275" text-anchor="middle" font-size="11px" fill="#212529">ขา 3 (GND)</text>
  </g>
</g>

<!-- Wire Routing -->
<!-- 1. 3V3 Pad -> POT Pin 1 (115+50+420=585, 100+255+150=505) -->
<path d="M {p_3v3[0]} {p_3v3[1]} L 30 {p_3v3[1]} L 30 780 L 585 780 L 585 505" stroke="#dc3545" stroke-width="4.5" class="wire" />
<circle cx="{p_3v3[0]}" cy="{p_3v3[1]}" r="3" fill="#ffffff" />

<!-- 2. G34 Pad -> POT Wiper (115+110+420=645, 505) -->
<path d="M {p_g34[0]} {p_g34[1]} L 45 {p_g34[1]} L 45 805 L 645 805 L 645 505" stroke="#0d6efd" stroke-width="4.5" class="wire" />
<circle cx="{p_g34[0]}" cy="{p_g34[1]}" r="3" fill="#ffffff" />

<!-- 3. GND Pad -> POT Pin 3 (115+170+420=705, 505) -->
<path d="M {p_gnd_l[0]} {p_gnd_l[1]} L 15 {p_gnd_l[1]} L 15 830 L 705 830 L 705 505" stroke="#212529" stroke-width="4.5" class="wire" />
<circle cx="{p_gnd_l[0]}" cy="{p_gnd_l[1]}" r="3" fill="#ffffff" />

<!-- Right Side Pinout Box -->
<g transform="translate(900, 150)">
  <rect x="0" y="0" width="355" height="600" rx="12" class="card" />
  <text x="25" y="35" font-size="16px" font-weight="bold" fill="#0d6efd">📋 ตารางการต่อสาย Potentiometer</text>
  
  <g transform="translate(20, 60)" font-size="13px">
    <rect x="0" y="0" width="315" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <circle cx="15" cy="25" r="6" fill="#dc3545" />
    <text x="32" y="22" font-weight="bold" fill="#dc3545">ขา 3V3 (ESP32 ซ้ายแถว 1)</text>
    <text x="32" y="40" font-size="12px" fill="#495057">→ ขาที่ 1 ของ POT (สายสีแดง)</text>

    <rect x="0" y="65" width="315" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <circle cx="15" cy="90" r="6" fill="#0d6efd" />
    <text x="32" y="87" font-weight="bold" fill="#0d6efd">GPIO 34 (ESP32 ซ้ายแถว 5)</text>
    <text x="32" y="105" font-size="12px" fill="#495057">→ ขากลาง Wiper (สายสีน้ำเงิน ADC1)</text>

    <rect x="0" y="130" width="315" height="50" rx="6" fill="#f8f9fa" stroke="#dee2e6" />
    <circle cx="15" cy="155" r="6" fill="#212529" />
    <text x="32" y="152" font-weight="bold" fill="#212529">GND (ESP32 ซ้ายแถว 14)</text>
    <text x="32" y="170" font-size="12px" fill="#495057">→ ขาที่ 3 ของ POT (สายสีดำ)</text>
  </g>

  <g transform="translate(20, 270)">
    <rect x="0" y="0" width="315" height="180" rx="8" fill="#fff3cd" stroke="#ffecb5" />
    <text x="15" y="25" font-size="14px" font-weight="bold" fill="#664d03">⚠️ ข้อควรระวังเรื่องแรงดันไฟฟ้า:</text>
    <text x="15" y="52" font-size="12px" fill="#664d03">• ห้ามนำขาไฟเลี้ยงของ POT ไปต่อเข้าขา 5V/VIN</text>
    <text x="15" y="74" font-size="12px" fill="#664d03">  เพราะภาค ADC1 ของ ESP32 ทนแรงดันได้สูงสุด</text>
    <text x="15" y="96" font-size="12px" font-weight="bold" fill="#dc3545">  3.3V เท่านั้น! (หากต่อ 5V ขา GPIO 34 อาจพังได้)</text>
    <text x="15" y="122" font-size="12px" fill="#664d03">• ใช้ขา 3.3V สีแดง เพื่อความปลอดภัย 100%</text>
    <text x="15" y="145" font-size="12px" fill="#664d03">• ค่า ADC ที่อ่านได้จะอยู่ในช่วง 0 ถึง 4095</text>
  </g>
</g>
</svg>
"""
    return svg

# Save Circuit 3 SVG
c3_content = build_circuit_3_svg()
with open(os.path.join(OUTPUT_DIR, "circuit_03_pot_adc.svg"), "w", encoding="utf-8") as f:
    f.write(c3_content)
with open(os.path.join(ARTIFACT_DIR, "circuit_03_pot_adc.svg"), "w", encoding="utf-8") as f:
    f.write(c3_content)

print("Generated Complete 38-Pin Circuit 3 SVG!")
