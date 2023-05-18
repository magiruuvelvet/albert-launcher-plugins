set(CURRENT_TARGET "libotpgenpy")
set(CURRENT_TARGET_NAME "libotpgenpy")

find_package(PythonInterp 3.11 REQUIRED)
find_package(PythonLibs 3.11 REQUIRED)

message(STATUS "Python include directory: ${PYTHON_INCLUDE_DIR}")
message(STATUS "Python library: ${PYTHON_LIBRARY}")

CreateTarget(${CURRENT_TARGET} SHARED ${CURRENT_TARGET_NAME} C++ 17)

# libotp doesn't provide a cmake or pkgconf file
set(LIBOTPGEN_INCLUDE_DIR "${CMAKE_SYSTEM_INCLUDE_PATH}/otpgen")

target_include_directories(${CURRENT_TARGET}
PRIVATE
    ${PYTHON_INCLUDE_DIR}
    ${LIBOTPGEN_INCLUDE_DIR}
)

target_link_libraries(${CURRENT_TARGET}
PRIVATE
    ${PYTHON_LIBRARY}
    -lotpgen
)
