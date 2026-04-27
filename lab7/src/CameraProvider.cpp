#include "CameraProvider.hpp"
#include <iostream>

CameraProvider::CameraProvider(int cameraId) {
    cap.open(cameraId);
    if (!cap.isOpened()) {
        std::cerr << "Помилка: Не вдалося відкрити камеру!" << std::endl;
    }
}

CameraProvider::~CameraProvider() {
    if (cap.isOpened()) cap.release();
}

bool CameraProvider::isOpened() const {
    return cap.isOpened();
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}
