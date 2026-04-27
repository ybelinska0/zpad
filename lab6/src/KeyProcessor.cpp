#include "KeyProcessor.hpp"
#include <iostream>

KeyProcessor::KeyProcessor() : currentMode(ProcessMode::NORMAL) {}

void KeyProcessor::processKey(int key) {
    if (key == -1) return; // Клавішу не натиснуто

    switch (key) {
        case '1': currentMode = ProcessMode::NORMAL; std::cout << "Режим: NORMAL\n"; break;
        case '2': currentMode = ProcessMode::INVERT; std::cout << "Режим: INVERT\n"; break;
        case '3': currentMode = ProcessMode::BLUR; std::cout << "Режим: BLUR\n"; break;
        case '4': currentMode = ProcessMode::CANNY; std::cout << "Режим: CANNY\n"; break;
        case '5': currentMode = ProcessMode::GLITCH; std::cout << "Режим: GLITCH\n"; break;
    }
}

ProcessMode KeyProcessor::getCurrentMode() const {
    return currentMode;
}
