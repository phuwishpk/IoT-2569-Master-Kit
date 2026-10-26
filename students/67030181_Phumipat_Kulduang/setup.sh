#!/bin/bash
# 1-Click Environment Setup for 67030181 (นายภูมิพัฒน์ กุลด้วง)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030181 - นายภูมิพัฒน์ กุลด้วง"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030181 --name-en "Phumipat Kulduang" --name-th "นายภูมิพัฒน์ กุลด้วง" --wifi "IoT-Lab-0181" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
