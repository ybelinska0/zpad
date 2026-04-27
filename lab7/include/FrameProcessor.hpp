#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"
#include "FaceDetector.hpp"

class FrameProcessor {
public:
    cv::Mat process(const cv::Mat& inputFrame, ProcessMode mode, int brightness, FaceDetector* faceDetector = nullptr);
};
