#!/usr/bin/env python3
"""
Generate complete, professional PNG diagrams showing ALL 38 pins of the ESP32
for all 7 circuits with clear color wire routing, breadboard components, and Thai annotations.
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

FONT_TITLE = get_font(26, bold=True)
FONT_SUBTITLE = get_font(17)
FONT_HEADING = get_font(19, bold=True)
FONT_LABEL = get_font(15, bold=True)
FONT_BODY = get_font(13)
FONT_SMALL = get_font(11)
FONT_PIN = get_font(10)

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
# 1. CIRCUIT 1: BARE ESP32
# ==========================================
def render_png_circuit_1():
    img = Image.new("RGB", (1400, 850), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 1: ผังขาบอร์ด ESP32 ฉบับสมบูรณ์ (Full 38-Pin Master Reference)",
        "แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมคำอธิบายขาสำคัญ, ปุ่ม EN/BOOT, เสาอากาศ Wi-Fi และพอร์ต USB",
        "📌 ไม่ต้องต่อ Breadboard (Week 01, 05, 06, 07, 08)"
    )
    
    act_l = {"3V3": WIRE_3V3, "EN": (255, 193, 7), "5V": (255, 100, 100), "GND": WIRE_GND}
    act_r = {"TX0": (13, 202, 240), "RX0": (13, 202, 240), "G2": WIRE_PWM, "GND": WIRE_GND}
    l_coords, r_coords, bh = draw_esp32_all_pins(draw, 70, 140, act_l, act_r)
    
    # Middle Box: USB Cable & Computer Connection
    cx, cy = 400, 150
    draw.rounded_rectangle([(cx, cy), (cx + 460, cy + 650)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((cx + 30, cy + 30), "💻 การเชื่อมต่อกับคอมพิวเตอร์ (Host PC)", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    # Draw Laptop Outline
    lx, ly = cx + 80, cy + 90
    draw.rounded_rectangle([(lx, ly), (lx + 300, ly + 180)], radius=8, fill=(40, 44, 52), outline=(90, 95, 105), width=2)
    draw.rectangle([(lx + 15, ly + 15), (lx + 285, ly + 165)], fill=(15, 23, 42))
    draw.text((lx + 30, ly + 40), "$ idf.py -p /dev/ttyUSB0 flash monitor", font=FONT_SMALL, fill=(56, 189, 248))
    draw.text((lx + 30, ly + 70), "App 'Week01_Intro' hash: a1b2c3d...", font=FONT_SMALL, fill=(74, 222, 128))
    draw.text((lx + 30, ly + 100), "Connecting to Wi-Fi SSID: IoT-Lab...", font=FONT_SMALL, fill=(250, 204, 21))
    draw.text((lx + 30, ly + 130), "FreeRTOS Heap Free: 298,420 bytes", font=FONT_SMALL, fill=(244, 114, 182))
    # Laptop Base
    draw.polygon([(lx - 25, ly + 195), (lx + 325, ly + 195), (lx + 300, ly + 180), (lx, ly + 180)], fill=(100, 105, 115))
    
    # USB Cable line from laptop to ESP32 USB port
    usb_port_pos = (70 + 130, 140 + bh)
    draw.line([(lx + 150, ly + 195), (lx + 150, 770), (usb_port_pos[0], 770), usb_port_pos], fill=(50, 50, 50), width=6)
    draw.text((lx + 40, 745), "สาย USB Type-C / Micro-USB", font=FONT_LABEL, fill=(100, 105, 115))
    
    # Middle Bottom Info
    draw.rounded_rectangle([(cx + 30, cy + 340), (cx + 430, cy + 620)], radius=8, fill=(241, 245, 249), outline=BORDER_COLOR)
    draw.text((cx + 45, cy + 360), "⚡ ฟังก์ชันที่รันบนบอร์ดเปล่า (No Breadboard):", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.text((cx + 45, cy + 395), "• Week 01: FreeRTOS Multi-Tasking & Blink บนบอร์ด", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((cx + 45, cy + 430), "• Week 05: Wi-Fi Scanner ค้นหา AP รอบตัว และดู RSSI", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((cx + 45, cy + 465), "• Week 06: SoftAP โหมดกระจาย Wi-Fi + วัด TCP Throughput", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((cx + 45, cy + 500), "• Week 07: BLE Provisioning ปล่อยบลูทูธตั้งค่า Wi-Fi", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((cx + 45, cy + 535), "• Week 08: ส่ง HTTP GET / HTTPS JSON ขึ้น Cloud", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((cx + 45, cy + 575), "✨ เสียบสาย USB เส้นเดียว รันผ่านทั้งหมด 5 สัปดาห์!", font=FONT_LABEL, fill=SUCCESS_GREEN)
    
    # Right Box: Pinout Category Table
    rx, ry = 890, 150
    draw.rounded_rectangle([(rx, ry), (rx + 470, ry + 650)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((rx + 25, ry + 25), "📋 สรุปคุณสมบัติขา ESP32 (ครบ 38 ขา)", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    specs = [
        ("ADC1 (ใช้คู่กับ Wi-Fi ได้)", "GPIO 32, 33, 34, 35, 36 (VP), 39 (VN)", (13, 110, 253)),
        ("ADC2 (ห้ามใช้ตอนเปิด Wi-Fi)", "GPIO 0, 2, 4, 12, 13, 14, 15, 25, 26, 27", (220, 53, 69)),
        ("Strapping Pins (มีผลตอน Boot)", "GPIO 0 (BOOT), 2 (LED), 5, 12, 15", (255, 159, 28)),
        ("Flash SPI Pins (ห้ามต่อภายนอก)", "GPIO 6, 7, 8, 9, 10, 11 (CLK, D0, D1, D2, D3, CMD)", (108, 117, 125)),
        ("Hardware UART0 (USB Serial)", "GPIO 1 (TX0), GPIO 3 (RX0) เชื่อมชิป USB", (25, 135, 84)),
        ("DAC (แปลง Digital เป็น Analog)", "GPIO 25 (DAC1), GPIO 26 (DAC2) แรงดัน 0-3.3V", (111, 66, 193)),
    ]
    for i, (title_p, desc_p, col_p) in enumerate(specs):
        sy = ry + 65 + i * 90
        draw.rounded_rectangle([(rx + 20, sy), (rx + 450, sy + 78)], radius=6, fill=(248, 249, 250), outline=BORDER_COLOR)
        draw.line([(rx + 30, sy + 20), (rx + 30, sy + 60)], fill=col_p, width=4)
        draw.text((rx + 45, sy + 15), title_p, font=FONT_LABEL, fill=col_p)
        draw.text((rx + 45, sy + 42), desc_p, font=FONT_SMALL, fill=TEXT_DARK)
        
    img.save(os.path.join(OUTPUT_DIR, "circuit_01_bare_esp32.png"), "PNG")
    img.save(os.path.join(ARTIFACT_DIR, "circuit_01_bare_esp32.png"), "PNG")
    print("Rendered PNG: circuit_01_bare_esp32.png")

# ==========================================
# 2. CIRCUIT 2: LED ON GPIO 2 (Week 02 Lab 2.1)
# ==========================================
def render_png_circuit_2():
    img = Image.new("RGB", (1400, 850), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 2: วงจรหลอดไฟ LED หรี่แสง PWM (GPIO 2)",
        "แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายขา GPIO 2 ผ่านตัวต้านทาน 220Ω เข้าหลอดไฟ LED และต่อลงกราวด์ GND",
        "📌 ใช้ใน: Week 02 (Lab 2.1: LED Breathing PWM)"
    )
    
    act_l = {}
    act_r = {"G2": WIRE_PWM, "GND": WIRE_GND}
    l_coords, r_coords, bh = draw_esp32_all_pins(draw, 70, 140, act_l, act_r)
    
    # Breadboard Container
    bx, by = 420, 150
    draw.rounded_rectangle([(bx, by), (bx + 460, by + 650)], radius=12, fill=(242, 244, 248), outline=BORDER_COLOR, width=2)
    draw.text((bx + 180, by + 15), "BREADBOARD", font=FONT_HEADING, fill=(170, 175, 185))
    
    # LED Component Box
    lx, ly = bx + 120, by + 70
    draw.rounded_rectangle([(lx, ly), (lx + 220, ly + 300)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.ellipse([(lx + 75, ly + 30), (lx + 145, ly + 100)], fill=(235, 50, 50), outline=(180, 0, 0), width=2)
    draw.polygon([(lx + 85, ly + 100), (lx + 135, ly + 100), (lx + 110, ly + 125)], fill=(200, 0, 0))
    draw.text((lx + 110, ly + 145), "LED (Red 5mm)", font=FONT_LABEL, fill=TEXT_DARK, anchor="mm")
    
    # Resistor 220 Ohm
    draw.rounded_rectangle([(lx + 70, ly + 175), (lx + 150, ly + 205)], radius=3, fill=(210, 185, 150), outline=(130, 100, 70), width=1)
    draw.line([(lx + 85, ly + 175), (lx + 85, ly + 205)], fill=(220, 50, 50), width=3)
    draw.line([(lx + 100, ly + 175), (lx + 100, ly + 205)], fill=(220, 50, 50), width=3)
    draw.line([(lx + 115, ly + 175), (lx + 115, ly + 205)], fill=(139, 69, 19), width=3)
    draw.text((lx + 110, ly + 222), "R 220Ω (Red-Red-Brown)", font=FONT_SMALL, fill=(130, 80, 30), anchor="mm")
    
    led_anode = (lx + 85, ly + 265)
    led_cathode = (lx + 135, ly + 265)
    draw.ellipse([(led_anode[0]-6, led_anode[1]-6), (led_anode[0]+6, led_anode[1]+6)], fill=WIRE_PWM, outline=(30,30,30), width=1)
    draw.text((led_anode[0], led_anode[1] + 16), "Anode (+)", font=FONT_PIN, fill=WIRE_PWM, anchor="mm")
    draw.ellipse([(led_cathode[0]-6, led_cathode[1]-6), (led_cathode[0]+6, led_cathode[1]+6)], fill=WIRE_GND, outline=(30,30,30), width=1)
    draw.text((led_cathode[0], led_cathode[1] + 16), "GND (-)", font=FONT_PIN, fill=WIRE_GND, anchor="mm")
    
    # Wire Routing
    p_g2 = r_coords["G2"]
    draw.line([p_g2, (360, p_g2[1]), (360, 680), (led_anode[0], 680), led_anode], fill=WIRE_PWM, width=4)
    p_gnd_r = r_coords["GND"]
    draw.line([p_gnd_r, (380, p_gnd_r[1]), (380, 710), (led_cathode[0], 710), led_cathode], fill=WIRE_GND, width=4)
    
    # Explanation Bottom
    draw.rounded_rectangle([(bx + 30, by + 400), (bx + 430, by + 620)], radius=8, fill=CARD_BG, outline=BORDER_COLOR)
    draw.text((bx + 45, by + 420), "💡 คำแนะนำและหลักการทำงาน:", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.text((bx + 45, by + 455), "• ใช้ Hardware LEDC Timer ของ ESP32 ในการสร้าง PWM", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 45, by + 490), "• ความถี่ 5,000 Hz, ความละเอียด 13-bit (0-8191)", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 45, by + 525), "• ห้ามต่อตรงโดยไม่มีตัวต้านทาน 220Ω เพราะกระแสจะเกินพิกัด", font=FONT_BODY, fill=DANGER_RED)
    draw.text((bx + 45, by + 560), "⭐ หรือหากไม่มีอุปกรณ์ภายนอก สามารถดูหลอด Blue LED บนบอร์ดได้", font=FONT_LABEL, fill=SUCCESS_GREEN)
    
    # Right Box
    rx, ry = 920, 150
    draw.rounded_rectangle([(rx, ry), (rx + 440, ry + 650)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((rx + 25, ry + 25), "📋 ตารางการต่อสายไฟวงจร LED", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    rows = [
        ("ขา G2 (ESP32 ขวาแถว 14)", "ต่อเข้า R 220Ω > ขาขายาว Anode (+) ของ LED", WIRE_PWM),
        ("ขา GND (ESP32 ขวาแถว 1)", "ต่อเข้า ขาขาสั้น Cathode (-) ของ LED", WIRE_GND)
    ]
    for i, (rt, rd, rc) in enumerate(rows):
        cy = ry + 80 + i * 80
        draw.rounded_rectangle([(rx + 20, cy), (rx + 420, cy + 65)], radius=6, fill=(248, 249, 250), outline=BORDER_COLOR)
        draw.line([(rx + 35, cy + 32), (rx + 55, cy + 32)], fill=rc, width=5)
        draw.text((rx + 65, cy + 15), rt, font=FONT_LABEL, fill=rc)
        draw.text((rx + 65, cy + 38), rd, font=FONT_SMALL, fill=TEXT_DARK)
        
    img.save(os.path.join(OUTPUT_DIR, "circuit_02_led_pwm.png"), "PNG")
    img.save(os.path.join(ARTIFACT_DIR, "circuit_02_led_pwm.png"), "PNG")
    print("Rendered PNG: circuit_02_led_pwm.png")

# ==========================================
# 3. CIRCUIT 3: POTENTIOMETER ON GPIO 34 (Week 02 Lab 2.2)
# ==========================================
def render_png_circuit_3():
    img = Image.new("RGB", (1400, 850), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 3: วงจรตัวต้านทานปรับค่าได้ (Potentiometer 10k บนขา GPIO 34)",
        "แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายไฟ 3.3V, GND และขากลาง (Wiper) เข้าสู่ภาค ADC1_CH6 (GPIO 34)",
        "📌 ใช้ใน: Week 02 (Lab 2.2: วัดมุม 0°-180°) & Week 08 (Lab 8.3: Stream ADC)"
    )
    
    act_l = {"3V3": WIRE_3V3, "G34": WIRE_ADC, "GND": WIRE_GND}
    l_coords, r_coords, bh = draw_esp32_all_pins(draw, 70, 140, act_l, {})
    
    bx, by = 420, 150
    draw.rounded_rectangle([(bx, by), (bx + 460, by + 650)], radius=12, fill=(242, 244, 248), outline=BORDER_COLOR, width=2)
    draw.text((bx + 180, by + 15), "BREADBOARD", font=FONT_HEADING, fill=(170, 175, 185))
    
    px, py = bx + 120, by + 80
    draw.rounded_rectangle([(px, py), (px + 220, py + 280)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.ellipse([(px + 60, py + 30), (px + 160, py + 130)], fill=PRIMARY_BLUE, outline=(10, 80, 200), width=3)
    draw.ellipse([(px + 85, py + 55), (px + 135, py + 105)], fill=(230, 235, 245))
    draw.line([(px + 110, py + 80), (px + 140, py + 50)], fill=(10, 80, 200), width=4)
    draw.text((px + 110, py + 155), "Potentiometer 10 kΩ", font=FONT_LABEL, fill=TEXT_DARK, anchor="mm")
    draw.text((px + 110, py + 180), "หมุนปรับมุม 0° ถึง 180°", font=FONT_SMALL, fill=TEXT_MUTED, anchor="mm")
    
    pot_p1 = (px + 50, py + 240)
    pot_p2 = (px + 110, py + 240)
    pot_p3 = (px + 170, py + 240)
    for p, c, t in [(pot_p1, WIRE_3V3, "3.3V"), (pot_p2, WIRE_ADC, "G34"), (pot_p3, WIRE_GND, "GND")]:
        draw.ellipse([(p[0]-6, p[1]-6), (p[0]+6, p[1]+6)], fill=c, outline=(30,30,30), width=1)
        draw.text((p[0], p[1] + 16), t, font=FONT_PIN, fill=c, anchor="mm")
        
    # Wire routing
    draw.line([l_coords["3V3"], (30, l_coords["3V3"][1]), (30, 730), (pot_p1[0], 730), pot_p1], fill=WIRE_3V3, width=4)
    draw.line([l_coords["G34"], (45, l_coords["G34"][1]), (45, 755), (pot_p2[0], 755), pot_p2], fill=WIRE_ADC, width=4)
    draw.line([l_coords["GND"], (20, l_coords["GND"][1]), (20, 780), (pot_p3[0], 780), pot_p3], fill=WIRE_GND, width=4)
    
    # Right Box
    rx, ry = 920, 150
    draw.rounded_rectangle([(rx, ry), (rx + 440, ry + 650)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((rx + 25, ry + 25), "📋 ตารางสรุปการต่อสาย Potentiometer", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    rows = [
        ("ขา 3V3 (ESP32 ซ้ายแถว 1)", "ต่อเข้า ขา 1 ของ POT (สายสีแดง)", WIRE_3V3),
        ("ขา G34 (ESP32 ซ้ายแถว 5)", "ต่อเข้า ขากลาง Wiper ของ POT (สายสีน้ำเงิน)", WIRE_ADC),
        ("ขา GND (ESP32 ซ้ายแถว 14)", "ต่อเข้า ขา 3 ของ POT (สายสีดำ)", WIRE_GND),
    ]
    for i, (rt, rd, rc) in enumerate(rows):
        cy = ry + 80 + i * 80
        draw.rounded_rectangle([(rx + 20, cy), (rx + 420, cy + 65)], radius=6, fill=(248, 249, 250), outline=BORDER_COLOR)
        draw.line([(rx + 35, cy + 32), (rx + 55, cy + 32)], fill=rc, width=5)
        draw.text((rx + 65, cy + 15), rt, font=FONT_LABEL, fill=rc)
        draw.text((rx + 65, cy + 38), rd, font=FONT_SMALL, fill=TEXT_DARK)
        
    draw.rounded_rectangle([(rx + 20, ry + 360), (rx + 420, ry + 620)], radius=8, fill=(255, 243, 205), outline=(255, 236, 181))
    draw.text((rx + 35, ry + 385), "⚠️ ข้อควรระวังเรื่องแรงดันไฟฟ้า:", font=FONT_LABEL, fill=(102, 77, 3))
    draw.text((rx + 35, ry + 420), "• ห้ามนำขาไฟเลี้ยงของ POT ไปต่อเข้า 5V / VIN เด็ดขาด!", font=FONT_BODY, fill=(102, 77, 3))
    draw.text((rx + 35, ry + 455), "• ภาค ADC ของ ESP32 ทนแรงดันสูงสุด 3.3V เท่านั้น", font=FONT_BODY, fill=(102, 77, 3))
    draw.text((rx + 35, ry + 490), "• หากต่อ 5V อาจทำให้วงจรภายในพังเสียหายถาวรได้", font=FONT_BODY, fill=DANGER_RED)
    draw.text((rx + 35, ry + 530), "• ช่วงค่าดิจิทัลที่อ่านได้: 0 ถึง 4095 (12-bit ADC)", font=FONT_LABEL, fill=PRIMARY_BLUE)
    
    img.save(os.path.join(OUTPUT_DIR, "circuit_03_pot_adc.png"), "PNG")
    img.save(os.path.join(ARTIFACT_DIR, "circuit_03_pot_adc.png"), "PNG")
    print("Rendered PNG: circuit_03_pot_adc.png")

# ==========================================
# 4. CIRCUIT 4: LDR VOLTAGE DIVIDER (Week 03)
# ==========================================
def render_png_circuit_4():
    img = Image.new("RGB", (1400, 850), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 4: วงจรแบ่งแรงดันเซนเซอร์แสง LDR 10k + LED (Voltage Divider)",
        "แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายวงจร Voltage Divider (LDR + R 10kΩ) เข้า GPIO 34 และ LED บน GPIO 2",
        "📌 ใช้ใน: Week 03 (LDR Lux Calibration & Low Power)"
    )
    
    act_l = {"3V3": WIRE_3V3, "G34": WIRE_ADC, "GND": WIRE_GND}
    act_r = {"G2": WIRE_PWM, "GND": WIRE_GND}
    l_coords, r_coords, bh = draw_esp32_all_pins(draw, 70, 140, act_l, act_r)
    
    bx, by = 420, 150
    draw.rounded_rectangle([(bx, by), (bx + 460, by + 650)], radius=12, fill=(242, 244, 248), outline=BORDER_COLOR, width=2)
    draw.text((bx + 180, by + 15), "BREADBOARD", font=FONT_HEADING, fill=(170, 175, 185))
    
    # LDR Divider Card
    px, py = bx + 40, by + 60
    draw.rounded_rectangle([(px, py), (px + 170, py + 260)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    # LDR Symbol
    draw.ellipse([(px + 55, py + 25), (px + 115, py + 85)], fill=(255, 235, 150), outline=(220, 180, 50), width=2)
    draw.line([(px + 30, py + 20), (px + 50, py + 35)], fill=(230, 120, 0), width=2)
    draw.line([(px + 35, py + 10), (px + 55, py + 25)], fill=(230, 120, 0), width=2)
    draw.text((px + 85, py + 100), "LDR (Photoresistor)", font=FONT_SMALL, fill=TEXT_DARK, anchor="mm")
    
    # R 10k Resistor
    draw.rounded_rectangle([(px + 45, py + 130), (px + 125, py + 160)], radius=3, fill=(210, 185, 150), outline=(130, 100, 70), width=1)
    draw.line([(px + 60, py + 130), (px + 60, py + 160)], fill=(139, 69, 19), width=3) # Brown
    draw.line([(px + 75, py + 130), (px + 75, py + 160)], fill=(0, 0, 0), width=3)       # Black
    draw.line([(px + 90, py + 130), (px + 90, py + 160)], fill=(255, 140, 0), width=3)   # Orange
    draw.text((px + 85, py + 180), "R 10 kΩ (Divider)", font=FONT_SMALL, fill=(130, 80, 30), anchor="mm")
    
    ldr_p1 = (px + 45, py + 225)
    ldr_mid = (px + 85, py + 225)
    ldr_p2 = (px + 125, py + 225)
    for p, c, t in [(ldr_p1, WIRE_3V3, "3.3V"), (ldr_mid, WIRE_ADC, "G34"), (ldr_p2, WIRE_GND, "GND")]:
        draw.ellipse([(p[0]-6, p[1]-6), (p[0]+6, p[1]+6)], fill=c, outline=(30,30,30), width=1)
        draw.text((p[0], p[1] + 16), t, font=FONT_PIN, fill=c, anchor="mm")
        
    # LED Card
    lx, ly = bx + 250, by + 60
    draw.rounded_rectangle([(lx, ly), (lx + 170, py + 260)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.ellipse([(lx + 50, py + 25), (lx + 120, py + 95)], fill=(235, 50, 50), outline=(180, 0, 0), width=2)
    draw.polygon([(lx + 60, py + 95), (lx + 110, py + 95), (lx + 85, py + 120)], fill=(200, 0, 0))
    draw.text((lx + 85, py + 135), "LED (Red)", font=FONT_LABEL, fill=TEXT_DARK, anchor="mm")
    
    led_anode = (lx + 65, py + 225)
    led_cathode = (lx + 105, py + 225)
    draw.ellipse([(led_anode[0]-6, led_anode[1]-6), (led_anode[0]+6, led_anode[1]+6)], fill=WIRE_PWM, outline=(30,30,30), width=1)
    draw.text((led_anode[0], led_anode[1] + 16), "G2 (+)", font=FONT_PIN, fill=WIRE_PWM, anchor="mm")
    draw.ellipse([(led_cathode[0]-6, led_cathode[1]-6), (led_cathode[0]+6, led_cathode[1]+6)], fill=WIRE_GND, outline=(30,30,30), width=1)
    draw.text((led_cathode[0], led_cathode[1] + 16), "GND (-)", font=FONT_PIN, fill=WIRE_GND, anchor="mm")

    # Wire Routings
    draw.line([l_coords["3V3"], (30, l_coords["3V3"][1]), (30, 730), (ldr_p1[0], 730), ldr_p1], fill=WIRE_3V3, width=4)
    draw.line([l_coords["G34"], (45, l_coords["G34"][1]), (45, 755), (ldr_mid[0], 755), ldr_mid], fill=WIRE_ADC, width=4)
    draw.line([l_coords["GND"], (20, l_coords["GND"][1]), (20, 780), (ldr_p2[0], 780), ldr_p2], fill=WIRE_GND, width=4)
    draw.line([r_coords["G2"], (360, r_coords["G2"][1]), (360, 730), (led_anode[0], 730), led_anode], fill=WIRE_PWM, width=4)
    draw.line([r_coords["GND"], (380, r_coords["GND"][1]), (380, 755), (led_cathode[0], 755), led_cathode], fill=WIRE_GND, width=4)

    # Formula Card Bottom
    draw.rounded_rectangle([(bx + 30, by + 340), (bx + 430, by + 610)], radius=8, fill=CARD_BG, outline=BORDER_COLOR)
    draw.text((bx + 50, by + 365), "📐 สูตรคำนวณการแบ่งแรงดัน (Voltage Divider):", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.text((bx + 50, by + 405), "V_out = 3.3V × [ R_10k / (R_LDR + R_10k) ]", font=FONT_BODY, fill=DANGER_RED)
    draw.text((bx + 50, by + 440), "• เมื่อแสงสว่างมาก: R_LDR ลดต่ำลง (แรงดัน V_out สูงขึ้น)", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 475), "• เมื่อมืดสนิท: R_LDR พุ่งสูงถึง Mega-ohm (V_out ใกล้ 0V)", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 510), "• นำค่า ADC ที่ได้เทียบตาราง Lux เพื่อเปิด-ปิดไฟอัตโนมัติ", font=FONT_BODY, fill=TEXT_DARK)

    # Right Box
    rx, ry = 920, 150
    draw.rounded_rectangle([(rx, ry), (rx + 440, ry + 650)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((rx + 25, ry + 25), "📋 ตารางสรุปการต่อสายเซนเซอร์ LDR", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    rows = [
        ("ขา 3V3 (ESP32 ซ้ายแถว 1)", "ต่อเข้า ขาที่ 1 ของ LDR (สายสีแดง)", WIRE_3V3),
        ("ขา G34 (ESP32 ซ้ายแถว 5)", "ต่อเข้า จุดร่วมระหว่าง LDR กับ R 10k (สายสีน้ำเงิน)", WIRE_ADC),
        ("ขา GND (ESP32 ซ้ายแถว 14)", "ต่อเข้า ขาอีกข้างของ R 10k (สายสีดำ)", WIRE_GND),
        ("ขา G2 (ESP32 ขวาแถว 14)", "ต่อเข้า R 220Ω > Anode (+) ของ LED (สายสีส้ม)", WIRE_PWM),
        ("ขา GND (ESP32 ขวาแถว 1)", "ต่อเข้า Cathode (-) ของ LED (สายสีดำ)", WIRE_GND)
    ]
    for i, (rt, rd, rc) in enumerate(rows):
        cy = ry + 75 + i * 65
        draw.rounded_rectangle([(rx + 20, cy), (rx + 420, cy + 55)], radius=6, fill=(248, 249, 250), outline=BORDER_COLOR)
        draw.line([(rx + 35, cy + 27), (rx + 55, cy + 27)], fill=rc, width=5)
        draw.text((rx + 65, cy + 12), rt, font=FONT_LABEL, fill=rc)
        draw.text((rx + 65, cy + 32), rd, font=FONT_SMALL, fill=TEXT_DARK)
        
    img.save(os.path.join(OUTPUT_DIR, "circuit_04_ldr_divider.png"), "PNG")
    img.save(os.path.join(ARTIFACT_DIR, "circuit_04_ldr_divider.png"), "PNG")
    print("Rendered PNG: circuit_04_ldr_divider.png")

# ==========================================
# 5. CIRCUIT 5: RGB LED + LDR SENSING (Week 04)
# ==========================================
def render_png_circuit_5():
    img = Image.new("RGB", (1400, 850), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "วงจรที่ 5: ตรวจจับสีวัตถุด้วย RGB LED + LDR (Color Sensing Unit)",
        "แสดงขาทั้งหมดของ ESP32 (ครบ 38 ขา) พร้อมโยงสายหลอดแม่สี RGB (GPIO 4, 5, 23) และเซนเซอร์แสง LDR (GPIO 34)",
        "📌 ใช้ใน: Week 04 (LED & RGB Color Sensing)"
    )
    
    act_l = {"3V3": WIRE_3V3, "G34": WIRE_ADC, "GND": WIRE_GND}
    act_r = {"G23": (13, 110, 253), "G5": (25, 135, 84), "G4": (220, 53, 69), "GND": WIRE_GND}
    l_coords, r_coords, bh = draw_esp32_all_pins(draw, 70, 140, act_l, act_r)
    
    bx, by = 420, 150
    draw.rounded_rectangle([(bx, by), (bx + 460, by + 650)], radius=12, fill=(242, 244, 248), outline=BORDER_COLOR, width=2)
    draw.text((bx + 180, by + 15), "BREADBOARD", font=FONT_HEADING, fill=(170, 175, 185))
    
    # RGB LED Module
    rx_m, ry_m = bx + 40, by + 60
    draw.rounded_rectangle([(rx_m, ry_m), (rx_m + 200, ry_m + 260)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.ellipse([(rx_m + 60, ry_m + 30), (rx_m + 140, ry_m + 110)], fill=(240, 240, 245), outline=(160, 165, 175), width=2)
    draw.ellipse([(rx_m + 80, ry_m + 50), (rx_m + 100, ry_m + 70)], fill=(255, 50, 50))
    draw.ellipse([(rx_m + 100, ry_m + 50), (rx_m + 120, ry_m + 70)], fill=(50, 200, 50))
    draw.ellipse([(rx_m + 90, ry_m + 70), (rx_m + 110, ry_m + 90)], fill=(50, 100, 255))
    draw.text((rx_m + 100, ry_m + 130), "RGB LED (Common Cathode)", font=FONT_SMALL, fill=TEXT_DARK, anchor="mm")
    
    rgb_r = (rx_m + 35, ry_m + 225)
    rgb_g = (rx_m + 75, ry_m + 225)
    rgb_b = (rx_m + 120, ry_m + 225)
    rgb_cat = (rx_m + 165, ry_m + 225)
    for p, c, t in [(rgb_r, (220, 53, 69), "R (G4)"), (rgb_g, (25, 135, 84), "G (G5)"), (rgb_b, (13, 110, 253), "B (G23)"), (rgb_cat, WIRE_GND, "Cathode")]:
        draw.ellipse([(p[0]-5, p[1]-5), (p[0]+5, p[1]+5)], fill=c, outline=(30,30,30), width=1)
        draw.text((p[0], p[1] + 16), t, font=FONT_PIN, fill=c, anchor="mm")

    # LDR Module
    lx_m, ly_m = bx + 260, by + 60
    draw.rounded_rectangle([(lx_m, ly_m), (lx_m + 160, ry_m + 260)], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    draw.ellipse([(lx_m + 50, ly_m + 30), (lx_m + 110, ly_m + 90)], fill=(255, 235, 150), outline=(220, 180, 50), width=2)
    draw.text((lx_m + 80, ly_m + 120), "LDR Sensor", font=FONT_LABEL, fill=TEXT_DARK, anchor="mm")
    
    ldr_p1 = (lx_m + 45, ly_m + 225)
    ldr_mid = (lx_m + 80, ly_m + 225)
    ldr_p2 = (lx_m + 115, ly_m + 225)
    for p, c, t in [(ldr_p1, WIRE_3V3, "3.3V"), (ldr_mid, WIRE_ADC, "G34"), (ldr_p2, WIRE_GND, "GND")]:
        draw.ellipse([(p[0]-5, p[1]-5), (p[0]+5, p[1]+5)], fill=c, outline=(30,30,30), width=1)
        draw.text((p[0], p[1] + 16), t, font=FONT_PIN, fill=c, anchor="mm")

    # Wire Routings
    draw.line([r_coords["G4"], (350, r_coords["G4"][1]), (350, 710), (rgb_r[0], 710), rgb_r], fill=(220, 53, 69), width=3)
    draw.line([r_coords["G5"], (365, r_coords["G5"][1]), (365, 730), (rgb_g[0], 730), rgb_g], fill=(25, 135, 84), width=3)
    draw.line([r_coords["G23"], (380, r_coords["G23"][1]), (380, 750), (rgb_b[0], 750), rgb_b], fill=(13, 110, 253), width=3)
    draw.line([r_coords["GND"], (335, r_coords["GND"][1]), (335, 770), (rgb_cat[0], 770), rgb_cat], fill=WIRE_GND, width=3)
    
    draw.line([l_coords["3V3"], (30, l_coords["3V3"][1]), (30, 730), (ldr_p1[0], 730), ldr_p1], fill=WIRE_3V3, width=3)
    draw.line([l_coords["G34"], (45, l_coords["G34"][1]), (45, 755), (ldr_mid[0], 755), ldr_mid], fill=WIRE_ADC, width=3)
    draw.line([l_coords["GND"], (20, l_coords["GND"][1]), (20, 780), (ldr_p2[0], 780), ldr_p2], fill=WIRE_GND, width=3)

    # Explanation Bottom
    draw.rounded_rectangle([(bx + 30, by + 340), (bx + 430, by + 610)], radius=8, fill=CARD_BG, outline=BORDER_COLOR)
    draw.text((bx + 50, by + 365), "🎯 หลักการตรวจจับสีวัตถุ (Color Reflection):", font=FONT_LABEL, fill=PRIMARY_BLUE)
    draw.text((bx + 50, by + 400), "1. ส่องแสงแม่สีทีละสี: แดง (Red) -> เขียว (Green) -> น้ำเงิน (Blue)", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 435), "2. วัตถุสีแดง จะสะท้อนแสงสีแดงได้มากที่สุด ทำให้ LDR วัดค่าแสงได้สูงสุด", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 470), "3. บันทึกค่า ADC ทั้ง 3 ค่า แล้วคำนวณเวกเตอร์เพื่อจำแนกสีวัตถุ", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((bx + 50, by + 510), "✨ ตรวจจับสีได้แม่นยำด้วยการ Calibrate ค่าพื้นผิวขาว-ดำ", font=FONT_LABEL, fill=SUCCESS_GREEN)

    # Right Box
    rx, ry = 920, 150
    draw.rounded_rectangle([(rx, ry), (rx + 440, ry + 650)], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.text((rx + 25, ry + 25), "📋 ตารางสรุปการต่อสาย RGB LED", font=FONT_HEADING, fill=PRIMARY_BLUE)
    
    rows = [
        ("ขา G4 (ESP32 ขวาแถว 13)", "ต่อเข้า R 220Ω > ขา Red ของ RGB (สายสีแดง)", (220, 53, 69)),
        ("ขา G5 (ESP32 ขวาแถว 10)", "ต่อเข้า R 220Ω > ขา Green ของ RGB (สายสีเขียว)", (25, 135, 84)),
        ("ขา G23 (ESP32 ขวาแถว 2)", "ต่อเข้า R 220Ω > ขา Blue ของ RGB (สายสีน้ำเงิน)", (13, 110, 253)),
        ("ขา GND (ESP32 ขวาแถว 1)", "ต่อเข้า ขายาวสุด Cathode (-) ของ RGB (สายสีดำ)", WIRE_GND),
        ("ขา G34 (ESP32 ซ้ายแถว 5)", "ต่อเข้า ขากลางวงจร LDR Divider (สายสีฟ้า)", WIRE_ADC)
    ]
    for i, (rt, rd, rc) in enumerate(rows):
        cy = ry + 75 + i * 65
        draw.rounded_rectangle([(rx + 20, cy), (rx + 420, cy + 55)], radius=6, fill=(248, 249, 250), outline=BORDER_COLOR)
        draw.line([(rx + 35, cy + 27), (rx + 55, cy + 27)], fill=rc, width=5)
        draw.text((rx + 65, cy + 12), rt, font=FONT_LABEL, fill=rc)
        draw.text((rx + 65, cy + 32), rd, font=FONT_SMALL, fill=TEXT_DARK)
        
    img.save(os.path.join(OUTPUT_DIR, "circuit_05_rgb_color_sensing.png"), "PNG")
    img.save(os.path.join(ARTIFACT_DIR, "circuit_05_rgb_color_sensing.png"), "PNG")
    print("Rendered PNG: circuit_05_rgb_color_sensing.png")

# Run all renders!
if __name__ == "__main__":
    print("Rendering All 5 Remaining Circuits...")
    render_png_circuit_1()
    render_png_circuit_2()
    render_png_circuit_3()
    render_png_circuit_4()
    render_png_circuit_5()
    print("ALL PNGs RENDERED SUCCESSFULLY!")
