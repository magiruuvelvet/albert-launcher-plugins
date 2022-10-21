cmake_minimum_required(VERSION 3.14)
set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}" "${CMAKE_CURRENT_LIST_DIR}/../kiten/cmake/modules")

project(otpgen-python CXX)
include(ProjectSetup)

add_subdirectory(otpgen-python)
