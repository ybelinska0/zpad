#include "FrameProcessor.hpp"
#include <vector>

cv::Mat FrameProcessor::process(const cv::Mat& inputFrame, ProcessMode mode, int brightness) {
    cv::Mat result;
    
    // Застосовуємо яскравість (trackbar)
    inputFrame.convertTo(result, -1, 1, brightness - 50); // -50 щоб можна було робити і темніше

    switch (mode) {
        case ProcessMode::INVERT:
            cv::bitwise_not(result, result);
            break;
        case ProcessMode::BLUR:
            cv::GaussianBlur(result, result, cv::Size(15, 15), 0);
            break;
        case ProcessMode::CANNY:
            cv::cvtColor(result, result, cv::COLOR_BGR2GRAY);
            cv::Canny(result, result, 50, 150);
            break;
        case ProcessMode::GLITCH: {
            std::vector<cv::Mat> channels;
            cv::split(result, channels);
            // Зсуваємо червоний канал вправо, синій вліво
            cv::Mat R = cv::Mat::zeros(channels[2].size(), channels[2].type());
            cv::Mat B = cv::Mat::zeros(channels[0].size(), channels[0].type());
            channels[2](cv::Rect(0, 0, result.cols - 10, result.rows)).copyTo(R(cv::Rect(10, 0, result.cols - 10, result.rows)));
            channels[0](cv::Rect(10, 0, result.cols - 10, result.rows)).copyTo(B(cv::Rect(0, 0, result.cols - 10, result.rows)));
            channels[2] = R;
            channels[0] = B;
            cv::merge(channels, result);
            break;
        }
        case ProcessMode::NORMAL:
        default:
            break;
    }

    // Додаємо текст FPS/Інфо
    cv::putText(result, "Mode: " + std::to_string(static_cast<int>(mode)), cv::Point(10, 30),
                cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 255, 0), 2);
    
    return result;
}
