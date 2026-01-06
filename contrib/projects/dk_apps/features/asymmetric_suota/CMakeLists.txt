cmake_minimum_required(VERSION 3.20.0)

set(CONFIG_USE_BLE ON)
set(SDK10_INCLUDE_DIRECTORIES config)
set(SDK10_INCLUDE_FILES config/custom_config_eflash_suota.h)

find_package(SDK10 REQUIRED HINTS "$ENV{SDK10_ROOT}")

project(asymmetric_suota)

target_include_directories(app PRIVATE config)
target_sources(app PRIVATE main.c)
