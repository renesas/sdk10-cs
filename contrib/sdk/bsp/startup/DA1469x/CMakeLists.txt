if(NOT DA1469X)
	return()
endif()

sdk10_sources(
	init_da1469x.c
	system_da1469x.c
)

add_subdirectory(GCC)
