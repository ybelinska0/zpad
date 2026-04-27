#include "FrameProcessor.hpp"
#include <vector>

cv::Mat FrameProcessor::process(const cv::Mat& inputFrame, ProcessMode mode, int brightness, FaceDetector* faceDetector) {
    cv::Mat result;
    // Налаштування яскравості
    inputFrame.convertTo(result, -1, 1, brightness - 50); 

    switch (mode) {
        case ProcessMode::INVERT: {
            cv::bitwise_not(result, result);
            break;
        }

        case ProcessMode::BLUR: {
            cv::GaussianBlur(result, result, cv::Size(15, 15), 0);
            break;
        }

        case ProcessMode::CANNY: {
            cv::Mat gray, edges;
            cv::cvtColor(result, gray, cv::COLOR_BGR2GRAY);
            cv::Canny(gray, edges, 50, 150);
            cv::cvtColor(edges, result, cv::COLOR_GRAY2BGR);
            break;
        }

        case ProcessMode::GLITCH: {
    std::vector<cv::Mat> channels;
    cv::split(result, channels);

    // Створюємо порожні канали (заповнені чорним) такого ж розміру, як оригінал
    cv::Mat R = cv::Mat::zeros(channels[2].size(), channels[2].type());
    cv::Mat B = cv::Mat::zeros(channels[0].size(), channels[0].type());
    
    int offset = 20; // Зсув у пікселях

    // ПЕРЕВІРКА: чи не виходимо ми за межі кадру
    if (result.cols > offset) {
        // Вирізаємо частину з оригінального каналу
        cv::Rect sourceRect(offset, 0, result.cols - offset, result.rows);
        // Вказуємо, куди вставити в нову матрицю (зсуваємо вліво)
        cv::Rect targetRect(0, 0, result.cols - offset, result.rows);

        channels[2](sourceRect).copyTo(R(targetRect));
        
        // Для синього каналу робимо зсув у інший бік
        cv::Rect sourceRectB(0, 0, result.cols - offset, result.rows);
        cv::Rect targetRectB(offset, 0, result.cols - offset, result.rows);
        
        channels[0](sourceRectB).copyTo(B(targetRectB));
    } else {
        // Якщо кадр занадто малий, просто копіюємо як є
        channels[2].copyTo(R);
        channels[0].copyTo(B);
    }
    
    // Збираємо канали назад
    std::vector<cv::Mat> glitchChannels = {B, channels[1], R};
    cv::merge(glitchChannels, result);
    break;
}
        
        case ProcessMode::FACE_DETECT: {
            if (faceDetector != nullptr) {
                // Відправляємо на обробку
                faceDetector->processFrameAsync(result);

                // Забираємо результат детекції
                std::vector<cv::Rect> faces = faceDetector->getFaces();

                // Малюємо рамки
                for (const auto& face : faces) {
                    cv::rectangle(result, face, cv::Scalar(0, 255, 0), 2);
                    cv::putText(result, "Face: 99%", cv::Point(face.x, face.y - 10), 
                                cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 255, 0), 2);
                }
            }
            break;
        }

        case ProcessMode::NORMAL:
        default:
            break;
    }

    // Виводимо текст поточного режиму
    cv::putText(result, "Mode: " + std::to_string(static_cast<int>(mode)), cv::Point(10, 30),
                cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 255, 0), 2);
    
    return result;
}
