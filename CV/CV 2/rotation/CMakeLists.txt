cmake_minimum_required(VERSION 3.10)
project( run )
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
message(STATUS "Requested C++ Standard: ${CMAKE_CXX_STANDARD}")
execute_process(
    COMMAND ${CMAKE_CXX_COMPILER} --version
    OUTPUT_VARIABLE CXX_COMPILER_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
message(STATUS "C++ Compiler Version: ${CXX_COMPILER_VERSION}")
find_package( OpenCV REQUIRED )
include_directories(${OpenCV_INCLUDE_DIRS})
add_executable( run c.cpp )
target_link_libraries( run ${OpenCV_LIBS} )
