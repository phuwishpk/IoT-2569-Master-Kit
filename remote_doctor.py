#!/usr/bin/env python3
"""
remote_doctor.py — สคริปต์ตรวจความพร้อมเครื่อง, วินิจฉัยพอร์ต ESP32, ตรวจสอบ Environment, และแก้ปัญหาอัตโนมัติ
วิธีใช้:
  python3 remote_doctor.py              # วินิจฉัยทุกระบบ พร้อมแนะนำคำสั่งแก้ปัญหา
  python3 remote_doctor.py --fix-ports  # เคลียร์พอร์ตและโปรเซสที่ค้าง (dotnet, mosquitto, serial)
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

def check_python_module(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Remote Doctor & Environment Debugger for IoT-App-2569")
    parser.add_argument("--fix-ports", action="store_true", help="เคลียร์พอร์ตและโปรเซสที่ค้าง (เช่น Mosquitto, Kestrel dotnet)")
    parser.add_argument("--clear-port", action="store_true", help="Alias for --fix-ports")
    args = parser.parse_args()

    do_fix = args.fix_ports or args.clear_port
    system = platform.system()
    
    print("=" * 64)
    print(f"🩺 IoT-2569 Remote Doctor & Environment Clinic")
    print(f"   OS: {system} {platform.release()} ({platform.machine()})")
    print("=" * 64)

    # 1. ตรวจสอบ IP Address
    ips = get_lan_ips()
    print(f"\n🌐 [1] ข้อมูลเครือข่าย & IP Address:")
    if ips:
        for ip in ips:
            print(f"   ✓ LAN IP: {ip}  (ใช้ใส่ใน MQTT_BROKER_URI หรือเปิดแอปมือถือ)")
    else:
        print("   ⚠️  ไม่พบ IP วง LAN (ตรวจสอบว่าเชื่อมต่อ Wi-Fi หรือสาย LAN หรือยัง)")

    # 2. ตรวจสอบพอร์ตเชื่อมต่อบอร์ด ESP32
    print(f"\n🔌 [2] ตรวจสอบพอร์ต USB / Serial (ESP32):")
    ports = find_serial_ports()
    if ports:
        for p in ports:
            print(f"   ✅ พบบอร์ดที่พอร์ต: {p}")
        print(f"   👉 คำสั่งแฟลชตัวอย่าง: idf.py -p {ports[0]} flash monitor")
    else:
        print("   ❌ ไม่พบพอร์ตบอร์ด ESP32!")
        print("   💡 วิธีแก้ปัญหาพอร์ตหาไม่เจอ:")
        print("      1. ตรวจสอบสาย USB: ต้องเป็นสาย Data ที่ส่งข้อมูลได้ (สายชาร์จอย่างเดียวจะมองไม่เห็นพอร์ต)")
        print("      2. ลงไดรเวอร์ชิป USB-to-UART ให้ตรงรุ่น:")
        print("         - CP2102 Driver: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers")
        print("         - CH340/CH341 Driver: http://www.wch-ic.com/downloads/CH341SER_ZIP.html")
        if system == "Linux":
            print("      3. เพิ่มสิทธิ์ dialout บน Linux:")
            print("         sudo usermod -a -G dialout $USER && newgrp dialout")

    # 3. ตรวจสอบ ESP-IDF Environment
    print(f"\n⚡ [3] ตรวจสอบ ESP-IDF Environment (Toolchain):")
    idf_path = shutil.which("idf.py")
    if idf_path:
        print(f"   ✅ idf.py พร้อมใช้งาน: {idf_path}")
        try:
            ver = subprocess.check_output(["idf.py", "--version"], stderr=subprocess.DEVNULL).decode().strip()
            print(f"      เวอร์ชัน: {ver}")
        except Exception:
            pass
    else:
        print("   ❌ ไม่พบคำสั่ง 'idf.py' ใน Terminal ปัจจุบัน (Environment ยังไม่ได้โหลด)")
        print("   💡 คำสั่งกู้คืน Environment แบบรวดเร็ว:")
        if system == "Windows":
            print("      • เปิดโปรแกรม 'ESP-IDF 5.x PowerShell' จาก Start Menu โดยตรง (แนะนำที่สุด)")
            print("      • หรือรันใน PowerShell ปัจจุบัน:")
            print('        & "$env:USERPROFILE\\esp\\esp-idf\\export.ps1"')
            print('        # หรือถ้าลงไว้ที่ C:\\Espressif:')
            print('        & "C:\\Espressif\\frameworks\\esp-idf-v5.3\\export.ps1"')
        else:
            print("      • รันคำสั่งใน Terminal:")
            print("        . $HOME/esp/esp-idf/export.sh")
            print("      • หรือเพิ่ม alias ลง ~/.zshrc หรือ ~/.bashrc:")
            print('        echo \'alias get_idf=". $HOME/esp/esp-idf/export.sh"\' >> ~/.zshrc && source ~/.zshrc')
            print('        get_idf')

    # 4. ตรวจสอบ Python Modules ที่ต้องใช้
    print(f"\n🐍 [4] ตรวจสอบ Python & Libraries สำหรับวิชานี้:")
    py_path = shutil.which("python3") or shutil.which("python")
    print(f"   • Python Executable: {py_path or '❌ ไม่พบ Python'}")
    
    needed_modules = {
        "serial": "pyserial (สำหรับบริดจ์ Serial Monitor & Kestrel Gateway)",
        "paho.mqtt": "paho-mqtt (สำหรับทดสอบรับ-ส่ง MQTT Broker)",
        "requests": "requests (สำหรับทดสอบ HTTP REST & CoAP API)",
    }
    missing_mods = []
    for mod, desc in needed_modules.items():
        ok = check_python_module(mod)
        status = "✅ มีแล้ว" if ok else "❌ ขาด"
        print(f"   • {mod}: {status} — {desc}")
        if not ok:
            pkg_name = "pyserial" if mod == "serial" else ("paho-mqtt" if "mqtt" in mod else mod)
            missing_mods.append(pkg_name)
            
    if missing_mods:
        print(f"\n   💡 ติดตั้งไลบรารีที่ขาดด้วยคำสั่งเดียว:")
        pip_cmd = f"{sys.executable} -m pip install {' '.join(missing_mods)}"
        print(f"      {pip_cmd}")

    # 5. ตรวจสอบ SDKs อื่นๆ
    print(f"\n🧰 [5] ตรวจสอบ SDKs ประจำสัปดาห์ขั้นสูง:")
    dotnet_path = shutil.which("dotnet")
    if dotnet_path:
        try:
            dver = subprocess.check_output(["dotnet", "--version"], stderr=subprocess.DEVNULL).decode().strip()
            print(f"   ✅ .NET SDK (Week 8, 9, 13): พบเวอร์ชัน {dver} ({dotnet_path})")
        except Exception:
            print(f"   ✅ .NET SDK: พบที่ {dotnet_path}")
    else:
        print("   ❌ .NET SDK: ไม่พบใน PATH (จำเป็นสำหรับ Week 8, 9, 13)")
        print("      ดาวน์โหลดฟรี: https://dotnet.microsoft.com/download/dotnet/8.0")

    flutter_path = shutil.which("flutter")
    if flutter_path:
        print(f"   ✅ Flutter SDK (Week 12): พบที่ {flutter_path}")
    else:
        print("   ⚠️  Flutter SDK: ไม่พบใน PATH (จำเป็นสำหรับ Week 12 โมบายแอป)")
        print("      รันบน Chrome Web: flutter run -d chrome (หรือดาวน์โหลดจาก flutter.dev)")

    mosquitto_path = shutil.which("mosquitto") or (os.path.exists(r"C:\Program Files\mosquitto\mosquitto.exe") if system == "Windows" else False)
    if mosquitto_path:
        print(f"   ✅ Mosquitto MQTT Broker (Week 11): พบที่ {mosquitto_path}")
    else:
        print("   ⚠️  Mosquitto: ไม่พบใน PATH (สัปดาห์ 11 ต้องใช้รัน Broker mTLS)")
        if system == "Darwin":
            print("      ติดตั้งบน Mac: brew install mosquitto")
        elif system == "Windows":
            print("      ดาวน์โหลด: https://mosquitto.org/download/")
        else:
            print("      ติดตั้งบน Linux: sudo apt install -y mosquitto mosquitto-clients")

    # 6. ตรวจสอบพอร์ตเครือข่ายที่ใช้ในแล็บ
    print(f"\n📡 [6] ตรวจสอบสถานะพอร์ตเครือข่าย (Lab Ports Conflict):")
    lab_ports = [
        (1883, "MQTT Broker TCP (Week 11, 12, 13)"),
        (8883, "MQTTS TLS Port (Week 11.3)"),
        (5000, "Kestrel Web Server HTTP (Week 8)"),
        (5117, "Kestrel Calibration API (Week 9)"),
        (5123, "Kestrel Converged Gateway (Week 13)"),
        (5050, "Master Kit Local Report Sync Server"),
    ]
    conflicts = []
    for p, desc in lab_ports:
        in_use = check_port_in_use(p)
        status = "🟢 กำลังเปิดใช้งาน (IN USE)" if in_use else "⚪ ว่างพร้อมใช้งาน (FREE)"
        print(f"   • Port {p:5d}: {status} — {desc}")
        if in_use and p not in (5050,):
            conflicts.append(p)

    # 7. Action: เคลียร์พอร์ตค้าง
    if do_fix:
        print("\n🧹 [7] กำลังเคลียร์โปรเซสและพอร์ตที่ค้างอยู่ (--fix-ports)...")
        if system == "Windows":
            procs = ["dotnet.exe", "ESP32.Kestrel.Webserver.exe", "Kestrel_Serial_Gateway.exe", 
                     "Kestrel_SVG_Dashboard.exe", "Kestrel_Dual_Dashboard.exe", "mosquitto.exe"]
            for pr in procs:
                subprocess.run(["taskkill", "/F", "/IM", pr], stderr=subprocess.DEVNULL)
            print("   ✅ ส่งคำสั่งหยุดโปรเซส dotnet และ mosquitto ที่ค้างอยู่บน Windows แล้ว")
        else:
            subprocess.run("pkill -f dotnet 2>/dev/null || true", shell=True)
            subprocess.run("pkill -f mosquitto 2>/dev/null || true", shell=True)
            subprocess.run("pkill -f Kestrel 2>/dev/null || true", shell=True)
            print("   ✅ ส่งสัญญาณ pkill ล้างโปรเซส dotnet, mosquitto, Kestrel บนระบบ Unix เรียบร้อย")
    elif conflicts:
        print(f"\n💡 ตรวจพบพอร์ตที่กำลังถูกใช้งาน {conflicts}")
        print("   หากต้องการสั่งปิดโปรเซสที่ค้างอยู่ทั้งหมด ให้รันคำสั่ง:")
        print("   python3 remote_doctor.py --fix-ports")

    print("\n" + "=" * 64)
    print("✨ การวินิจฉัยเสร็จสมบูรณ์! พร้อมทำแล็บ IoT-App-2569 ครบทั้ง 13 สัปดาห์")
    print("=" * 64)

if __name__ == "__main__":
    main()
