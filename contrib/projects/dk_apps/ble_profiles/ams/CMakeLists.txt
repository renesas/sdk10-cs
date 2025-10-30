cmake_minimum_required(VERSION 3.20.0)

set(CONFIG_USE_BLE ON)
set(SDK10_INCLUDE_FILES config/custom_config_eflash.h)

find_package(SDK10 REQUIRED)

project(ams)

target_include_directories(app PRIVATE config)
target_sources(app PRIVATE
	ams_client.c
	ams_task.c
	display.c
	main.c
)
