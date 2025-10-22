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
set(KERNEL_NAME "sdk10")
set(KERNEL_ELF_NAME "${KERNEL_NAME}.elf")
set(KERNEL_BIN_NAME "${KERNEL_NAME}.bin")
set(KERNEL_MAP_NAME "${KERNEL_NAME}.map")

