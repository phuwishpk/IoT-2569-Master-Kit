#!/usr/bin/env zsh
# ssh_deploy.sh — ส่งชุด IoT-2569-Master-Kit เข้าเครื่องเพื่อนผ่าน SSH แล้วเปิดหน้าต่างควบคุมทันที
# วิธีใช้:
#   ./ssh_deploy.sh user@192.168.1.55

if [ -z "$1" ]; then
  echo "วิธีใช้: ./ssh_deploy.sh <username@friend-ip>"
  echo "ตัวอย่าง: ./ssh_deploy.sh Acer@192.168.1.55"
  exit 1
fi

TARGET="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================================"
echo "📦 กำลังส่งโฟลเดอร์ IoT-2569-Master-Kit ไปยัง $TARGET ..."
echo "============================================================"

scp -r "$SCRIPT_DIR" "$TARGET:~/IoT-2569-Master-Kit"

echo "============================================================"
echo "✅ ส่งไฟล์เสร็จสมบูรณ์! กำลังเข้าสู่ระบบ SSH ของ $TARGET ..."
echo "💡 คำสั่งแนะนำเมื่อเข้าเครื่องเพื่อนแล้ว:"
echo "   cd ~/IoT-2569-Master-Kit"
echo "   python3 remote_doctor.py"
echo "   python3 setup_friend.py --id 67030XXX --name \"Somchai\" --thai-name \"นายสมชาย ใจดี\" --wifi \"Hotspot\" --pass \"12345678\""
echo "============================================================"

ssh -t "$TARGET"
