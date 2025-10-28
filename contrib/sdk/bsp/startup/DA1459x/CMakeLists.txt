if(NOT DA1459X)
	return()
endif()

sdk10_sources(
	init_da1459x.c
	system_da1459x.c
)

add_subdirectory(GCC)
