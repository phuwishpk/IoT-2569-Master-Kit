#!/bin/bash
# 1-Click Environment Setup for 67030268 (นายกร แดงทอง)
echo "=========================================================="
echo " Setting up IoT-2569 Master Kit for 67030268 - นายกร แดงทอง"
echo "=========================================================="
cd ../..
python3 setup_friend.py --id 67030268 --name-en "Korn Daengthong" --name-th "นายกร แดงทอง" --wifi "IoT-Lab-0268" --pass "12345678"
echo "Done! All templates and Lab 8.5 Dual Widgets configured."
