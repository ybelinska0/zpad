#include <iostream>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"

// Глобальна змінна для Trackbar (яскравість)
int brightnessValue = 50; 

int main() {
    CameraProvider camera(0);
    if (!camera.isOpened()) return -1;

    Display display("Lab 6 - OpenCV");
    KeyProcessor keyProcessor;
    FrameProcessor frameProcessor;

    // Створюємо інтерактивний слайдер (Trackbar)
    cv::createTrackbar("Brightness", display.getWindowName(), &brightnessValue, 100);

    std::cout << "Програму запущено. Натисніть 'ESC' або 'q' для виходу.\n";
    std::cout << "Клавіші 1-5 для зміни режимів.\n";

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        // Обробка кадру
        cv::Mat processedFrame = frameProcessor.process(frame, keyProcessor.getCurrentMode(), brightnessValue);

        // Відображення
        display.show(processedFrame);

        // Обробка клавіатури (затримка 1 мс)
        int key = cv::waitKey(1);
        if (key == 27 || key == 'q') { // ESC або q
            break;
        }
        
        keyProcessor.processKey(key);
    }

    return 0;
}
