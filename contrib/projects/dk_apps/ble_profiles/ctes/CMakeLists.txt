cmake_minimum_required(VERSION 3.20.0)

# CTES is only supported by the 594
set(DEVICE DA14594)

set(CONFIG_USE_BLE ON)
set(SDK10_INCLUDE_FILES config/custom_config_eflash.h)

find_package(SDK10 REQUIRED HINTS "$ENV{SDK10_ROOT}")

project(ctes)

target_include_directories(app PRIVATE config)
target_sources(app PRIVATE
	ctes_task.c
	main.c
)
