cmake_minimum_required(VERSION 3.10)
project(lab7_opencv_dnn) 

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Шукаємо потоки
find_package(Threads REQUIRED)

find_package(OpenCV REQUIRED)
include_directories(include ${OpenCV_INCLUDE_DIRS})

file(GLOB SOURCES "src/*.cpp")

add_executable(lab7_app ${SOURCES})
# Лінкуємо OpenCV та Threads
target_link_libraries(lab7_app ${OpenCV_LIBS} Threads::Threads)
