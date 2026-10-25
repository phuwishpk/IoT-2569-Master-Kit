#!/bin/bash
# 1-Click Environment Setup for 67030270 (นายกฤษฏิณัช สำราญกิจ)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030270 - นายกฤษฏิณัช สำราญกิจ"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030270 --name-en "Kritsadinat Samrankit" --name-th "นายกฤษฏิณัช สำราญกิจ" --wifi "IoT-Lab-0270" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
