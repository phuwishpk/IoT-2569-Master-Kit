#!/bin/bash
# 1-Click Environment Setup for 67030180 (นายภูมิชนะ เทียมแก้ว)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030180 - นายภูมิชนะ เทียมแก้ว"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030180 --name-en "Phumchana Thiamkaew" --name-th "นายภูมิชนะ เทียมแก้ว" --wifi "IoT-Lab-0180" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
