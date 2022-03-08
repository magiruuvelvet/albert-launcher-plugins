cmake_minimum_required(VERSION 3.14)
set(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH}" "${CMAKE_CURRENT_LIST_DIR}/../../lib/cmake/modules")

project(clipboard CXX)
include(ProjectSetup)

add_subdirectory(src)
