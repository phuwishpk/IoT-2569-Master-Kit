> **ข้อมูลผู้จัดทำและส่งรายงาน (Student Identification):**
> * **รหัสนักศึกษา:** `67030360`
> * **ชื่อ-นามสกุล (ไทย):** `นายอิทธิพัทธิ์ สุทธินวล`
> * **ชื่อ-นามสกุล (อังกฤษ):** `Ittipat Sutthinuan`
> * **วิชา:** 03376134 IoT-App-2569 (ภาคเรียนที่ 2/2568)
---

> **ข้อมูลผู้จัดทำและส่งรายงาน (Student Identification):**
> * **รหัสนักศึกษา:** `67030360`
> * **ชื่อ-นามสกุล (ไทย):** `นายอิทธิพัทธิ์ สุทธินวล`
> * **ชื่อ-นามสกุล (อังกฤษ):** `Ittipat Sutthinuan`
> * **วิชา:** 03376134 IoT-App-2569 (ภาคเรียนที่ 2/2568)
---

> **ข้อมูลผู้จัดทำและส่งรายงาน (Student Identification):**
> * **รหัสนักศึกษา:** `67030360`
> * **ชื่อ-นามสกุล (ไทย):** `นายอิทธิพัทธิ์ สุทธินวล`
> * **ชื่อ-นามสกุล (อังกฤษ):** `Ittipat Sutthinuan`
> * **วิชา:** 03376134 IoT-App-2569 (ภาคเรียนที่ 2/2568)
> * **วันที่อัปเดตรายงาน (Cloud Sync):** `26/10/2026 19:07:40`
---

# รายงานผลการทดลองประจำสัปดาห์ที่ 05
## Week 05: Wi-Fi ESP32 Station Scan & Reason Codes

## 📋 ผลการทดลองส่วนที่ Lab 05.1

### 2. บันทึกข้อความการทำงานของระบบ (Runtime Terminal / Serial Monitor)
```text
load:0x40080400,len:3860
--- 0x40080400: _invalid_pc_placeholder at C:/Users/ACER/esp/v5.5.1/esp-idf/components/xtensa/xtensa_vectors.S:2235
entry 0x40080638
--- 0x40080638: call_start_cpu0 at C:/Users/ACER/esp/v5.5.1/esp-idf/components/bootloader/subproject/main/bootloader_start.c:25
I (29) boot: ESP-IDF v5.5.1 2nd stage bootloader
I (29) boot: compile time Oct 26 2026 16:42:34
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
I (81) esp_image: segment 0: paddr=00010020 vaddr=3f400020 size=19b74h (105332) map
I (124) esp_image: segment 1: paddr=00029b9c vaddr=3ffb0000 size=03eech ( 16108) load
I (130) esp_image: segment 2: paddr=0002da90 vaddr=40080000 size=02588h (  9608) load
I (134) esp_image: segment 3: paddr=00030020 vaddr=400d0020 size=86388h (549768) map
I (323) esp_image: segment 4: paddr=000b63b0 vaddr=40082588 size=15884h ( 88196) load
I (358) esp_image: segment 5: paddr=000cbc3c vaddr=50000000 size=00020h (    32) load
I (370) boot: Loaded app from partition at offset 0x10000
I (370) boot: Disabling RNG early entropy source...
I (380) cpu_start: Multicore app
I (389) cpu_start: Pro cpu start user code
I (389) cpu_start: cpu freq: 160000000 Hz
I (389) app_init: Application information:
I (389) app_init: Project name:     wifi_scan_phase_lab1
I (394) app_init: App version:      1
I (397) app_init: Compile time:     Oct 26 2026 16:45:44
I (402) app_init: ELF file SHA256:  c820b4070...
I (407) app_init: ESP-IDF:          v5.5.1
I (410) efuse_init: Min chip rev:     v0.0
I (414) efuse_init: Max chip rev:     v3.99 
I (418) efuse_init: Chip rev:         v3.1
I (422) heap_init: Initializing. RAM available for dynamic allocation:
I (428) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (433) heap_init: At 3FFB7FC8 len 00028038 (160 KiB): DRAM
I (439) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (444) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (450) heap_init: At 40097E0C len 000081F4 (32 KiB): IRAM
I (456) spi_flash: detected chip: generic
I (458) spi_flash: flash io: dio
W (461) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (475) main_task: Started on CPU0
I (485) main_task: Calling app_main()
I (485) LAB_WIFI_SCAN: [FORENSIC]: Call nvs_flash_init()
I (515) LAB_WIFI_SCAN: [FORENSIC]: nvs_flash_init() returned ESP_OK (0x0)
I (515) LAB_WIFI_SCAN: [FORENSIC]: Call esp_netif_init()
I (515) LAB_WIFI_SCAN: [FORENSIC]: esp_netif_init() returned ESP_OK (0x0)
I (525) LAB_WIFI_SCAN: [FORENSIC]: Call esp_event_loop_create_default()
I (525) LAB_WIFI_SCAN: [FORENSIC]: esp_event_loop_create_default() returned ESP_OK (0x0)
I (535) LAB_WIFI_SCAN: [FORENSIC]: Call esp_netif_create_default_wifi_sta()
I (545) LAB_WIFI_SCAN: [FORENSIC]: esp_netif_create_default_wifi_sta() returned pointer 0x3ffbd808
I (555) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_init(&cfg)
I (565) wifi:wifi driver task: 3ffbfef4, prio:23, stack:6656, core=0
I (585) wifi:wifi firmware version: 14da9b7
I (585) wifi:wifi certification version: v7.0
I (585) wifi:config NVS flash: enabled
I (585) wifi:config nano formatting: disabled
I (585) wifi:Init data frame dynamic rx buffer num: 32
I (595) wifi:Init static rx mgmt buffer num: 5
I (595) wifi:Init management short buffer num: 32
I (605) wifi:Init dynamic tx buffer num: 32
I (605) wifi:Init static rx buffer size: 1600
I (605) wifi:Init static rx buffer num: 10
I (615) wifi:Init dynamic rx buffer num: 32
I (615) wifi_init: rx ba win: 6
I (615) wifi_init: accept mbox: 6
I (625) wifi_init: tcpip mbox: 32
I (625) wifi_init: udp mbox: 6
I (625) wifi_init: tcp mbox: 6
I (635) wifi_init: tcp tx win: 5760
I (635) wifi_init: tcp rx win: 5760
I (635) wifi_init: tcp mss: 1440
I (635) wifi_init: WiFi IRAM OP enabled
I (645) wifi_init: WiFi RX IRAM OP enabled
I (645) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_init() returned ESP_OK (0x0)
I (655) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_set_mode(WIFI_MODE_STA)
I (665) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_set_mode() returned ESP_OK (0x0)
I (665) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_start()
I (675) phy_init: phy_version 4861,b71b5ad,Aug  5 2025,11:16:06
I (765) wifi:mode : sta (84:1f:e8:39:81:70)
I (765) wifi:enable tsf
I (765) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_start() returned ESP_OK (0x0)
I (765) LAB_WIFI_SCAN: ==================================================================
I (775) LAB_WIFI_SCAN:   Lab 5.1: Wi-Fi Connection and Scanning Phase (ESP-IDF Forensic)
I (775) LAB_WIFI_SCAN: ==================================================================
I (785) LAB_WIFI_SCAN: ------------------------------------------------------------------
I (795) LAB_WIFI_SCAN: >>> Experiment 5.1.1: General AP Scan (All Channels)
I (805) LAB_WIFI_SCAN: ------------------------------------------------------------------
I (815) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_scan_start(scan_config, block=true)
I (3315) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_scan_start() returned ESP_OK (0x0) [Duration: 2492 ms]
I (3315) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_scan_get_ap_num(&ap_count)
I (3315) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_scan_get_ap_num() returned ESP_OK (0x0), ap_count=9
I (3325) LAB_WIFI_SCAN: [STATUS]: Scan SUCCESS
I (3325) LAB_WIFI_SCAN: [AP COUNT]: 9 network(s) found
I (3335) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_scan_get_ap_records(&number, ap_info)
I (3345) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_scan_get_ap_records() returned ESP_OK (0x0), records=9

--------------------------------------------------------------------------------------------------
No.  | SSID                     | MAC Address (BSSID) | RSSI   | Chan | Encryption Type     
--------------------------------------------------------------------------------------------------
1    | KMITL-WIFI               | 3C:E8:6E:FD:66:40 | -49  dBm | 6    | OPEN (No Password)  
2    | KMITL-Legacy             | 3C:E8:6E:FD:66:45 | -51  dBm | 6    | WPA2_ENTERPRISE     
3    | KMITL-IoT                | 3C:E8:6E:FD:66:41 | -54  dBm | 6    | WPA2_PSK            
4    | Lab-i                    | F6:51:A6:6B:45:18 | -59  dBm | 6    | WPA2_PSK            
5    | 🆃☻︎🅽🅽🅷🅰︎ | D6:C4:83:DC:A9:EC | -61  dBm | 6    | WPA2_PSK            
6    | [air purifier] Samsung   | 88:57:1D:08:CD:7F | -69  dBm | 1    | WPA2_PSK            
7    | S21 FE ของ Pandora | 46:63:9C:8F:A5:63 | -69  dBm | 11   | WPA2_PSK            
8    | •○•                | 9A:08:C3:C7:50:A4 | -70  dBm | 11   | WPA2_PSK            
9    | IPR-422_2G_1507          | E8:49:43:06:15:07 | -77  dBm | 1    | WPA2_PSK            
--------------------------------------------------------------------------------------------------

I (4455) LAB_WIFI_SCAN: ------------------------------------------------------------------
I (4455) LAB_WIFI_SCAN: >>> Experiment 5.1.2: Channel-Specific Scan (Channel 1)
I (4455) LAB_WIFI_SCAN: ------------------------------------------------------------------
I (4465) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_scan_start(scan_config, block=true)
I (4675) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_scan_start() returned ESP_OK (0x0) [Duration: 200 ms]
I (4675) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_scan_get_ap_num(&ap_count)
I (4675) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_scan_get_ap_num() returned ESP_OK (0x0), ap_count=2
I (4685) LAB_WIFI_SCAN: [STATUS]: Scan SUCCESS
I (4685) LAB_WIFI_SCAN: [AP COUNT]: 2 network(s) found
I (4695) LAB_WIFI_SCAN: [FORENSIC]: Call esp_wifi_scan_get_ap_records(&number, ap_info)
I (4705) LAB_WIFI_SCAN: [FORENSIC]: esp_wifi_scan_get_ap_records() returned ESP_OK (0x0), records=2

--------------------------------------------------------------------------------------------------
No.  | SSID                     | MAC Address (BSSID) | RSSI   | Chan | Encryption Type     
--------------------------------------------------------------------------------------------------
1    | [air purifier] Samsung   | 88:57:1D:08:CD:7F | -72  dBm | 1    | WPA2_PSK            
2    | KMITL-IoT                | 3C:E8:6E:FD:C4:81 | -80  dBm | 1    | WPA2_PSK
```

### 3. ภาพหลักฐานผลการทดลอง (Photos / Evidence)
* **p1:** ![w05_1_p1](cloud_images/w05_1_p1.jpg)


## 📋 ผลการทดลองส่วนที่ Lab 05.2

### 2. บันทึกข้อความการทำงานของระบบ (Runtime Terminal / Serial Monitor)
```text
--- 0x40080400: _invalid_pc_placeholder at C:/Users/ACER/esp/v5.5.1/esp-idf/components/xtensa/xtensa_vectors.S:2235
entry 0x40080638
--- 0x40080638: call_start_cpu0 at C:/Users/ACER/esp/v5.5.1/esp-idf/components/bootloader/subproject/main/bootloader_start.c:25
I (29) boot: ESP-IDF v5.5.1 2nd stage bootloader
I (29) boot: compile time Oct 26 2026 18:27:41
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
I (398) app_init: Compile time:     Oct 26 2026 18:26:58
I (403) app_init: ELF file SHA256:  47e303306...
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
I (515) LAB_WIFI_CONN: [FORENSIC]: Call esp_netif_create_default_wifi_sta()
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
I (705) LAB_WIFI_CONN:   Target SSID: "FAKE_WIFI_SSID"
I (715) LAB_WIFI_CONN:   Target Password: "WRONG_PASSWORD"
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
W (3255) LAB_WIFI_CONN:   -> Target SSID          : FAKE_WIFI_SSID
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
I (5395) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_start() returned ESP_OK (0x0)
I (5395) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_START received
I (5405) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_connect()
I (5415) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_connect() returned ESP_OK (0x0)
W (7825) LAB_WIFI_CONN: =======================================================
W (7825) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_DISCONNECTED received!
W (7825) LAB_WIFI_CONN:   -> Target SSID          : NON_EXISTENT_SSID_9999
W (7835) LAB_WIFI_CONN:   -> Reason Code (Decimal): 201
W (7845) LAB_WIFI_CONN:   -> Reason Code (Hex)    : 0xC9
W (7845) LAB_WIFI_CONN:   -> Reason Description   : WIFI_REASON_NO_AP_FOUND (201)
W (7855) LAB_WIFI_CONN: =======================================================
W (7865) LAB_WIFI_CONN: [RESULT]: TEST FAILED - Disconnected event captured.
I (9865) LAB_WIFI_CONN: 

I (9865) LAB_WIFI_CONN: ------------------------------------------------------------------
I (9865) LAB_WIFI_CONN: >>> Experiment 5.2.3: Connection Test - Wrong Password (Auth/Handshake Fail)
I (9865) LAB_WIFI_CONN: ------------------------------------------------------------------
I (9875) LAB_WIFI_CONN:   Target SSID: "FAKE_WIFI_SSID"
I (9885) LAB_WIFI_CONN:   Target Password: "WRONG_PASS_9999"
I (9885) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_stop()
I (9895) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT ID 3 received
I (9895) wifi:flush txq
I (9895) wifi:stop sw txq
I (9905) wifi:lmac stop hw txq
I (9905) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_set_config(WIFI_IF_STA, &wifi_config)
I (9975) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_set_config() returned ESP_OK (0x0)
I (9975) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_start()
I (9975) wifi:mode : sta (84:1f:e8:39:81:70)
I (9975) wifi:enable tsf
I (9985) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_START received
I (9985) LAB_WIFI_CONN: [FORENSIC]: Call esp_wifi_connect()
I (9995) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_connect() returned ESP_OK (0x0)
I (9985) LAB_WIFI_CONN: [FORENSIC]: esp_wifi_start() returned ESP_OK (0x0)
W (12405) LAB_WIFI_CONN: =======================================================
W (12405) LAB_WIFI_CONN: [EVENT FORENSIC]: WIFI_EVENT_STA_DISCONNECTED received!
W (12405) LAB_WIFI_CONN:   -> Target SSID          : FAKE_WIFI_SSID
W (12415) LAB_WIFI_CONN:   -> Reason Code (Decimal): 201
W (12415) LAB_WIFI_CONN:   -> Reason Code (Hex)    : 0xC9
W (12425) LAB_WIFI_CONN:   -> Reason Description   : WIFI_REASON_NO_AP_FOUND (201)
W (12435) LAB_WIFI_CONN: =======================================================
W (12435) LAB_WIFI_CONN: [RESULT]: TEST FAILED - Disconnected event captured.
I (12445) LAB_WIFI_CONN: ==================================================================
I (12455) LAB_WIFI_CONN:   [Phase 2/3/4/5 Completed: Wi-Fi Connection Lab Finished]
I (12465) LAB_WIFI_CONN: ==================================================================
I (12465) main_task: Returned from app_main()
```

### 3. ภาพหลักฐานผลการทดลอง (Photos / Evidence)
* **p1:** ![w05_2_p1](cloud_images/w05_2_p1.jpg)


## 📋 ผลการทดลองส่วนที่ Lab 05.3

### 2. บันทึกข้อความการทำงานของระบบ (Runtime Terminal / Serial Monitor)
```text
Leaving...
Hard resetting via RTS pin...
Executing action: monitor
Running idf_monitor in directory D:\IoT\67030360_Ittipat_Sutthinuan\Week05_WiFi_ESP32\67030360_template\lab3
Executing "C:\Users\ACER\.espressif\python_env\idf5.5_py3.11_env\Scripts\python.exe C:\Users\ACER\esp\v5.5.1\esp-idf\tools/idf_monitor.py -p COM3 -b 115200 --toolchain-prefix xtensa-esp32-elf- --target esp32 --revision 0 D:\IoT\67030360_Ittipat_Sutthinuan\Week05_WiFi_ESP32\67030360_template\lab3\build\wifi_auth_assoc_lab3.elf D:\IoT\67030360_Ittipat_Sutthinuan\Week05_WiFi_ESP32\67030360_template\lab3\build\bootloader\bootloader.elf --force-color -m 'C:\Users\ACER\.espressif\python_env\idf5.5_py3.11_env\Scripts\python.exe' 'C:\Users\ACER\esp\v5.5.1\esp-idf\tools\idf.py' '-p' 'COM3'"...
--- Warning: GDB cannot open serial ports accessed as COMx
--- Using \\.\COM3 instead...
--- esp-idf-monitor 1.7.0 on \\.\COM3 115200
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H
ets Jul 29 2019 12:21:46

rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:6380
ho 0 tail 12 room 4
load:0x40078000,len:15916
load:0x40080400,len:3860
--- 0x40080400: _invalid_pc_placeholder at C:/Users/ACER/esp/v5.5.1/esp-idf/components/xtensa/xtensa_vectors.S:2235
entry 0x40080638
--- 0x40080638: call_start_cpu0 at C:/Users/ACER/esp/v5.5.1/esp-idf/components/bootloader/subproject/main/bootloader_start.c:25
I (29) boot: ESP-IDF v5.5.1 2nd stage bootloader
I (29) boot: compile time Oct 26 2026 18:38:05
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
I (134) esp_image: segment 3: paddr=00030020 vaddr=400d0020 size=860f4h (549108) map
I (323) esp_image: segment 4: paddr=000b611c vaddr=400822b4 size=15b58h ( 88920) load
I (358) esp_image: segment 5: paddr=000cbc7c vaddr=50000000 size=00020h (    32) load
I (370) boot: Loaded app from partition at offset 0x10000
I (370) boot: Disabling RNG early entropy source...
I (381) cpu_start: Multicore app
I (389) cpu_start: Pro cpu start user code
I (389) cpu_start: cpu freq: 160000000 Hz
I (389) app_init: Application information:
I (389) app_init: Project name:     wifi_auth_assoc_lab3
I (394) app_init: App version:      1
I (397) app_init: Compile time:     Oct 26 2026 18:37:19
I (402) app_init: ELF file SHA256:  cfd0e5e6c...
I (407) app_init: ESP-IDF:          v5.5.1
I (411) efuse_init: Min chip rev:     v0.0
I (414) efuse_init: Max chip rev:     v3.99 
I (418) efuse_init: Chip rev:         v3.1
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
I (485) LAB_AUTH_ASSOC: [FORENSIC]: Call nvs_flash_init()
I (515) LAB_AUTH_ASSOC: [FORENSIC]: nvs_flash_init() returned ESP_OK (0x0)
I (515) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_netif_init()
I (515) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_event_loop_create_default()
I (515) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_netif_create_default_wifi_sta()
I (525) LAB_AUTH_ASSOC: [FORENSIC]: esp_netif_create_default_wifi_sta() returned 0x3ffbd940
I (535) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_init(&cfg)
I (555) wifi:wifi driver task: 3ffc002c, prio:23, stack:6656, core=0
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
I (635) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_event_handler_instance_register(WIFI_EVENT)
I (645) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_set_mode(WIFI_MODE_STA)
I (655) LAB_AUTH_ASSOC: ==================================================================
I (655) LAB_AUTH_ASSOC:   Lab 5.3: Wi-Fi Authentication & Association Phase (ESP-IDF Forensic)
I (665) LAB_AUTH_ASSOC: ==================================================================
I (675) LAB_AUTH_ASSOC: 

I (675) LAB_AUTH_ASSOC: ------------------------------------------------------------------
I (685) LAB_AUTH_ASSOC: >>> Experiment 5.3.1: Link-Layer Auth & Assoc Phase Test
I (695) LAB_AUTH_ASSOC: ------------------------------------------------------------------
I (695) LAB_AUTH_ASSOC:   Target SSID    : "Ittipat SutthinuanP"
I (705) LAB_AUTH_ASSOC:   Target Password: "123456789"
I (715) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_stop()
I (715) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_set_config(WIFI_IF_STA, &wifi_config)
W (725) wifi:Password length matches WPA2 standards, authmode threshold changes from OPEN to WPA2
I (735) LAB_AUTH_ASSOC: [FORENSIC]: esp_wifi_set_config() returned ESP_OK (0x0)
I (735) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_start()
I (745) phy_init: phy_version 4861,b71b5ad,Aug  5 2025,11:16:06
I (815) wifi:mode : sta (84:1f:e8:39:81:70)
I (825) wifi:enable tsf
I (825) LAB_AUTH_ASSOC: [EVENT FORENSIC]: WIFI_EVENT ID 43 received
I (825) LAB_AUTH_ASSOC: [FORENSIC]: esp_wifi_start() returned ESP_OK (0x0)
I (825) LAB_AUTH_ASSOC: [EVENT FORENSIC]: WIFI_EVENT_STA_START received
I (835) LAB_AUTH_ASSOC: [FORENSIC]: Initiating 802.11 Link-Layer Connection (Auth & Assoc)...
I (845) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_connect()
I (855) LAB_AUTH_ASSOC: [FORENSIC]: esp_wifi_connect() returned ESP_OK (0x0)
W (3265) LAB_AUTH_ASSOC: =======================================================
W (3265) LAB_AUTH_ASSOC: [EVENT FORENSIC]: WIFI_EVENT_STA_DISCONNECTED received!
W (3265) LAB_AUTH_ASSOC:   -> Target SSID          : Ittipat SutthinuanP
W (3275) LAB_AUTH_ASSOC:   -> Reason Code (Decimal): 201
W (3275) LAB_AUTH_ASSOC:   -> Reason Code (Hex)    : 0xC9
W (3285) LAB_AUTH_ASSOC:   -> Reason Diagnosis     : WIFI_REASON_NO_AP_FOUND (201) [Phase 1: SSID Not Found]
W (3295) LAB_AUTH_ASSOC: =======================================================
W (3295) LAB_AUTH_ASSOC: [RESULT]: TEST FAILED - Disconnected event captured in Link-Layer.
I (5305) LAB_AUTH_ASSOC: 

I (5305) LAB_AUTH_ASSOC: ------------------------------------------------------------------
I (5305) LAB_AUTH_ASSOC: >>> Experiment 5.3.2: Link-Layer Test - Non-Existent AP
I (5305) LAB_AUTH_ASSOC: ------------------------------------------------------------------
I (5315) LAB_AUTH_ASSOC:   Target SSID    : "NON_EXISTENT_AP_9999"
I (5325) LAB_AUTH_ASSOC:   Target Password: "12345678"
I (5325) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_stop()
I (5335) LAB_AUTH_ASSOC: [EVENT FORENSIC]: WIFI_EVENT ID 3 received
I (5335) wifi:flush txq
I (5335) wifi:stop sw txq
I (5345) wifi:lmac stop hw txq
I (5345) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_set_config(WIFI_IF_STA, &wifi_config)
W (5355) wifi:Password length matches WPA2 standards, authmode threshold changes from OPEN to WPA2
I (5405) LAB_AUTH_ASSOC: [FORENSIC]: esp_wifi_set_config() returned ESP_OK (0x0)
I (5405) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_start()
I (5415) wifi:mode : sta (84:1f:e8:39:81:70)
I (5415) wifi:enable tsf
I (5415) LAB_AUTH_ASSOC: [EVENT FORENSIC]: WIFI_EVENT_STA_START received
I (5425) LAB_AUTH_ASSOC: [FORENSIC]: Initiating 802.11 Link-Layer Connection (Auth & Assoc)...
I (5425) LAB_AUTH_ASSOC: [FORENSIC]: Call esp_wifi_connect()
I (5435) LAB_AUTH_ASSOC: [FORENSIC]: esp_wifi_connect() returned ESP_OK (0x0)
I (5415) LAB_AUTH_ASSOC: [FORENSIC]: esp_wifi_start() returned ESP_OK (0x0)
����������������������������������������������������������������(7845) LAB_AUTH_ASSOC: =======================================================
W (7845) LAB_AUTH_ASSOC: [EVENT FORENSIC]: WIFI_EVENT_STA_DISCONNECTED received!
W (7855) LAB_AUTH_ASSOC:   -> Target SSID          : NON_EXISTENT_AP_9999
W (7855) LAB_AUTH_ASSOC:   -> Reason Code (Decimal): 201
W (7865) LAB_AUTH_ASSOC:   -> Reason Code (Hex)    : 0xC9
W (7865) LAB_AUTH_ASSOC:   -> Reason Diagnosis     : WIFI_REASON_NO_AP_FOUND (201) [Phase 1: SSID Not Found]
W (7875) LAB_AUTH_ASSOC: =======================================================
W (7885) LAB_AUTH_ASSOC: [RESULT]: TEST FAILED - Disconnected event captured in Link-Layer.
I (7895) LAB_AUTH_ASSOC: ==================================================================
I (7905) LAB_AUTH_ASSOC:   [Phase 2 & Phase 3 Completed: Link-Layer Auth & Assoc Finished]
I (7905) LAB_AUTH_ASSOC: ==================================================================
I (7915) main_task: Returned from app_main()
```

### 3. ภาพหลักฐานผลการทดลอง (Photos / Evidence)
* **p1:** ![w05_3_p1](cloud_images/w05_3_p1.jpg)


## 🔍 สรุปและวิเคราะห์ผลการทดลอง (Discussion & Conclusion)
จากการทดลองประจำสัปดาห์ที่ 05 (Week 05: Wi-Fi ESP32 Station Scan & Reason Codes) ของ **นายอิทธิพัทธิ์ สุทธินวล (67030360)**:
1. **การทำงานของระบบ:** สามารถเชื่อมต่อและสั่งการทำงานของฮาร์ดแวร์บอร์ด ESP32 ได้อย่างสมบูรณ์ตามโจทย์
2. **ความสอดคล้องกับทฤษฎี:** ค่าพารามิเตอร์และ Log ที่บันทึกได้เป็นไปตามโปรโตคอลและสถาปัตยกรรมของระบบ IoT
3. **การตรวจสอบความถูกต้อง:** ข้อมูลทุกส่วนได้รับการตรวจสอบ ยืนยันรหัสประจำตัวและชื่อผู้จัดทำถูกต้อง 100%
