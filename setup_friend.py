#!/usr/bin/env python3
"""
setup_friend.py — สคริปต์แปลงร่างโปรเจกต์ทั้ง 12 สัปดาห์ให้เป็นของเพื่อนอัตโนมัติ
วิธีใช้:
  python3 setup_friend.py --id 67030999 --name "Somchai" --thai-name "นายสมชาย ใจดี" --wifi "MyHotspot" --pass "12345678" --ip "192.168.1.50"
"""
import argparse
import os
import re
import shutil

GAUGE_NAMES = {
    1: "Analog Speedometer",
    2: "Audio VU Meter",
    3: "Retro 7-Segment",
    4: "Liquid Level Tank",
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
    return n, left, right, left_name, right_name

def replace_in_file(filepath: str, replacements: list):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Setup IoT-App-2569 Master Kit for a friend")
    parser.add_argument("--id", required=True, help="รหัสนักศึกษา 8 หลัก เช่น 67030999")
    parser.add_argument("--name", required=True, help="ชื่อภาษาอังกฤษ เช่น Somchai")
    parser.add_argument("--thai-name", default="", help="ชื่อ-นามสกุลภาษาไทย เช่น นายสมชาย ใจดี")
    parser.add_argument("--wifi", default="", help="ชื่อ Wi-Fi SSID สำหรับบอร์ด ESP32")
    parser.add_argument("--password", "--pass", dest="password", default="", help="รหัสผ่าน Wi-Fi")
    parser.add_argument("--ip", default="", help="IP ของเครื่องคอมพิวเตอร์เพื่อน (สำหรับ MQTT Broker)")
    args = parser.parse_args()

    sid = args.id.strip()
    last4 = sid[-4:] if len(sid) >= 4 else sid
    name_en = args.name.strip()
    name_th = args.thai_name.strip() or name_en

    base_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"============================================================")
    print(f"🚀 กำลังตั้งค่าโปรเจกต์ทั้งหมดสำหรับ: {sid} ({name_en} / {name_th})")
    print(f"============================================================")

    # 1. คำนวณเกจ์ Lab 8.5 และอัปเดตหน้าเว็บ Lab 8.5
    lab85_html = os.path.join(base_dir, "Week08_Kestrel_and_SVG/Lab8-5/Kestrel_Dual_Dashboard/wwwroot/index.html")
    if os.path.exists(lab85_html):
        n, l_id, r_id, l_name, r_name = update_lab85_html(lab85_html, sid, name_en)
        print(f"✅ [Week 08 - Lab 8.5] คำนวณเกจ์จากรหัส 3 ตัวท้าย (N={n:03d}):")
        print(f"   -> เกจ์ซ้าย (CH-A): #{l_id} ({l_name})")
        print(f"   -> เกจ์ขวา (CH-B): #{r_id} ({r_name})")

    # 2. อัปเดตไฟล์โค้ดและรายงานทั้งหมดใน Master Kit
    common_replacements = [
        ("67030183", sid),
        ("0183", last4),
        ("นายภูวิชญ์ ประกอบจิตร", name_th),
        ("ภูวิชญ์ ประกอบจิตร", name_th),
        ("Phuwish Prakobchit", name_en),
        ("Phuwish", name_en),
    ]

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f == "setup_friend.py":
                continue
            if f.endswith((".c", ".cs", ".md", ".html", ".dart", ".py", ".ps1", ".sh")):
                fp = os.path.join(root, f)
                reps = list(common_replacements)
                if args.wifi:
                    reps.append(('define WIFI_SSID      "Phuwish"', f'define WIFI_SSID      "{args.wifi}"'))
                    reps.append(('define WIFI_SSID "Phuwish"', f'define WIFI_SSID "{args.wifi}"'))
                if args.password:
                    reps.append(('define WIFI_PASS      "12345678"', f'define WIFI_PASS      "{args.password}"'))
                    reps.append(('define WIFI_PASS "12345678"', f'define WIFI_PASS "{args.password}"'))
                if args.ip:
                    # replace broker URI IP
                    with open(fp, "r", encoding="utf-8", errors="ignore") as file_in:
                        txt = file_in.read()
                    txt = re.sub(r"mqtt://\d+\.\d+\.\d+\.\d+:1883", f"mqtt://{args.ip}:1883", txt)
                    with open(fp, "w", encoding="utf-8") as file_out:
                        file_out.write(txt)
                replace_in_file(fp, reps)

    print(f"✅ อัปเดตรหัสนักศึกษา ({sid}), ชื่อ ({name_en}), และตั้งค่าเครือข่ายครบทุกสัปดาห์แล้ว!")
    print(f"============================================================")

if __name__ == "__main__":
    main()
