#!/usr/bin/env bash
# Lab 11.1 (Mosquitto Broker & MQTT Fundamentals) — รันทุกกิจกรรมในคำสั่งเดียว
# ใช้: ./lab11_1_auto.sh <รหัสนักศึกษา> "<ชื่อ-นามสกุล>"
# บน macOS สคริปต์จะแคปหน้าจอ 2 รูปให้อัตโนมัติ (~/mqtt_lab/<รหัส>_lab11_1_photo1.png, photo2.png)
# ให้แต่ละคนรันบนเครื่องของตัวเอง ผลลัพธ์จริงจาก Broker จะถูกบันทึกไว้ที่ ~/mqtt_lab/lab11_1_<รหัส>.txt
set -u
ID="${1:-}"
NAME="${2:-}"
if [ -z "$ID" ]; then echo "ใช้: $0 <รหัสนักศึกษา> \"<ชื่อ-นามสกุล>\""; exit 1; fi
WHO="$ID${NAME:+ $NAME}"
H=127.0.0.1
LAB="$HOME/mqtt_lab"; mkdir -p "$LAB"
OUT="$LAB/lab11_1_${ID}.txt"; BLOG="$LAB/broker_${ID}.log"; : > "$BLOG"
printf '\033]0;Lab 11.1 — %s\007' "$WHO"

MOSQ="$(command -v mosquitto || true)"
[ -z "$MOSQ" ] && command -v brew >/dev/null && [ -x "$(brew --prefix)/sbin/mosquitto" ] && MOSQ="$(brew --prefix)/sbin/mosquitto"
[ -z "$MOSQ" ] && [ -x /usr/sbin/mosquitto ] && MOSQ=/usr/sbin/mosquitto
if [ -z "$MOSQ" ] || ! command -v mosquitto_sub >/dev/null; then
  echo "❌ ไม่พบ Mosquitto — ติดตั้งก่อน: brew install mosquitto"; exit 1; fi

PORT=1883
if (echo > /dev/tcp/$H/$PORT) 2>/dev/null; then
  echo "⚠️  พอร์ต 1883 มีโปรแกรมใช้อยู่ (เช่น brew services) — ปิดด้วย: brew services stop mosquitto แล้วรันใหม่"; exit 1; fi
printf 'listener %s 0.0.0.0\nallow_anonymous true\nlog_type all\n' "$PORT" > "$LAB/mosquitto.conf"

"$MOSQ" -c "$LAB/mosquitto.conf" -v > "$BLOG" 2>&1 &
BPID=$!
cleanup() { kill "$BPID" 2>/dev/null; wait "$BPID" 2>/dev/null; }
trap cleanup EXIT
for i in $(seq 1 30); do grep -q "running" "$BLOG" && break; sleep 0.2; done
grep -q "running" "$BLOG" || { echo "❌ Broker ไม่ขึ้น:"; cat "$BLOG"; exit 1; }

SUB="mosquitto_sub -h $H -p $PORT"; PUB="mosquitto_pub -h $H -p $PORT"
hr()  { printf '\n\033[1;36m══════ %s ══════\033[0m\n' "$1"; }
cam() { printf '\n\033[1;33m📸 %s\033[0m\n' "$1"; }
# แคปหน้าต่าง Terminal อัตโนมัติ (macOS) — ครั้งแรก macOS อาจถามสิทธิ์ Screen Recording ให้กดอนุญาตแล้วรันใหม่
snap() {
  local f="$LAB/${ID}_lab11_1_$1.png"
  if command -v screencapture >/dev/null 2>&1; then
    sleep 1
    local wid; wid="$(osascript -e 'tell application "Terminal" to id of front window' 2>/dev/null || true)"
    if [ -n "$wid" ]; then screencapture -x -o -l"$wid" "$f" 2>/dev/null; else screencapture -x "$f" 2>/dev/null; fi
    if [ -s "$f" ]; then printf '\033[1;32m✅ บันทึกรูปแล้ว: %s\033[0m\n' "$f"; else printf '\033[1;31m⚠️ แคปอัตโนมัติไม่สำเร็จ — กด Cmd+Shift+4 แคปเองตรงนี้\033[0m\n'; fi
  fi
}
mark() { wc -l < "$BLOG"; }
since() { tail -n +"$(( $1 + 1 ))" "$BLOG"; }

{
hr "Lab 11.1 — $WHO"
echo "เครื่อง: $(whoami)@$(hostname)   เวลา: $(date '+%Y-%m-%d %H:%M:%S')   Broker: $($MOSQ -h 2>/dev/null | head -1)"

hr "11-1.1 Broker เริ่มทำงาน"
head -n 6 "$BLOG"

printf '\033[2J\033[H'; hr "Lab 11.1 — $WHO  ($(date '+%Y-%m-%d %H:%M'))"
hr "11-1.2 Publish/Subscribe + Wildcards (# และ +)"
M=$(mark)
$SUB -t "home/#" -v -C 3 -W 6 > "$LAB/.s1" 2>/dev/null & S1=$!; sleep 0.6
$PUB -t "home/livingroom/light" -m "ON"; $PUB -t "home/livingroom/temp" -m "26.4"; $PUB -t "home/bedroom/balcony/light" -m "ON"
wait $S1 2>/dev/null
echo "[Subscriber home/#] ได้รับ:"; sed 's/^/   /' "$LAB/.s1"
$SUB -t "home/+/light" -v -C 2 -W 4 > "$LAB/.s2" 2>/dev/null & S2=$!; sleep 0.6
$PUB -t "home/livingroom/light" -m "ON"; $PUB -t "home/kitchen/light" -m "OFF"; $PUB -t "home/bedroom/balcony/light" -m "ON"
wait $S2 2>/dev/null
echo "[Subscriber home/+/light] ได้รับ (home/bedroom/balcony/light ต้องไม่ผ่าน):"; sed 's/^/   /' "$LAB/.s2"
echo; echo "[Broker Verbose Log]"; since "$M" | grep -E "New client|SUBSCRIBE|PUBLISH|Sending" | head -n 12
cam "รูปที่ 1: Broker Verbose Log (New client / SUBSCRIBE / PUBLISH)"
snap photo1

hr "11-1.3 QoS 0 / 1 / 2 (ดูแพ็กเก็ตใน Broker Log)"
for q in 0 1 2; do
  M=$(mark)
  $SUB -t "test/qos" -q $q -v -C 1 -W 4 > /dev/null 2>&1 & SQ=$!; sleep 0.5
  $PUB -t "test/qos" -m "QoS $q Message" -q $q; wait $SQ 2>/dev/null; sleep 0.2
  echo "--- QoS $q ---"; since "$M" | grep -E "PUBLISH|PUBACK|PUBREC|PUBREL|PUBCOMP" | grep -v "Sending PUBLISH to auto" | sed 's/^/   /'
done

printf '\033[2J\033[H'; hr "Lab 11.1 — $WHO  ($(date '+%Y-%m-%d %H:%M'))"
hr "11-1.4 Retained Message"
$PUB -t "sensor/state" -n -r
$PUB -t "sensor/state" -m "Normal"
echo "[ส่งแบบไม่มี -r แล้วเปิด Subscriber ใหม่] ได้รับ:"; $SUB -t "sensor/state" -v -C 1 -W 2 2>/dev/null | sed 's/^/   /' || true
echo "   (ว่างเปล่า = ถูกต้อง เพราะไม่มีข้อความคงค้าง)"
$PUB -t "sensor/state" -m "CRITICAL_ALERT" -r
echo "[ส่งแบบมี -r แล้วเปิด Subscriber ใหม่] ได้รับทันที:"; $SUB -t "sensor/state" -v -C 1 -W 3 2>/dev/null | sed 's/^/   /'
cam "รูปที่ 2: Retained Message — Subscriber ใหม่ได้ CRITICAL_ALERT ทันที"
snap photo2
$PUB -t "sensor/state" -n -r

hr "11-1.5 Last Will and Testament (LWT)"
$SUB -t "node/esp32/status" -v -C 2 -W 8 > "$LAB/.s5" 2>/dev/null & S5=$!; sleep 0.5
$SUB -i "Node_Client_01" -t "dummy/listen" --will-topic "node/esp32/status" --will-payload "LOST_CONNECTION_OFFLINE" --will-qos 1 > /dev/null 2>&1 & W=$!; sleep 0.6
$PUB -t "node/esp32/status" -m "ONLINE"; sleep 0.4
kill -9 "$W" 2>/dev/null   # จำลองไฟดับ / เน็ตหลุดกะทันหัน
wait $S5 2>/dev/null
echo "[Subscriber node/esp32/status] ได้รับ:"; sed 's/^/   /' "$LAB/.s5"

hr "เสร็จสิ้น"
echo "📄 Log ทั้งหมด (วางในช่อง 💻 Lab 11.1): $OUT"
echo "🖼️  รูปที่ต้องอัปโหลด: $LAB/${ID}_lab11_1_photo1.png และ photo2.png"
} 2>&1 | tee "$OUT"
rm -f "$LAB"/.s1 "$LAB"/.s2 "$LAB"/.s5
