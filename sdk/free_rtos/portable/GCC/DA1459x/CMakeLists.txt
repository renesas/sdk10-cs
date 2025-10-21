if(NOT DA1459X)
	return()
endif()

sdk10_include_directories(.)

sdk10_sources(
	port.c
	portasm.c
)

