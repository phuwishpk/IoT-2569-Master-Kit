#!/usr/bin/env python3
"""
Generate professional wiring diagrams for IoT-App-2569 (Week 01 to Week 12).
Outputs high-res PNG images with clear pinouts, color-coded wires, and Thai annotations.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/Users/phuwish/Downloads/fortest week1 week2/IoT-2569-Master-Kit/circuits"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/Supplemental/Thonburi.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

FONT_TITLE = get_font(34, bold=True)
FONT_SUBTITLE = get_font(20)
FONT_HEADING = get_font(22, bold=True)
FONT_LABEL = get_font(18, bold=True)
FONT_SMALL = get_font(15)
FONT_NOTE = get_font(16)

# Colors
BG_COLOR = (248, 249, 250)
CARD_BG = (255, 255, 255)
BORDER_COLOR = (222, 226, 230)
TEXT_DARK = (33, 37, 41)
TEXT_MUTED = (108, 117, 125)
PRIMARY_BLUE = (13, 110, 253)
SUCCESS_GREEN = (25, 135, 84)
WARNING_AMBER = (255, 193, 7)
DANGER_RED = (220, 53, 69)
PURPLE = (111, 66, 193)
ESP32_DARK = (40, 44, 52)
ESP32_SILVER = (200, 205, 215)
WIRE_3V3 = (220, 53, 69)      # Red
WIRE_GND = (33, 37, 41)       # Black
WIRE_ADC = (13, 110, 253)     # Blue
WIRE_PWM = (255, 159, 28)     # Orange
WIRE_SPI_CLK = (25, 135, 84)  # Green
WIRE_SPI_DAT = (111, 66, 193) # Purple
WIRE_SPI_RST = (23, 162, 184) # Cyan
WIRE_SPI_DC  = (232, 62, 140) # Pink
WIRE_SPI_CS  = (253, 126, 20) # Orange-red

def draw_header(draw, title, subtitle, labs_used, badge_text=""):
    # Header card
    draw.rectangle([(30, 20), (1370, 140)], fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((50, 32), title, font=FONT_TITLE, fill=PRIMARY_BLUE)
    draw.text((50, 78), subtitle, font=FONT_SUBTITLE, fill=TEXT_DARK)
    draw.text((50, 106), f"📌 สัปดาห์ที่ใช้วงจรนี้: {labs_used}", font=FONT_LABEL, fill=PURPLE)
    
    if badge_text:
        # Badge on right
        bbox = draw.textbbox((0, 0), badge_text, font=FONT_HEADING)
        bw = bbox[2] - bbox[0] + 30
        draw.rounded_rectangle([(1370 - bw - 30, 45), (1370 - 30, 95)], radius=8, fill=SUCCESS_GREEN)
        draw.text((1370 - bw - 15, 57), badge_text, font=FONT_HEADING, fill=(255, 255, 255))

def draw_esp32_board(draw, x, y, width=280, height=520):
    # Main PCB
    draw.rounded_rectangle([(x, y), (x + width, y + height)], radius=16, fill=ESP32_DARK, outline=(70, 75, 85), width=3)
    # Metal RF Shield
    draw.rounded_rectangle([(x + 40, y + 50), (x + width - 40, y + 210)], radius=6, fill=ESP32_SILVER, outline=(160, 165, 175), width=2)
    draw.text((x + 75, y + 105), "ESP-WROOM-32", font=FONT_LABEL, fill=(30, 35, 45))
    draw.text((x + 95, y + 135), "CE / FCC / Wi-Fi", font=FONT_SMALL, fill=(80, 85, 95))
    # Micro-USB port at bottom
    draw.rounded_rectangle([(x + width//2 - 35, y + height - 25), (x + width//2 + 35, y + height + 10)], radius=4, fill=(180, 185, 195), outline=(100, 105, 115), width=2)
    draw.text((x + width//2 - 25, y + height - 18), "USB", font=FONT_SMALL, fill=(50, 55, 65))
    # Reset & Boot buttons
    draw.rectangle([(x + 20, y + height - 60), (x + 50, y + height - 35)], fill=(200, 50, 50))
    draw.text((x + 18, y + height - 80), "EN", font=FONT_SMALL, fill=(200, 200, 200))
    draw.rectangle([(x + width - 50, y + height - 60), (x + width - 20, y + height - 35)], fill=(50, 50, 50))
    draw.text((x + width - 55, y + height - 80), "BOOT", font=FONT_SMALL, fill=(200, 200, 200))
    
    # Left Pins (3.3V, EN, GPIO 36, 39, 34, 35, 32, 33, 25, 26, 27, 14, 12, GND...)
    left_pins = [
        ("3V3", WIRE_3V3), ("EN", TEXT_MUTED), ("VP (36)", TEXT_MUTED), ("VN (39)", TEXT_MUTED),
        ("G34", WIRE_ADC), ("G35", TEXT_MUTED), ("G32", TEXT_MUTED), ("G33", TEXT_MUTED),
        ("G25", TEXT_MUTED), ("G26", TEXT_MUTED), ("G27", TEXT_MUTED), ("G14", TEXT_MUTED),
        ("G12", TEXT_MUTED), ("GND", WIRE_GND)
    ]
    pin_y_start = y + 70
    pin_step = 28
    left_coords = {}
    for i, (pname, pcolor) in enumerate(left_pins):
        py = pin_y_start + i * pin_step
        # Pin hole
        draw.ellipse([(x - 8, py - 6), (x + 8, py + 6)], fill=(255, 215, 0), outline=(150, 130, 0), width=1)
        draw.text((x + 15, py - 9), pname, font=FONT_SMALL, fill=(220, 220, 220))
        left_coords[pname] = (x, py)
        
    # Right Pins (GND, G23, G22, TX, RX, G21, G19, G18, G5, G4, G2, G15...)
    right_pins = [
        ("GND", WIRE_GND), ("G23", WIRE_SPI_DAT), ("G22", TEXT_MUTED), ("TX0", TEXT_MUTED),
        ("RX0", TEXT_MUTED), ("G21", TEXT_MUTED), ("G19", TEXT_MUTED), ("G18", WIRE_SPI_CLK),
        ("G5", WIRE_SPI_CS), ("G4", WIRE_SPI_RST), ("G2", WIRE_PWM), ("G15", TEXT_MUTED),
        ("GND", WIRE_GND), ("5V", TEXT_MUTED)
    ]
    right_coords = {}
    for i, (pname, pcolor) in enumerate(right_pins):
        py = pin_y_start + i * pin_step
        draw.ellipse([(x + width - 8, py - 6), (x + width + 8, py + 6)], fill=(255, 215, 0), outline=(150, 130, 0), width=1)
        bbox = draw.textbbox((0, 0), pname, font=FONT_SMALL)
        pw = bbox[2] - bbox[0]
        draw.text((x + width - 15 - pw, py - 9), pname, font=FONT_SMALL, fill=(220, 220, 220))
        right_coords[f"R_{pname}_{i}"] = (x + width, py)
        if pname not in right_coords:
            right_coords[pname] = (x + width, py)

    return left_coords, right_coords

def draw_legend(draw, x, y, items):
    draw.rounded_rectangle([(x, y), (x + 420, y + len(items)*32 + 40)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((x + 20, y + 12), "📋 สรุปการเชื่อมต่อสาย (Pin Connection Guide)", font=FONT_LABEL, fill=TEXT_DARK)
    for i, (wire_color, pin_text, desc_text) in enumerate(items):
        iy = y + 45 + i * 32
        # Wire color swatch
        draw.line([(x + 20, iy + 10), (x + 50, iy + 10)], fill=wire_color, width=5)
        draw.ellipse([(x + 47, iy + 7), (x + 53, iy + 13)], fill=wire_color)
        draw.text((x + 65, iy), pin_text, font=FONT_LABEL, fill=PRIMARY_BLUE)
        draw.text((x + 200, iy + 2), desc_text, font=FONT_SMALL, fill=TEXT_DARK)

def save_image(img, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, "PNG", dpi=(150, 150))
    print(f"Generated: {filepath}")

# ==========================================
# 1. SETUP 1: BARE ESP32
# ==========================================
def gen_bare_esp32():
    img = Image.new("RGB", (1400, 780), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 1: บอร์ด ESP32 แบบไม่ต้องต่อวงจรภายนอก (Bare Board)",
        "ใช้การเชื่อมต่อผ่านพอร์ต Micro-USB เข้าคอมพิวเตอร์อย่างเดียว ไม่ต้องเสียบลง Breadboard",
        "Week 01, Week 05, Week 06, Week 07, Week 08 (Lab 8.1, 8.2, 8.4, 8.5)",
        "เสียบสาย USB เส้นเดียวจบ"
    )
    
    # Draw ESP32
    draw_esp32_board(draw, 450, 180)
    
    # Draw USB Cable & Laptop
    draw.line([(590, 700), (590, 740), (280, 740)], fill=(70, 75, 85), width=8)
    draw.rounded_rectangle([(80, 480), (320, 680)], radius=12, fill=(230, 235, 245), outline=PRIMARY_BLUE, width=3)
    draw.rectangle([(100, 500), (300, 630)], fill=(30, 40, 60))
    draw.text((120, 550), "Computer / IDE", font=FONT_HEADING, fill=(255, 255, 255))
    draw.text((115, 585), "idf.py flash monitor", font=FONT_SMALL, fill=(0, 255, 120))
    draw.rectangle([(60, 675), (340, 695)], fill=(180, 185, 195)) # Keyboard base
    
    # Explanatory card
    draw.rounded_rectangle([(800, 200), (1350, 680)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((830, 225), "📝 รายละเอียดและข้อแนะนำของวงจรนี้", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    notes = [
        ("Week 01 (Intro & Architecture)", "ทดสอบต่อคอมพิวเตอร์ ดู Serial Log และคุยกับ AI TA"),
        ("Week 05 (Wi-Fi ESP32 Station)", "บอร์ดใช้ชิป Wi-Fi ภายใน สแกน AP และเชื่อมต่อเน็ต"),
        ("Week 06 (Wi-Fi SoftAP & FreeRTOS)", "บอร์ดปล่อย Wi-Fi Hotspot ในตัว (ESP32_AP_XXXX)"),
        ("Week 07 (Wi-Fi Provisioning)", "ใช้ BLE / SoftAP ในชิป รับค่า Wi-Fi จากสมาร์ทโฟน"),
        ("Week 08 (Kestrel Simulation)", "รัน C# Web Server บนคอมพิวเตอร์ จำลองค่าผ่านซอฟต์แวร์"),
        ("💡 เทคนิคสำคัญ", "ใช้สาย USB Data (ไม่ใช่สายชาร์จ) และกด BOOT ค้างตอน Flash หากบอร์ดไม่ Auto-reset")
    ]
    
    ny = 275
    for title, desc in notes:
        draw.text((830, ny), f"• {title}:", font=FONT_LABEL, fill=TEXT_DARK)
        draw.text((850, ny + 26), desc, font=FONT_SMALL, fill=TEXT_MUTED)
        ny += 64
        
    save_image(img, "circuit_01_bare_esp32.png")

# ==========================================
# 2. SETUP 2: LED BLINK (GPIO 2)
# ==========================================
def gen_led_pwm():
    img = Image.new("RGB", (1400, 780), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 2: ควบคุมหลอดไฟ LED ผ่านขา GPIO 2 (LED Blink & PWM)",
        "ต่อหลอดไฟ LED อนุกรมกับตัวต้านทานจำกัดกระแส 220Ω เข้าขา GPIO 2 (หรือใช้ Onboard LED)",
        "Week 02 (Lab 2.1)",
        "วงจรพื้นฐาน Actuator"
    )
    
    l_pins, r_pins = draw_esp32_board(draw, 250, 180)
    
    # Draw Breadboard on right
    bx, by = 680, 240
    draw.rounded_rectangle([(bx, by), (bx + 350, by + 440)], radius=12, fill=(245, 245, 240), outline=(200, 200, 190), width=2)
    draw.text((bx + 110, by + 15), "Breadboard", font=FONT_LABEL, fill=TEXT_MUTED)
    
    # Power rails (+ Red, - Blue)
    draw.line([(bx + 30, by + 50), (bx + 30, by + 410)], fill=(220, 50, 50), width=3)
    draw.line([(bx + 50, by + 50), (bx + 50, by + 410)], fill=(50, 50, 220), width=3)
    
    # LED Component
    draw.text((bx + 160, by + 80), "LED (Red / Blue)", font=FONT_HEADING, fill=DANGER_RED)
    draw.ellipse([(bx + 180, by + 130), (bx + 240, by + 190)], fill=(255, 60, 60), outline=(180, 0, 0), width=2)
    draw.polygon([(bx + 190, by + 190), (bx + 230, by + 190), (bx + 210, by + 230)], fill=(200, 0, 0)) # LED bulb triangle base
    # Anode (Long leg) & Cathode (Flat leg)
    draw.text((bx + 130, by + 240), "Anode (+) ขายาว", font=FONT_SMALL, fill=TEXT_DARK)
    draw.text((bx + 245, by + 240), "Cathode (-) ขาสั้น", font=FONT_SMALL, fill=TEXT_DARK)
    
    # Resistor 220 Ohm
    draw.text((bx + 120, by + 310), "Resistor 220Ω (แดง-แดง-น้ำตาล)", font=FONT_SMALL, fill=TEXT_DARK)
    draw.rounded_rectangle([(bx + 160, by + 340), (bx + 250, by + 370)], radius=4, fill=(210, 180, 140), outline=(120, 100, 80), width=2)
    # Color bands: Red, Red, Brown, Gold
    draw.rectangle([(bx + 175, by + 340), (bx + 182, by + 370)], fill=(220, 20, 20))
    draw.rectangle([(bx + 192, by + 340), (bx + 199, by + 370)], fill=(220, 20, 20))
    draw.rectangle([(bx + 209, by + 340), (bx + 216, by + 370)], fill=(139, 69, 19))
    draw.rectangle([(bx + 230, by + 340), (bx + 237, by + 370)], fill=(218, 165, 32))
    
    # Wire Connections:
    # 1. GPIO 2 -> Resistor -> LED Anode
    g2_x, g2_y = r_pins["G2"]
    draw.line([(g2_x, g2_y), (g2_x + 80, g2_y), (g2_x + 80, by + 355), (bx + 160, by + 355)], fill=WIRE_PWM, width=4)
    draw.line([(bx + 250, by + 355), (bx + 290, by + 355), (bx + 290, by + 230), (bx + 200, by + 230)], fill=WIRE_PWM, width=4)
    
    # 2. LED Cathode -> GND
    gnd_x, gnd_y = r_pins["GND"]
    draw.line([(bx + 220, by + 230), (bx + 260, by + 230), (bx + 260, by + 400), (bx + 50, by + 400)], fill=WIRE_GND, width=4)
    draw.line([(bx + 50, by + 400), (bx - 50, by + 400), (bx - 50, gnd_y), (gnd_x, gnd_y)], fill=WIRE_GND, width=4)

    # Legend
    legend_items = [
        (WIRE_PWM, "GPIO 2", "สัญญาณควบคุมเปิด-ปิด / PWM (ต่อผ่าน R 220Ω เข้า Anode +)"),
        (WIRE_GND, "GND", "กราวด์ระบบ (ต่อจาก Cathode - ขาสั้นของ LED)")
    ]
    draw_legend(draw, 1070, 240, legend_items)
    
    # Note
    draw.rounded_rectangle([(1070, 420), (1370, 680)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((1090, 440), "💡 เคล็ดลับหน้างาน", font=FONT_HEADING, fill=SUCCESS_GREEN)
    draw.text((1090, 485), "• บนบอร์ด NodeMCU-32S มี", font=FONT_LABEL, fill=TEXT_DARK)
    draw.text((1105, 515), "Blue LED ขา GPIO 2 อยู่แล้ว", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.text((1090, 555), "• หากไม่มี LED ภายนอก", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((1105, 580), "สามารถสั่งรันโค้ดแล้วดูไฟสีน้ำเงิน", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((1105, 605), "กระพริบบนตัวบอร์ดได้ทันที!", font=FONT_SMALL, fill=TEXT_MUTED)
    
    save_image(img, "circuit_02_led_pwm.png")

# ==========================================
# 3. SETUP 3: POTENTIOMETER ONLY (GPIO 34)
# ==========================================
def gen_pot_adc():
    img = Image.new("RGB", (1400, 780), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 3: ตัวต้านทานปรับค่าได้ (Potentiometer 10kΩ) เข้าขา GPIO 34",
        "วงจรแบ่งแรงดันแอนะล็อก ปรับค่าแรงดัน 0.00V - 3.30V แปลงเป็นสัญญาณดิจิทัล 0 - 4095 ด้วย ADC1",
        "Week 02 (Lab 2.2), Week 08 (Lab 8.3)",
        "วงจรเซนเซอร์อนาล็อก"
    )
    
    l_pins, r_pins = draw_esp32_board(draw, 250, 180)
    
    # Draw Breadboard on right
    bx, by = 680, 240
    draw.rounded_rectangle([(bx, by), (bx + 350, by + 440)], radius=12, fill=(245, 245, 240), outline=(200, 200, 190), width=2)
    draw.text((bx + 110, by + 15), "Breadboard", font=FONT_LABEL, fill=TEXT_MUTED)
    
    # Potentiometer Component (Rotary Knob)
    draw.text((bx + 80, by + 60), "Potentiometer 10kΩ", font=FONT_HEADING, fill=PRIMARY_BLUE)
    draw.ellipse([(bx + 110, by + 110), (bx + 240, by + 240)], fill=(70, 130, 180), outline=(30, 70, 120), width=4)
    draw.ellipse([(bx + 145, by + 145), (bx + 205, by + 205)], fill=(220, 225, 230), outline=(150, 155, 160), width=2)
    draw.line([(bx + 175, by + 175), (bx + 215, by + 145)], fill=(30, 70, 120), width=5) # Knob indicator pointer
    
    # 3 Pins of Potentiometer
    p1 = (bx + 110, by + 300) # 3.3V
    p2 = (bx + 175, by + 300) # Wiper (GPIO 34)
    p3 = (bx + 240, by + 300) # GND
    
    for px, py in [p1, p2, p3]:
        draw.rectangle([(px - 8, py - 40), (px + 8, py)], fill=(180, 185, 190), outline=(100, 105, 110), width=1)
        draw.ellipse([(px - 8, py - 6), (px + 8, py + 6)], fill=(255, 215, 0), outline=(150, 130, 0), width=1)
        
    draw.text((p1[0] - 25, p1[1] + 15), "ขา 1 (3.3V)", font=FONT_SMALL, fill=DANGER_RED)
    draw.text((p2[0] - 40, p2[1] + 45), "ขากลาง (Wiper)", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.text((p3[0] - 20, p3[1] + 15), "ขา 3 (GND)", font=FONT_SMALL, fill=TEXT_DARK)

    # Wires:
    # 3.3V from ESP32 left pins
    v3_x, v3_y = l_pins["3V3"]
    draw.line([(v3_x, v3_y), (v3_x - 60, v3_y), (v3_x - 60, by + 380), (p1[0], by + 380), p1], fill=WIRE_3V3, width=4)
    
    # GND from ESP32 left pins
    gnd_x, gnd_y = l_pins["GND"]
    draw.line([(gnd_x, gnd_y), (gnd_x - 40, gnd_y), (gnd_x - 40, by + 410), (p3[0], by + 410), p3], fill=WIRE_GND, width=4)
    
    # GPIO 34 (Wiper)
    g34_x, g34_y = l_pins["G34"]
    draw.line([(g34_x, g34_y), (g34_x - 80, g34_y), (g34_x - 80, by + 350), (p2[0], by + 350), p2], fill=WIRE_ADC, width=4)

    # Legend
    legend_items = [
        (WIRE_3V3, "3.3V (VCC)", "ไฟเลี้ยงแอนะล็อก ต่อเข้าขา 1 ของตัวต้านทานปรับค่าได้"),
        (WIRE_ADC, "GPIO 34", "ขาขากลาง (Wiper) ต่อเข้า ADC1 Channel 6"),
        (WIRE_GND, "GND", "กราวด์ ต่อเข้าขา 3 ของตัวต้านทานปรับค่าได้")
    ]
    draw_legend(draw, 1070, 240, legend_items)
    
    # Rules
    draw.rounded_rectangle([(1070, 440), (1370, 680)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((1090, 460), "⚠️ ข้อควรระวัง", font=FONT_HEADING, fill=DANGER_RED)
    draw.text((1090, 505), "• ห้ามต่อขาไฟเลี้ยงเข้า 5V/VIN", font=FONT_LABEL, fill=DANGER_RED)
    draw.text((1105, 535), "เพราะ ADC ของ ESP32 รับแรงดัน", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((1105, 560), "ได้สูงสุด 3.3V เท่านั้น (อาจพังได้)", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((1090, 595), "• ขา GPIO 34 เป็น Input-only", font=FONT_LABEL, fill=TEXT_DARK)
    draw.text((1105, 625), "อยู่ในยูนิต ADC1 ไม่ชนกับ Wi-Fi", font=FONT_SMALL, fill=SUCCESS_GREEN)
    
    save_image(img, "circuit_03_pot_adc.png")

# ==========================================
# 4. SETUP 4: LDR VOLTAGE DIVIDER (Week 03)
# ==========================================
def gen_ldr_divider():
    img = Image.new("RGB", (1400, 780), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 4: วงจรแบ่งแรงดันเซนเซอร์แสง LDR ร่วมกับ R 10kΩ",
        "ต่อตัวต้านทานไวแสง (LDR) อนุกรมกับตัวต้านทานคงที่ 10kΩ ดึงแรงดันกึ่งกลางเข้าขา GPIO 34 (ADC1)",
        "Week 03 (LDR Calibration II)",
        "เซนเซอร์แสง Lux"
    )
    
    l_pins, r_pins = draw_esp32_board(draw, 250, 180)
    
    # Draw Breadboard on right
    bx, by = 680, 240
    draw.rounded_rectangle([(bx, by), (bx + 350, by + 440)], radius=12, fill=(245, 245, 240), outline=(200, 200, 190), width=2)
    draw.text((bx + 110, by + 15), "Breadboard", font=FONT_LABEL, fill=TEXT_MUTED)
    
    # LDR Component
    draw.text((bx + 100, by + 60), "LDR (Photoresistor)", font=FONT_HEADING, fill=WARNING_AMBER)
    draw.ellipse([(bx + 140, by + 100), (bx + 210, by + 170)], fill=(230, 210, 170), outline=(180, 120, 50), width=3)
    # LDR squiggly line
    draw.line([(bx + 150, by + 135), (bx + 160, by + 125), (bx + 170, by + 145), (bx + 180, by + 125), (bx + 190, by + 145), (bx + 200, by + 135)], fill=(180, 50, 20), width=3)
    
    # Central Node (Tie Point)
    node_pt = (bx + 175, by + 230)
    draw.ellipse([(node_pt[0] - 10, node_pt[1] - 10), (node_pt[0] + 10, node_pt[1] + 10)], fill=(255, 215, 0), outline=(150, 130, 0), width=2)
    draw.text((node_pt[0] + 18, node_pt[1] - 10), "Vout (Node กลาง)", font=FONT_LABEL, fill=PRIMARY_BLUE)
    
    # Fixed Resistor 10k Ohm (น้ำตาล-ดำ-ส้ม)
    draw.text((bx + 80, by + 280), "Fixed Resistor 10kΩ", font=FONT_HEADING, fill=TEXT_DARK)
    draw.rounded_rectangle([(bx + 155, by + 320), (bx + 195, by + 390)], radius=4, fill=(210, 180, 140), outline=(120, 100, 80), width=2)
    # Bands: Brown, Black, Orange, Gold
    draw.rectangle([(bx + 155, by + 330), (bx + 195, by + 338)], fill=(139, 69, 19))
    draw.rectangle([(bx + 155, by + 348), (bx + 195, by + 356)], fill=(0, 0, 0))
    draw.rectangle([(bx + 155, by + 366), (bx + 195, by + 374)], fill=(255, 140, 0))
    draw.rectangle([(bx + 155, by + 380), (bx + 195, by + 386)], fill=(218, 165, 32))
    
    # Internal connection on breadboard:
    draw.line([(bx + 175, by + 170), node_pt], fill=WIRE_3V3, width=3) # LDR to Node
    draw.line([node_pt, (bx + 175, by + 320)], fill=WIRE_ADC, width=3) # Node to R10k
    
    # Wires from ESP32:
    # 3.3V to LDR top leg
    v3_x, v3_y = l_pins["3V3"]
    draw.line([(v3_x, v3_y), (v3_x - 60, v3_y), (v3_x - 60, by + 110), (bx + 140, by + 110)], fill=WIRE_3V3, width=4)
    
    # GND to R10k bottom leg
    gnd_x, gnd_y = l_pins["GND"]
    draw.line([(gnd_x, gnd_y), (gnd_x - 40, gnd_y), (gnd_x - 40, by + 410), (bx + 175, by + 410), (bx + 175, by + 390)], fill=WIRE_GND, width=4)
    
    # GPIO 34 to Node กลาง
    g34_x, g34_y = l_pins["G34"]
    draw.line([(g34_x, g34_y), (g34_x - 80, g34_y), (g34_x - 80, node_pt[1]), node_pt], fill=WIRE_ADC, width=4)

    # Legend
    legend_items = [
        (WIRE_3V3, "3.3V", "จ่ายไฟบวกเข้าขาที่ 1 ของเซนเซอร์ LDR"),
        (WIRE_ADC, "GPIO 34", "อ่านแรงดันแบ่งกึ่งกลาง (จุดแยก LDR กับ R 10kΩ)"),
        (WIRE_GND, "GND", "ต่อปลายขาของตัวต้านทานคงที่ 10kΩ ลงกราวด์")
    ]
    draw_legend(draw, 1070, 240, legend_items)
    
    # Formula box
    draw.rounded_rectangle([(1070, 440), (1370, 680)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((1090, 460), "📐 สูตรการทำงาน", font=FONT_HEADING, fill=PURPLE)
    draw.text((1090, 500), "Vout = (R10k / (R_ldr + R10k)) × 3.3V", font=FONT_SMALL, fill=TEXT_DARK)
    draw.text((1090, 535), "• เมื่อมืดสนิท: R_ldr สูงมาก (>200kΩ)", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((1105, 560), "-> Vout ต่ำ, ADC ได้ค่าสูง ~3900+", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((1090, 595), "• เมื่อแสงจ้า: R_ldr ลดลง (<1kΩ)", font=FONT_SMALL, fill=TEXT_MUTED)
    draw.text((1105, 620), "-> Vout สูง, ADC ลดลงเหลือ ~200-700", font=FONT_SMALL, fill=TEXT_MUTED)

    save_image(img, "circuit_04_ldr_divider.png")

# ==========================================
# 5. SETUP 5: RGB COLOR SENSING (Week 04)
# ==========================================
def gen_rgb_color_sensing():
    img = Image.new("RGB", (1400, 780), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 5: ตรวจจับสีวัตถุด้วย RGB LED (GPIO 4, 5, 23) และ LDR (GPIO 34)",
        "ส่องแสงสีแดง เขียว น้ำเงิน กระทบวัตถุทีละสี และวัดความเข้มแสงสะท้อนผ่านเซนเซอร์ LDR",
        "Week 04 (LED and Color Sensing)",
        "Color Sensor Module"
    )
    
    l_pins, r_pins = draw_esp32_board(draw, 220, 180)
    
    # Breadboard
    bx, by = 600, 220
    draw.rounded_rectangle([(bx, by), (bx + 440, by + 480)], radius=12, fill=(245, 245, 240), outline=(200, 200, 190), width=2)
    draw.text((bx + 160, by + 15), "Breadboard", font=FONT_LABEL, fill=TEXT_MUTED)
    
    # RGB LED Unit (Common Cathode)
    draw.text((bx + 30, by + 50), "RGB LED (Common Cathode)", font=FONT_HEADING, fill=TEXT_DARK)
    draw.ellipse([(bx + 80, by + 90), (bx + 160, by + 170)], fill=(240, 240, 250), outline=(150, 150, 160), width=3)
    # 4 Pins of RGB LED: R, Cathode, G, B
    rgb_pins = [
        ("Red (GPIO 4)", WIRE_3V3, bx + 50, by + 230),
        ("Cathode (-)", WIRE_GND, bx + 95, by + 250),
        ("Green (GPIO 5)", WIRE_SPI_CLK, bx + 140, by + 230),
        ("Blue (GPIO 23)", WIRE_ADC, bx + 185, by + 230),
    ]
    for pname, pcolor, px, py in rgb_pins:
        draw.line([(px, by + 170), (px, py)], fill=pcolor, width=4)
        draw.ellipse([(px - 6, py - 6), (px + 6, py + 6)], fill=(255, 215, 0), outline=(150, 130, 0), width=1)
        
    draw.text((bx + 30, by + 265), "R (R 220Ω)", font=FONT_SMALL, fill=DANGER_RED)
    draw.text((bx + 85, by + 290), "GND", font=FONT_SMALL, fill=TEXT_DARK)
    draw.text((bx + 130, by + 265), "G (R 220Ω)", font=FONT_SMALL, fill=SUCCESS_GREEN)
    draw.text((bx + 180, by + 265), "B (R 220Ω)", font=FONT_SMALL, fill=PRIMARY_BLUE)
    
    # LDR Unit on right side of Breadboard
    draw.text((bx + 260, by + 50), "LDR Sensor (Rx)", font=FONT_HEADING, fill=WARNING_AMBER)
    draw.ellipse([(bx + 290, by + 100), (bx + 360, by + 170)], fill=(230, 210, 170), outline=(180, 120, 50), width=3)
    node_ldr = (bx + 325, by + 230)
    draw.ellipse([(node_ldr[0] - 8, node_ldr[1] - 8), (node_ldr[0] + 8, node_ldr[1] + 8)], fill=(255, 215, 0))
    draw.text((node_ldr[0] + 15, node_ldr[1] - 8), "GPIO 34 (ADC1)", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.text((bx + 260, by + 270), "R 10kΩ ต่อลง GND", font=FONT_SMALL, fill=TEXT_MUTED)

    # Wiring from ESP32 Right Pins:
    # GPIO 4 -> Red
    g4_x, g4_y = r_pins["G4"]
    draw.line([(g4_x, g4_y), (g4_x + 50, g4_y), (g4_x + 50, by + 230), (bx + 50, by + 230)], fill=WIRE_3V3, width=4)
    # GPIO 5 -> Green
    g5_x, g5_y = r_pins["G5"]
    draw.line([(g5_x, g5_y), (g5_x + 40, g5_y), (g5_x + 40, by + 210), (bx + 140, by + 210), (bx + 140, by + 230)], fill=WIRE_SPI_CLK, width=4)
    # GPIO 23 -> Blue
    g23_x, g23_y = r_pins["G23"]
    draw.line([(g23_x, g23_y), (g23_x + 30, g23_y), (g23_x + 30, by + 190), (bx + 185, by + 190), (bx + 185, by + 230)], fill=WIRE_ADC, width=4)
    # Cathode -> GND
    draw.line([(bx + 95, by + 250), (bx + 95, by + 340), (bx + 20, by + 340), (bx + 20, r_pins["GND"][1]), r_pins["GND"]], fill=WIRE_GND, width=4)
    
    # GPIO 34 -> LDR Node
    draw.line([l_pins["G34"], (l_pins["G34"][0] - 50, l_pins["G34"][1]), (l_pins["G34"][0] - 50, by + 420), (node_ldr[0], by + 420), node_ldr], fill=WIRE_ADC, width=4)

    # Legend
    legend_items = [
        (WIRE_3V3, "GPIO 4", "ควบคุมไฟ LED สีแดง (Red) ผ่าน R 220Ω"),
        (WIRE_SPI_CLK, "GPIO 5", "ควบคุมไฟ LED สีเขียว (Green) ผ่าน R 220Ω"),
        (WIRE_ADC, "GPIO 23", "ควบคุมไฟ LED สีน้ำเงิน (Blue) ผ่าน R 220Ω"),
        (WIRE_GND, "GND", "ขากราวด์ร่วม (Cathode ขายาวสุดของ RGB LED)"),
        (WIRE_ADC, "GPIO 34", "ต่อจุดแยกของ LDR + R 10kΩ รับสัญญาณแสงสะท้อน")
    ]
    draw_legend(draw, 1070, 200, legend_items)

    save_image(img, "circuit_05_rgb_color_sensing.png")

# ==========================================
# 6. SETUP 6: SPI OLED + POTENTIOMETER (Week 09)
# ==========================================
def gen_spi_oled_pot():
    img = Image.new("RGB", (1400, 780), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 6: จอแสดงผล SPI OLED SSD1306 (7 ขา) ร่วมกับ Potentiometer",
        "ส่งข้อมูลภาพผ่านบัสความเร็วสูง SPI2 (10 MHz) และอ่านค่าตัวต้านทานปรับค่าได้ด้วย ADC1",
        "Week 09 (SPI OLED and Kestrel UI)",
        "SPI Display + Sensor"
    )
    
    l_pins, r_pins = draw_esp32_board(draw, 220, 180)
    
    # OLED Display Unit (128x64)
    ox, oy = 580, 220
    draw.rounded_rectangle([(ox, oy), (ox + 380, oy + 260)], radius=12, fill=(30, 35, 45), outline=(100, 110, 130), width=3)
    # Screen Glass
    draw.rounded_rectangle([(ox + 40, oy + 65), (ox + 340, oy + 230)], radius=4, fill=(10, 15, 25), outline=(60, 70, 85), width=2)
    draw.text((ox + 90, oy + 95), "HELLO WORLD", font=FONT_HEADING, fill=(0, 230, 255))
    draw.text((ox + 90, oy + 135), "ID: 67030XXX", font=FONT_LABEL, fill=(255, 215, 0))
    draw.text((ox + 90, oy + 175), "ADC: 2048 (1.65V)", font=FONT_SMALL, fill=(0, 255, 120))
    
    # 7 Header Pins at top of OLED module
    oled_pins = [
        ("GND", WIRE_GND, ox + 45),
        ("VCC", WIRE_3V3, ox + 90),
        ("D0 (SCK)", WIRE_SPI_CLK, ox + 140),
        ("D1 (MOSI)", WIRE_SPI_DAT, ox + 195),
        ("RES", WIRE_SPI_RST, ox + 245),
        ("DC", WIRE_SPI_DC, ox + 295),
        ("CS", WIRE_SPI_CS, ox + 340),
    ]
    for pname, pcolor, px in oled_pins:
        draw.rectangle([(px - 6, oy - 20), (px + 6, oy)], fill=(218, 165, 32), outline=(130, 100, 20), width=1)
        draw.text((px - 14, oy + 12), pname.split()[0], font=FONT_SMALL, fill=(200, 210, 220))
        
    # Potentiometer on lower breadboard
    px, py = 660, 530
    draw.rounded_rectangle([(px, py), (px + 240, py + 190)], radius=10, fill=(245, 245, 240), outline=BORDER_COLOR, width=2)
    draw.text((px + 25, py + 15), "Potentiometer 10k (GPIO 34)", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.ellipse([(px + 80, py + 55), (px + 160, py + 135)], fill=(70, 130, 180), outline=(30, 70, 120), width=3)
    draw.line([(px + 120, py + 95), (px + 145, py + 75)], fill=(255, 255, 255), width=4)

    # Connections from ESP32:
    # 1. SCK (D0) -> GPIO 18
    g18 = r_pins["G18"]
    draw.line([g18, (g18[0] + 50, g18[1]), (g18[0] + 50, oy - 30), (ox + 140, oy - 30), (ox + 140, oy - 20)], fill=WIRE_SPI_CLK, width=3)
    # 2. MOSI (D1) -> GPIO 23
    g23 = r_pins["G23"]
    draw.line([g23, (g23[0] + 70, g23[1]), (g23[0] + 70, oy - 45), (ox + 195, oy - 45), (ox + 195, oy - 20)], fill=WIRE_SPI_DAT, width=3)
    # 3. RES -> GPIO 4
    g4 = r_pins["G4"]
    draw.line([g4, (g4[0] + 30, g4[1]), (g4[0] + 30, oy - 15), (ox + 245, oy - 15), (ox + 245, oy - 20)], fill=WIRE_SPI_RST, width=3)
    # 4. DC -> GPIO 2
    g2 = r_pins["G2"]
    draw.line([g2, (g2[0] + 90, g2[1]), (g2[0] + 90, oy - 60), (ox + 295, oy - 60), (ox + 295, oy - 20)], fill=WIRE_SPI_DC, width=3)
    # 5. CS -> GPIO 5
    g5 = r_pins["G5"]
    draw.line([g5, (g5[0] + 40, g5[1]), (g5[0] + 40, oy - 5), (ox + 340, oy - 5), (ox + 340, oy - 20)], fill=WIRE_SPI_CS, width=3)

    # Legend Table
    legend_items = [
        (WIRE_GND, "GND", "กราวด์ระบบ (OLED Pin 1)"),
        (WIRE_3V3, "3.3V (VCC)", "ไฟเลี้ยง 3.3V (OLED Pin 2)"),
        (WIRE_SPI_CLK, "GPIO 18 (D0)", "SPI2 Clock (SCK)"),
        (WIRE_SPI_DAT, "GPIO 23 (D1)", "SPI2 MOSI (Data In)"),
        (WIRE_SPI_RST, "GPIO 4 (RES)", "Hardware Reset (Active Low)"),
        (WIRE_SPI_DC, "GPIO 2 (DC)", "Data/Command Select (0=Cmd, 1=Data)"),
        (WIRE_SPI_CS, "GPIO 5 (CS)", "Chip Select (Active Low)"),
        (WIRE_ADC, "GPIO 34", "Potentiometer Wiper (ADC1_CH6)")
    ]
    draw_legend(draw, 1020, 200, legend_items)

    save_image(img, "circuit_06_spi_oled_pot.png")

# ==========================================
# 7. SETUP 7: STANDARD IOT STATION (POT + LED) - MASTER LAB!
# ==========================================
def gen_standard_iot_station():
    img = Image.new("RGB", (1400, 780), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 7: สถานี IoT มาตรฐาน (Standard IoT Station: POT 10k + LED)",
        "วงจรเซนเซอร์อนาล็อก Potentiometer (GPIO 34) ทำงานคู่กับ Actuator หลอดไฟ LED ผ่าน R 220Ω (GPIO 2)",
        "Week 02 (Lab 2.3), Week 10, Week 11, Week 12 (ใช้วงจรเดียวกัน 100%!)",
        "⭐⭐ วงจรใช้ซ้ำ 4 สัปดาห์ ⭐⭐"
    )
    
    l_pins, r_pins = draw_esp32_board(draw, 220, 180)
    
    # Large Breadboard in middle
    bx, by = 580, 220
    draw.rounded_rectangle([(bx, by), (bx + 450, by + 480)], radius=14, fill=(245, 245, 240), outline=(200, 200, 190), width=2)
    draw.text((bx + 160, by + 15), "Breadboard", font=FONT_LABEL, fill=TEXT_MUTED)
    
    # Potentiometer on Left Side of Breadboard
    draw.text((bx + 30, by + 50), "1. Sensor: POT 10kΩ", font=FONT_HEADING, fill=PRIMARY_BLUE)
    draw.ellipse([(bx + 50, by + 90), (bx + 160, by + 200)], fill=(70, 130, 180), outline=(30, 70, 120), width=3)
    draw.line([(bx + 105, by + 145), (bx + 135, by + 120)], fill=(255, 255, 255), width=4)
    # POT Pins
    p1 = (bx + 55, by + 250)
    p2 = (bx + 105, by + 250)
    p3 = (bx + 155, by + 250)
    for pt in [p1, p2, p3]:
        draw.ellipse([(pt[0] - 6, pt[1] - 6), (pt[0] + 6, pt[1] + 6)], fill=(255, 215, 0))
    draw.text((p1[0] - 15, p1[1] + 12), "3.3V", font=FONT_SMALL, fill=DANGER_RED)
    draw.text((p2[0] - 25, p2[1] + 30), "GPIO 34", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.text((p3[0] - 15, p3[1] + 12), "GND", font=FONT_SMALL, fill=TEXT_DARK)

    # LED & Resistor on Right Side of Breadboard
    draw.text((bx + 250, by + 50), "2. Actuator: LED + R 220Ω", font=FONT_HEADING, fill=DANGER_RED)
    draw.ellipse([(bx + 290, by + 95), (bx + 350, by + 155)], fill=(255, 60, 60), outline=(180, 0, 0), width=2)
    draw.polygon([(bx + 300, by + 155), (bx + 340, by + 155), (bx + 320, by + 185)], fill=(200, 0, 0))
    # Resistor
    draw.rounded_rectangle([(bx + 285, by + 220), (bx + 355, by + 250)], radius=4, fill=(210, 180, 140), outline=(120, 100, 80), width=2)
    draw.rectangle([(bx + 295, by + 220), (bx + 302, by + 250)], fill=(220, 20, 20))
    draw.rectangle([(bx + 310, by + 220), (bx + 317, by + 250)], fill=(220, 20, 20))
    draw.rectangle([(bx + 325, by + 220), (bx + 332, by + 250)], fill=(139, 69, 19))
    draw.text((bx + 270, by + 260), "R 220Ω -> Anode (+)", font=FONT_SMALL, fill=TEXT_DARK)
    draw.text((bx + 270, by + 285), "Cathode (-) -> GND", font=FONT_SMALL, fill=TEXT_MUTED)

    # Wiring Connections:
    # 1. 3.3V to POT pin 1
    draw.line([l_pins["3V3"], (l_pins["3V3"][0] - 40, l_pins["3V3"][1]), (l_pins["3V3"][0] - 40, p1[1]), p1], fill=WIRE_3V3, width=4)
    # 2. GPIO 34 to POT Wiper (pin 2)
    draw.line([l_pins["G34"], (l_pins["G34"][0] - 60, l_pins["G34"][1]), (l_pins["G34"][0] - 60, p2[1] + 15), (p2[0], p2[1] + 15), p2], fill=WIRE_ADC, width=4)
    # 3. GND to POT pin 3 & LED Cathode
    draw.line([l_pins["GND"], (l_pins["GND"][0] - 80, l_pins["GND"][1]), (l_pins["GND"][0] - 80, by + 400), (bx + 360, by + 400), (bx + 360, by + 185), (bx + 330, by + 185)], fill=WIRE_GND, width=4)
    draw.line([(p3[0], p3[1]), (p3[0], by + 400)], fill=WIRE_GND, width=3)
    # 4. GPIO 2 to Resistor 220 Ohm
    g2 = r_pins["G2"]
    draw.line([g2, (g2[0] + 40, g2[1]), (g2[0] + 40, by + 235), (bx + 285, by + 235)], fill=WIRE_PWM, width=4)
    draw.line([(bx + 355, by + 235), (bx + 380, by + 235), (bx + 380, by + 185), (bx + 310, by + 185)], fill=WIRE_PWM, width=3)

    # Legend Table
    legend_items = [
        (WIRE_3V3, "3.3V (VCC)", "ไฟเลี้ยงแอนะล็อก เข้าขา 1 ของ Potentiometer"),
        (WIRE_ADC, "GPIO 34", "ขากลาง Wiper (ส่งค่าแรงดัน 0-3.3V เข้า ADC1)"),
        (WIRE_PWM, "GPIO 2", "สัญญาณสั่งเปิด/ปิด LED (ต่อเข้า R 220Ω -> Anode)"),
        (WIRE_GND, "GND", "กราวด์ร่วม (ต่อขา 3 ของ POT และ Cathode ของ LED)")
    ]
    draw_legend(draw, 1060, 210, legend_items)

    # Master Reuse Callout Box
    draw.rounded_rectangle([(1060, 430), (1370, 690)], radius=10, fill=(235, 245, 255), outline=PRIMARY_BLUE, width=2)
    draw.text((1080, 445), "🎯 ทำไมวงจรนี้ถึงสำคัญที่สุด?", font=FONT_HEADING, fill=PRIMARY_BLUE)
    reasons = [
        ("Week 02 (Lab 2.3)", "หมุน POT เพื่อหรี่แสง LED แบบ PWM"),
        ("Week 10 (HTTP/UDP/CoAP)", "อ่านค่า POT ส่ง Telemetry และรับคำสั่งเปิดไฟ"),
        ("Week 11 (MQTT / RainMaker)", "ส่ง JSON Telemetry ขึ้น Cloud และสั่งเปิดไฟผ่านแอป"),
        ("Week 12 (Flutter Mobile)", "แอป Flutter อ่านกราฟ POT และกดสวิตช์เปิดไฟ"),
        ("⭐ คำแนะนำหน้างาน", "ต่อวงจรนี้ครั้งเดียวบน Breadboard แล้วใช้ยาวๆ ได้ถึง 4 สัปดาห์ ไม่ต้องรื้อวงจรเลย!")
    ]
    ry = 485
    for tag, desc in reasons:
        draw.text((1080, ry), f"• {tag}:", font=FONT_LABEL, fill=TEXT_DARK)
        draw.text((1095, ry + 22), desc, font=FONT_SMALL, fill=TEXT_MUTED)
        ry += 42

    save_image(img, "circuit_07_standard_iot_station.png")

if __name__ == "__main__":
    print("Generating IoT-App-2569 Circuit Diagrams...")
    gen_bare_esp32()
    gen_led_pwm()
    gen_pot_adc()
    gen_ldr_divider()
    gen_rgb_color_sensing()
    gen_spi_oled_pot()
    gen_standard_iot_station()
    print("All diagrams generated successfully!")
