cmake_minimum_required(VERSION 2.8.12)
project(MAVLink_binder)

include_directories(
${PROJECT_SOURCE_DIR}/include
${PROJECT_SOURCE_DIR}/generated
)

add_subdirectory(pybind11)
pybind11_add_module(MAVLink_binder src/mavlink_bindings.cpp)
