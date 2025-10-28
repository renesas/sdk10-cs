set(PACKAGE_NAME SDK10)

include("${CMAKE_CURRENT_LIST_DIR}/sdk10-version.cmake")

if(WIN32)
	execute_process(COMMAND
		${CMAKE_COMMAND} -E write_regv
		"HKEY_CURRENT_USER\\Software\\Kitware\\CMake\\Packages\\${PACKAGE_NAME}\;${PACKAGE_VERSION}"
		"${CMAKE_CURRENT_LIST_DIR}"
	)
else()
	file(WRITE "$ENV{HOME}/.cmake/packages/${PACKAGE_NAME}/${PACKAGE_VERSION}" "${CMAKE_CURRENT_LIST_DIR}")
endif()
