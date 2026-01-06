if(NOT DA1459X)
	return()
endif()

sdk10_link_libraries("${CMAKE_CURRENT_LIST_DIR}/libble_stack_da1459x.a")
