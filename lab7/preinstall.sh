#!/bin/bash
echo "Оновлення системи та встановлення залежностей..."
sudo apt update -y
sudo apt install build-essential cmake libopencv-dev gcc g++ wget -y

echo "Завантаження моделей нейромережі..."
# Створюємо папку для моделей, якщо її немає
mkdir -p models
cd models

# Завантажуємо конфігурацію (архітектуру)
if [ ! -f deploy.prototxt ]; then
    wget https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
fi

# Завантажуємо ваги (саму нейромережу)
if [ ! -f res10_300x300_ssd_iter_140000.caffemodel ]; then
    wget https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
fi

cd ..
echo "Встановлення завершено!"
