#!/bin/bash
# 1-Click Environment Setup for 67030299 (นางสาวธนพร พิศมัย)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030299 - นางสาวธนพร พิศมัย"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030299 --name-en "Thanaporn Pitsamai" --name-th "นางสาวธนพร พิศมัย" --wifi "IoT-Lab-0299" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
