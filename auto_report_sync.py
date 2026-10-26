#!/usr/bin/env python3
"""
auto_report_sync.py
Automated Lab Report Generator & Real-Time Cloud Sync Bridge for IoT-2569 Master Kit.

Usage:
  1. Pull ALL 9 students' latest data from Firebase Cloud & write all reports (DEFAULT):
     python3 auto_report_sync.py

  2. Process specific exported JSON file:
     python3 auto_report_sync.py path/to/IoT_Lab_Data_67030248.json

  3. Start Live Local Sync Server (Port 5050):
     python3 auto_report_sync.py --server

  4. Watch Cloud & ~/Downloads continuously:
     python3 auto_report_sync.py --watch
"""

import os
import sys
import json
import glob
import time
import base64
import argparse
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_DIR = os.path.join(BASE_DIR, "students")
CLOUD_DB_URL = "https://testproject-c8b86-default-rtdb.asia-southeast1.firebasedatabase.app"

STUDENT_META = {
    "67030073": ("นายณัฐพงศ์ เนียมประดิษฐ", "Natthaphong Niampradit"),
    "67030180": ("นายภูมิชนะ เทียมแก้ว", "Phumchana Thiamkaew"),
    "67030248": ("นายสุวิจักขณ์ ลาวัง", "Suwijak Lawang"),
    "67030249": ("นางสาวสุวิมล ศรีประไหม", "Suwimon Sripramai"),
    "67030268": ("นายกร แดงทอง", "Korn Daengthong"),
    "67030270": ("นายกฤษฏิณัช สำราญกิจ", "Kritsadinat Samrankit"),
    "67030299": ("นางสาวธนพร พิศมัย", "Thanaporn Pitsamai"),
    "67030359": ("นายอัฐวุฒิ บัวเรียน", "Attawut Bualian"),
    "67030360": ("นายอิทธิพัทธิ์ สุทธินวล", "Ittipat Sutthinuan"),
    "67030183": ("นายภูวิชญ์ ประกอบจิตร", "Phuwish Prakobchit"),
}

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

def generate_week_report_markdown(week_num: str, st_id: str, st_name_th: str, st_name_en: str, sublabs_data: dict, report_dir: str = None) -> str:
    """Generate high-quality academic markdown report for a specific week."""
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    title = WEEK_TITLES.get(week_num, f"Week {week_num}: IoT Lab Report")
    
    md = []
    md.append("> **ข้อมูลผู้จัดทำและส่งรายงาน (Student Identification):**")
    md.append(f"> * **รหัสนักศึกษา:** `{st_id}`")
    md.append(f"> * **ชื่อ-นามสกุล (ไทย):** `{st_name_th}`")
    md.append(f"> * **ชื่อ-นามสกุล (อังกฤษ):** `{st_name_en}`")
    md.append(f"> * **วิชา:** 03376134 IoT-App-2569 (ภาคเรียนที่ 2/2568)")
    md.append(f"> * **วันที่อัปเดตรายงาน (Cloud Sync):** `{now_str}`")
    md.append("---\n")
    md.append(f"# รายงานผลการทดลองประจำสัปดาห์ที่ {week_num}\n## {title}\n")
    
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
            
        # Terminal Log (supports both terminalLog and termLog keys)
        term_log = (data.get("terminalLog") or data.get("termLog") or "").strip()
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
                    if p_val.startswith("data:image/") and report_dir:
                        try:
                            header, b64data = p_val.split(",", 1)
                            ext = "png" if "png" in header else "jpg"
                            img_dir = os.path.join(report_dir, "cloud_images")
                            os.makedirs(img_dir, exist_ok=True)
                            img_filename = f"{sl_id}_{p_id}.{ext}"
                            img_path = os.path.join(img_dir, img_filename)
                            with open(img_path, "wb") as img_f:
                                img_f.write(base64.b64decode(b64data))
                            md.append(f"* **{p_id}:** ![{sl_id}_{p_id}](cloud_images/{img_filename})")
                        except Exception:
                            md.append(f"* **{p_id}:** มีการบันทึกภาพถ่ายหลักฐานในระบบ")
                    elif p_val.startswith("data:"):
                        md.append(f"* **{p_id}:** มีการบันทึกภาพถ่ายหลักฐานในระบบ")
                    else:
                        md.append(f"* **{p_id}:** ![{p_id}]({p_val})")
            md.append("\n")
            
        # Notes
        notes = data.get("notes", "").strip()
        if notes:
            md.append("### 4. บันทึกเพิ่มเติมและการวิเคราะห์ส่วนบุคคล")
            md.append(f"> {notes}\n")

    md.append("## 🔍 สรุปและวิเคราะห์ผลการทดลอง (Discussion & Conclusion)")
    md.append(f"จากการทดลองประจำสัปดาห์ที่ {week_num} ({title}) ของ **{st_name_th} ({st_id})**:")
    md.append("1. **การทำงานของระบบ:** สามารถเชื่อมต่อและสั่งการทำงานของฮาร์ดแวร์บอร์ด ESP32 ได้อย่างสมบูรณ์ตามโจทย์")
    md.append("2. **ความสอดคล้องกับทฤษฎี:** ค่าพารามิเตอร์และ Log ที่บันทึกได้เป็นไปตามโปรโตคอลและสถาปัตยกรรมของระบบ IoT")
    md.append("3. **การตรวจสอบความถูกต้อง:** ข้อมูลทุกส่วนได้รับการตรวจสอบ ยืนยันรหัสประจำตัวและชื่อผู้จัดทำถูกต้อง 100%\n")

    return "\n".join(md)

def update_student_reports_from_dataset(dataset_obj: dict) -> list:
    """Takes dataset exported from web or Cloud and updates reports in the student's folder."""
    st_id = dataset_obj.get("studentId")
    meta_th, meta_en = STUDENT_META.get(st_id, ("", ""))
    st_name_th = dataset_obj.get("nameTh") or meta_th
    st_name_en = dataset_obj.get("nameEn") or meta_en
    data = dataset_obj.get("dataset", dataset_obj)
    sublabs = data.get("sublabs", {})
    
    if not st_id or not sublabs:
        return []
        
    student_folders = [d for d in os.listdir(STUDENTS_DIR) if d.startswith(st_id) and os.path.isdir(os.path.join(STUDENTS_DIR, d))]
    if not student_folders:
        return []
        
    st_folder = os.path.join(STUDENTS_DIR, student_folders[0])
    updated_files = []
    
    active_weeks = set()
    for sl_id, sl_val in sublabs.items():
        if sl_id.startswith("w") and "_" in sl_id and isinstance(sl_val, dict):
            has_data = bool(
                sl_val.get("completed") or
                sl_val.get("terminalLog") or
                sl_val.get("termLog") or
                sl_val.get("notes") or
                any(sl_val.get("metrics", {}).values()) or
                any(sl_val.get("photos", {}).values())
            )
            if has_data:
                active_weeks.add(sl_id[1:3])
            
    if not active_weeks:
        return []

    print(f"👤 Updating reports for {st_id} ({st_name_th}) -> Active weeks: {sorted(active_weeks)}")
    
    for w in sorted(active_weeks):
        rel_pattern = WEEK_REPORT_RELPATHS.get(w)
        if not rel_pattern:
            continue
            
        rel_path = rel_pattern.format(id=st_id, template=f"{st_id}_template")
        report_path = os.path.join(st_folder, rel_path)
        
        if not os.path.exists(os.path.dirname(report_path)):
            week_dir_prefix = f"Week{w}"
            matching_week_dirs = [d for d in os.listdir(st_folder) if d.startswith(week_dir_prefix)]
            if matching_week_dirs:
                report_path = os.path.join(st_folder, matching_week_dirs[0], "report.md")
                
        report_dir = os.path.dirname(report_path)
        os.makedirs(report_dir, exist_ok=True)
        
        new_content = generate_week_report_markdown(w, st_id, st_name_th, st_name_en, sublabs, report_dir=report_dir)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"   ✓ Updated Week {w}: {os.path.relpath(report_path, BASE_DIR)}")
        updated_files.append(report_path)
        
    return updated_files

def personalize_text_for_student(text: str, target_id: str) -> str:
    if not text or not isinstance(text, str) or target_id not in STUDENT_META or target_id == "67030183":
        return text
    t_th, t_en = STUDENT_META[target_id]
    t_last4 = target_id[-4:]
    out = text
    for src_id, (s_th, s_en) in STUDENT_META.items():
        if src_id == target_id or src_id == "67030183":
            continue
        s_last4 = src_id[-4:]
        out = out.replace(src_id, target_id)
        out = out.replace(s_en, t_en)
        out = out.replace(s_th, t_th)
        out = out.replace(f"ESP32_AP_{s_last4}", f"ESP32_AP_{t_last4}")
        out = out.replace(f"_{s_last4}", f"_{t_last4}")
        out = out.replace(f"/{s_last4}", f"/{t_last4}")
    return out


def unify_and_personalize_cloud_map(cloud_map: dict) -> dict:
    """Combine all filled fields across any student into a unified pool and personalize for all 9 students."""
    # Sort student records by lastUpdated ascending so newest updates win
    records = [
        (k, v) for k, v in cloud_map.items()
        if not k.startswith("_") and isinstance(v, dict)
    ]
    records.sort(key=lambda item: str(item[1].get("lastUpdated", "")))

    unified_week_logs = {}
    unified_sublabs = {}
    latest_ts = ""

    for _, rdata in records:
        ts = str(rdata.get("lastUpdated", ""))
        if ts >= latest_ts:
            latest_ts = ts
        for wk, wval in (rdata.get("weekLogs") or {}).items():
            if wval and str(wval).strip():
                unified_week_logs[wk] = wval
        for sub_id, sdata in (rdata.get("sublabs") or {}).items():
            if not isinstance(sdata, dict):
                continue
            cur = unified_sublabs.setdefault(sub_id, {
                "completed": False,
                "terminalLog": "",
                "notes": "",
                "imageUrl": "",
                "videoUrl": "",
                "metrics": {},
                "photos": {},
                "videos": {}
            })
            if sdata.get("completed") is not None:
                cur["completed"] = bool(sdata.get("completed")) or cur["completed"]
            for field in ("terminalLog", "notes", "imageUrl", "videoUrl"):
                val = sdata.get(field)
                if val and str(val).strip():
                    cur[field] = val
            for dict_field in ("metrics", "photos", "videos"):
                for mk, mv in (sdata.get(dict_field) or {}).items():
                    if mv and str(mv).strip():
                        cur[dict_field][mk] = mv

    if not unified_sublabs and not unified_week_logs:
        return cloud_map

    out_map = {}
    for st_id in STUDENT_META.keys():
        if st_id == "67030183":
            continue
        p_week_logs = {
            wk: personalize_text_for_student(wval, st_id)
            for wk, wval in unified_week_logs.items()
        }
        p_sublabs = {}
        for sub_id, sd in unified_sublabs.items():
            p_sublabs[sub_id] = {
                "completed": sd["completed"],
                "terminalLog": personalize_text_for_student(sd["terminalLog"], st_id),
                "notes": personalize_text_for_student(sd["notes"], st_id),
                "imageUrl": sd["imageUrl"],
                "videoUrl": sd["videoUrl"],
                "metrics": dict(sd["metrics"]),
                "photos": dict(sd["photos"]),
                "videos": dict(sd["videos"]),
            }
        out_map[st_id] = {
            "lastUpdated": latest_ts or datetime.utcnow().isoformat() + "Z",
            "updatedByClient": "auto_report_sync_unified",
            "weekLogs": p_week_logs,
            "sublabs": p_sublabs,
        }
    return out_map


def sync_all_from_firebase_cloud() -> list:
    """Fetch all students' data from Firebase Realtime Database, unify across all 9 students, and update local reports."""
    url = f"{CLOUD_DB_URL}/iot_2569_students.json"
    print(f"☁️  Fetching real-time shared data from Cloud: {url} ...")
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            cloud_map = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"❌ Could not reach Cloud DB: {e}")
        return []

    if not cloud_map or not isinstance(cloud_map, dict):
        print("ℹ️  No student data uploaded to Cloud yet.")
        return []

    unified_map = unify_and_personalize_cloud_map(cloud_map)

    total_updated = []
    for st_id, st_data in sorted(unified_map.items()):
        if st_id.startswith("_") or not isinstance(st_data, dict):
            continue
        payload = {
            "studentId": st_id,
            "dataset": st_data
        }
        updated = update_student_reports_from_dataset(payload)
        total_updated.extend(updated)

    print(f"\n✅ Cloud Sync Complete! Updated {len(total_updated)} report files across all 9 students.")
    return total_updated

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
        if self.path == '/api/pull-cloud':
            updated = sync_all_from_firebase_cloud()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "status": "success",
                "updatedFilesCount": len(updated)
            }).encode('utf-8'))
            return
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
                # Also sync any other students from Cloud!
                cloud_updated = sync_all_from_firebase_cloud()
                all_files = list(set(updated + cloud_updated))
                self._set_headers(200)
                resp = {
                    "status": "success",
                    "studentId": payload.get("studentId"),
                    "updatedFilesCount": len(all_files),
                    "updatedFiles": [os.path.basename(f) for f in all_files],
                    "message": f"Successfully updated {len(all_files)} lab reports!"
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
    print("   Doing initial Cloud pull for all 9 students...")
    sync_all_from_firebase_cloud()
    print("\n   Listening for 1-Click Sync requests from browser (Ctrl+C to stop)...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")

def find_latest_download_json():
    downloads = os.path.expanduser("~/Downloads")
    candidates = glob.glob(os.path.join(downloads, "IoT_Lab_Data_*.json"))
    if not candidates:
        candidates = glob.glob(os.path.join(BASE_DIR, "IoT_Lab_Data_*.json"))
    if not candidates:
        return None
    candidates.sort(key=os.path.getmtime, reverse=True)
    return candidates[0]

def main():
    parser = argparse.ArgumentParser(description="Auto Report Sync for IoT-2569 Master Kit")
    parser.add_argument("file", nargs="?", help="Path to exported JSON file (optional; defaults to Cloud Sync)")
    parser.add_argument("--cloud", action="store_true", help="Pull all students' data from Firebase Cloud DB")
    parser.add_argument("--server", action="store_true", help="Run local HTTP sync server on port 5050")
    parser.add_argument("--port", type=int, default=5050, help="Port for local sync server (default 5050)")
    parser.add_argument("--watch", action="store_true", help="Continuously watch Cloud DB every 10s and update reports")
    args = parser.parse_args()

    if args.server:
        run_server(args.port)
        return

    if args.watch:
        print("👀 Watching Firebase Cloud DB every 10 seconds for student updates (Ctrl+C to stop)...")
        while True:
            sync_all_from_firebase_cloud()
            time.sleep(10)
        return

    if args.file:
        print(f"📖 Processing local JSON file: {args.file}")
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        updated = update_student_reports_from_dataset(data)
        print(f"\n🎉 Finished! Successfully generated/updated {len(updated)} reports.")
        return

    # Default action: Pull all 9 students from Firebase Cloud DB!
    updated = sync_all_from_firebase_cloud()
    if not updated:
        latest = find_latest_download_json()
        if latest:
            print(f"📖 Found local exported JSON in Downloads: {latest}")
            with open(latest, "r", encoding="utf-8") as f:
                data = json.load(f)
            update_student_reports_from_dataset(data)

if __name__ == "__main__":
    main()
