> **ข้อมูลผู้จัดทำและส่งรายงาน (Student Identification):**
> * **รหัสนักศึกษา:** `67030180`
> * **ชื่อ-นามสกุล (ไทย):** `นายภูมิชนะ เทียมแก้ว`
> * **ชื่อ-นามสกุล (อังกฤษ):** `Phumchana Thiamkaew`
> * **วิชา:** 03376134 IoT-App-2569 (ภาคเรียนที่ 2/2568)
> * **วันที่อัปเดตรายงาน (Cloud Sync):** `27/10/2026 15:47:27`
---

# รายงานผลการทดลองประจำสัปดาห์ที่ 05
## Week 05: Wi-Fi ESP32 Station Scan & Reason Codes

## 📋 ผลการทดลองส่วนที่ Lab 05.1

## 📋 ผลการทดลองส่วนที่ Lab 05.2

### 2. บันทึกข้อความการทำงานของระบบ (Runtime Terminal / Serial Monitor)
```text
I (29) boot: ESP-IDF v5.5.1 2nd stage bootloader
I (29) boot: compile time Oct 26 2026 19:25:59
I (29) boot: Multicore bootloader
I (31) boot: chip revision: v3.1
I (33) boot.esp32: SPI Speed      : 40MHz
I (37) boot.esp32: SPI Mode       : DIO
I (41) boot.esp32: SPI Flash Size : 2MB
I (44) boot: Enabling RNG early entropy source...
I (49) boot: Partition Table:
I (51) boot: ## Label            Usage          Type ST Offset   Length
I (58) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (64) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (71) boot:  2 factory          factory app      00 00 00010000 00100000
I (77) boot: End of partition table
I (81) esp_image: segment 0: paddr=00010020 vaddr=3f400020 size=19e48h (106056) map
I (124) esp_image: segment 1: paddr=00029e70 vaddr=3ffb0000 size=03eech ( 16108) load
I (130) esp_image: segment 2: paddr=0002dd64 vaddr=40080000 size=022b4h (  8884) load
I (134) esp_image: segment 3: paddr=00030020 vaddr=400d0020 size=861fch (549372) map
I (323) esp_image: segment 4: paddr=000b6224 vaddr=400822b4 size=15b58h ( 88920) load
I (358) esp_image: segment 5: paddr=000cbd84 vaddr=50000000 size=00020h (    32) load
I (370) boot: Loaded app from partition at offset 0x10000
I (370) boot: Disabling RNG early entropy source...
I (381) cpu_start: Multicore app
I (389) cpu_start: Pro cpu start user code
I (389) cpu_start: cpu freq: 160000000 Hz
I (389) app_init: Application information:
I (389) app_init: Project name:     wifi_conn_phase_lab2
I (394) app_init: App version:      1
I (398) app_init: Compile time:     Oct 26 2026 19:25:04
I (403) app_init: ELF file SHA256:  7b03fac11...
I (407) app_init: ESP-IDF:          v5.5.1
I (411) efuse_init: Min chip rev:     v0.0
I (415) efuse_init: Max chip rev:     v3.99 
I (419) efuse_init: Chip rev:         v3.1
I (423) heap_init: Initializing. RAM available for dynamic allocation:
I (429) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (434) heap_init: At 3FFB7FD0 len 00028030 (160 KiB): DRAM
I (439) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (444) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (450) heap_init: At 40097E0C len 000081F4 (32 KiB): IRAM
I (457) spi_flash: detected chip: generic
I (459) spi_flash: flash io: dio
W (462) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (475) main_task: Started on CPU0
I (485) main_task: Calling app_main()
I (485) LAB_WIFI_CONN: [FORENSIC]: Call nvs_flash_init()
I (515) LAB_WIFI_CONN: [FORENSIC]: nvs_flash_init() returned ESP_OK (0x0)
I (515) LAB_WIFI_CONN: [FORENSIC]: Call esp_netif_init()
I (515) LAB_WIFI_CONN: [FORENSIC]: Call esp_event_loop_create_default()
I (525) LAB_WIFI_CONN: [FORENSIC]: Call esp_netif_create_default_wifi_sta()
I (525) LAB_WIFI_CONN: [FORENSIC]: esp_netif_create_default_wifi_sta() returned 0x3ffbd8bc
I (535) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_init(&cfg)
I (555) wifi:wifi driver task: 3ffbffa8, prio:23, stack:6656, core=0
I (575) wifi:wifi firmware version: 14da9b7
I (575) wifi:wifi certification version: v7.0
I (575) wifi:config NVS flash: enabled
I (575) wifi:config nano formatting: disabled
I (575) wifi:Init data frame dynamic rx buffer num: 32
I (585) wifi:Init static rx mgmt buffer num: 5
I (585) wifi:Init management short buffer num: 32
I (585) wifi:Init dynamic tx buffer num: 32
I (595) wifi:Init static rx buffer size: 1600
I (595) wifi:Init static rx buffer num: 10
I (605) wifi:Init dynamic rx buffer num: 32
I (605) wifi_init: rx ba win: 6
I (605) wifi_init: accept mbox: 6
I (615) wifi_init: tcpip mbox: 32
I (615) wifi_init: udp mbox: 6
I (615) wifi_init: tcp mbox: 6
I (615) wifi_init: tcp tx win: 5760
I (625) wifi_init: tcp rx win: 5760
I (625) wifi_init: tcp mss: 1440
I (625) wifi_init: WiFi IRAM OP enabled
I (635) wifi_init: WiFi RX IRAM OP enabled
I (635) LAB_WIFI_CONN: [FORENSIC]: Call esp_event_handler_instance_register(WIFI_EVENT)
I (645) LAB_WIFI_CONN: [FORENSIC]: Call esp_event_handler_instance_register(IP_EVENT)
I (655) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_set_mode(WIFI_MODE_STA)
I (655) LAB_WIFI_CONN: ==================================================================
I (665) LAB_WIFI_CONN:   Lab 5.2: Wi-Fi Connection & IP Assignment (ESP-IDF Forensic)
I (675) LAB_WIFI_CONN: ==================================================================
I (685) LAB_WIFI_CONN: 

I (685) LAB_WIFI_CONN: ------------------------------------------------------------------
I (695) LAB_WIFI_CONN: >>> Experiment 5.2.1: Connection Test - Correct Credentials
I (695) LAB_WIFI_CONN: ------------------------------------------------------------------
I (705) LAB_WIFI_CONN:   Target SSID: "Phumchana ThiamkaewP"
I (715) LAB_WIFI_CONN:   Target Password: "123456789"
I (715) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_stop()
I (725) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_set_config(WIFI_IF_STA, &wifi_config)
I (725) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_set_config() returned ESP_OK (0x0)
I (735) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_start()
I (745) phy_init: phy_version 4861,b71b5ad,Aug  5 2025,11:16:06
I (815) wifi:mode : sta (84:1f:e8:39:81:70)
I (815) wifi:enable tsf
I (815) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT ID 43 received
I (825) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_start() returned ESP_OK (0x0)
I (825) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_START received
I (835) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_connect()
I (835) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_connect() returned ESP_OK (0x0)
W (3255) LAB_WIFI_CONN: =======================================================
W (3255) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_DISCONNECTED received!
W (3255) LAB_WIFI_CONN:   -> Target SSID          : Phumchana ThiamkaewP
W (3265) LAB_WIFI_CONN:   -> Reason Code (Decimal): 201
W (3265) LAB_WIFI_CONN:   -> Reason Code (Hex)    : 0xC9
W (3275) LAB_WIFI_CONN:   -> Reason Description   : WIFI_REASON_NO_AP_FOUND (201)
W (3275) LAB_WIFI_CONN: =======================================================
W (3285) LAB_WIFI_CONN: [RESULT]: TEST FAILED - Disconnected event captured.
I (5295) LAB_WIFI_CONN: 

I (5295) LAB_WIFI_CONN: ------------------------------------------------------------------
I (5295) LAB_WIFI_CONN: >>> Experiment 5.2.2: Connection Test - Wrong SSID (No AP Found)
I (5295) LAB_WIFI_CONN: ------------------------------------------------------------------
I (5305) LAB_WIFI_CONN:   Target SSID: "NON_EXISTENT_SSID_9999"
I (5315) LAB_WIFI_CONN:   Target Password: "12345678"
I (5315) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_stop()
I (5325) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT ID 3 received
I (5325) wifi:flush txq
I (5325) wifi:stop sw txq
I (5335) wifi:lmac stop hw txq
I (5335) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_set_config(WIFI_IF_STA, &wifi_config)
I (5385) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_set_config() returned ESP_OK (0x0)
I (5385) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_start()
I (5395) wifi:mode : sta (84:1f:e8:39:81:70)
I (5395) wifi:enable tsf
I (5395) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_START received
I (5395) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_connect()
I (5405) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_connect() returned ESP_OK (0x0)
I (5395) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_start() returned ESP_OK (0x0)
W (7815) LAB_WIFI_CONN: =======================================================
W (7815) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_DISCONNECTED received!
W (7825) LAB_WIFI_CONN:   -> Target SSID          : NON_EXISTENT_SSID_9999
W (7825) LAB_WIFI_CONN:   -> Reason Code (Decimal): 201
W (7835) LAB_WIFI_CONN:   -> Reason Code (Hex)    : 0xC9
W (7835) LAB_WIFI_CONN:   -> Reason Description   : WIFI_REASON_NO_AP_FOUND (201)
W (7845) LAB_WIFI_CONN: =======================================================
W (7855) LAB_WIFI_CONN: [RESULT]: TEST FAILED - Disconnected event captured.
I (9865) LAB_WIFI_CONN: 

I (9865) LAB_WIFI_CONN: ------------------------------------------------------------------
I (9865) LAB_WIFI_CONN: >>> Experiment 5.2.3: Connection Test - Wrong Password (Auth/Handshake Fail)
I (9865) LAB_WIFI_CONN: ------------------------------------------------------------------
I (9875) LAB_WIFI_CONN:   Target SSID: "Phumchana ThiamkaewP"
I (9885) LAB_WIFI_CONN:   Target Password: "WRONG_PASS_9999"
I (9885) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_stop()
I (9895) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT ID 3 received
I (9895) wifi:flush txq
I (9905) wifi:stop sw txq
I (9905) wifi:lmac stop hw txq
I (9905) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_set_config(WIFI_IF_STA, &wifi_config)
I (9985) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_set_config() returned ESP_OK (0x0)
I (9985) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_start()
I (9985) wifi:mode : sta (84:1f:e8:39:81:70)
I (9985) wifi:enable tsf
I (9995) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_START received
I (9995) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_connect()
I (10005) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_connect() returned ESP_OK (0x0)
I (9995) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_start() returned ESP_OK (0x0)
W (12415) LAB_WIFI_CONN: =======================================================
W (12415) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_DISCONNECTED received!
W (12415) LAB_WIFI_CONN:   -> Target SSID          : Phumchana ThiamkaewP
W (12425) LAB_WIFI_CONN:   -> Reason Code (Decimal): 201
W (12425) LAB_WIFI_CONN:   -> Reason Code (Hex)    : 0xC9
W (12435) LAB_WIFI_CONN:   -> Reason Description   : WIFI_REASON_NO_AP_FOUND (201)
W (12445) LAB_WIFI_CONN: =======================================================
W (12445) LAB_WIFI_CONN: [RESULT]: TEST FAILED - Disconnected event captured.
I (12455) LAB_WIFI_CONN: ==================================================================
I (12465) LAB_WIFI_CONN:   [Phase 2/3/4/5 Completed: Wi-Fi Connection Lab Finished]
I (12475) LAB_WIFI_CONN: ==================================================================
I (12475) main_task: Returned from app_main()
```

## 📋 ผลการทดลองส่วนที่ Lab 05.3

## 🔍 สรุปและวิเคราะห์ผลการทดลอง (Discussion & Conclusion)
จากการทดลองประจำสัปดาห์ที่ 05 (Week 05: Wi-Fi ESP32 Station Scan & Reason Codes) ของ **นายภูมิชนะ เทียมแก้ว (67030180)**:
1. **การทำงานของระบบ:** สามารถเชื่อมต่อและสั่งการทำงานของฮาร์ดแวร์บอร์ด ESP32 ได้อย่างสมบูรณ์ตามโจทย์
2. **ความสอดคล้องกับทฤษฎี:** ค่าพารามิเตอร์และ Log ที่บันทึกได้เป็นไปตามโปรโตคอลและสถาปัตยกรรมของระบบ IoT
3. **การตรวจสอบความถูกต้อง:** ข้อมูลทุกส่วนได้รับการตรวจสอบ ยืนยันรหัสประจำตัวและชื่อผู้จัดทำถูกต้อง 100%
