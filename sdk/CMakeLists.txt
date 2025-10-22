cmake_minimum_required(VERSION 3.20.0)

# variables
include(cmake/sdk10-module.cmake)

# compile options
sdk10_compile_options_ifdef(LLVM
	-Wno-unknown-attributes
	-fgnuc-version=8.0.0
)
sdk10_compile_options(
	-mcpu=cortex-m33
	-mthumb
	-mfloat-abi=hard
	-mfpu=fpv5-sp-d16
	-Og
	-fmessage-length=0
	-fsigned-char
	-ffunction-sections
	-fdata-sections
)
sdk10_link_options(
	-Xlinker --gc-sections
	"-Wl,-Map,${CMAKE_CURRENT_BINARY_DIR}/${KERNEL_MAP_NAME}"
)
sdk10_link_options_ifdef(GCC
	--specs=nano.specs
	--specs=nosys.specs
)
sdk10_include_files("${SDK10_INCLUDE_FILES}")
sdk10_compile_definitions(dg_configBUILD_FOR_PROCESSOR=${BUILD_PROCESSOR})

# project
project(SDK10 VERSION 10.1.6.108 LANGUAGES C ASM)

# file extensions
list(APPEND CMAKE_ASM_SOURCE_FILE_EXTENSIONS "S")
set(CMAKE_EXECUTABLE_SUFFIX .elf)

# executables
add_library(app)
add_library(SDK10)
add_executable("${KERNEL_NAME}" cmake/empty.c)

# flash command
add_custom_target(
	flash
	COMMAND ezFlashCLI image_flash "${KERNEL_BIN_NAME}"
	DEPENDS "${KERNEL_BIN_NAME}"
	USES_TERMINAL
)

# .elf -> .bin
add_custom_command(
	OUTPUT "${KERNEL_BIN_NAME}"
	COMMAND "${CMAKE_OBJCOPY}" -O binary "${KERNEL_ELF_NAME}" "${KERNEL_BIN_NAME}"
	DEPENDS "${KERNEL_NAME}"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
	VERBATIM
)

# print size after building
add_custom_command(
	TARGET "${KERNEL_NAME}"
	POST_BUILD
	COMMAND "${CMAKE_SIZE}" "${KERNEL_NAME}${CMAKE_EXECUTABLE_SUFFIX}"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
	USES_TERMINAL
	VERBATIM
)

# sdk sources
add_subdirectory(bsp)
add_subdirectory(free_rtos)
add_subdirectory(interfaces)
add_subdirectory(middleware)

# iidirng
add_library(iidirng STATIC IMPORTED)
set_target_properties(iidirng PROPERTIES
	IMPORTED_LOCATION "${CMAKE_CURRENT_LIST_DIR}/middleware/intrinsic/lib/libiidirng.a"
)

# ble stack
add_library(ble_stack STATIC IMPORTED)
set_target_properties(ble_stack PROPERTIES
	IMPORTED_LOCATION "${CMAKE_CURRENT_LIST_DIR}/interfaces/ble/binaries/${DEVICE}-Release/libble_stack_${LIBBLE_STACK_VER}.a"
)

# linker scripts
set(LDSCRIPT_PATH "${CMAKE_CURRENT_LIST_DIR}/bsp/ldscripts/${PROJECT_TYPE}_projects")
sdk10_get_compiler_flags(compiler_flags)
foreach(script IN ITEMS mem sections)
	add_custom_command(
		OUTPUT "${script}.ld"
		COMMAND
			"${CMAKE_C_COMPILER}"
				-E -P
				${compiler_flags}
				"${LDSCRIPT_PATH}/${script}.ld.h"
				-o "${script}.ld"
		DEPENDS "${LDSCRIPT_PATH}/${script}.ld.h"
		WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
		VERBATIM
	)
	add_custom_target("linker_script_${script}" DEPENDS "${script}.ld")
	add_dependencies(SDK10 "linker_script_${script}")
	sdk10_link_options("-T${script}.ld")
endforeach()

sdk10_link_libraries_ifdef(CONFIG_USE_BLE
	iidirng
	ble_stack
)
target_link_libraries(app PUBLIC SDK10)
target_link_libraries("${KERNEL_NAME}" PUBLIC app)

sdk10_get_compile_options(compile_options)
target_compile_options(SDK10 PRIVATE "${compile_options}")
target_compile_options(app PRIVATE "${compile_options}")
target_compile_options("${KERNEL_NAME}" PRIVATE "${compile_options}")

sdk10_get_compile_definitions(compile_definitions)
target_compile_definitions(SDK10 PRIVATE "${compile_definitions}")
target_compile_definitions(app PRIVATE "${compile_definitions}")
target_compile_definitions("${KERNEL_NAME}" PRIVATE "${compile_definitions}")

sdk10_get_include_directories(include_directories)
target_include_directories(SDK10 PRIVATE "${include_directories}")
target_include_directories(app PRIVATE "${include_directories}")
target_include_directories("${KERNEL_NAME}" PRIVATE "${include_directories}")

sdk10_get_link_options(link_options)
target_link_options("${KERNEL_NAME}" PRIVATE "${link_options}" "${compile_options}")

