cmake_minimum_required(VERSION 3.20.0)

set(CONFIG_USE_BLE ON)
set(SDK10_INCLUDE_DIRECTORIES config)
set(SDK10_INCLUDE_FILES config/custom_config_eflash.h)

find_package(SDK10 REQUIRED)

project(ble_peripheral)

target_sources(app PRIVATE
	main.c
	platform_devices.c
	st_fw.c
)
