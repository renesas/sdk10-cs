--- !patchspec
processors:
  - id: jinja
...
cmake_minimum_required(VERSION 3.20.0)

set(CONFIG_USE_BLE ON)
set(SDK10_INCLUDE_DIRECTORIES config)
{{ find_config_headers() }}

find_package(SDK10 REQUIRED HINTS "$ENV{SDK10_ROOT}")

project(ble_peripheral)

target_sources(app PRIVATE
	main.c
	platform_devices.c
	st_fw.c
)
