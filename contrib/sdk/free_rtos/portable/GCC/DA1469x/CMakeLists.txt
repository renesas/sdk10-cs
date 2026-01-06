if(NOT DA1469X)
	return()
endif()

sdk10_include_directories(.)

sdk10_sources(
	port.c
)
