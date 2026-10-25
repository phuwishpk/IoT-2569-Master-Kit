#!/bin/bash
# 1-Click Environment Setup for 67030360 (นายอิทธิพัทธิ์ สุทธินวล)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030360 - นายอิทธิพัทธิ์ สุทธินวล"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030360 --name-en "Ittipat Sutthinuan" --name-th "นายอิทธิพัทธิ์ สุทธินวล" --wifi "IoT-Lab-0360" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
