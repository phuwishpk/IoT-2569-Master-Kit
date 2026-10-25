#!/bin/bash
# 1-Click Environment Setup for 67030359 (นายอัฐวุฒิ บัวเรียน)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030359 - นายอัฐวุฒิ บัวเรียน"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030359 --name-en "Attawut Bualian" --name-th "นายอัฐวุฒิ บัวเรียน" --wifi "IoT-Lab-0359" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
