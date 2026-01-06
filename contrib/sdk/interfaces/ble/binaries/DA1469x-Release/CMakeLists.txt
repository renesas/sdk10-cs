if(NOT DA1469X)
	return()
endif()

sdk10_link_libraries("${CMAKE_CURRENT_LIST_DIR}/libble_stack_da1469x.a")
