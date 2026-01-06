if(NOT SDK10_TARGET STREQUAL "DA1469x")
	return()
endif()

sdk10_include_directories(include)
add_subdirectory(src)
