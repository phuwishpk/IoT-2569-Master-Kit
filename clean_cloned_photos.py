#!/usr/bin/env python3
"""
Clean Cloned Photos Script
Removes mirrored photos/links from students who didn't upload them,
keeping student 67030248's authentic uploads intact.
Ensures every student has clean, independent photo and link slots.
"""

import json
import urllib.request

FIREBASE_URL = "https://testproject-c8b86-default-rtdb.asia-southeast1.firebasedatabase.app/iot_2569_students.json"
ORIGINAL_UPLOADER_ID = "67030248"

def main():
    import sys, time
    # ⚠️ GUARD (เพิ่ม 2026-10-26): สคริปต์นี้ลบรูป/ลิงก์ของ "ทุกคนยกเว้น 67030248" และเขียนทับฐานข้อมูลทั้งก้อนด้วย PUT
    # ถ้ามีใครกำลังแก้ข้อมูลอยู่ตอนรัน ข้อมูลนั้นจะหายทันที — ให้ใช้ find_cloned_links.py แทน (ตรวจก่อน/ลบเฉพาะช่องที่ซ้ำ)
    if "--force" not in sys.argv:
        print("⛔ สคริปต์นี้อันตราย: จะลบรูป/ลิงก์ของนักศึกษาทุกคน (ยกเว้น 67030248) และเขียนทับทั้งฐานข้อมูล")
        print("   แนะนำให้ใช้:  python3 find_cloned_links.py   (รายงานอย่างเดียว ไม่แก้ข้อมูล)")
        print("   ถ้าจำเป็นต้องรันจริง ๆ ให้ใส่ --force")
        return
    print(f"Fetching cloud data from {FIREBASE_URL}...")
    req = urllib.request.Request(FIREBASE_URL)
    with urllib.request.urlopen(req, timeout=15) as resp:
        cloud_data = json.loads(resp.read().decode("utf-8"))

    backup_name = time.strftime("cloud_backup_before_clean_%Y%m%d_%H%M%S.json")
    with open(backup_name, "w", encoding="utf-8") as bf:
        json.dump(cloud_data, bf, ensure_ascii=False)
    print(f"💾 Backup of the original cloud data saved to {backup_name}")

    if not cloud_data:
        print("No cloud data found.")
        return

    cleaned_count = 0
    for st_id, st_val in cloud_data.items():
        if st_id.startswith("_") or not isinstance(st_val, dict):
            continue
        
        if st_id == ORIGINAL_UPLOADER_ID:
            print(f"Keeping authentic uploads for original uploader: {st_id}")
            continue

        sublabs = st_val.get("sublabs", {})
        st_cleaned_photos = 0
        for sub_id, sub_data in sublabs.items():
            if not isinstance(sub_data, dict):
                continue
            
            # If photos exist, clear them
            if "photos" in sub_data and sub_data["photos"]:
                st_cleaned_photos += len(sub_data["photos"])
                sub_data["photos"] = {}

            # If imageUrl exists, clear it
            if sub_data.get("imageUrl"):
                sub_data["imageUrl"] = ""

            # If videoUrl exists and was cloned, clear it
            if sub_data.get("videoUrl"):
                sub_data["videoUrl"] = ""

        if st_cleaned_photos > 0:
            print(f"Cleaned {st_cleaned_photos} cloned photo slots for Student {st_id}")
            cleaned_count += st_cleaned_photos

    print(f"\nTotal cloned photo slots cleaned: {cleaned_count}")
    print("Writing updated independent data back to Firebase...")

    data_bytes = json.dumps(cloud_data).encode("utf-8")
    put_req = urllib.request.Request(
        FIREBASE_URL,
        data=data_bytes,
        headers={"Content-Type": "application/json"},
        method="PUT"
    )

    with urllib.request.urlopen(put_req, timeout=15) as resp:
        print(f"Firebase response code: {resp.status}")

    print("Firebase Cloud DB successfully cleaned! Verification:")
    verify_req = urllib.request.Request(FIREBASE_URL)
    with urllib.request.urlopen(verify_req, timeout=15) as resp:
        verified_data = json.loads(resp.read().decode("utf-8"))
        for sid, sval in verified_data.items():
            if sid.startswith("_") or not isinstance(sval, dict):
                continue
            p_count = sum(len(sub.get("photos", {})) for sub in sval.get("sublabs", {}).values() if isinstance(sub, dict))
            print(f"  Student {sid}: {p_count} photos stored.")

if __name__ == "__main__":
    main()
