#!/usr/bin/env python3
"""
remote_doctor.py — สคริปต์ตรวจสอบความพร้อมเครื่องเพื่อน, เช็กพอร์ต USB/Serial, เช็ก IP, และช่วย Debug อัตโนมัติ
วิธีใช้:
  python3 remote_doctor.py
  python3 remote_doctor.py --fix-ports
"""
import argparse
import glob
import os
import platform
import shutil
import socket
import subprocess
import sys

def get_lan_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127.") and not ip.startswith("169.254.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip not in ips:
            ips.append(ip)
    except Exception:
        pass
    return ips

def find_serial_ports():
    system = platform.system()
    ports = []
    if system == "Windows":
        try:
            out = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", "[System.IO.Ports.SerialPort]::GetPortNames()"],
                stderr=subprocess.DEVNULL
            ).decode(errors="ignore").splitlines()
            ports = [p.strip() for p in out if p.strip()]
        except Exception:
            pass
    elif system == "Darwin":
        ports = sorted(glob.glob("/dev/cu.usbserial*") + glob.glob("/dev/cu.SLAB*") + glob.glob("/dev/cu.wchusbserial*") + glob.glob("/dev/cu.usbmodem*"))
    else:
        ports = sorted(glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*"))
    return ports

def check_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0

def main():
    parser = argparse.ArgumentParser(description="Remote Doctor & Debugger for IoT-App-2569")
    parser.add_argument("--fix-ports", action="store_true", help="เคลียร์พอร์ตที่ค้างอยู่ (เช่น Mosquitto, Kestrel dotnet)")
    args = parser.parse_args()

    system = platform.system()
    print("============================================================")
    print(f"🩺 IoT-2569 Remote Doctor & Debugger ({system} {platform.release()})")
    print("============================================================")

    # 1. ตรวจสอบ IP Address
    ips = get_lan_ips()
    print(f"🌐 [1] IP Address ของเครื่องนี้ (ใช้ใส่ MQTT_BROKER_URI / มือถือ): {ips or ['ไม่พบเชื่อมต่อ LAN']}")

    # 2. ตรวจสอบสาย USB / บอร์ด ESP32
    ports = find_serial_ports()
    if ports:
        print(f"🔌 [2] พบบอร์ด ESP32 เสียบอยู่ที่พอร์ต: {ports}")
    else:
        print("⚠️  [2] ไม่พบบอร์ด ESP32! (ตรวจสอบว่าเสียบสาย USB ที่มี Data หรือลงไดรเวอร์ CP210x/CH340 แล้วหรือยัง)")

    # 3. ตรวจสอบ Tools ที่จำเป็น
    tools = {
        "python3 / python": shutil.which("python3") or shutil.which("python"),
        "git": shutil.which("git"),
        "dotnet (.NET SDK - Week 8,9)": shutil.which("dotnet"),
        "mosquitto (MQTT Broker - Week 11,12)": shutil.which("mosquitto") or (os.path.exists(r"C:\Program Files\mosquitto\mosquitto.exe") if system == "Windows" else False),
        "flutter (Flutter SDK - Week 12)": shutil.which("flutter"),
        "idf.py (ESP-IDF)": shutil.which("idf.py"),
        "docker (กรณีคอมไพล์ผ่าน Docker)": shutil.which("docker"),
    }
    print("\n🧰 [3] สถานะโปรแกรมและเครื่องมือในเครื่อง:")
    for name, path in tools.items():
        status = f"✅ พบ ({path})" if path else "❌ ไม่พบใน PATH"
        print(f"   - {name}: {status}")

    # 4. ตรวจสอบพอร์ตเครือข่ายที่ใช้ในแล็บ
    print("\n📡 [4] สถานะพอร์ตเครือข่าย (Lab Ports):")
    for p, desc in [(1883, "MQTT Broker (Week 11, 12)"), (8883, "MQTTS TLS (Week 11.3)"), (5000, "Kestrel Web Server (Week 8)"), (5117, "Kestrel API (Week 9)")]:
        in_use = check_port_in_use(p)
        print(f"   - Port {p} ({desc}): {'🟢 กำลังรันอยู่ (OPEN)' if in_use else '⚪ ว่าง (FREE)'}")

    if args.fix_ports:
        print("\n🧹 กำลังเคลียร์โปรเซส Kestrel (dotnet) ที่อาจค้างแย่งพอร์ต...")
        if system == "Windows":
            subprocess.run(["taskkill", "/F", "/IM", "ESP32.Kestrel.Webserver.exe"], stderr=subprocess.DEVNULL)
            subprocess.run(["taskkill", "/F", "/IM", "Kestrel_Serial_Gateway.exe"], stderr=subprocess.DEVNULL)
            subprocess.run(["taskkill", "/F", "/IM", "Kestrel_SVG_Dashboard.exe"], stderr=subprocess.DEVNULL)
            subprocess.run(["taskkill", "/F", "/IM", "Kestrel_Dual_Dashboard.exe"], stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "-f", "Kestrel"], stderr=subprocess.DEVNULL)
        print("✅ เคลียร์โปรเซสเรียบร้อย!")

    print("============================================================")

if __name__ == "__main__":
    main()
