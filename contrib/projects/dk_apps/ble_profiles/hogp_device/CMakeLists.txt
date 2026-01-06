cmake_minimum_required(VERSION 3.20.0)

set(CONFIG_USE_BLE ON)
set(SDK10_INCLUDE_FILES config/custom_config_eflash.h)

find_package(SDK10 REQUIRED HINTS "$ENV{SDK10_ROOT}")

project(hogp_device)

target_include_directories(app PRIVATE config)
target_sources(app PRIVATE
	hogp_device_task.c
	main.c
	platform_devices.c
)
