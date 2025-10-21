include_guard(GLOBAL)

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_CROSSCOMPILING 1)
set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

if (NOT DEFINED TARGET_TRIPLE)
	set(TARGET_TRIPLE arm-none-eabi)
endif()

# default compiler
function(sdk10_find_compiler)
	unset(compiler_path)
	find_program(compiler_path "${TARGET_TRIPLE}-gcc")
	if (compiler_path)
		get_filename_component(bin_path "${compiler_path}" DIRECTORY)
		get_filename_component(home "${bin_path}" DIRECTORY)

		set(COMPILER_ID "GNU" PARENT_SCOPE)
		set(TOOLCHAIN_HOME "${home}" PARENT_SCOPE)

		return()
	endif()

	unset(compiler_path)
	find_program(compiler_path clang)
	if (compiler_path)
		get_filename_component(bin_path "${compiler_path}" DIRECTORY)
		get_filename_component(home "${bin_path}" DIRECTORY)

		set(COMPILER_ID "Clang" PARENT_SCOPE)
		set(TOOLCHAIN_HOME "${home}" PARENT_SCOPE)

		return()
	endif()

	message(FATAL_ERROR
		"No toolchain explicitly configured and could not find supported toolchain"
	)
endfunction()

function(sdk10_detect_compiler_id)
	if (DEFINED COMPILER_ID)
		return()
	endif()

	unset(compiler)
	find_program(compiler "${TARGET_TRIPLE}-gcc" ${FIND_ARGS})
	if (compiler AND EXISTS "${TOOLCHAIN_HOME}/lib/gcc")
		set(COMPILER_ID "GNU" PARENT_SCOPE)
		return()
	endif()

	unset(compiler)
	find_program(compiler "clang" ${FIND_ARGS})
	if (compiler AND EXISTS "${TOOLCHAIN_HOME}/lib/clang")
		set(COMPILER_ID "Clang" PARENT_SCOPE)
		return()
	endif()

	message(FATAL_ERROR
		"COMPILER_ID could not be determined, is your TOOLCHAIN_HOME set correctly?"
	)
endfunction()

if (NOT DEFINED COMPILER_ID AND NOT DEFINED TOOLCHAIN_HOME)
	sdk10_find_compiler()
endif()
if (NOT TOOLCHAIN_BIN_PATH)
	set(TOOLCHAIN_BIN_PATH "${TOOLCHAIN_HOME}/bin")
endif()
set(FIND_ARGS "")
if (TOOLCHAIN_BIN_PATH)
	list(APPEND FIND_ARGS
		NO_DEFAULT_PATH
		NO_CMAKE_ENVIRONMENT_PATH
		NO_SYSTEM_ENVIRONMENT_PATH
		NO_CMAKE_FIND_ROOT_PATH
		PATHS "${TOOLCHAIN_BIN_PATH}"
	)
endif()

sdk10_detect_compiler_id()

# copmiler type variables
if (COMPILER_ID STREQUAL "GNU")
	set(GNU 1)
elseif(COMPILER_ID STREQUAL "Clang")
	set(LLVM 1)
else()
	message(FATAL_ERROR
		"Unsupported toolchain configured, please configure TOOLCHAIN_HOME or "
		"COMPILER_ID to a supported toolchain path or family"
	)
endif()

if (GNU)
	find_program(CMAKE_C_COMPILER   "${TARGET_TRIPLE}-gcc"     ${FIND_ARGS})
	find_program(CMAKE_CXX_COMPILER "${TARGET_TRIPLE}-g++"     ${FIND_ARGS})
	find_program(CMAKE_ASM_COMPILER "${TARGET_TRIPLE}-gcc"     ${FIND_ARGS})
	find_program(CMAKE_LINKER       "${TARGET_TRIPLE}-gcc"     ${FIND_ARGS})
	find_program(CMAKE_OBJCOPY      "${TARGET_TRIPLE}-objcopy" ${FIND_ARGS})
	find_program(CMAKE_OBJDUMP      "${TARGET_TRIPLE}-objdump" ${FIND_ARGS})
	find_program(CMAKE_AS           "${TARGET_TRIPLE}-as"      ${FIND_ARGS})
	find_program(CMAKE_AR           "${TARGET_TRIPLE}-ar"      ${FIND_ARGS})
	find_program(CMAKE_RANLIB       "${TARGET_TRIPLE}-ranlib"  ${FIND_ARGS})
	find_program(CMAKE_READELF      "${TARGET_TRIPLE}-readelf" ${FIND_ARGS})
	find_program(CMAKE_NM           "${TARGET_TRIPLE}-nm"      ${FIND_ARGS})
	find_program(CMAKE_STRIP        "${TARGET_TRIPLE}-strip"   ${FIND_ARGS})
	find_program(CMAKE_SIZE         "${TARGET_TRIPLE}-size"    ${FIND_ARGS})
elseif(LLVM)
	sdk10_compile_options(-target "${TARGET_TRIPLE}")
	find_program(CMAKE_C_COMPILER   "clang"        ${FIND_ARGS})
	find_program(CMAKE_CXX_COMPILER "clang++"      ${FIND_ARGS})
	find_program(CMAKE_ASM_COMPILER "clang"        ${FIND_ARGS})
	find_program(CMAKE_LINKER       "clang"        ${FIND_ARGS})
	find_program(CMAKE_OBJCOPY      "llvm-objcopy" ${FIND_ARGS})
	find_program(CMAKE_OBJDUMP      "llvm-objdump" ${FIND_ARGS})
	find_program(CMAKE_AS           "clang"        ${FIND_ARGS})
	find_program(CMAKE_AR           "llvm-ar"      ${FIND_ARGS})
	find_program(CMAKE_RANLIB       "llvm-ranlib"  ${FIND_ARGS})
	find_program(CMAKE_READELF      "llvm-readelf" ${FIND_ARGS})
	find_program(CMAKE_NM           "llvm-nm"      ${FIND_ARGS})
	find_program(CMAKE_STRIP        "llvm-strip"   ${FIND_ARGS})
	find_program(CMAKE_SIZE         "llvm-size"    ${FIND_ARGS})
endif()

