#pragma once

enum class ProcessMode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY,
    GLITCH,
    FACE_DETECT
};

class KeyProcessor {
private:
    ProcessMode currentMode;
public:
    KeyProcessor();
    void processKey(int key);
    ProcessMode getCurrentMode() const;
};
