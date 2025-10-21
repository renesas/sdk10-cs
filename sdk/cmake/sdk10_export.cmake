set(PACKAGE_NAME SDK10)

if(WIN32)
  execute_process(COMMAND
		${CMAKE_COMMAND} -E write_regv
		"HKEY_CURRENT_USER\\Software\\Kitware\\CMake\\Packages\\${PACKAGE_NAME}\;location"
		"${CMAKE_CURRENT_LIST_DIR}"
	)
else()
	file(WRITE "$ENV{HOME}/.cmake/packages/${PACKAGE_NAME}/location" "${CMAKE_CURRENT_LIST_DIR}")
endif()

