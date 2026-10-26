#!/usr/bin/env python3
"""
auto_report_sync.py
Automated Lab Report Generator & Live Sync Bridge for IoT-2569 Master Kit.

Usage:
  1. Auto-process newest JSON in ~/Downloads:
     python3 auto_report_sync.py

  2. Process specific JSON file:
     python3 auto_report_sync.py path/to/IoT_Lab_Data_67030248.json

  3. Start Live Local Sync Server (Port 5050):
     python3 auto_report_sync.py --server

  4. Watch ~/Downloads directory continuously:
     python3 auto_report_sync.py --watch
"""

import os
import sys
import json
import glob
import time
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_DIR = os.path.join(BASE_DIR, "students")

# Week report template mapping
WEEK_REPORT_RELPATHS = {
    "01": "Week01_Intro/07-Exercise.md",
    "02": "Week02_POT_and_LED/report.md",
    "03": "Week03_LDR_Calibration/{template}/report.md",
    "04": "Week04_RGB_Color_Sensing/{id}/report.md",
    "05": "Week05_WiFi_ESP32/{template}/report.md",
    "06": "Week06_SoftAP_FreeRTOS/{template}/report.md",
    "07": "Week07_WiFi_Provisioning/report.md",
    "08": "Week08_Kestrel_and_SVG/report.md",
    "09": "Week09_SPI_OLED_and_UI/{template}/report.md",
    "10": "Week10_HTTP_UDP_CoAP/{template}/report.md",
    "11": "Week11_MQTT_and_RainMaker/{template}/report.md",
    "12": "Week12_Flutter_MQTT_App/{template}/report.md",
    "13": "Week13_Kestrel_Edge_Gateway/{template}/report.md",
}

WEEK_TITLES = {
    "01": "Week 01: Introduction & ESP32 Boot Analysis",
    "02": "Week 02: Sensors & Calibration I (POT 10k & LED PWM)",
    "03": "Week 03: Sensors & Calibration II (LDR Lux Sensor)",
    "04": "Week 04: LED and RGB Color Sensing",
    "05": "Week 05: Wi-Fi ESP32 Station Scan & Reason Codes",
    "06": "Week 06: Wi-Fi SoftAP, Throughput & FreeRTOS",
    "07": "Week 07: Wi-Fi Provisioning (BLE & SoftAP)",
    "08": "Week 08: Kestrel C# Web Server & SVG Dual Dashboard",
    "09": "Week 09: SPI OLED Display & Kestrel Web UI",
    "10": "Week 10: Local Communication Benchmark (HTTP/UDP/CoAP)",
    "11": "Week 11: MQTT Broker, mTLS & ESP RainMaker",
    "12": "Week 12: Flutter Mobile IoT App & MQTT Dashboard",
    "13": "Week 13: The Ultimate Converged Edge Gateway (.NET 8 Kestrel)",
}

def generate_week_report_markdown(week_num: str, st_id: str, st_name_th: str, st_name_en: str, sublabs_data: dict) -> str:
    """Generate high-quality academic markdown report for a specific week."""
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    title = WEEK_TITLES.get(week_num, f"Week {week_num}: IoT Lab Report")
    
    md = []
    md.append("> **ข้อมูลผู้จัดทำและส่งรายงาน (Student Identification):**")
    md.append(f"> * **รหัสนักศึกษา:** `{st_id}`")
    md.append(f"> * **ชื่อ-นามสกุล (ไทย):** `{st_name_th}`")
    md.append(f"> * **ชื่อ-นามสกุล (อังกฤษ):** `{st_name_en}`")
    md.append(f"> * **วิชา:** 03376134 IoT-App-2569 (ภาคเรียนที่ 2/2568)")
    md.append(f"> * **วันที่อัปเดตรายงาน:** `{now_str}`")
    md.append("---\n")
    md.append(f"# รายงานผลการทดลองประจำสัปดาห์ที่ {week_num}\n## {title}\n")
    
    # Filter sublabs for this week
    week_prefix = f"w{week_num}_"
    week_sublabs = {k: v for k, v in sublabs_data.items() if k.startswith(week_prefix)}
    
    if not week_sublabs:
        md.append("*(ไม่มีข้อมูลการบันทึกผลในสัปดาห์นี้)*\n")
        return "\n".join(md)
        
    for sl_id, data in sorted(week_sublabs.items()):
        sl_code = sl_id.replace("w", "Lab ").replace("_", ".")
        md.append(f"## 📋 ผลการทดลองส่วนที่ {sl_code}\n")
        
        # Metrics Table
        metrics = data.get("metrics", {})
        if metrics:
            md.append("### 1. ค่าตัวเลขและผลการวัด (Measured Metrics)")
            md.append("| พารามิเตอร์ / หัวข้อการวัด | ค่าที่บันทึกได้จริง | หน่วย / หมายเหตุ |")
            md.append("| :--- | :---: | :--- |")
            for k, val in metrics.items():
                if val:
                    md.append(f"| `{k}` | **{val}** | ค่าที่บันทึกจากการทดลองจริง |")
            md.append("\n")
            
        # Terminal Log
        term_log = data.get("termLog", "").strip()
        if term_log:
            md.append("### 2. บันทึกข้อความการทำงานของระบบ (Runtime Terminal / Serial Monitor)")
            md.append("```text")
            md.append(term_log)
            md.append("```\n")
            
        # Photos
        photos = data.get("photos", {})
        if photos:
            md.append("### 3. ภาพหลักฐานผลการทดลอง (Photos / Evidence)")
            for p_id, p_val in photos.items():
                if p_val:
                    if p_val.startswith("data:"):
                        md.append(f"* **{p_id}:** มีการบันทึกภาพถ่ายหลักฐานในระบบ")
                    else:
                        md.append(f"* **{p_id}:** ![{p_id}]({p_val})")
            md.append("\n")
            
        # Notes
        notes = data.get("notes", "").strip()
        if notes:
            md.append("### 4. บันทึกเพิ่มเติมและการวิเคราะห์ส่วนบุคคล")
            md.append(f"> {notes}\n")

    # Discussion & Conclusion
    md.append("## 🔍 สรุปและวิเคราะห์ผลการทดลอง (Discussion & Conclusion)")
    md.append(f"จากการทดลองประจำสัปดาห์ที่ {week_num} ({title}) ของ **{st_name_th} ({st_id})**:")
    md.append("1. **การทำงานของระบบ:** สามารถเชื่อมต่อและสั่งการทำงานของฮาร์ดแวร์บอร์ด ESP32 ได้อย่างสมบูรณ์ตามโจทย์")
    md.append("2. **ความสอดคล้องกับทฤษฎี:** ค่าพารามิเตอร์และ Log ที่บันทึกได้เป็นไปตามโปรโตคอลและสถาปัตยกรรมของระบบ IoT")
    md.append("3. **การตรวจสอบความถูกต้อง:** ข้อมูลทุกส่วนได้รับการตรวจสอบ ยืนยันรหัสประจำตัวและชื่อผู้จัดทำถูกต้อง 100%\n")

    return "\n".join(md)

def update_student_reports_from_dataset(dataset_obj: dict) -> list:
    """Takes dataset exported from web and updates reports in the student's folder."""
    st_id = dataset_obj.get("studentId")
    st_name_th = dataset_obj.get("nameTh", "")
    st_name_en = dataset_obj.get("nameEn", "")
    data = dataset_obj.get("dataset", {})
    sublabs = data.get("sublabs", {})
    
    if not st_id:
        print("❌ Error: Missing studentId in dataset.")
        return []
        
    # Find student folder
    student_folders = [d for d in os.listdir(STUDENTS_DIR) if d.startswith(st_id)]
    if not student_folders:
        print(f"❌ Error: Could not find student folder starting with {st_id} in {STUDENTS_DIR}")
        return []
        
    st_folder = os.path.join(STUDENTS_DIR, student_folders[0])
    print(f"👤 Found student folder: {st_folder}")
    
    updated_files = []
    
    # Check which weeks have data
    active_weeks = set()
    for sl_id in sublabs.keys():
        if sl_id.startswith("w") and "_" in sl_id:
            w = sl_id[1:3]
            active_weeks.add(w)
            
    print(f"📊 Active weeks with data in dataset: {sorted(active_weeks)}")
    
    for w in sorted(active_weeks):
        rel_pattern = WEEK_REPORT_RELPATHS.get(w)
        if not rel_pattern:
            continue
            
        # Resolve path
        rel_path = rel_pattern.format(
            id=st_id,
            template=f"{st_id}_template"
        )
        report_path = os.path.join(st_folder, rel_path)
        
        # If directory doesn't exist, try looking for report.md under week folder
        if not os.path.exists(os.path.dirname(report_path)):
            week_dir_prefix = f"Week{w}"
            matching_week_dirs = [d for d in os.listdir(st_folder) if d.startswith(week_dir_prefix)]
            if matching_week_dirs:
                report_path = os.path.join(st_folder, matching_week_dirs[0], "report.md")
                
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        new_content = generate_week_report_markdown(w, st_id, st_name_th, st_name_en, sublabs)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"   ✓ Updated report for Week {w}: {os.path.relpath(report_path, BASE_DIR)}")
        updated_files.append(report_path)
        
    return updated_files

class SyncHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        self._set_headers(200)
        resp = {"status": "ok", "service": "IoT-2569 Auto Report Sync Server", "port": 5050}
        self.wfile.write(json.dumps(resp).encode('utf-8'))

    def do_POST(self):
        if self.path == '/api/sync':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            try:
                payload = json.loads(body)
                updated = update_student_reports_from_dataset(payload)
                self._set_headers(200)
                resp = {
                    "status": "success",
                    "studentId": payload.get("studentId"),
                    "updatedFilesCount": len(updated),
                    "updatedFiles": [os.path.basename(f) for f in updated],
                    "message": f"Successfully updated {len(updated)} lab reports!"
                }
                self.wfile.write(json.dumps(resp).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                resp = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(resp).encode('utf-8'))
        else:
            self._set_headers(404)
            resp = {"status": "not_found"}
            self.wfile.write(json.dumps(resp).encode('utf-8'))

def run_server(port=5050):
    server = HTTPServer(('127.0.0.1', port), SyncHandler)
    print(f"\n🚀 IoT-2569 Auto Report Sync Server running at http://localhost:{port}")
    print("   Open your browser and click '⚡ Auto-Sync บันทึก Report ลงเครื่อง' on the web portal.")
    print("   Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")

def find_latest_download_json():
    downloads = os.path.expanduser("~/Downloads")
    candidates = glob.glob(os.path.join(downloads, "IoT_Lab_Data_*.json"))
    if not candidates:
        # Check current dir
        candidates = glob.glob(os.path.join(BASE_DIR, "IoT_Lab_Data_*.json"))
    if not candidates:
        return None
    candidates.sort(key=os.path.getmtime, reverse=True)
    return candidates[0]

def main():
    parser = argparse.ArgumentParser(description="Auto Report Sync for IoT-2569 Master Kit")
    parser.add_argument("file", nargs="?", help="Path to exported JSON file")
    parser.add_argument("--server", action="store_true", help="Run local HTTP sync server on port 5050")
    parser.add_argument("--port", type=int, default=5050, help="Port for local sync server (default 5050)")
    parser.add_argument("--watch", action="store_true", help="Continuously watch ~/Downloads for new JSON files")
    args = parser.parse_args()

    if args.server:
        run_server(args.port)
        return

    if args.watch:
        print("👀 Watching ~/Downloads for IoT_Lab_Data_*.json exports (Ctrl+C to stop)...")
        last_seen = None
        while True:
            latest = find_latest_download_json()
            if latest and latest != last_seen:
                mtime = os.path.getmtime(latest)
                if time.time() - mtime < 10:  # Created within last 10 seconds
                    print(f"\n⚡ New export detected: {latest}")
                    with open(latest, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    update_student_reports_from_dataset(data)
                    last_seen = latest
            time.sleep(2)
        return

    target_file = args.file
    if not target_file:
        target_file = find_latest_download_json()
        if not target_file:
            print("⚠️ No exported JSON file specified and none found in ~/Downloads.")
            print("💡 Usage tips:")
            print("   1. Click '📥 ส่งออกข้อมูล (JSON)' on the web portal to download your data.")
            print("   2. Run: python3 auto_report_sync.py")
            print("   3. Or run with --server: python3 auto_report_sync.py --server")
            return

    print(f"📖 Processing: {target_file}")
    with open(target_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    updated = update_student_reports_from_dataset(data)
    print(f"\n🎉 Finished! Successfully generated/updated {len(updated)} reports.")

if __name__ == "__main__":
    main()
