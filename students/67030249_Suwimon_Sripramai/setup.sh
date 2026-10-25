#!/bin/bash
# 1-Click Environment Setup for 67030249 (นางสาวสุวิมล ศรีประไหม)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030249 - นางสาวสุวิมล ศรีประไหม"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030249 --name-en "Suwimon Sripramai" --name-th "นางสาวสุวิมล ศรีประไหม" --wifi "IoT-Lab-0249" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
