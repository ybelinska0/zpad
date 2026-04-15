#!/bin/bash
echo "Оновлення системи та встановлення залежностей..."
sudo apt update -y
sudo apt install build-essential cmake libopencv-dev gcc g++ -y
echo "Встановлення завершено"
