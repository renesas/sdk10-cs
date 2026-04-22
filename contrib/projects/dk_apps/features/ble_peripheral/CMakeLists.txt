--- !patchspec
processors:
  - id: jinja
...
cmake_minimum_required(VERSION 3.20.0)

set(CONFIG_USE_BLE ON)
{{ find_config_headers() }}

find_package(SDK10 REQUIRED HINTS "$ENV{SDK10_ROOT}")

project(ble_peripheral)

target_include_directories(app PRIVATE config)
target_sources(app PRIVATE
	ble_peripheral_task.c
	main.c
)
