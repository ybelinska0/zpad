#pragma once
#include <opencv2/opencv.hpp>

class CameraProvider {
private:
    cv::VideoCapture cap;
public:
    CameraProvider(int cameraId = 0);
    ~CameraProvider();
    bool isOpened() const;
    cv::Mat getFrame();
};
