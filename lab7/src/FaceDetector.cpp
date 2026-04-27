#include "FaceDetector.hpp"
#include <iostream>

FaceDetector::FaceDetector(const std::string& configPath, const std::string& modelPath) 
    : isRunning(true), hasNewFrame(false) 
{
    // Завантажуємо мережу
    net = cv::dnn::readNetFromCaffe(configPath, modelPath);
    // Запускаємо фоновий потік (Worker Thread)
    workerThread = std::thread(&FaceDetector::detectionLoop, this);
}

FaceDetector::~FaceDetector() {
    isRunning = false;
    if (workerThread.joinable()) workerThread.join();
}

void FaceDetector::processFrameAsync(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(dataMutex);
    frame.copyTo(currentFrame); // Відправляємо копію кадру (під м'ютексом)
    hasNewFrame = true;
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(dataMutex);
    return detectedFaces; // Забираємо координати (під м'ютексом)
}

void FaceDetector::detectionLoop() {
    while (isRunning) {
        cv::Mat frameToProcess;
        bool shouldProcess = false;

        // Чекаємо на новий кадр
        {
            std::lock_guard<std::mutex> lock(dataMutex);
            if (hasNewFrame && !currentFrame.empty()) {
                currentFrame.copyTo(frameToProcess);
                hasNewFrame = false;
                shouldProcess = true;
            }
        }

        if (shouldProcess) {
            // 1. Перетворюємо кадр у blob 
            cv::Mat blob = cv::dnn::blobFromImage(frameToProcess, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
            
            // 2. Запускаємо інференс
            net.setInput(blob);
            cv::Mat detection = net.forward(); // net.forward()

            // 3. Обробляємо результати
            cv::Mat detectionMat(detection.size[2], detection.size[3], CV_32F, detection.ptr<float>());
            std::vector<cv::Rect> newFaces;

            for (int i = 0; i < detectionMat.rows; i++) {
                float confidence = detectionMat.at<float>(i, 2);
                if (confidence > 0.5) { // Фільтруємо > 50%
                    int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frameToProcess.cols);
                    int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frameToProcess.rows);
                    int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frameToProcess.cols);
                    int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frameToProcess.rows);
                    newFaces.push_back(cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2)));
                }
            }

            // 4. Оновлюємо координати у спільній змінній (під м'ютексом)
            {
                std::lock_guard<std::mutex> lock(dataMutex);
                detectedFaces = newFaces;
            }
        } else {
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        }
    }
}
