include_guard(GLOBAL)

add_library(sdk10_interface INTERFACE)

function(sdk10_compile_options)
	target_compile_options(sdk10_interface INTERFACE ${ARGV})
endfunction()

function(sdk10_link_options)
	target_link_options(sdk10_interface INTERFACE ${ARGV})
endfunction()

function(sdk10_include_directories)
  target_include_directories(sdk10_interface INTERFACE ${ARGV})
endfunction()

function(sdk10_compile_definitions)
  target_compile_definitions(sdk10_interface INTERFACE ${ARGV})
endfunction()

function(sdk10_sources)
	target_sources(SDK10 PRIVATE ${ARGV})
endfunction()

function(sdk10_link_libraries)
  target_link_libraries(SDK10 PUBLIC ${ARGV})
endfunction()

function(sdk10_compile_options_ifdef var)
	if(${var})
		sdk10_compile_options(${ARGN})
	endif()
endfunction()

function(sdk10_link_options_ifdef var)
	if(${var})
		sdk10_link_options(${ARGN})
	endif()
endfunction()

function(sdk10_include_directories_ifdef var)
	if(${var})
		sdk10_include_directories(${ARGN})
	endif()
endfunction()

function(sdk10_compile_definitions_ifdef var)
	if(${var})
		sdk10_compile_definitions(${ARGN})
	endif()
endfunction()

function(sdk10_sources_ifdef var)
	if(${var})
		sdk10_sources(${ARGN})
	endif()
endfunction()

function(sdk10_link_libraries_ifdef var)
	if(${var})
		sdk10_link_libraries(${ARGN})
	endif()
endfunction()

function(sdk10_include_files)
  foreach(file IN LISTS ARGV)
    cmake_path(ABSOLUTE_PATH file BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" NORMALIZE)
    sdk10_compile_options(-include "${file}")
  endforeach()
endfunction()

function(sdk10_get_compile_options output)
	get_target_property(compile_options sdk10_interface INTERFACE_COMPILE_OPTIONS)
	set(${output} ${compile_options} PARENT_SCOPE)
endfunction()

function(sdk10_get_compile_definitions output)
	get_target_property(compile_definitions sdk10_interface INTERFACE_COMPILE_DEFINITIONS)
	set(${output} ${compile_definitions} PARENT_SCOPE)
endfunction()

function(sdk10_get_include_directories output)
	get_target_property(include_directories sdk10_interface INTERFACE_INCLUDE_DIRECTORIES)
	set(${output} ${include_directories} PARENT_SCOPE)
endfunction()

function(sdk10_get_link_options output)
	get_target_property(link_options sdk10_interface INTERFACE_LINK_OPTIONS)
	set(${output} ${link_options} PARENT_SCOPE)
endfunction()

function(sdk10_get_compiler_flags output)
	sdk10_get_compile_options(compile_options)
	sdk10_get_compile_definitions(compile_definitions)
	sdk10_get_include_directories(include_directories)

	list(TRANSFORM compile_definitions PREPEND "-D")
	list(TRANSFORM include_directories PREPEND "-I")

	set(${output} ${compile_options} ${compile_definitions} ${include_directories} PARENT_SCOPE)
endfunction()

