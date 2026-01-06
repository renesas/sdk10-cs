if(NOT DA1459X)
	return()
endif()

if(NOT CONFIG_USE_BLE)
	return()
endif()

sdk10_include_directories(include)
add_subdirectory(lib)
