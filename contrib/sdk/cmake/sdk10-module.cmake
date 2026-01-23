include_guard(GLOBAL)

include(sdk10-version)

# default options
macro(sdk10_def_option name default_value)
	if (NOT DEFINED ${name})
		set(${name} ${default_value})
	endif()
endmacro()

sdk10_def_option(DEVICE "$ENV{SDK10_DEVICE}")
sdk10_def_option(TOOLCHAIN_HOME "$ENV{SDK10_TOOLCHAIN_HOME}")
sdk10_def_option(CONFIG_USE_BLE NO)

sdk10_def_option(SDK10_SECURE_KEYS product_keys.xml)
sdk10_def_option(SDK10_SECURE_CONFIG secure_cfg.xml)
sdk10_def_option(SDK10_SECURE_VERSION sw_version.h)
cmake_path(ABSOLUTE_PATH SDK10_SECURE_KEYS BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" NORMALIZE)
cmake_path(ABSOLUTE_PATH SDK10_SECURE_CONFIG BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" NORMALIZE)
cmake_path(ABSOLUTE_PATH SDK10_SECURE_VERSION BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" NORMALIZE)

set(sdk10_security_default OFF)
function(sdk10_default_security_setup)
	if (DEFINED SDK10_SECURITY)
		return()
	endif()
	if (NOT EXISTS "${SDK10_SECURE_KEYS}")
		return()
	endif()
	if (NOT EXISTS "${SDK10_SECURE_CONFIG}")
		return()
	endif()
	if (NOT EXISTS "${SDK10_SECURE_VERSION}")
		return()
	endif()
	set(sdk10_security_default ON PARENT_SCOPE)
endfunction()
sdk10_default_security_setup()
sdk10_def_option(SDK10_SECURITY "${sdk10_security_default}")

set(PYTHON_SCRIPTS_PATH "${CMAKE_CURRENT_LIST_DIR}/../../utilities/python_scripts")
cmake_path(ABSOLUTE_PATH PYTHON_SCRIPTS_PATH NORMALIZE)

# modules
include(interface)
include(toolchain)
include(devices)

# other build variables
set(CMAKE_C_STANDARD 11)
set(BUILD_PROCESSOR BUILD_FOR_MAIN_PROCESSOR)
if (CONFIG_USE_BLE)
	set(PROJECT_TYPE ble)
else()
	set(PROJECT_TYPE non_ble)
endif()

# binary names
set(KERNEL_NAME "sdk10")
set(KERNEL_ELF_NAME "${KERNEL_NAME}.elf")
set(KERNEL_BIN_NAME "${KERNEL_NAME}.bin")
set(KERNEL_RAW_NAME "${KERNEL_NAME}.raw.bin")
set(KERNEL_IMG_NAME "${KERNEL_NAME}.img")
set(KERNEL_MAP_NAME "${KERNEL_NAME}.map")

if (SDK10_SECURITY)
	set(FLASH_FILE "${KERNEL_IMG_NAME}")
else()
	set(FLASH_FILE "${KERNEL_BIN_NAME}")
endif()


# create_nvparam.py
set(NVPARAM_SYMBOLS_NAME "nvparam-symbols.o")
set(NVPARAM_ELF_NAME "nvparam.elf")
set(NVPARAM_BIN_NAME "nvparam.bin")
