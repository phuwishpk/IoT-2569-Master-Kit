#!/usr/bin/env python3
"""
find_cloned_links.py — ตรวจหา "ลิงก์ YouTube / ลิงก์รูป / รูปอัปโหลด" ที่ซ้ำกันข้ามนักศึกษาใน Firebase
(อาการ: ลิงก์ของคนหนึ่งไปโผล่ในโปรไฟล์ของคนอื่น)

ความปลอดภัยของข้อมูล:
  * ค่าเริ่มต้น = รายงานอย่างเดียว ไม่แก้อะไรบน Cloud
  * ก่อนแก้ไขทุกครั้ง จะดาวน์โหลดสำรองทั้งฐานข้อมูลเป็นไฟล์ cloud_backup_*.json ก่อนเสมอ
  * ลบเฉพาะช่องที่ซ้ำ ของคนที่คุณสั่งเท่านั้น ด้วย PATCH ทีละช่อง (ไม่ใช้ PUT ทับทั้งก้อน)
  * ต้องพิมพ์ YES ยืนยันก่อนลบ

วิธีใช้:
  python3 find_cloned_links.py                         # ดูรายงานลิงก์ที่ซ้ำกัน
  python3 find_cloned_links.py --videos-only           # ดูเฉพาะลิงก์วิดีโอ
  python3 find_cloned_links.py --keep 67030248         # เก็บของ 67030248 ไว้ ลบช่องที่ซ้ำออกจากคนอื่นในกลุ่มเดียวกัน
  python3 find_cloned_links.py --keep 67030248 --only-from 67030249 --only-from 67030250
"""
import argparse, hashlib, json, sys, time, urllib.request

DB_ROOT = "https://testproject-c8b86-default-rtdb.asia-southeast1.firebasedatabase.app"
NODE = "iot_2569_students"


def http(method, url, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else None


def fingerprint(value):
    v = str(value).strip()
    if v.startswith("data:"):
        return "upload-sha1:" + hashlib.sha1(v.encode("utf-8")).hexdigest()[:16]
    return v.rstrip("/")


def collect(cloud, videos_only):
    groups = {}
    for st_id, st in (cloud or {}).items():
        if st_id.startswith("_") or not isinstance(st, dict):
            continue
        for sub_id, sub in (st.get("sublabs") or {}).items():
            if not isinstance(sub, dict):
                continue
            fields = []
            for vid, url in (sub.get("videos") or {}).items():
                fields.append((f"sublabs/{sub_id}/videos/{vid}", url, "video"))
            if sub.get("videoUrl"):
                fields.append((f"sublabs/{sub_id}/videoUrl", sub["videoUrl"], "video"))
            if not videos_only:
                for pid, url in (sub.get("photos") or {}).items():
                    fields.append((f"sublabs/{sub_id}/photos/{pid}", url, "photo"))
                if sub.get("imageUrl"):
                    fields.append((f"sublabs/{sub_id}/imageUrl", sub["imageUrl"], "photo"))
            for path, val, kind in fields:
                if val is None or str(val).strip() == "":
                    continue
                groups.setdefault((kind, fingerprint(val)), []).append((st_id, path, val))
    # เก็บเฉพาะค่าที่อยู่ในมากกว่า 1 คน
    return {k: v for k, v in groups.items() if len({s for s, _, _ in v}) > 1}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--videos-only", action="store_true", help="ตรวจเฉพาะลิงก์วิดีโอ")
    ap.add_argument("--keep", metavar="STUDENT_ID", help="รหัสนักศึกษาเจ้าของตัวจริง (เก็บไว้) — คนอื่นในกลุ่มเดียวกันจะถูกลบช่องที่ซ้ำ")
    ap.add_argument("--only-from", metavar="STUDENT_ID", action="append", default=[], help="จำกัดว่าจะลบจากรหัสไหนบ้าง (ใส่ซ้ำได้)")
    args = ap.parse_args()

    print("⏬ กำลังดาวน์โหลดข้อมูลจาก Cloud ...")
    cloud = http("GET", f"{DB_ROOT}/{NODE}.json") or {}
    dups = collect(cloud, args.videos_only)

    if not dups:
        print("✅ ไม่พบลิงก์/รูปที่ซ้ำกันข้ามนักศึกษา")
        return

    print(f"\n⚠️  พบ {len(dups)} ค่า ที่ซ้ำกันในหลายโปรไฟล์:\n")
    for (kind, fp), items in sorted(dups.items(), key=lambda kv: (kv[0][0], -len(kv[1]))):
        shown = fp if not fp.startswith("upload-sha1:") else f"(รูปที่อัปโหลด {fp})"
        print(f"[{kind}] {shown}")
        for st_id, path, _ in sorted(items):
            print(f"     - {st_id}  {path}")
        print()

    if not args.keep:
        print("ℹ️  โหมดรายงานอย่างเดียว ไม่ได้แก้ไขอะไร")
        print("   ถ้ารู้ว่าใครเป็นเจ้าของตัวจริง ให้รันซ้ำพร้อม --keep <รหัส> เพื่อลบช่องที่ซ้ำออกจากคนอื่น")
        return

    plan = {}
    for (_, _), items in dups.items():
        owners = {s for s, _, _ in items}
        if args.keep not in owners:
            continue
        for st_id, path, _ in items:
            if st_id == args.keep:
                continue
            if args.only_from and st_id not in args.only_from:
                continue
            plan.setdefault(st_id, {})[path] = None

    if not plan:
        print(f"ไม่มีช่องที่ต้องลบสำหรับ --keep {args.keep}")
        return

    total = sum(len(p) for p in plan.values())
    print(f"🧹 จะลบ {total} ช่อง ออกจาก {len(plan)} คน (เก็บของ {args.keep} ไว้):")
    for st_id, ops in sorted(plan.items()):
        for path in sorted(ops):
            print(f"     - {st_id}/{path}")

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = f"cloud_backup_{stamp}.json"
    with open(backup, "w", encoding="utf-8") as f:
        json.dump(cloud, f, ensure_ascii=False, indent=2)
    print(f"\n💾 สำรองข้อมูลทั้งหมดไว้ที่ {backup} แล้ว (ใช้กู้คืนได้)")

    if input("พิมพ์ YES เพื่อยืนยันการลบ: ").strip() != "YES":
        print("ยกเลิก — ไม่ได้แก้ไขอะไรบน Cloud")
        return

    for st_id, ops in plan.items():
        payload = dict(ops)
        payload["lastUpdated"] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        payload["updatedByClient"] = "find_cloned_links.py"
        http("PATCH", f"{DB_ROOT}/{NODE}/{st_id}.json", payload)
        print(f"  ✓ {st_id}: ลบ {len(ops)} ช่อง")
    print("เสร็จสิ้น ✅")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
