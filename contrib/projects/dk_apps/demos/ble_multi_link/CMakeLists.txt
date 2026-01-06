
cmake_minimum_required(VERSION 3.20.0)

set(CONFIG_USE_BLE ON)
set(SDK10_INCLUDE_FILES config/custom_config_eflash.h)

find_package(SDK10 REQUIRED HINTS "$ENV{SDK10_ROOT}")

project(ble_multi_link)

target_sources(app PRIVATE
	ble_multi_link_task.c
	dlg_mls.c
	main.c
)
