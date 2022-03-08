set(CURRENT_TARGET "clipboard-tool")
set(CURRENT_TARGET_NAME "clipboard-tool")

find_package(Qt5Core REQUIRED)
find_package(Qt5Gui REQUIRED)

CreateTarget(${CURRENT_TARGET} EXECUTABLE ${CURRENT_TARGET_NAME} C++ 17)

# Qt deprecated warnings
target_compile_definitions(${CURRENT_TARGET} PRIVATE -DQT_DEPRECATED_WARNINGS)
target_compile_definitions(${CURRENT_TARGET} PRIVATE -DQT_DISABLE_DEPRECATED_BEFORE=0x060000)

# disable Qt foreach macro
target_compile_definitions(${CURRENT_TARGET} PRIVATE -DQT_NO_FOREACH)

target_link_libraries(${CURRENT_TARGET}
PRIVATE
    Qt5::Core
    Qt5::Gui
)
