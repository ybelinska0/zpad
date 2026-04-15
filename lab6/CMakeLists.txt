cmake_minimum_required(VERSION 3.10)
project(lab6_opencv)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenCV REQUIRED)
include_directories(include ${OpenCV_INCLUDE_DIRS})

file(GLOB SOURCES "src/*.cpp")

add_executable(lab6_app ${SOURCES})
target_link_libraries(lab6_app ${OpenCV_LIBS})
