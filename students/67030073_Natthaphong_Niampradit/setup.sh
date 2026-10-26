#!/bin/bash
# 1-Click Environment Setup for 67030073 (นายณัฐพงศ์ เนียมประดิษฐ)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030073 - นายณัฐพงศ์ เนียมประดิษฐ"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030073 --name-en "Natthaphong Niampradit" --name-th "นายณัฐพงศ์ เนียมประดิษฐ" --wifi "IoT-Lab-0073" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
