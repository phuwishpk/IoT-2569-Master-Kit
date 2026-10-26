#!/usr/bin/env python3
"""
Generate high-resolution PNGs (1400x950) showing ALL 38 pins of the ESP32 board
and clean wire routing for each circuit.
Ensures universal display on GitHub, VS Code, and all image viewers.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/Users/phuwish/Downloads/fortest week1 week2/IoT-2569-Master-Kit/circuits"
ARTIFACT_DIR = "/Users/phuwish/.gemini/antigravity/brain/861fb457-eb55-478a-9ecd-4d4221975e10/circuits"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/Supplemental/Thonburi.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

FONT_TITLE = get_font(28, bold=True)
FONT_SUBTITLE = get_font(18)
FONT_HEADING = get_font(20, bold=True)
FONT_LABEL = get_font(16, bold=True)
FONT_BODY = get_font(14)
FONT_SMALL = get_font(12)
FONT_PIN = get_font(11)

# Colors
BG_COLOR = (248, 249, 250)
CARD_BG = (255, 255, 255)
BORDER_COLOR = (222, 226, 230)
PRIMARY_BLUE = (13, 110, 253)
SUCCESS_GREEN = (25, 135, 84)
DANGER_RED = (220, 53, 69)
DARK_PCB = (30, 34, 43)
RF_SHIELD = (205, 210, 220)
TEXT_DARK = (33, 37, 41)
TEXT_MUTED = (108, 117, 125)

WIRE_3V3 = (220, 53, 69)       # Red
WIRE_GND = (33, 37, 41)        # Black
WIRE_ADC = (13, 110, 253)      # Blue
WIRE_PWM = (253, 126, 20)      # Orange
WIRE_SPI_CLK = (25, 135, 84)   # Green
WIRE_SPI_DAT = (163, 112, 247) # Purple
WIRE_SPI_RST = (13, 202, 240)  # Cyan
WIRE_SPI_DC  = (214, 51, 132)  # Pink
WIRE_SPI_CS  = (253, 126, 20)  # Orange

# All 19 Left + 19 Right pins
LEFT_PINS = [
    "3V3", "EN", "VP (36)", "VN (39)", "G34 (ADC)", "G35", "G32", "G33",
    "G25", "G26", "G27", "G14", "G12", "GND", "G13", "D2", "D3", "CMD", "5V (VIN)"
]

RIGHT_PINS = [
    "GND", "G23 (MOSI)", "G22", "TX0", "RX0", "G21", "GND", "G19",
    "G18 (SCK)", "G5 (CS)", "TX2", "RX2", "G4 (RES)", "G2 (LED)", "G15", "D1", "D0", "CLK", "GND"
]

def draw_header(draw, title, subtitle, badge_text):
    draw.rounded_rectangle([(30, 20), (1370, 115)], radius=10, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((50, 32), title, font=FONT_TITLE, fill=PRIMARY_BLUE)
    draw.text((50, 72), subtitle, font=FONT_SUBTITLE, fill=TEXT_DARK)
    
    # Badge
    bbox = draw.textbbox((0, 0), badge_text, font=FONT_LABEL)
    bw = bbox[2] - bbox[0] + 24
    draw.rounded_rectangle([(1370 - bw - 30, 42), (1370 - 30, 88)], radius=6, fill=SUCCESS_GREEN)
    draw.text((1370 - bw - 18, 53), badge_text, font=FONT_LABEL, fill=(255, 255, 255))

def draw_esp32_all_pins(draw, x, y, active_left=None, active_right=None):
    active_left = active_left or {}
    active_right = active_right or {}
    
    board_w = 260
    pin_step = 32
    board_h = len(LEFT_PINS) * pin_step + 90
    
    # PCB Body
    draw.rounded_rectangle([(x, y), (x + board_w, y + board_h)], radius=14, fill=DARK_PCB, outline=(70, 75, 85), width=2)
    # RF Shield
    draw.rounded_rectangle([(x + 45, y + 40), (x + board_w - 45, y + 210)], radius=6, fill=RF_SHIELD, outline=(160, 165, 175), width=2)
    draw.text((x + 75, y + 105), "ESP-WROOM-32", font=FONT_LABEL, fill=(33, 37, 41))
    draw.text((x + 85, y + 130), "Wi-Fi & Bluetooth", font=FONT_SMALL, fill=(80, 85, 95))
    draw.text((x + 80, y + 150), "240MHz DUAL CORE", font=FONT_PIN, fill=(100, 105, 115))
    
    # USB Port
    draw.rounded_rectangle([(x + board_w//2 - 25, y + board_h - 18), (x + board_w//2 + 25, y + board_h + 8)], radius=3, fill=(180, 185, 195))
    draw.text((x + board_w//2 - 12, y + board_h - 14), "USB", font=FONT_PIN, fill=(30, 35, 45))
    
    # EN / BOOT
    draw.rectangle([(x + 20, y + board_h - 55), (x + 45, y + board_h - 35)], fill=(220, 53, 69))
    draw.text((x + 23, y + board_h - 70), "EN", font=FONT_PIN, fill=(200, 200, 200))
    draw.rectangle([(x + board_w - 45, y + board_h - 55), (x + board_w - 20, y + board_h - 35)], fill=(60, 65, 75))
    draw.text((x + board_w - 45, y + board_h - 70), "BOOT", font=FONT_PIN, fill=(200, 200, 200))
    
    # Blue LED
    draw.rectangle([(x + board_w - 55, y + board_h - 95), (x + board_w - 43, y + board_h - 85)], fill=(13, 110, 253))
    draw.text((x + board_w - 75, y + board_h - 110), "LED:D2", font=FONT_PIN, fill=(13, 202, 240))
    
    l_coords = {}
    r_coords = {}
    
    # Draw all 19 Left Pins
    pin_y_start = y + 50
    for i, pname in enumerate(LEFT_PINS):
        py = pin_y_start + i * pin_step
        p_short = pname.split()[0]
        is_active = p_short in active_left
        color = active_left.get(p_short, (255, 193, 7))
        text_color = (255, 255, 255) if is_active else (180, 185, 195)
        
        draw.ellipse([(x + 4, py - 5), (x + 14, py + 5)], fill=color, outline=(30, 30, 30), width=1)
        draw.text((x + 20, py - 7), pname, font=FONT_PIN, fill=text_color)
        l_coords[p_short] = (x + 9, py)
        
    # Draw all 19 Right Pins
    for i, pname in enumerate(RIGHT_PINS):
        py = pin_y_start + i * pin_step
        p_short = pname.split()[0]
        is_active = p_short in active_right
        color = active_right.get(p_short, (255, 193, 7))
        text_color = (255, 255, 255) if is_active else (180, 185, 195)
        
        draw.ellipse([(x + board_w - 14, py - 5), (x + board_w - 4, py + 5)], fill=color, outline=(30, 30, 30), width=1)
        bbox = draw.textbbox((0, 0), pname, font=FONT_PIN)
        tw = bbox[2] - bbox[0]
        draw.text((x + board_w - 20 - tw, py - 7), pname, font=FONT_PIN, fill=text_color)
        r_coords[p_short] = (x + board_w - 9, py)
        
    return l_coords, r_coords, board_h

# ==========================================
# 1. CIRCUIT 7: STANDARD IOT STATION (POT + LED)
# ==========================================
def render_png_circuit_7():
    img = Image.new("RGB", (1400, 850), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 7: สถานี IoT มาตรฐาน (Standard IoT Station: POT 10k + LED)",
        "แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายไปยัง Potentiometer (GPIO 34) และหลอดไฟ LED (GPIO 2)",
        "⭐ วงจรหลักใช้ซ้ำ 4 สัปดาห์ (Week 02, 10, 11, 12)"
    )
    
    act_l = {"3V3": WIRE_3V3, "G34": WIRE_ADC, "GND": WIRE_GND}
    act_r = {"G2": WIRE_PWM, "GND": WIRE_GND}
    l_coords, r_coords, bh = draw_esp32_all_pins(draw, 60, 140, act_l, act_r)
    
    # Breadboard Container
    bx, by = 420, 150
    draw.rounded_rectangle([(bx, by), (bx + 460, by + 650)], radius=12, fill=(242, 244, 248), outline=BORDER_COLOR, width=2)
    draw.text((bx + 180, by + 15), "BREADBOARD", font=FONT_HEADING, fill=(170, 175, 185))
    
    # Potentiometer 10k Card
    px, py = bx + 40, by + 50
    draw.rounded_rectangle([(px, py), (px + 170, py + 260)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.ellipse([(px + 35, py + 30), (px + 135, py + 130)], fill=PRIMARY_BLUE, outline=(10, 80, 200), width=3)
    draw.ellipse([(px + 60, py + 55), (px + 110, py + 105)], fill=(230, 235, 245))
    draw.line([(px + 85, py + 80), (px + 115, py + 50)], fill=(10, 80, 200), width=4)
    draw.text((px + 85, py + 150), "Potentiometer", font=FONT_LABEL, fill=TEXT_DARK, anchor="mm")
    draw.text((px + 85, py + 175), "10 kΩ", font=FONT_HEADING, fill=PRIMARY_BLUE, anchor="mm")
    
    pot_p1 = (px + 40, py + 230)
    pot_p2 = (px + 85, py + 230)
    pot_p3 = (px + 130, py + 230)
    for p, c, t in [(pot_p1, WIRE_3V3, "3.3V"), (pot_p2, WIRE_ADC, "G34"), (pot_p3, WIRE_GND, "GND")]:
        draw.ellipse([(p[0]-6, p[1]-6), (p[0]+6, p[1]+6)], fill=c, outline=(30,30,30), width=1)
        draw.text((p[0], p[1] + 16), t, font=FONT_PIN, fill=c, anchor="mm")
        
    # LED Card
    lx, ly = bx + 250, by + 50
    draw.rounded_rectangle([(lx, ly), (lx + 170, py + 260)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.ellipse([(lx + 50, py + 25), (lx + 120, py + 95)], fill=(235, 50, 50), outline=(180, 0, 0), width=2)
    draw.polygon([(lx + 60, py + 95), (lx + 110, py + 95), (lx + 85, py + 120)], fill=(200, 0, 0))
    draw.text((lx + 85, py + 135), "LED (Red)", font=FONT_LABEL, fill=TEXT_DARK, anchor="mm")
    
    # Resistor 220 Ohm
    draw.rounded_rectangle([(lx + 45, py + 155), (lx + 125, py + 185)], radius=3, fill=(210, 185, 150), outline=(130, 100, 70), width=1)
    draw.line([(lx + 60, py + 155), (lx + 60, py + 185)], fill=(220, 50, 50), width=3)
    draw.line([(lx + 75, py + 155), (lx + 75, py + 185)], fill=(220, 50, 50), width=3)
    draw.line([(lx + 90, py + 155), (lx + 90, py + 185)], fill=(139, 69, 19), width=3)
    draw.text((lx + 85, py + 200), "R 220Ω", font=FONT_SMALL, fill=(130, 80, 30), anchor="mm")
    
    led_anode = (lx + 65, py + 230)
    led_cathode = (lx + 105, py + 230)
    draw.ellipse([(led_anode[0]-6, led_anode[1]-6), (led_anode[0]+6, led_anode[1]+6)], fill=WIRE_PWM, outline=(30,30,30), width=1)
    draw.text((led_anode[0], led_anode[1] + 16), "Anode (+)", font=FONT_PIN, fill=WIRE_PWM, anchor="mm")
    draw.ellipse([(led_cathode[0]-6, led_cathode[1]-6), (led_cathode[0]+6, led_cathode[1]+6)], fill=WIRE_GND, outline=(30,30,30), width=1)
    draw.text((led_cathode[0], led_cathode[1] + 16), "GND (-)", font=FONT_PIN, fill=WIRE_GND, anchor="mm")

    # Wire Routings (Exact from pads):
    # 1. 3.3V
    p_3v3 = l_coords["3V3"]
    draw.line([p_3v3, (30, p_3v3[1]), (30, 730), (pot_p1[0], 730), pot_p1], fill=WIRE_3V3, width=4)
    # 2. GPIO 34
    p_g34 = l_coords["G34"]
    draw.line([p_g34, (45, p_g34[1]), (45, 755), (pot_p2[0], 755), pot_p2], fill=WIRE_ADC, width=4)
    # 3. GND Left
    p_gnd_l = l_coords["GND"]
    draw.line([p_gnd_l, (20, p_gnd_l[1]), (20, 780), (pot_p3[0], 780), pot_p3], fill=WIRE_GND, width=4)
    # 4. GPIO 2
    p_g2 = r_coords["G2"]
    draw.line([p_g2, (340, p_g2[1]), (340, 730), (led_anode[0], 730), led_anode], fill=WIRE_PWM, width=4)
    # 5. GND Right
    p_gnd_r = r_coords["GND"]
    draw.line([p_gnd_r, (360, p_gnd_r[1]), (360, 755), (led_cathode[0], 755), led_cathode], fill=WIRE_GND, width=4)

    # Explanation Card in Breadboard Bottom
    draw.rounded_rectangle([(bx + 30, by + 340), (bx + 430, by + 610)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.text((bx + 50, by + 365), "🎯 หน้าที่ของวงจรในแต่ละสัปดาห์:", font=FONT_LABEL, fill=SUCCESS_GREEN)
    draw.text((bx + 50, by + 405), "• Week 02 (Lab 2.3): หมุน POT หรี่ไฟ LED แบบ PWM", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 440), "• Week 10 (HTTP/UDP/CoAP): อ่านค่า POT และสั่งเปิดไฟผ่าน API", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 475), "• Week 11 (MQTT / RainMaker): ส่ง Telemetry ขึ้น Cloud และสั่งไฟ", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 510), "• Week 12 (Flutter App): แสดงกราฟบนมือถือ และกดปุ่มเปิดไฟ", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 555), "✨ สรุป: ต่อครั้งเดียว ใช้ได้ถึง 4 สัปดาห์ ไม่ต้องรื้อวงจร!", font=FONT_LABEL, fill=PRIMARY_BLUE)

    # Right Legend Card
    rx, ry = 920, 150
    draw.rounded_rectangle([(rx, ry), (rx + 440, ry + 650)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((rx + 25, ry + 25), "📋 ตารางสรุปการต่อสายทุกเส้น", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    rows = [
        ("ขา 3V3 (ซ้ายแถว 1)", "ต่อเข้า ขา 1 ของ POT (สายสีแดง)", WIRE_3V3),
        ("ขา G34 (ซ้ายแถว 5)", "ต่อเข้า ขากลาง Wiper ของ POT (สายสีน้ำเงิน)", WIRE_ADC),
        ("ขา GND (ซ้ายแถว 14)", "ต่อเข้า ขา 3 ของ POT (สายสีดำ)", WIRE_GND),
        ("ขา G2 (ขวาแถว 14)", "ต่อเข้า R 220Ω > Anode (+) ของ LED (สายสีส้ม)", WIRE_PWM),
        ("ขา GND (ขวาแถว 1)", "ต่อเข้า Cathode (-) ของ LED (สายสีดำ)", WIRE_GND)
    ]
    
    for i, (p_title, p_desc, w_col) in enumerate(rows):
        cy = ry + 75 + i * 65
        draw.rounded_rectangle([(rx + 20, cy), (rx + 420, cy + 55)], radius=6, fill=(248, 249, 250), outline=BORDER_COLOR)
        draw.line([(rx + 35, cy + 27), (rx + 55, cy + 27)], fill=w_col, width=5)
        draw.text((rx + 65, cy + 12), p_title, font=FONT_LABEL, fill=w_col)
        draw.text((rx + 65, cy + 32), p_desc, font=FONT_SMALL, fill=TEXT_DARK)

    # Box at bottom right
    draw.rounded_rectangle([(rx + 20, ry + 420), (rx + 420, ry + 620)], radius=8, fill=(209, 231, 221), outline=(163, 207, 187))
    draw.text((rx + 35, ry + 440), "💡 คำแนะนำหน้างานให้เสร็จไว:", font=FONT_LABEL, fill=(15, 81, 50))
    draw.text((rx + 35, ry + 475), "1. เสียบบอร์ด ESP32 ค่อมร่องกลาง Breadboard", font=FONT_BODY, fill=(15, 81, 50))
    draw.text((rx + 35, ry + 505), "2. เสียบ POT 10k และ LED ตามผังนี้", font=FONT_BODY, fill=(15, 81, 50))
    draw.text((rx + 35, ry + 535), "3. เชื่อมสายไฟ 5 เส้นตามสีที่ระบุ", font=FONT_BODY, fill=(15, 81, 50))
    draw.text((rx + 35, ry + 570), "4. ใช้บอร์ดนี้รันได้ทั้ง Week 02, 10, 11, 12 ทันที!", font=FONT_LABEL, fill=(15, 81, 50))

    img.save(os.path.join(OUTPUT_DIR, "circuit_07_standard_iot_station.png"), "PNG")
    img.save(os.path.join(ARTIFACT_DIR, "circuit_07_standard_iot_station.png"), "PNG")
    print("Rendered PNG: circuit_07_standard_iot_station.png")

# Execute
render_png_circuit_7()

# ==========================================
# 6. CIRCUIT 6: SPI OLED (7 PINS) + POTENTIOMETER (Week 09)
# ==========================================
def render_png_circuit_6():
    img = Image.new("RGB", (1400, 850), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 6: จอแสดงผลกราฟิก SPI OLED SSD1306 (7 ขา) ร่วมกับ Potentiometer",
        "แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายบัส SPI2 (10 MHz) 5 ขา + ไฟเลี้ยง 2 ขา + Potentiometer บนขา GPIO 34",
        "📌 ใช้ใน: Week 09 (SPI OLED and Kestrel UI)"
    )
    
    act_l = {"3V3": WIRE_3V3, "G34": WIRE_ADC, "GND": WIRE_GND}
    act_r = {
        "G23": WIRE_SPI_DAT, "G18": WIRE_SPI_CLK, "G5": WIRE_SPI_CS,
        "G4": WIRE_SPI_RST, "G2": WIRE_SPI_DC, "GND": WIRE_GND
    }
    l_coords, r_coords, bh = draw_esp32_all_pins(draw, 60, 140, act_l, act_r)
    
    bx, by = 420, 150
    draw.rounded_rectangle([(bx, by), (bx + 460, by + 650)], radius=12, fill=(242, 244, 248), outline=BORDER_COLOR, width=2)
    draw.text((bx + 180, by + 15), "BREADBOARD", font=FONT_HEADING, fill=(170, 175, 185))
    
    # OLED Module (128x64)
    ox, oy = bx + 30, by + 45
    draw.rounded_rectangle([(ox, oy), (ox + 400, oy + 260)], radius=10, fill=DARK_PCB, outline=(70, 75, 85), width=2)
    # Glass Screen
    draw.rounded_rectangle([(ox + 35, oy + 70), (ox + 365, oy + 235)], radius=4, fill=(5, 8, 17), outline=(50, 60, 75))
    draw.text((ox + 60, oy + 105), "HELLO WORLD", font=FONT_HEADING, fill=(13, 202, 240))
    draw.text((ox + 60, oy + 145), "ID: 67030XXX", font=FONT_LABEL, fill=(255, 193, 7))
    draw.text((ox + 60, oy + 185), "ADC: 2048 (1.65V)", font=FONT_BODY, fill=(32, 201, 151))
    
    # 7 OLED Pins at Top
    oled_pins_info = [
        ("GND", WIRE_GND, ox + 45),
        ("VCC", WIRE_3V3, ox + 95),
        ("D0", WIRE_SPI_CLK, ox + 150),
        ("D1", WIRE_SPI_DAT, ox + 205),
        ("RES", WIRE_SPI_RST, ox + 260),
        ("DC", WIRE_SPI_DC, ox + 310),
        ("CS", WIRE_SPI_CS, ox + 360),
    ]
    oled_coords = {}
    for pname, pcolor, px in oled_pins_info:
        draw.ellipse([(px - 5, oy + 30), (px + 5, oy + 40)], fill=pcolor, outline=(30,30,30), width=1)
        draw.text((px, oy + 15), pname, font=FONT_PIN, fill=(200, 205, 215), anchor="mm")
        oled_coords[pname] = (px, oy + 35)

    # Potentiometer Box at Bottom of Breadboard
    px, py = bx + 120, by + 340
    draw.rounded_rectangle([(px, py), (px + 220, py + 260)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.ellipse([(px + 60, py + 30), (px + 160, py + 130)], fill=PRIMARY_BLUE, outline=(10, 80, 200), width=3)
    draw.ellipse([(px + 85, py + 55), (px + 135, py + 105)], fill=(230, 235, 245))
    draw.text((px + 110, py + 155), "Potentiometer 10 kΩ", font=FONT_LABEL, fill=TEXT_DARK, anchor="mm")
    draw.text((px + 110, py + 180), "หมุนเทียบ Kestrel UI กับ OLED", font=FONT_SMALL, fill=TEXT_MUTED, anchor="mm")
    
    pot_p1 = (px + 60, py + 225)
    pot_p2 = (px + 110, py + 225)
    pot_p3 = (px + 160, py + 225)
    for p, c, t in [(pot_p1, WIRE_3V3, "3.3V"), (pot_p2, WIRE_ADC, "G34"), (pot_p3, WIRE_GND, "GND")]:
        draw.ellipse([(p[0]-6, p[1]-6), (p[0]+6, p[1]+6)], fill=c, outline=(30,30,30), width=1)
        draw.text((p[0], p[1] + 16), t, font=FONT_PIN, fill=c, anchor="mm")

    # Wire Routings
    # 1. VCC (3.3V) -> OLED Pin 2
    draw.line([l_coords["3V3"], (35, l_coords["3V3"][1]), (35, 125), (oled_coords["VCC"][0], 125), oled_coords["VCC"]], fill=WIRE_3V3, width=3)
    # 2. D0 (SCK) -> GPIO 18
    draw.line([r_coords["G18"], (335, r_coords["G18"][1]), (335, 135), (oled_coords["D0"][0], 135), oled_coords["D0"]], fill=WIRE_SPI_CLK, width=3)
    # 3. D1 (MOSI) -> GPIO 23
    draw.line([r_coords["G23"], (350, r_coords["G23"][1]), (350, 145), (oled_coords["D1"][0], 145), oled_coords["D1"]], fill=WIRE_SPI_DAT, width=3)
    # 4. RES -> GPIO 4
    draw.line([r_coords["G4"], (365, r_coords["G4"][1]), (365, 155), (oled_coords["RES"][0], 155), oled_coords["RES"]], fill=WIRE_SPI_RST, width=3)
    # 5. DC -> GPIO 2
    draw.line([r_coords["G2"], (380, r_coords["G2"][1]), (380, 165), (oled_coords["DC"][0], 165), oled_coords["DC"]], fill=WIRE_SPI_DC, width=3)
    # 6. CS -> GPIO 5
    draw.line([r_coords["G5"], (370, r_coords["G5"][1]), (370, 175), (oled_coords["CS"][0], 175), oled_coords["CS"]], fill=WIRE_SPI_CS, width=3)
    # 7. GND -> Right GND
    draw.line([r_coords["GND"], (320, r_coords["GND"][1]), (320, 115), (oled_coords["GND"][0], 115), oled_coords["GND"]], fill=WIRE_GND, width=3)
    
    # POT Wires
    draw.line([l_coords["G34"], (45, l_coords["G34"][1]), (45, 755), (pot_p2[0], 755), pot_p2], fill=WIRE_ADC, width=4)
    draw.line([(35, 730), (pot_p1[0], 730), pot_p1], fill=WIRE_3V3, width=3)
    draw.line([l_coords["GND"], (20, l_coords["GND"][1]), (20, 780), (pot_p3[0], 780), pot_p3], fill=WIRE_GND, width=3)

    # Right Legend Card
    rx, ry = 920, 150
    draw.rounded_rectangle([(rx, ry), (rx + 440, ry + 650)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((rx + 25, ry + 25), "📋 ตารางสรุปการต่อสาย OLED 7 ขา", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    oled_table = [
        ("1. GND", "-> GND บนบอร์ด (กราวด์)", WIRE_GND),
        ("2. VCC", "-> 3.3V (ไฟเลี้ยงจอภาพ ห้ามต่อ 5V)", WIRE_3V3),
        ("3. D0 (SCK)", "-> GPIO 18 (SPI2 Clock)", WIRE_SPI_CLK),
        ("4. D1 (MOSI)", "-> GPIO 23 (SPI2 Data Out)", WIRE_SPI_DAT),
        ("5. RES (Reset)", "-> GPIO 4 (Active Low)", WIRE_SPI_RST),
        ("6. DC (Data/Cmd)", "-> GPIO 2 (0=Command, 1=Data)", WIRE_SPI_DC),
        ("7. CS (Chip Sel)", "-> GPIO 5 (Active Low)", WIRE_SPI_CS),
        ("POT Wiper", "-> GPIO 34 (ADC1 Channel 6)", WIRE_ADC)
    ]
    for i, (p_title, p_desc, w_col) in enumerate(oled_table):
        cy = ry + 65 + i * 44
        draw.rounded_rectangle([(rx + 20, cy), (rx + 420, cy + 38)], radius=5, fill=(248, 249, 250), outline=BORDER_COLOR)
        draw.line([(rx + 30, cy + 19), (rx + 45, cy + 19)], fill=w_col, width=4)
        draw.text((rx + 55, cy + 10), p_title, font=FONT_LABEL, fill=w_col)
        draw.text((rx + 180, cy + 11), p_desc, font=FONT_SMALL, fill=TEXT_DARK)

    # Fault Clinic Box
    draw.rounded_rectangle([(rx + 20, ry + 440), (rx + 420, ry + 620)], radius=8, fill=(255, 243, 205), outline=(255, 236, 181))
    draw.text((rx + 35, ry + 455), "⚠️ การแก้ปัญหาหน้างาน (Fault Clinic):", font=FONT_LABEL, fill=(102, 77, 3))
    draw.text((rx + 35, ry + 485), "• จอมืดสนิท: ตรวจสอบสาย SCK (GPIO 18) หลุด", font=FONT_BODY, fill=(102, 77, 3))
    draw.text((rx + 35, ry + 515), "• จอขึ้นเส้นขยะ: สลับสาย DC (GPIO 2) กับ RES (GPIO 4)", font=FONT_BODY, fill=(102, 77, 3))
    draw.text((rx + 35, ry + 545), "• บัฟเฟอร์ค้าง: กดปุ่ม EN บนตัวบอร์ดเพื่อรีเซ็ต", font=FONT_BODY, fill=(102, 77, 3))
    draw.text((rx + 35, ry + 580), "📷 ถ่ายรูปจอจริง 2 รูปให้เห็นชื่อ/รหัสชัดเจน", font=FONT_LABEL, fill=PRIMARY_BLUE)

    img.save(os.path.join(OUTPUT_DIR, "circuit_06_spi_oled_pot.png"), "PNG")
    img.save(os.path.join(ARTIFACT_DIR, "circuit_06_spi_oled_pot.png"), "PNG")
    print("Rendered PNG: circuit_06_spi_oled_pot.png")

render_png_circuit_6()
