#!/usr/bin/env bash
# Lab 13.3 / 13.4 — เปิด Kestrel Converged Edge Gateway + หน้าเว็บแดชบอร์ด พร้อมชื่อสมาชิกกลุ่มบนหัวเว็บ
# ใช้: bash lab13_3_auto.sh <รหัส1> <รหัส2> [<รหัส3> <รหัส4>] [--port=/dev/cu.usbserial-XXXX]
#   ต้องแฟลชบอร์ดด้วย ESP32_ADC_Stream ไว้ก่อน และปิด idf.py monitor (Gateway ต้องใช้พอร์ต Serial เอง)
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

if [ "${#IDS[@]}" -lt 2 ]; then echo "❌ ใส่รหัสนักศึกษาของทุกคนในกลุ่ม (อย่างน้อย 2 คน) เช่น  bash $0 67030183 67030248 67030249 [--port=/dev/cu.usbserial-XXXX]"; exit 1; fi
printf '\033]0;Lab 13.3 — กลุ่ม %s\007' "$GROUP_IDS"
say() { printf '\033[1;36m▶ %s\033[0m\n' "$1"; }
ok()  { printf '\033[1;32m✅ %s\033[0m\n' "$1"; }
die() { printf '\033[1;31m❌ %s\033[0m\n' "$1"; exit 1; }
open_port() { (echo > "/dev/tcp/$1/$2") 2>/dev/null; }

DIR="$(cd "$(dirname "$0")" && pwd)"
GW="$(ls -d "$DIR"/67030183_template/Lab13-3 "$DIR"/*_template/Lab13-3 2>/dev/null | head -1)"
[ -n "$GW" ] || die "ไม่พบโฟลเดอร์ Lab13-3"
OUTD="$HOME/mqtt_lab"; mkdir -p "$OUTD"; TAG="$(printf '%s' "$GROUP_IDS" | tr ',' '_')"
GLOG="$OUTD/.gateway13_$TAG.log"; LOG="$OUTD/lab13_3_group_$TAG.txt"
URL="http://localhost:5001/?group=$GROUP_IDS"

echo "👥 กลุ่ม: ${GROUP_TXT//|/  •  }"
say "1/4 ตรวจ .NET SDK"
command -v dotnet >/dev/null || die "ไม่พบ dotnet — ติดตั้ง .NET 10 SDK ก่อน (เช่น brew install --cask dotnet-sdk)"
dotnet --list-sdks 2>/dev/null | grep -qE '^(1[0-9])\.' || die "โปรเจกต์นี้ใช้ net10.0 — ต้องมี .NET 10 SDK (ตอนนี้มี: $(dotnet --list-sdks 2>/dev/null | awk '{print $1}' | paste -sd ' ' -))"
ok "$(dotnet --version)"

say "2/4 ตรวจพอร์ต 1883 (MQTT) และ 5001 (เว็บ)"
for p in 1883 5001; do
  if open_port 127.0.0.1 "$p"; then
    who="$(lsof -nP -iTCP:"$p" -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print $1" (pid "$2")"}' | sort -u | paste -sd ',' -)"
    die "พอร์ต $p ถูกใช้อยู่โดย ${who:-โปรแกรมอื่น} — Gateway ต้องใช้พอร์ตนี้เอง ถ้าเป็น mosquitto ให้รัน: brew services stop mosquitto (หรือปิดสคริปต์ Lab 11/12 ที่เปิดค้าง) แล้วรันใหม่"
  fi
done
ok "ว่างทั้งสองพอร์ต"

say "3/4 หาบอร์ด ESP32 (Serial)"
SP="$(opt_val --port || true)"
[ -z "$SP" ] && SP="$(ls /dev/cu.usbserial* /dev/cu.SLAB_USBtoUART* /dev/cu.wchusbserial* /dev/cu.usbmodem* 2>/dev/null | head -1)"
if [ -n "$SP" ]; then ok "ใช้พอร์ต $SP (ถ้าเปิด idf.py monitor อยู่ ให้ปิดก่อน)"
else SP="/dev/cu.usbserial-0001"; printf '\033[1;33m⚠️  ยังไม่เจอบอร์ด — เสียบสาย USB ได้เลย Gateway จะลองเชื่อมต่อใหม่ทุก 3 วินาที (ถ้าพอร์ตชื่ออื่น ใส่ --port=/dev/cu.xxx)\033[0m\n'; fi

GPID=""
cleanup() { [ -n "$GPID" ] && kill "$GPID" 2>/dev/null; pkill -f "ConvergedEdgeGateway" 2>/dev/null; true; }
trap cleanup EXIT

say "4/4 เปิด Gateway (ครั้งแรกจะดาวน์โหลดแพ็กเกจและ build อาจใช้ 1–2 นาที)"
( cd "$GW" && SERIAL_PORT="$SP" exec dotnet run --no-launch-profile ) > "$GLOG" 2>&1 &
GPID=$!
for i in $(seq 1 180); do
  open_port 127.0.0.1 5001 && break
  kill -0 "$GPID" 2>/dev/null || { tail -25 "$GLOG"; die "Gateway หยุดทำงาน — ดู Log ด้านบน"; }
  sleep 1
done
open_port 127.0.0.1 5001 || { tail -25 "$GLOG"; die "Gateway ไม่ขึ้นภายใน 3 นาที"; }
ok "Gateway พร้อม: เว็บ http://localhost:5001  •  MQTT Broker พอร์ต 1883"
open "$URL" 2>/dev/null || echo "   เปิดเบราว์เซอร์ไปที่: $URL"

echo
printf '\033[1;33m📸 รูป 13.3: แคปหน้าเว็บ (มีชื่อกลุ่มบนหัว) ขณะค่าแรงดันและตัวนับวิ่ง — Cmd+Shift+4 แล้วกด Space แล้วคลิกหน้าต่างเบราว์เซอร์\033[0m\n'
printf '\033[1;33m🎥 คลิป 13.4: เปิดอีก Terminal แล้วรัน  bash Week12_Flutter_MQTT_App/lab12_4_auto.sh %s --app-only\n    แล้วถ่ายให้เห็นแอป เว็บ และบอร์ด: สั่งไฟจากแอป → เว็บกับบอร์ดตอบสนอง และสั่งจากเว็บ → แอปกับบอร์ดตอบสนอง\033[0m\n' "${IDS[*]}"
echo "Log ของ Gateway (กด Ctrl+C เมื่อถ่ายเสร็จ — สคริปต์จะปิด Gateway ให้):"
{ echo "══════ Lab 13.3 — กลุ่ม ${GROUP_TXT//|/, } ══════"; echo "เครื่อง: $(whoami)@$(hostname)   เวลา: $(date '+%Y-%m-%d %H:%M:%S')   Serial: $SP"; } > "$LOG"
tail -n +1 -f "$GLOG" | grep --line-buffered -vE "^\s*$" | tee -a "$LOG"
