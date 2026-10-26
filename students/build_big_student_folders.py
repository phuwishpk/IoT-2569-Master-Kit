#!/usr/bin/env python3
"""
build_big_student_folders.py
Build a full, complete, standalone big folder for EACH student.
Each student's folder contains all 12 weeks of code, reports, circuits, checklists,
and customized run commands, pre-configured with their ID, name, MQTT topic,
Wi-Fi SSID, and assigned Lab 8.5 Dual Gauge widgets.
"""

import os
import shutil
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
        "id": "67030180",
        "name_th": "นายภูมิชนะ เทียมแก้ว",
        "name_en": "Phumchana Thiamkaew",
        "folder_name": "67030180_Phumchana_Thiamkaew"
    },
    {
        "id": "67030073",
        "name_th": "นายณัฐพงศ์ เนียมประดิษฐ",
        "name_en": "Natthaphong Niampradit",
        "folder_name": "67030073_Natthaphong_Niampradit"
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

def generate_widget_svg(gtype: int, side: str) -> str:
    prefix = "left" if side == "left" else "right"
    if gtype == 1:
        return f"""
            <svg width="240" height="170" viewBox="0 0 240 170" id="{prefix}-speedo">
                <path d="M 30 140 A 90 90 0 0 1 210 140" fill="none" stroke="#1e293b" stroke-width="18" stroke-linecap="round"/>
                <path d="M 30 140 A 90 90 0 0 1 210 140" fill="none" stroke="#00f2fe" stroke-width="18" stroke-linecap="round"
                      stroke-dasharray="283" stroke-dashoffset="283" id="{prefix}-arc"/>
                <g id="{prefix}-needle" transform="rotate(-90, 120, 140)" style="transition: transform 0.12s ease-out;">
                    <polygon points="116,140 124,140 120,45" fill="#ff0055"/>
                    <circle cx="120" cy="140" r="10" fill="#f8fafc"/>
                </g>
            </svg>"""
    elif gtype == 2:
        bars = []
        for i in range(10):
            y = 190 - i * 18
            color = "#10b981" if i < 6 else ("#f59e0b" if i < 8 else "#ff0055")
            bars.append(f'<rect x="45" y="{y}" width="130" height="12" rx="4" fill="{color}" opacity="0.15" class="{prefix}-led" id="{prefix}-led-{i}"/>')
        return f'<svg width="220" height="220" viewBox="0 0 220 220" id="{prefix}-vu">' + "\n".join(bars) + "</svg>"
    elif gtype == 3:
        return f"""
            <svg width="220" height="160" viewBox="0 0 220 160" id="{prefix}-seg">
                <rect x="15" y="20" width="190" height="120" rx="16" fill="#050811" stroke="#38bdf8" stroke-width="2"/>
                <text x="110" y="102" text-anchor="middle" fill="#00f2fe" font-family="Orbitron, monospace" font-size="64" font-weight="900" id="{prefix}-seg-text">00</text>
            </svg>"""
    else:
        return f"""
            <svg width="220" height="220" viewBox="0 0 220 220" id="{prefix}-tank">
                <defs>
                    <clipPath id="{prefix}-tank-clip">
                        <rect x="45" y="20" width="130" height="180" rx="22" />
                    </clipPath>
                    <linearGradient id="{prefix}-liquid-grad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.95"/>
                        <stop offset="100%" stop-color="#0284c7" stop-opacity="0.85"/>
                    </linearGradient>
                </defs>
                <rect x="45" y="20" width="130" height="180" rx="22" fill="#0b1324" stroke="#334155" stroke-width="4"/>
                <g clip-path="url(#{prefix}-tank-clip)">
                    <rect id="{prefix}-water-fill" x="45" y="200" width="130" height="0" fill="url(#{prefix}-liquid-grad)" style="transition: y 0.12s ease-out, height 0.12s ease-out;"/>
                </g>
                <rect x="45" y="20" width="130" height="180" rx="22" fill="none" stroke="rgba(0, 242, 254, 0.45)" stroke-width="3"/>
            </svg>"""

def update_lab85_html(html_path: str, student_id: str, name_en: str):
    n, left, right, collision = calc_lab85_gauges(student_id)
    left_name = GAUGE_NAMES[left]
    right_name = GAUGE_NAMES[right]
    left_svg = generate_widget_svg(left, "left")
    right_svg = generate_widget_svg(right, "right")

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Dual-Channel IoT Command Center - {student_id}</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {{ background: radial-gradient(circle at 50% 15%, #132238 0%, #070b14 100%); color: #f8fafc; font-family: 'Rajdhani', sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 28px 16px; margin: 0; }}
        .student-pill {{ font-size: 0.9rem; font-weight: 700; color: #00f2fe; background: rgba(0, 242, 254, 0.12); border: 1px solid rgba(0, 242, 254, 0.4); border-radius: 20px; padding: 5px 18px; letter-spacing: 1.5px; margin-bottom: 8px; display: inline-block; }}
        .header-title {{ font-family: 'Orbitron', sans-serif; font-size: 1.75rem; color: #38bdf8; margin: 4px 0 10px; }}
        .formula-calc {{ font-size: 0.9rem; color: #cbd5e1; background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 6px 16px; margin-bottom: 20px; }}
        .command-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 24px; width: 100%; max-width: 960px; }}
        .widget-panel {{ background: rgba(14, 22, 38, 0.82); border: 1px solid rgba(0, 242, 254, 0.28); border-radius: 22px; padding: 24px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 20px 45px rgba(0,0,0,0.6); }}
        .panel-header {{ width: 100%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; margin-bottom: 14px; }}
        .tag {{ font-family: 'Orbitron', sans-serif; font-size: 0.78rem; padding: 3px 10px; border-radius: 6px; background: rgba(0, 242, 254, 0.15); color: #00f2fe; }}
        .svg-container {{ min-height: 220px; display: flex; align-items: center; justify-content: center; }}
        .metric-banner {{ font-family: 'Orbitron', monospace; font-size: 2.1rem; font-weight: 900; color: #00f2fe; margin: 8px 0 14px; }}
        .metrics-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; width: 100%; }}
        .metric-card {{ background: rgba(10, 16, 28, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 10px; text-align: center; }}
        .metric-label {{ font-size: 0.72rem; color: #94a3b8; }}
        .metric-val {{ font-family: 'Orbitron', sans-serif; font-size: 1.1rem; font-weight: 700; color: #fff; margin-top: 3px; }}
    </style>
</head>
<body>
    <div style="text-align:center;">
        <div class="student-pill">STUDENT ID: {student_id} &bull; {name_en.upper()}</div>
        <h1 class="header-title">DUAL-CHANNEL IOT COMMAND CENTER</h1>
        <div class="formula-calc">
            Calculation (N={n:03d}): Left = ({n}%4)+1 = <strong style="color:#00f2fe;">{left} ({left_name})</strong> |
            Right = (&lfloor;{n}/4&rfloor;%4)+1 {"(+1 Anti-Collision)" if collision else ""} = <strong style="color:#10b981;">{right} ({right_name})</strong>
        </div>
    </div>

    <div class="command-grid">
        <div class="widget-panel">
            <div class="panel-header">
                <span class="tag">CHANNEL A (LEFT #{left})</span>
                <strong>{left_name}</strong>
                <span style="font-size:0.75rem;color:#10b981;">● HARDWARE POT</span>
            </div>
            <div class="svg-container">{left_svg}</div>
            <div class="metric-banner" id="left-pct">0.0%</div>
            <div class="metrics-grid">
                <div class="metric-card"><div class="metric-label">RAW ADC (12-BIT)</div><div class="metric-val" id="left-raw">0</div></div>
                <div class="metric-card"><div class="metric-label">VOLTAGE (V)</div><div class="metric-val" id="left-volt">0.00 V</div></div>
            </div>
        </div>

        <div class="widget-panel">
            <div class="panel-header">
                <span class="tag" style="color:#10b981;background:rgba(16,185,129,0.15);">CHANNEL B (RIGHT #{right})</span>
                <strong>{right_name}</strong>
                <span style="font-size:0.75rem;color:#38bdf8;">● CHANNEL B STREAM</span>
            </div>
            <div class="svg-container">{right_svg}</div>
            <div class="metric-banner" id="right-pct" style="color:#10b981;">0.0%</div>
            <div class="metrics-grid">
                <div class="metric-card"><div class="metric-label">RAW ADC (12-BIT)</div><div class="metric-val" id="right-raw">0</div></div>
                <div class="metric-card"><div class="metric-label">VOLTAGE (V)</div><div class="metric-val" id="right-volt">0.00 V</div></div>
            </div>
        </div>
    </div>

    <script>
        function updateGauge(side, gtype, pct) {{
            const clamped = Math.max(0, Math.min(100, pct));
            if (gtype === 1) {{
                const deg = -90 + (clamped / 100) * 180;
                const needle = document.getElementById(side + '-needle');
                const arc = document.getElementById(side + '-arc');
                if (needle) needle.setAttribute('transform', `rotate(${{deg}}, 120, 140)`);
                if (arc) arc.setAttribute('stroke-dashoffset', (283 - (clamped / 100) * 283).toFixed(1));
            }} else if (gtype === 2) {{
                const activeCount = Math.round((clamped / 100) * 10);
                for (let i = 0; i < 10; i++) {{
                    const led = document.getElementById(`${{side}}-led-${{i}}`);
                    if (led) led.setAttribute('opacity', i < activeCount ? '1.0' : '0.15');
                }}
            }} else if (gtype === 3) {{
                const txt = document.getElementById(side + '-seg-text');
                if (txt) txt.textContent = Math.min(99, Math.round(clamped)).toString().padStart(2, '0');
            }} else if (gtype === 4) {{
                const fill = document.getElementById(side + '-water-fill');
                if (fill) {{
                    const h = (clamped / 100) * 180;
                    fill.setAttribute('y', (200 - h).toFixed(1));
                    fill.setAttribute('height', h.toFixed(1));
                }}
            }}
        }}

        async function poll() {{
            try {{
                const res = await fetch('/api/telemetry');
                const d = await res.json();
                const chA = d.channelA || {{ rawAdc: d.rawAdc || 0, voltage: d.voltage || 0, percentage: d.percentage || 0 }};
                const chB = d.channelB || {{ rawAdc: 2048, voltage: 1.65, percentage: 50 }};

                document.getElementById('left-pct').textContent = chA.percentage.toFixed(1) + '%';
                document.getElementById('left-raw').textContent = chA.rawAdc;
                document.getElementById('left-volt').textContent = chA.voltage.toFixed(2) + ' V';
                updateGauge('left', {left}, chA.percentage);

                document.getElementById('right-pct').textContent = chB.percentage.toFixed(1) + '%';
                document.getElementById('right-raw').textContent = chB.rawAdc;
                document.getElementById('right-volt').textContent = chB.voltage.toFixed(2) + ' V';
                updateGauge('right', {right}, chB.percentage);
            }} catch (e) {{}}
        }}
        setInterval(poll, 100);
        poll();
    </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as fp:
        fp.write(html)

def replace_in_file(filepath: str, replacements: list):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

MASTER_DIR = "/Users/phuwish/Downloads/fortest week1 week2/IoT-2569-Master-Kit"
STUDENTS_DIR = os.path.join(MASTER_DIR, "students")

WEEKS_AND_DIRS = [
    "Week01_Intro",
    "Week02_POT_and_LED",
    "Week03_LDR_Calibration",
    "Week04_RGB_Color_Sensing",
    "Week05_WiFi_ESP32",
    "Week06_SoftAP_FreeRTOS",
    "Week07_WiFi_Provisioning",
    "Week08_Kestrel_and_SVG",
    "Week09_SPI_OLED_and_UI",
    "Week10_HTTP_UDP_CoAP",
    "Week11_MQTT_and_RainMaker",
    "Week12_Flutter_MQTT_App",
    "Week13_Kestrel_Edge_Gateway",
    "circuits"
]

SHARED_FILES = [
    "CHECKLIST_AND_DATA_COPY.md",
    "CIRCUITS_WIRING_GUIDE.md",
    "MASTER_CHECKLIST.md",
    "remote_doctor.py"
]

print("Starting generation of standalone big folders for all students...")

for st in STUDENTS:
    sid = st["id"]
    nth = st["name_th"]
    nen = st["name_en"]
    folder = st["folder_name"]
    last4 = sid[-4:]
    
    st_big_folder = os.path.join(STUDENTS_DIR, folder)
    print(f"\n=======================================================")
    print(f"📦 Building Big Standalone Folder for: {sid} - {nth} ({nen})")
    print(f"   Target: {st_big_folder}")
    print(f"=======================================================")
    
    # Ensure directory exists
    os.makedirs(st_big_folder, exist_ok=True)
    
    # 1. Copy all Week directories and circuits
    for item in WEEKS_AND_DIRS:
        src = os.path.join(MASTER_DIR, item)
        dst = os.path.join(st_big_folder, item)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('build', '.git', 'bin', 'obj', '.vs', '.cache', '__pycache__', '*.tmp'))
        
    # 2. Copy shared reference files
    for item in SHARED_FILES:
        src = os.path.join(MASTER_DIR, item)
        dst = os.path.join(st_big_folder, item)
        shutil.copy2(src, dst)
        
    # 3. Rename internal template folders & report files
    # Week 03
    p3 = os.path.join(st_big_folder, "Week03_LDR_Calibration")
    if os.path.exists(os.path.join(p3, "67030183_template")):
        os.rename(os.path.join(p3, "67030183_template"), os.path.join(p3, f"{sid}_template"))
        
    # Week 04
    p4 = os.path.join(st_big_folder, "Week04_RGB_Color_Sensing")
    if os.path.exists(os.path.join(p4, "67030183")):
        os.rename(os.path.join(p4, "67030183"), os.path.join(p4, sid))
        
    # Week 05
    p5 = os.path.join(st_big_folder, "Week05_WiFi_ESP32")
    if os.path.exists(os.path.join(p5, "67030183_template")):
        os.rename(os.path.join(p5, "67030183_template"), os.path.join(p5, f"{sid}_template"))
        
    # Week 06
    p6 = os.path.join(st_big_folder, "Week06_SoftAP_FreeRTOS")
    if os.path.exists(os.path.join(p6, "67030183_template")):
        os.rename(os.path.join(p6, "67030183_template"), os.path.join(p6, f"{sid}_template"))
        
    # Week 07
    p7 = os.path.join(st_big_folder, "Week07_WiFi_Provisioning")
    if os.path.exists(os.path.join(p7, "67030183_template")):
        w7_dest = os.path.join(p7, f"{sid}_template")
        os.rename(os.path.join(p7, "67030183_template"), w7_dest)
        rep7 = os.path.join(w7_dest, "Report_67030183.md")
        if os.path.exists(rep7):
            os.rename(rep7, os.path.join(w7_dest, f"Report_{sid}.md"))
            
    # Week 08
    p8 = os.path.join(st_big_folder, "Week08_Kestrel_and_SVG")
    if os.path.exists(os.path.join(p8, "67030183")):
        w8_dest = os.path.join(p8, sid)
        os.rename(os.path.join(p8, "67030183"), w8_dest)
        rep8 = os.path.join(w8_dest, "Report_67030183.md")
        if os.path.exists(rep8):
            os.rename(rep8, os.path.join(w8_dest, f"Report_{sid}.md"))
            
    # Week 09
    p9 = os.path.join(st_big_folder, "Week09_SPI_OLED_and_UI")
    if os.path.exists(os.path.join(p9, "67030183_template")):
        os.rename(os.path.join(p9, "67030183_template"), os.path.join(p9, f"{sid}_template"))
        
    # Week 10
    p10 = os.path.join(st_big_folder, "Week10_HTTP_UDP_CoAP")
    if os.path.exists(os.path.join(p10, "67030183_template")):
        os.rename(os.path.join(p10, "67030183_template"), os.path.join(p10, f"{sid}_template"))
        
    # Week 11
    p11 = os.path.join(st_big_folder, "Week11_MQTT_and_RainMaker")
    if os.path.exists(os.path.join(p11, "67030183_template")):
        os.rename(os.path.join(p11, "67030183_template"), os.path.join(p11, f"{sid}_template"))
        
    # Week 12
    p12 = os.path.join(st_big_folder, "Week12_Flutter_MQTT_App")
    if os.path.exists(os.path.join(p12, "67030183_template")):
        os.rename(os.path.join(p12, "67030183_template"), os.path.join(p12, f"{sid}_template"))

    # Week 13
    p13 = os.path.join(st_big_folder, "Week13_Kestrel_Edge_Gateway")
    if os.path.exists(os.path.join(p13, "67030183_template")):
        os.rename(os.path.join(p13, "67030183_template"), os.path.join(p13, f"{sid}_template"))

    # 4. Update Week 08 Lab 8.5 Dual Gauge HTML
    lab85_html = os.path.join(st_big_folder, "Week08_Kestrel_and_SVG/Lab8-5/Kestrel_Dual_Dashboard/wwwroot/index.html")
    if os.path.exists(lab85_html):
        update_lab85_html(lab85_html, sid, nen)
        print(f"   ✓ Lab 8.5 Dual Gauge HTML generated for {sid}")
        
    # 5. String replacements across all files
    replacements = [
        ("67030183", sid),
        ("0183", last4),
        ("นายภูวิชญ์ ประกอบจิตร", nth),
        ("ภูวิชญ์ ประกอบจิตร", nth),
        ("Phuwish Prakobchit", nen),
        ("Phuwish", nen),
        ("ESP32_AP_0183", f"ESP32_AP_{last4}"),
        ("PROV_0183", f"PROV_{last4}"),
        ("iot/67030183/", f"iot/{sid}/"),
        ("IoT-Lab-0183", f"IoT-Lab-{last4}"),
    ]
    
    file_count = 0
    for root, dirs, files in os.walk(st_big_folder):
        for f in files:
            if f.endswith((".c", ".cs", ".md", ".html", ".dart", ".py", ".ps1", ".sh", ".json", ".txt")):
                fp = os.path.join(root, f)
                replace_in_file(fp, replacements)
                file_count += 1
                
    print(f"   ✓ Replaced ID and Name in {file_count} project files.")
    
    # 6. Create a personalized README.md in the root of the student's big folder
    readme_content = f"""# 🚀 IoT-App-2569: ชุดโปรเจกต์ประจำตัวฉบับสมบูรณ์ (Standalone Kit)
## นักศึกษา: {nth} ({nen})
### รหัสนักศึกษา: `{sid}` | Sec: IoT-App-2569

โฟลเดอร์นี้เป็น **ชุดโปรเจกต์ฉบับสมบูรณ์ที่พร้อมรันและส่งงานได้ทันที** ครบทั้ง 13 สัปดาห์ (Week 01 – Week 13) โดยโค้ด, รายงาน, หัวข้อ MQTT, ชื่อ Wi-Fi/BLE, และหน้าปัด SVG Gauge ได้รับการผูกค่าเป็นของ **{nth} ({sid})** เรียบร้อยแล้ว 100%

---

## 📂 โครงสร้างโฟลเดอร์ของ {sid}

```text
{folder}/
├── RUN_COMMANDS.md            # ⭐ รวมคำสั่งรันทุกสัปดาห์ ผูกรหัส {sid} เรียบร้อย
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
├── Week06_SoftAP_FreeRTOS/    # Week 06: SoftAP (ESP32_AP_{last4}) & TCP Throughput
├── Week07_WiFi_Provisioning/  # Week 07: BLE Provisioning (PROV_{last4})
├── Week08_Kestrel_and_SVG/    # Week 08: Kestrel C# Server & Gauge Dashboard
├── Week09_SPI_OLED_and_UI/    # Week 09: SPI OLED (7 ขา) & Kestrel Web UI
├── Week10_HTTP_UDP_CoAP/      # Week 10: Local Communication Benchmark (HTTP/UDP/CoAP)
├── Week11_MQTT_and_RainMaker/ # Week 11: MQTT Broker mTLS (iot/{sid}/...) & RainMaker
├── Week12_Flutter_MQTT_App/   # Week 12: Flutter Mobile IoT Dashboard
└── Week13_Kestrel_Edge_Gateway/ # Week 13: Converged Edge Gateway (.NET 8 Kestrel)
```

---

## ⚡ เริ่มต้นใช้งานทันที (Quick Start)
1. เปิดไฟล์ [`RUN_COMMANDS.md`](RUN_COMMANDS.md) ในโฟลเดอร์นี้
2. เสียบบอร์ด ESP32 เข้าคอมพิวเตอร์
3. คัดลอกคำสั่งในสัปดาห์ที่ต้องการรันไปวางใน Terminal ได้ทันที!
"""
    with open(os.path.join(st_big_folder, "README.md"), "w", encoding="utf-8") as rf:
        rf.write(readme_content)
        
    # Copy the personalized RUN_COMMANDS_<sid>.md as RUN_COMMANDS.md in root of student folder
    src_rc = os.path.join(st_big_folder, f"RUN_COMMANDS_{sid}.md")
    dst_rc = os.path.join(st_big_folder, "RUN_COMMANDS.md")
    if os.path.exists(src_rc):
        shutil.copy2(src_rc, dst_rc)
        
    print(f"   ✓ Created personalized README.md and RUN_COMMANDS.md")

print("\n=======================================================")
print("ALL 8 BIG STANDALONE STUDENT FOLDERS CREATED SUCCESSFULLY!")
print("=======================================================")
