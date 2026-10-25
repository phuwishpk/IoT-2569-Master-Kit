#!/bin/bash
# 1-Click Environment Setup for 67030248 (นายสุวิจักขณ์ ลาวัง)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030248 - นายสุวิจักขณ์ ลาวัง"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030248 --name-en "Suwijak Lawang" --name-th "นายสุวิจักขณ์ ลาวัง" --wifi "IoT-Lab-0248" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
