cmake_minimum_required(VERSION 3.15.0)
project(
    test_pattern_analyzer
    VERSION 0.1.0
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# universal binaries
# set(CMAKE_OSX_ARCHITECTURES arm64;x86_64)
add_executable(test_main ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp)
