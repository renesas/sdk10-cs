if(NOT DEVICE STREQUAL "DA14592")
	return()
endif()

sdk10_include_directories(include)
add_subdirectory(src)
