#!/usr/bin/env bash
# Lab 12.4 (End-to-End: แอป Flutter + บอร์ด ESP32) — เปิดทุกอย่างในคำสั่งเดียว พร้อมชื่อสมาชิกกลุ่มบนจอแอป
# ใช้: bash lab12_4_auto.sh <รหัส1> <รหัส2> [<รหัส3> <รหัส4>] [--mock] [--app-only]
#   --mock      ไม่มีบอร์ด: ใช้ mock_esp32.py จำลองบอร์ดแทน (ทางเลือก B ในใบงาน)
#   --app-only  เปิดแค่แอป ใช้ Broker ที่เปิดอยู่แล้ว (เช่น Kestrel Gateway ของ Lab 13 ตอนถ่ายคลิป 13.4)
set -u
# ---- รายชื่อกลุ่ม (รหัส -> ชื่อไทย) ----
roster_th() {
  case "$1" in
    67030073) echo "ณัฐพงศ์ เนียมประดิษฐ";;
    67030180) echo "ภูมิชนะ เทียมแก้ว";;
    67030183) echo "ภูวิชญ์ ประกอบจิตร";;
    67030248) echo "สุวิจักขณ์ ลาวัง";;
    67030249) echo "สุวิมล ศรีประไหม";;
    67030268) echo "กร แดงทอง";;
    67030270) echo "กฤษฏิณัช สำราญกิจ";;
    67030299) echo "ธนพร พิศมัย";;
    67030359) echo "อัฐวุฒิ บัวเรียน";;
    67030360) echo "อิทธิพัทธิ์ สุทธินวล";;
  esac
}
# อ่านรหัสสมาชิก (รับแบบ 67030183 หรือ 67030183_Name ก็ได้) และตัวเลือกที่ขึ้นต้นด้วย --
IDS=(); OPTS=()
for a in "$@"; do
  case "$a" in
    --*) OPTS+=("$a");;
    *) i="$(printf '%s' "$a" | grep -oE '^[0-9]{8}' || true)"; [ -n "$i" ] && IDS+=("$i") || echo "ℹ️  ข้าม '$a' (ไม่ใช่รหัส 8 หลัก)";;
  esac
done
has_opt() { local o; for o in "${OPTS[@]:-}"; do [ "$o" = "$1" ] && return 0; done; return 1; }
opt_val() { local o; for o in "${OPTS[@]:-}"; do case "$o" in "$1"=*) echo "${o#*=}"; return 0;; esac; done; return 1; }
GROUP_TXT=""; GROUP_IDS=""
for i in "${IDS[@]:-}"; do
  [ -z "$i" ] && continue
  n="$(roster_th "$i")"; [ -z "$n" ] && echo "ℹ️  รหัส $i ไม่อยู่ในรายชื่อ — แสดงแค่รหัส"
  GROUP_TXT="${GROUP_TXT:+$GROUP_TXT|}$i${n:+ $n}"; GROUP_IDS="${GROUP_IDS:+$GROUP_IDS,}$i"
done

if [ "${#IDS[@]}" -lt 2 ]; then echo "❌ ใส่รหัสนักศึกษาของทุกคนในกลุ่ม (อย่างน้อย 2 คน) เช่น  bash $0 67030183 67030248 67030249 [--mock] [--app-only]"; exit 1; fi
MOCK=0; APPONLY=0; has_opt --mock && MOCK=1; has_opt --app-only && APPONLY=1
printf '\033]0;Lab 12.4 — กลุ่ม %s\007' "$GROUP_IDS"
say() { printf '\033[1;36m▶ %s\033[0m\n' "$1"; }
ok()  { printf '\033[1;32m✅ %s\033[0m\n' "$1"; }
die() { printf '\033[1;31m❌ %s\033[0m\n' "$1"; exit 1; }

DIR="$(cd "$(dirname "$0")" && pwd)"
LAB4="$(ls -d "$DIR"/67030183_template/Lab12-4 "$DIR"/*_template/Lab12-4 2>/dev/null | head -1)"
[ -n "$LAB4" ] || die "ไม่พบโฟลเดอร์ Lab12-4"
APP="$LAB4/iot_unified_dashboard"
OUTD="$HOME/mqtt_lab"; mkdir -p "$OUTD"; TAG="$(printf '%s' "$GROUP_IDS" | tr ',' '_')"
BLOG="$OUTD/.broker124_$TAG.log"; LOG="$OUTD/lab12_4_group_$TAG.txt"
command -v flutter >/dev/null || die "ไม่พบ flutter"
xcodebuild -version >/dev/null 2>&1 || die "แอป macOS ต้องใช้ Xcode — ติดตั้ง Xcode จาก App Store แล้วรัน: sudo xcode-select -s /Applications/Xcode.app"
LANIP="$( (ipconfig getifaddr en0 || ipconfig getifaddr en1 || hostname -I | awk '{print $1}') 2>/dev/null | head -1)"

MYB=""; SIM=""; PROC=""; SUBP=""
cleanup() {
  [ -n "$SUBP" ] && kill "$SUBP" 2>/dev/null
  [ -n "$SIM" ] && kill "$SIM" 2>/dev/null
  [ -n "$PROC" ] && pkill -f "$PROC.app/Contents/MacOS" 2>/dev/null
  [ -n "$MYB" ] && kill "$MYB" 2>/dev/null
}
trap cleanup EXIT
open_port() { (echo > "/dev/tcp/$1/$2") 2>/dev/null; }

echo "👥 กลุ่ม: ${GROUP_TXT//|/  •  }"
say "1/5 Broker MQTT พอร์ต 1883"
if [ "$APPONLY" = "1" ]; then
  open_port 127.0.0.1 1883 || die "ไม่มี Broker ที่ 1883 — เปิด Kestrel Gateway (lab13_3_auto.sh) ก่อน หรือรันโดยไม่ใส่ --app-only"
  ok "ใช้ Broker ที่เปิดอยู่แล้ว"
elif open_port 127.0.0.1 1883; then
  if [ "$MOCK" = "0" ] && [ -n "$LANIP" ] && ! open_port "$LANIP" 1883; then
    die "Broker ที่เปิดอยู่รับเฉพาะเครื่องนี้ บอร์ดจะต่อไม่ได้ — ปิดก่อนด้วย: brew services stop mosquitto แล้วรันคำสั่งนี้ใหม่"
  fi
  ok "ใช้ Broker ที่เปิดอยู่แล้ว"
else
  MOSQ="$(command -v mosquitto || true)"; [ -z "$MOSQ" ] && command -v brew >/dev/null && MOSQ="$(brew --prefix)/sbin/mosquitto"
  [ -x "$MOSQ" ] || die "ไม่พบ Mosquitto — brew install mosquitto"
  printf 'listener 1883 0.0.0.0\nallow_anonymous true\nlog_type all\n' > "$OUTD/mosquitto_124.conf"
  "$MOSQ" -c "$OUTD/mosquitto_124.conf" -v > "$BLOG" 2>&1 & MYB=$!
  for i in $(seq 1 25); do grep -q running "$BLOG" && break; sleep 0.2; done
  grep -q running "$BLOG" || { cat "$BLOG"; die "เปิด Broker ไม่สำเร็จ"; }
  ok "เปิด Broker ให้บอร์ดต่อได้ที่ ${LANIP:-<IP เครื่องนี้>}:1883 (ถ้า macOS ถามเรื่องรับการเชื่อมต่อเข้า ให้กดอนุญาต)"
fi

cd "$APP" || exit 1
say "2/5 เตรียมแอปให้รันบน macOS (ทำครั้งแรกครั้งเดียว)"
if [ ! -d macos ]; then flutter create --platforms=macos . >/dev/null || die "flutter create ไม่สำเร็จ"; fi
for f in macos/Runner/DebugProfile.entitlements macos/Runner/Release.entitlements; do
  /usr/libexec/PlistBuddy -c "Print :com.apple.security.network.client" "$f" >/dev/null 2>&1 \
    || /usr/libexec/PlistBuddy -c "Add :com.apple.security.network.client bool true" "$f"
done
ok "พร้อม"

say "3/5 Build แอปพร้อมชื่อกลุ่มบนหัวจอ (ครั้งแรกอาจใช้ 1–3 นาที)"
flutter build macos --debug --dart-define=GROUP="$GROUP_TXT" > "$OUTD/.build124.log" 2>&1 || { tail -25 "$OUTD/.build124.log"; die "build ไม่สำเร็จ"; }
APPB="$(ls -d build/macos/Build/Products/Debug/*.app | head -1)"; PROC="$(basename "$APPB" .app)"
pkill -f "$PROC.app/Contents/MacOS" 2>/dev/null
ok "build เสร็จ"

say "4/5 อุปกรณ์ ESP32"
FW="$LAB4/esp32_firmware/main/main.c"
if [ "$APPONLY" = "1" ]; then
  echo "   ใช้บอร์ดที่ต่อกับ Kestrel Gateway อยู่แล้ว"
elif [ "$MOCK" = "1" ]; then
  python3 -c "import paho.mqtt.client as m; m.CallbackAPIVersion" 2>/dev/null \
    || python3 -m pip install --user -q "paho-mqtt>=2" 2>/dev/null \
    || python3 -m pip install -q --break-system-packages "paho-mqtt>=2" || die "ติดตั้ง paho-mqtt ไม่สำเร็จ"
  python3 -u "$LAB4/mock_esp32.py" > "$OUTD/.mock124.log" 2>&1 & SIM=$!
  ok "เปิดบอร์ดจำลอง (mock_esp32.py) แล้ว"
else
  CUR="$(grep -E '^#define (WIFI_SSID|MQTT_BROKER_URI)' "$FW" 2>/dev/null | sed 's/^/      /')"
  echo "   ตั้งค่าในเฟิร์มแวร์ $FW ให้ตรงกับเครื่องนี้:"
  echo "      #define WIFI_SSID        \"<Wi-Fi วงเดียวกับ Mac เครื่องนี้>\""
  echo "      #define WIFI_PASS        \"<รหัส Wi-Fi>\""
  echo "      #define MQTT_BROKER_URI  \"mqtt://${LANIP:-<IP เครื่องนี้>}:1883\""
  echo "   ค่าปัจจุบันในไฟล์:"; echo "$CUR"
  echo "   แล้วแฟลชในอีก Terminal:  cd \"$LAB4/esp32_firmware\" && idf.py build && idf.py -p <PORT> flash monitor"
fi

say "5/5 เปิดแอป"
open -n "$APPB"
ok "เปิดแอปแล้ว — ชื่อกลุ่มอยู่แถบบนสุดของแอป"
echo
printf '\033[1;33m🎥 พร้อมถ่ายคลิป 12.4: ถ่ายให้เห็นจอแอป (มีชื่อกลุ่ม) กับบอร์ดพร้อมกัน แตะสวิตช์ในแท็บ Actuator Switch ให้ไฟบนบอร์ดติด/ดับ และหมุน POT ให้เข็ม Gauge ขยับ\033[0m\n'
echo "ข้อความ MQTT ที่วิ่งจริง (กด Ctrl+C เมื่อถ่ายเสร็จ — สคริปต์จะปิดแอปและ Broker ให้):"
{ echo "══════ Lab 12.4 — กลุ่ม ${GROUP_TXT//|/, } ══════"; echo "เครื่อง: $(whoami)@$(hostname)   เวลา: $(date '+%Y-%m-%d %H:%M:%S')"; } > "$LOG"
if command -v mosquitto_sub >/dev/null; then
  mosquitto_sub -h 127.0.0.1 -p 1883 -t 'iot/esp32/#' -v 2>&1 | while IFS= read -r line; do printf '[%s] %s\n' "$(date +%H:%M:%S)" "$line"; done | tee -a "$LOG" &
  SUBP=$!
fi
wait
