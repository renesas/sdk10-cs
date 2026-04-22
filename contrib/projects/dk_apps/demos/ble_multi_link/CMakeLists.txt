--- !patchspec
processors:
  - id: jinja
...
cmake_minimum_required(VERSION 3.20.0)

set(CONFIG_USE_BLE ON)
{{ find_config_headers() }}

find_package(SDK10 REQUIRED HINTS "$ENV{SDK10_ROOT}")

project(ble_multi_link)

target_sources(app PRIVATE
	ble_multi_link_task.c
	dlg_mls.c
	main.c
)
