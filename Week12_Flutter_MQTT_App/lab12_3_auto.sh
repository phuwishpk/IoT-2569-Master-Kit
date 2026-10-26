#!/usr/bin/env bash
# Lab 12.3 (Realtime Telemetry Dashboard & Radial Gauge) — คำสั่งเดียว แต่ละคนรันเอง
# ใช้: bash lab12_3_auto.sh <รหัสนักศึกษา> "<ชื่อ-นามสกุล>"
# ได้: ~/mqtt_lab/<รหัส>_lab12_3_photo1.png (หน้าต่างแอปที่มีรหัส/ชื่อบนแถบหัว) และ ~/mqtt_lab/lab12_3_<รหัส>.txt
set -u
ID="${1:-}"; NAME="${2:-}"
[ -z "$ID" ] && { echo "ใช้: bash $0 <รหัสนักศึกษา> \"<ชื่อ-นามสกุล>\""; exit 1; }
WHO="$ID${NAME:+ $NAME}"
printf '\033]0;Lab 12.3 — %s\007' "$WHO"
say() { printf '\033[1;36m▶ %s\033[0m\n' "$1"; }
ok()  { printf '\033[1;32m✅ %s\033[0m\n' "$1"; }
die() { printf '\033[1;31m❌ %s\033[0m\n' "$1"; exit 1; }

DIR="$(cd "$(dirname "$0")" && pwd)"
APP="$(ls -d "$DIR"/${ID}_*/Lab12-3/iot_telemetry_gauge "$DIR"/67030183_template/Lab12-3/iot_telemetry_gauge 2>/dev/null | head -1)"
[ -n "$APP" ] || die "ไม่พบโฟลเดอร์ Lab12-3/iot_telemetry_gauge"
OUTD="$HOME/mqtt_lab"; mkdir -p "$OUTD"
PHOTO="$OUTD/${ID}_lab12_3_photo1.png"; LOG="$OUTD/lab12_3_${ID}.txt"; SIMLOG="$OUTD/.sim_${ID}.log"
command -v flutter >/dev/null || die "ไม่พบ flutter"
command -v python3 >/dev/null || die "ไม่พบ python3"
xcodebuild -version >/dev/null 2>&1 || die "แอป macOS ต้องใช้ Xcode — ติดตั้ง Xcode จาก App Store แล้วรัน: sudo xcode-select -s /Applications/Xcode.app"

MYB=""; SIM=""; PROC=""
cleanup() {
  if [ -n "$PROC" ]; then osascript -e "tell application \"$PROC\" to quit" >/dev/null 2>&1; sleep 1; pkill -f "$PROC.app/Contents/MacOS" 2>/dev/null; fi
  [ -n "$SIM" ] && kill "$SIM" 2>/dev/null
  [ -n "$MYB" ] && kill "$MYB" 2>/dev/null
}
trap cleanup EXIT

say "1/6 ตรวจ Broker พอร์ต 1883 (แอปตั้งค่าไว้ที่ 127.0.0.1:1883)"
if (echo > /dev/tcp/127.0.0.1/1883) 2>/dev/null; then ok "มี Broker ทำงานอยู่แล้ว"
else
  MOSQ="$(command -v mosquitto || true)"; [ -z "$MOSQ" ] && command -v brew >/dev/null && MOSQ="$(brew --prefix)/sbin/mosquitto"
  [ -x "$MOSQ" ] || die "ไม่พบ Mosquitto — brew install mosquitto"
  "$MOSQ" -p 1883 > "$OUTD/.broker12_${ID}.log" 2>&1 & MYB=$!; sleep 1; ok "เปิด Broker ชั่วคราวแล้ว"
fi

cd "$APP"
say "2/6 เตรียมแอปให้รันบน macOS (ทำครั้งแรกครั้งเดียว)"
if [ ! -d macos ]; then flutter create --platforms=macos . >/dev/null || die "flutter create ไม่สำเร็จ"; fi
for f in macos/Runner/DebugProfile.entitlements macos/Runner/Release.entitlements; do
  /usr/libexec/PlistBuddy -c "Print :com.apple.security.network.client" "$f" >/dev/null 2>&1 \
    || /usr/libexec/PlistBuddy -c "Add :com.apple.security.network.client bool true" "$f"
done
ok "พร้อม"

say "3/6 ตรวจไลบรารี paho-mqtt สำหรับตัวจำลอง"
python3 -c "import paho.mqtt.client as m; m.CallbackAPIVersion" 2>/dev/null \
  || python3 -m pip install --user -q "paho-mqtt>=2" 2>/dev/null \
  || python3 -m pip install -q --break-system-packages "paho-mqtt>=2" || die "ติดตั้ง paho-mqtt ไม่สำเร็จ"
ok "พร้อม"

say "4/6 Build แอปพร้อมแสดง \"$WHO\" บนแถบหัว (ครั้งแรกอาจใช้ 1–3 นาที)"
flutter build macos --debug --dart-define=STUDENT="$WHO" > "$OUTD/.build12_${ID}.log" 2>&1 || { tail -20 "$OUTD/.build12_${ID}.log"; die "build ไม่สำเร็จ"; }
APPB="$(ls -d build/macos/Build/Products/Debug/*.app | head -1)"; PROC="$(basename "$APPB" .app)"
ok "build เสร็จ: $PROC"

say "5/6 เปิดตัวจำลองส่งค่า Telemetry และเปิดแอป"
python3 -u pyTeleSim.py > "$SIMLOG" 2>&1 & SIM=$!
open -n "$APPB"; sleep 9
grep -q Published "$SIMLOG" || die "ตัวจำลองส่งค่าไม่ได้ — ดู $SIMLOG"

say "6/6 แคปหน้าต่างแอป"
osascript -e "tell application \"$PROC\" to activate" >/dev/null 2>&1; sleep 1
B="$(osascript -e "tell application \"System Events\" to tell process \"$PROC\" to get {position, size} of window 1" 2>/dev/null | tr -d ' ')"
[ -n "$B" ] && screencapture -x -o -R"$B" "$PHOTO" 2>/dev/null
if [ ! -s "$PHOTO" ]; then
  printf '\033[1;33m👆 คลิกที่หน้าต่างแอป Flutter 1 ครั้งเพื่อแคป\033[0m\n'
  screencapture -W -o "$PHOTO"
fi
[ -s "$PHOTO" ] && ok "บันทึกรูปแล้ว: $PHOTO" || echo "⚠️ ยังไม่ได้รูป — กด Cmd+Shift+4 แล้ว Space แล้วคลิกหน้าต่างแอป"

{
  echo "══════ Lab 12.3 — $WHO ══════"
  echo "เครื่อง: $(whoami)@$(hostname)   เวลา: $(date '+%Y-%m-%d %H:%M:%S')   Flutter: $(flutter --version 2>/dev/null | head -1)"
  echo "--- ข้อความที่ตัวจำลองส่งไปยัง iot/esp32/telemetry ---"
  tail -n 15 "$SIMLOG"
} > "$LOG"
ok "Log สำหรับช่อง 💻 Lab 12.3: $LOG"
