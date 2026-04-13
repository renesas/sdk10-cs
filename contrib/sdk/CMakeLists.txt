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
	-Os
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
foreach(dir IN LISTS SDK10_INCLUDE_DIRECTORIES)
	cmake_path(ABSOLUTE_PATH dir BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" NORMALIZE)
	sdk10_include_directories("${dir}")
endforeach()
sdk10_compile_definitions(dg_configBUILD_FOR_PROCESSOR=${BUILD_PROCESSOR})

foreach(dir IN LISTS SDK10_NVPARAM_CONFIG_DIR)
	cmake_path(ABSOLUTE_PATH dir BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" NORMALIZE)
	list(APPEND SDK10_NVPARAM_CONFIG_DIRS "${dir}")
endforeach()
list(APPEND SDK10_NVPARAM_CONFIG_DIRS
	"${CMAKE_CURRENT_LIST_DIR}/middleware/adapters/include"
)

# project
project(SDK10 VERSION 10.1.6.108 LANGUAGES C ASM)

# file extensions
list(APPEND CMAKE_ASM_SOURCE_FILE_EXTENSIONS "S")
set(CMAKE_EXECUTABLE_SUFFIX .elf)

# executables
add_library(app)
add_library(SDK10)
add_executable("${KERNEL_NAME}" cmake/empty.c)

# print size after building
add_custom_command(
	TARGET "${KERNEL_NAME}"
	POST_BUILD
	COMMAND "${CMAKE_SIZE}" "${KERNEL_NAME}${CMAKE_EXECUTABLE_SUFFIX}"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
	USES_TERMINAL
	VERBATIM
)

# regular .bin file
add_custom_command(
	OUTPUT "${KERNEL_BIN_NAME}"
	COMMAND "${CMAKE_OBJCOPY}" -O binary "${KERNEL_ELF_NAME}" "${KERNEL_BIN_NAME}"
	DEPENDS "${KERNEL_NAME}"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
	VERBATIM
)

# .raw.bin file
add_custom_command(
	OUTPUT "${KERNEL_RAW_NAME}"
	COMMAND "${CMAKE_OBJCOPY}" -O binary --remove-section=.prod_head --remove-section=.prod_head_backup --remove-section=.img_head "${KERNEL_ELF_NAME}" "${KERNEL_RAW_NAME}"
	DEPENDS "${KERNEL_NAME}"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
	VERBATIM
)

# create_nvparam
add_custom_target(nvparam DEPENDS
	"${NVPARAM_BIN_NAME}"
)

add_custom_command(
	OUTPUT "${NVPARAM_BIN_NAME}"
	COMMAND
		"${CMAKE_PYTHON3}" "${PYTHON_SCRIPTS_PATH}/qspi/create_nvparam.py" --quiet
		--arm_gcc_path "${TOOLCHAIN_HOME}/bin"
		"${CMAKE_CURRENT_BINARY_DIR}"
		${SDK10_NVPARAM_CONFIG_DIRS}
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
	VERBATIM
)

if (SDK10_IMAGE)
	list(APPEND mkimage_args
		--sw_version "${SDK10_SW_VERSION}"
	)
endif()
if (SDK10_SECURITY)
	list(APPEND mkimage_args
		--sec_cfg "${SDK10_SECURE_CONFIG}"
		--prod_keys "${SDK10_SECURE_KEYS}"
	)
endif()
add_custom_command(
	OUTPUT "${KERNEL_IMG_NAME}"
	COMMAND
		"${CMAKE_PYTHON3}" "${PYTHON_SCRIPTS_PATH}/suota/v11/mkimage.py" --quiet
		--prod_id "${PRODUCT_ID}"
		${mkimage_args}
		"${KERNEL_RAW_NAME}" "${KERNEL_IMG_NAME}"
	DEPENDS "${KERNEL_RAW_NAME}"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
	VERBATIM
)

add_custom_target(flash
	COMMAND ezFlashCLI image_flash "${FLASH_FILE}"
	DEPENDS "${FLASH_FILE}"
	VERBATIM
	USES_TERMINAL
)

# sdk sources
add_subdirectory(bsp)
add_subdirectory(free_rtos)
add_subdirectory(interfaces)
add_subdirectory(middleware)

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
		WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
		VERBATIM
	)
	add_custom_target("linker_script_${script}" DEPENDS "${script}.ld")
	add_dependencies(SDK10 "linker_script_${script}")
	sdk10_link_options("-T${CMAKE_CURRENT_BINARY_DIR}/${script}.ld")
endforeach()

# preprocessor reflection
add_custom_command(
	OUTPUT reflect.txt
	COMMAND
		"${CMAKE_C_COMPILER}"
		-E -P
		${compiler_flags}
		"${CMAKE_CURRENT_LIST_DIR}/cmake/reflect.txt.h"
		-o reflect.txt
	DEPENDS "${CMAKE_CURRENT_LIST_DIR}/cmake/reflect.txt.h"
	WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
	VERBATIM
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

# "default" target for post-processing stuff by default
add_custom_target(default ALL DEPENDS
	"${KERNEL_BIN_NAME}"
	"${FLASH_FILE}"
)
