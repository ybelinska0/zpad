#pragma once
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
private:
    cv::dnn::Net net;
    
    // Дані для фонового потоку
    std::thread workerThread;
    std::atomic<bool> isRunning;
    
    // Спільні ресурси (захищені м'ютексом)
    std::mutex dataMutex;
    cv::Mat currentFrame;       // Кадр, який треба обробити
    bool hasNewFrame;           // Прапорець, чи є новий кадр
    std::vector<cv::Rect> detectedFaces; // Результати детекції

    // Головна функція потоку
    void detectionLoop();

public:
    FaceDetector(const std::string& configPath, const std::string& modelPath);
    ~FaceDetector();

    // Відправити кадр на обробку (викликається з Main Thread)
    void processFrameAsync(const cv::Mat& frame);

    // Отримати останні координати облич (викликається з Main Thread)
    std::vector<cv::Rect> getFaces();
};
