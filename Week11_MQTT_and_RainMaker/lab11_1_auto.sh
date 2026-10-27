#!/usr/bin/env bash
# Lab 11.1 (Mosquitto Broker & MQTT Fundamentals) — รันทุกกิจกรรมในคำสั่งเดียว
# ใช้: bash lab11_1_auto.sh <รหัสนักศึกษา>   (ชื่อดึงจากรายชื่อกลุ่มให้เอง)
# บน macOS สคริปต์จะแคปหน้าจอ 2 รูปให้อัตโนมัติ (~/mqtt_lab/<รหัส>_lab11_1_photo1.png, photo2.png)
# ให้แต่ละคนรันบนเครื่องของตัวเอง ผลลัพธ์จริงจาก Broker จะถูกบันทึกไว้ที่ ~/mqtt_lab/lab11_1_<รหัส>.txt
set -u
# ---- รายชื่อกลุ่ม: พิมพ์แค่รหัสก็พอ (หรือพิมพ์ตามชื่อโฟลเดอร์ รหัส_ชื่อ_นามสกุล ก็ได้) ----
roster_name() {
  case "$1" in
    67030073) echo "Natthaphong Niampradit";;
    67030180) echo "Phumchana Thiamkaew";;
    67030183) echo "Phuwish Prakobchit";;
    67030248) echo "Suwijak Lawang";;
    67030249) echo "Suwimon Sripramai";;
    67030268) echo "Korn Daengthong";;
    67030270) echo "Kritsadinat Samrankit";;
    67030299) echo "Thanaporn Pitsamai";;
    67030359) echo "Attawut Bualian";;
    67030360) echo "Ittipat Sutthinuan";;
  esac
}
RAW="${1:-}"; ID="$(printf '%s' "$RAW" | grep -oE '^[0-9]{8}' || true)"
[ -z "$ID" ] && { echo "ใช้: bash $0 <รหัสนักศึกษา 8 หลัก>   เช่น  bash $0 67030073"; exit 1; }
NAME="${2:-$(roster_name "$ID")}"
[ -z "$NAME" ] && NAME="$(printf '%s' "${RAW#"$ID"}" | tr '_' ' ' | sed 's/^ *//')"
[ -z "$(roster_name "$ID")" ] && echo "ℹ️  รหัส $ID ไม่อยู่ในรายชื่อกลุ่ม — ใช้ชื่อ: ${NAME:-(ไม่ระบุ)}"
WHO="$ID${NAME:+ $NAME}"
SELF="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"

# รูปต้องเป็นหน้าต่าง Terminal ที่รันสคริปต์นี้เอง — ถ้ารันจาก VS Code/iTerm จะเปิดหน้าต่าง Terminal ใหม่ให้รันต่อ
if [ "$(uname)" = Darwin ] && [ "${TERM_PROGRAM:-}" != "Apple_Terminal" ]; then
  echo "ℹ️  เปิดหน้าต่าง Terminal ใหม่ให้รัน Lab 11.1 ของ $WHO (รูปจะได้เป็นหน้าต่างนั้น)..."
  osascript - "$SELF" "$ID" "$NAME" >/dev/null <<'OSA' && exit 0
on run argv
  tell application "Terminal"
    activate
    do script "bash " & quoted form of item 1 of argv & " " & quoted form of item 2 of argv & " " & quoted form of item 3 of argv
  end tell
end run
OSA
  echo "❌ เปิด Terminal ให้ไม่ได้ — เปิดแอป Terminal เองแล้วรัน: bash \"$SELF\" $ID"; exit 1
fi
# หาเลขหน้าต่าง Terminal ของ tty นี้ (ไม่ใช่หน้าต่างที่อยู่ด้านหน้า ซึ่งอาจเป็นหน้าต่างอื่น)
my_window() {
  osascript - "$1" 2>/dev/null <<'OSA'
on run argv
  tell application "Terminal"
    repeat with w in windows
      repeat with tb in tabs of w
        if tty of tb is (item 1 of argv) then return id of w
      end repeat
    end repeat
  end tell
  return ""
end run
OSA
}
MYWIN=""
[ "$(uname)" = Darwin ] && MYWIN="$(my_window "$(tty)")"
H=127.0.0.1
LAB="$HOME/mqtt_lab"; mkdir -p "$LAB"
OUT="$LAB/lab11_1_${ID}.txt"; BLOG="$LAB/broker_${ID}.log"; : > "$BLOG"
printf '\033]0;Lab 11.1 — %s\007' "$WHO"

MOSQ="$(command -v mosquitto || true)"
[ -z "$MOSQ" ] && command -v brew >/dev/null && [ -x "$(brew --prefix)/sbin/mosquitto" ] && MOSQ="$(brew --prefix)/sbin/mosquitto"
[ -z "$MOSQ" ] && [ -x /usr/sbin/mosquitto ] && MOSQ=/usr/sbin/mosquitto
if [ -z "$MOSQ" ] || ! command -v mosquitto_sub >/dev/null; then
  echo "❌ ไม่พบ Mosquitto — ติดตั้งก่อน: brew install mosquitto"; exit 1; fi

# ใช้พอร์ต 1883 ตามใบงาน ถ้ามีโปรแกรมอื่นใช้อยู่ (เช่น brew services) จะเลือกพอร์ตว่างถัดไปให้อัตโนมัติ
PORT=""
for p in 1883 1884 1885 1886 1887 1888 1889 1890; do
  if ! (echo > /dev/tcp/$H/$p) 2>/dev/null; then PORT=$p; break; fi
done
[ -z "$PORT" ] && { echo "❌ พอร์ต 1883–1890 ถูกใช้หมด — ลอง: brew services stop mosquitto"; exit 1; }
[ "$PORT" != "1883" ] && echo "ℹ️  พอร์ต 1883 มีโปรแกรมอื่นใช้อยู่ — ใช้พอร์ต $PORT แทน (ผลการทดลองเหมือนกัน)"
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
    rm -f "$f"
    if [ -n "$MYWIN" ]; then screencapture -x -o -l"$MYWIN" "$f" 2>/dev/null; fi
    if [ -s "$f" ]; then printf '\033[1;32m✅ บันทึกรูปแล้ว: %s\033[0m\n' "$f"; else printf '\033[1;31m⚠️ แคปอัตโนมัติไม่สำเร็จ — กด Cmd+Shift+4 แล้ว Space แล้วคลิกหน้าต่างนี้\033[0m\n'; fi
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
QSEQ=(); QN=()
for q in 0 1 2; do
  M=$(mark)
  $SUB -i "sub_qos$q" -t "test/qos" -q $q -v -C 1 -W 4 > /dev/null 2>&1 & SQ=$!; sleep 0.5
  $PUB -i "pub_qos$q" -t "test/qos" -m "QoS $q Message" -q $q; wait $SQ 2>/dev/null; sleep 0.2
  echo "--- QoS $q (Publisher <-> Broker) ---"; since "$M" | grep "pub_qos$q" | grep -E "PUBLISH|PUBACK|PUBREC|PUBREL|PUBCOMP" | sed 's/^/   /'
  QSEQ[$q]="$(since "$M" | grep "pub_qos$q" | grep -oE "(Received|Sending) (PUBLISH|PUBACK|PUBREC|PUBREL|PUBCOMP)" | awk '{print $2}' | awk 'BEGIN{ORS=""} {if (NR>1) print " → "; print}')"
  QN[$q]="$(since "$M" | grep "pub_qos$q" | grep -cE "(Received|Sending) (PUBLISH|PUBACK|PUBREC|PUBREL|PUBCOMP)")"
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

hr "ค่าสำหรับกรอกในเว็บ — Lab 11.1"
echo "พอร์ต Plain MQTT      : $PORT"
echo "พอร์ต mTLS Secure     : 8883 (ใช้ใน Lab 11.3)"
echo "Topic Filter ที่ Sub    : home/#  และ  home/+/light"
echo "LWT Topic             : node/esp32/status"
echo "LWT Payload           : LOST_CONNECTION_OFFLINE"
echo "Retain Message Flag   : -r (retain = 1)"
echo
echo "ตารางผล (ก๊อปไปวางในช่อง 📋 ตารางผล):"
echo "#### ตารางเปรียบเทียบลำดับแพ็กเก็ต QoS 0 / 1 / 2 (จาก Broker Log)"
echo "| QoS | ลำดับแพ็กเก็ตที่สังเกตได้ | จำนวนแพ็กเก็ต |"
echo "|---|---|---|"
for q in 0 1 2; do echo "| $q | ${QSEQ[$q]} | ${QN[$q]} |"; done

hr "เสร็จสิ้น"
echo "📄 Log ทั้งหมด (วางในช่อง 💻 Lab 11.1): $OUT"
echo "🖼️  รูปที่ต้องอัปโหลด: $LAB/${ID}_lab11_1_photo1.png และ photo2.png"
} 2>&1 | tee "$OUT"
rm -f "$LAB"/.s1 "$LAB"/.s2 "$LAB"/.s5
