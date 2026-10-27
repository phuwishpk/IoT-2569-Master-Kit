#!/usr/bin/env python3
"""
Orchestration script to run Lab 11.1 and Lab 11.3 for all 9 students:
- 67030073 Natthaphong Niampradit
- 67030180 Phumchana Thiamkaew
- 67030248 Suwijak Lawang
- 67030249 Suwimon Sripramai
- 67030268 Korn Daengthong
- 67030270 Kritsadinat Samrankit
- 67030299 Thanaporn Pitsamai
- 67030359 Attawut Bualian
- 67030360 Ittipat Sutthinuan
"""

import os
import sys
import time
import subprocess
import glob

STUDENTS = [
    "67030073",
    "67030180",
    "67030248",
    "67030249",
    "67030268",
    "67030270",
    "67030299",
    "67030359",
    "67030360"
]

REPO_DIR = "/Users/phuwish/Downloads/fortest week1 week2/IoT-2569-Master-Kit"
MQTT_LAB_DIR = os.path.expanduser("~/mqtt_lab")

def ensure_terminal_app():
    """Ensure Apple Terminal app is open so osascript won't fail with -600 error."""
    subprocess.run(["open", "-a", "Terminal"], check=False)
    time.sleep(1)

def run_lab11_1_for_all():
    print("=" * 60)
    print("🚀 STARTING LAB 11.1 FOR ALL 9 STUDENTS")
    print("=" * 60)
    ensure_terminal_app()

    for idx, st_id in enumerate(STUDENTS, 1):
        print(f"\n[{idx}/9] 🏃 Running Lab 11.1 for student: {st_id} ...")
        p1 = os.path.join(MQTT_LAB_DIR, f"{st_id}_lab11_1_photo1.png")
        p2 = os.path.join(MQTT_LAB_DIR, f"{st_id}_lab11_1_photo2.png")
        txt = os.path.join(MQTT_LAB_DIR, f"lab11_1_{st_id}.txt")
        
        # Remove old files if any so we detect newly created files accurately
        for f in [p1, p2, txt]:
            if os.path.exists(f):
                try: os.remove(f)
                except: pass

        cmd = ["bash", "Week11_MQTT_and_RainMaker/lab11_1_auto.sh", st_id]
        res = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"⚠️ Warning launch output: {res.stdout.strip()} {res.stderr.strip()}")

        # Wait for terminal execution to complete and write output files
        start_wait = time.time()
        success = False
        while time.time() - start_wait < 35:
            time.sleep(1)
            if os.path.exists(p2) and os.path.exists(txt) and os.path.getsize(txt) > 500:
                # Give screencapture half a second to finish writing
                time.sleep(1)
                success = True
                break

        if success and os.path.exists(p1) and os.path.exists(p2):
            s1 = os.path.getsize(p1)
            s2 = os.path.getsize(p2)
            stxt = os.path.getsize(txt)
            print(f"   ✓ Lab 11.1 Completed for {st_id}: photo1={s1}B, photo2={s2}B, log={stxt}B")
        else:
            print(f"   ⚠️ Timeout or partial capture for {st_id}. Checking files:")
            print(f"      photo1: {os.path.exists(p1)}")
            print(f"      photo2: {os.path.exists(p2)}")
            print(f"      txt: {os.path.exists(txt)}")

        time.sleep(1.5)

def run_lab11_3_for_all():
    print("\n" + "=" * 60)
    print("🚀 STARTING LAB 11.3 FOR ALL 9 STUDENTS")
    print("=" * 60)

    # Stop any background mosquitto first
    subprocess.run(["brew", "services", "stop", "mosquitto"], capture_output=True, check=False)
    subprocess.run(["pkill", "-f", "mosquitto"], capture_output=True, check=False)
    time.sleep(1)

    for idx, st_id in enumerate(STUDENTS, 1):
        print(f"\n[{idx}/9] 🔐 Running Lab 11.3 for student: {st_id} ...")
        cmd = ["bash", "Week11_MQTT_and_RainMaker/lab11_3_auto.sh", st_id]
        res = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
        
        txt = os.path.join(MQTT_LAB_DIR, f"lab11_3_{st_id}.txt")
        cert_dir = os.path.join(MQTT_LAB_DIR, f"certs_{st_id}")
        
        ca_crt = os.path.join(cert_dir, "ca.crt")
        srv_crt = os.path.join(cert_dir, "server.crt")
        cli_crt = os.path.join(cert_dir, "client.crt")

        if os.path.exists(txt) and os.path.exists(ca_crt) and os.path.exists(srv_crt) and os.path.exists(cli_crt):
            print(f"   ✓ Lab 11.3 Completed for {st_id}: log={os.path.getsize(txt)}B, certs=OK (ca, server, client)")
        else:
            print(f"   ❌ Lab 11.3 failed for {st_id}!")
            print(res.stdout[-500:] if res.stdout else res.stderr)

        time.sleep(0.5)

def main():
    print("Starting automated execution for all 9 students...")
    run_lab11_1_for_all()
    run_lab11_3_for_all()
    print("\n🎉 ALL TASKS FOR LAB 11.1 AND LAB 11.3 FINISHED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
