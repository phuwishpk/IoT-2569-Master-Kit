#!/usr/bin/env bash
# Lab 11.3 (MQTTS / TLS Mutual Authentication) — ส่วน CLI ข้อ 11-3.1 ถึง 11-3.3 ในคำสั่งเดียว
# ใช้: bash lab11_3_auto.sh <รหัสนักศึกษา> [--keep]
#   --keep  = เปิด Broker 8883 ค้างไว้หลังทดสอบ เพื่อให้บอร์ด ESP32 (ข้อ 11-3.4–11-3.5) เชื่อมต่อต่อได้
# ได้: ~/mqtt_lab/lab11_3_<รหัส>.txt (Log ทั้งหมด + ค่าที่ต้องกรอก) และใบรับรองที่ ~/mqtt_lab/certs_<รหัส>/
set -u
# ---- รายชื่อกลุ่ม: พิมพ์แค่รหัสก็พอ (หรือพิมพ์ตามชื่อโฟลเดอร์ รหัส_ชื่อ_นามสกุล ก็ได้) ----
roster_name() {
  case "$1" in
    67030073) echo "Natthaphong Niampradit";;
    67030180) echo "Phumchana Thiamkaew";;
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
[ -z "$ID" ] && { echo "ใช้: bash $0 <รหัสนักศึกษา 8 หลัก> [--keep]   เช่น  bash $0 67030073"; exit 1; }
KEEP=0; NAME="$(roster_name "$ID")"
for a in "${@:2}"; do if [ "$a" = "--keep" ]; then KEEP=1; elif [ -n "$a" ]; then NAME="$a"; fi; done
[ -z "$NAME" ] && NAME="$(printf '%s' "${RAW#"$ID"}" | tr '_' ' ' | sed 's/^ *//')"
WHO="$ID${NAME:+ $NAME}"
printf '\033]0;Lab 11.3 — %s\007' "$WHO"

H=127.0.0.1
LAB="$HOME/mqtt_lab"; CERT="$LAB/certs_${ID}"; mkdir -p "$CERT"
OUT="$LAB/lab11_3_${ID}.txt"; BLOG="$LAB/broker_tls_${ID}.log"; CONF="$LAB/mosquitto_tls_${ID}.conf"; : > "$BLOG"
command -v openssl >/dev/null || { echo "❌ ไม่พบ openssl"; exit 1; }
MOSQ="$(command -v mosquitto || true)"
[ -z "$MOSQ" ] && command -v brew >/dev/null && [ -x "$(brew --prefix)/sbin/mosquitto" ] && MOSQ="$(brew --prefix)/sbin/mosquitto"
[ -z "$MOSQ" ] && [ -x /usr/sbin/mosquitto ] && MOSQ=/usr/sbin/mosquitto
if [ -z "$MOSQ" ] || ! command -v mosquitto_sub >/dev/null; then echo "❌ ไม่พบ Mosquitto — ติดตั้งก่อน: brew install mosquitto"; exit 1; fi
LANIP="$( (ipconfig getifaddr en0 || ipconfig getifaddr en1 || hostname -I | awk '{print $1}') 2>/dev/null | head -1)"
PORT=""
for p in 8883 8884 8885 8886 8887 8888 8889 8890; do
  if ! (echo > /dev/tcp/$H/$p) 2>/dev/null; then PORT=$p; break; fi
done
[ -z "$PORT" ] && { echo "❌ พอร์ต 8883–8890 ถูกใช้หมด"; exit 1; }

BPID=""
cleanup() { [ -n "$BPID" ] && { kill "$BPID" 2>/dev/null; wait "$BPID" 2>/dev/null; }; rm -f "$LAB/.t3_sub"; }
trap cleanup EXIT
hr()  { printf '\n\033[1;36m══════ %s ══════\033[0m\n' "$1"; }
run() { printf '$ %s\n' "$*"; "$@" 2>&1 | sed 's/^/   /'; return "${PIPESTATUS[0]}"; }
mark() { wc -l < "$BLOG"; }
since() { tail -n +"$(( $1 + 1 ))" "$BLOG"; }

# ---------- 11-3.1 สร้างใบรับรอง (ทำก่อนเปิด Broker) ----------
{
hr "Lab 11.3 — $WHO"
echo "เครื่อง: $(whoami)@$(hostname)   เวลา: $(date '+%Y-%m-%d %H:%M:%S')   $(openssl version)   $($MOSQ -h 2>/dev/null | head -1)"

hr "11-3.1 สร้าง Root CA / Server / Client Certificate ด้วย OpenSSL"
cd "$CERT" || exit 1
rm -f ca.* server.* client.* ./*.srl
run openssl genrsa -out ca.key 2048
run openssl req -out ca.csr -key ca.key -new -subj "/C=TH/ST=Bangkok/O=IoT Security Lab/CN=IoT Root CA ($ID)"
printf 'basicConstraints=critical,CA:TRUE\nkeyUsage=critical,keyCertSign,cRLSign\n' > ca.ext
run openssl x509 -req -in ca.csr -out ca.crt -sha256 -days 3650 -signkey ca.key -extfile ca.ext
printf 'subjectAltName=IP:127.0.0.1%s,DNS:localhost\nextendedKeyUsage=serverAuth\n' "${LANIP:+,IP:$LANIP}" > server.ext
run openssl genrsa -out server.key 2048
run openssl req -out server.csr -key server.key -new -subj "/C=TH/ST=Bangkok/O=IoT Broker/CN=${LANIP:-127.0.0.1}"
run openssl x509 -req -in server.csr -out server.crt -sha256 -CA ca.crt -CAkey ca.key -CAcreateserial -days 3650 -extfile server.ext
printf 'extendedKeyUsage=clientAuth\n' > client.ext
run openssl genrsa -out client.key 2048
run openssl req -out client.csr -key client.key -new -subj "/C=TH/ST=Bangkok/O=IoT Node ($ID)/CN=esp32-secure-node"
run openssl x509 -req -in client.csr -out client.crt -sha256 -CA ca.crt -CAkey ca.key -CAcreateserial -days 3650 -extfile client.ext
echo; echo "ไฟล์ที่ได้ (6 ไฟล์):"
for f in ca.key ca.crt server.key server.crt client.key client.crt; do printf '   %-11s %6s bytes\n' "$f" "$(wc -c < "$f" | tr -d ' ')"; done
run openssl verify -CAfile ca.crt server.crt client.crt
for c in server client; do echo "[$c.crt]"; openssl x509 -in "$c.crt" -noout -subject -issuer -enddate 2>&1 | sed 's/^/   /'; done
} 2>&1 | tee "$OUT"
[ -s "$CERT/client.crt" ] && [ -s "$CERT/server.crt" ] || { echo "❌ สร้างใบรับรองไม่สำเร็จ"; exit 1; }

# ---------- 11-3.2 เปิด Broker MQTTS ----------
cat > "$CONF" <<EOF
listener $PORT 0.0.0.0
cafile $CERT/ca.crt
certfile $CERT/server.crt
keyfile $CERT/server.key
require_certificate true
tls_version tlsv1.2
allow_anonymous true
log_type all
EOF
"$MOSQ" -c "$CONF" -v > "$BLOG" 2>&1 &
BPID=$!
for i in $(seq 1 30); do grep -q "running" "$BLOG" && break; sleep 0.2; done
grep -q "running" "$BLOG" || { echo "❌ Broker MQTTS ไม่ขึ้น:"; cat "$BLOG"; exit 1; }

TLS=(--cafile "$CERT/ca.crt" --cert "$CERT/client.crt" --key "$CERT/client.key")
{
hr "11-3.2 Mosquitto MQTTS พอร์ต $PORT (บังคับใบรับรอง Client)"
[ "$PORT" != "8883" ] && echo "ℹ️  พอร์ต 8883 มีโปรแกรมอื่นใช้อยู่ — ใช้พอร์ต $PORT แทน (ผลการทดลองเหมือนกัน)"
sed "s#$CERT/#<certs>/#" "$CONF" | sed 's/^/   /'
head -n 8 "$BLOG" | sed 's/^/   /'

hr "11-3.3 (1) Client ที่ถูกต้อง — ส่ง ca.crt + client.crt + client.key"
M=$(mark)
mosquitto_sub -h "$H" -p "$PORT" -t "secure/test" "${TLS[@]}" -v -C 1 -W 8 > "$LAB/.t3_sub" 2>&1 & S1=$!; sleep 1
echo "\$ mosquitto_pub -h $H -p $PORT -t secure/test -m \"Hello Secure World! ($ID)\" --cafile ca.crt --cert client.crt --key client.key"
mosquitto_pub -h "$H" -p "$PORT" -t "secure/test" -m "Hello Secure World! ($ID)" "${TLS[@]}" 2>&1 | sed 's/^/   /'
wait $S1 2>/dev/null
echo "[Subscriber ได้รับผ่านช่องทางเข้ารหัส]"; sed 's/^/   /' "$LAB/.t3_sub"
echo "[Broker Log]"; since "$M" | grep -E "New connection|New client|CONNACK|PUBLISH|SUBSCRIBE" | head -n 8 | sed 's/^/   /'

hr "11-3.3 (2) ผู้บุกรุก — ไม่ส่งใบรับรอง Client (ส่งแค่ ca.crt)"
M=$(mark)
echo "\$ mosquitto_pub -h $H -p $PORT -t secure/test -m \"Hacker message\" --cafile ca.crt"
mosquitto_pub -h "$H" -p "$PORT" -t "secure/test" -m "Hacker message" --cafile "$CERT/ca.crt" 2>&1 | sed 's/^/   /'
echo "   (exit code ${PIPESTATUS[0]} — ไม่เป็น 0 แปลว่าถูกปฏิเสธ)"
sleep 0.8
echo "[Broker Log]"; since "$M" | grep -viE "^\s*$" | head -n 8 | sed 's/^/   /'
UNAUTH="$(since "$M" | grep -oiE "peer did not return a certificate|certificate required|certificate verify failed|handshake failure" | head -1)"

hr "ข้อมูล TLS Handshake (openssl s_client)"
SOUT="$(openssl s_client -connect "$H:$PORT" -CAfile "$CERT/ca.crt" -cert "$CERT/client.crt" -key "$CERT/client.key" -tls1_2 < /dev/null 2>&1)"
CIPHER="$(printf '%s\n' "$SOUT" | grep -oE "Cipher is [A-Za-z0-9_-]+" | head -1 | awk '{print $3}')"
[ -z "$CIPHER" ] && CIPHER="$(printf '%s\n' "$SOUT" | grep -E "^ *Cipher *:" | head -1 | awk '{print $NF}')"
KEYBITS="$(printf '%s\n' "$SOUT" | grep -oE "Server public key is [0-9]+ bit" | head -1 | grep -oE "[0-9]+")"
PROTO="$(printf '%s\n' "$SOUT" | grep -E "^ *Protocol *:" | head -1 | awk '{print $NF}')"
printf '%s\n' "$SOUT" | grep -E "subject=|issuer=|Cipher is|Server public key|Protocol *:|Verify return code" | head -n 8 | sed 's/^/   /'

hr "ค่าสำหรับกรอกในเว็บ — Lab 11.3"
echo "Cipher Suite                 : ${CIPHER:-ดูบรรทัด Cipher ด้านบน}${PROTO:+ ($PROTO)}"
echo "Key Length                   : RSA ${KEYBITS:-2048}-bit"
if [ -n "$UNAUTH" ]; then echo "Client ที่ไม่มีใบรับรองถูกปฏิเสธ : ใช่ — $UNAUTH"; else echo "Client ที่ไม่มีใบรับรองถูกปฏิเสธ : ดู Broker Log ข้อ (2)"; fi
echo
echo "สำหรับบอร์ด ESP32 (ข้อ 11-3.4–11-3.5): คัดลอก ca.crt, client.crt, client.key จาก $CERT ไปไว้ที่ main/certs/"
echo "   แล้วตั้ง Broker URI เป็น mqtts://${LANIP:-<IP เครื่องนี้>}:$PORT  (รันสคริปต์นี้แบบ --keep เพื่อเปิด Broker ค้างไว้)"

hr "เสร็จสิ้น"
echo "📄 Log ทั้งหมด (วางในช่อง 💻 Lab 11.3): $OUT"
} 2>&1 | tee -a "$OUT"

if [ "$KEEP" = "1" ]; then
  printf '\n\033[1;33m🔒 Broker MQTTS ยังเปิดอยู่ที่ %s:%s — ให้บอร์ด ESP32 เชื่อมต่อได้เลย (กด Ctrl+C เพื่อปิด)\033[0m\n' "${LANIP:-$H}" "$PORT"
  tail -n 0 -f "$BLOG" | grep --line-buffered -E "New connection|New client|OpenSSL|certificate|disconnected|PUBLISH"
fi
