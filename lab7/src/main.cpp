#include <iostream>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"
#include "FaceDetector.hpp"

// Глобальна змінна для слайдера яскравості
int brightnessValue = 50; 

int main() {
    // 1. Ініціалізуємо нейромережу. 
    // Шлях вказуємо відносно папки build (де лежить екзешник), тому ідемо на рівень вище у папку models
    FaceDetector faceDetector("models/deploy.prototxt", "models/res10_300x300_ssd_iter_140000.caffemodel");

    // 2. Ініціалізуємо камеру
    CameraProvider camera(0);
    if (!camera.isOpened()) {
        std::cerr << "Не вдалося відкрити камеру!" << std::endl;
        return -1;
    }

    // 3. Створюємо інші компоненти
    Display display("Lab 7 - Face Detection (Multi-threading)");
    KeyProcessor keyProcessor;
    FrameProcessor frameProcessor;

    // Створюємо слайдер яскравості у вікні
    cv::createTrackbar("Brightness", display.getWindowName(), &brightnessValue, 100);

    std::cout << "Програму запущено.\n";
    std::cout << "Клавіші:\n'6' - увімкнути детекцію облич\n'1-5' - інші фільтри\n'q' - вихід\n";

    while (true) {
        // Отримуємо кадр з камери
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        // ОБРОБКА: передаємо в метод process поточний режим та вказівник на наш FaceDetector
        // Тепер FrameProcessor сам вирішить: просто накласти фільтр чи задіяти нейронку
        cv::Mat processedFrame = frameProcessor.process(
            frame, 
            keyProcessor.getCurrentMode(), 
            brightnessValue, 
            &faceDetector
        );

        // ВІДОБРАЖЕННЯ
        display.show(processedFrame);

        // КЕРУВАННЯ
        int key = cv::waitKey(1);
        if (key == 27 || key == 'q') {
            break;
        }
        
        keyProcessor.processKey(key);
    }

    return 0;
}
