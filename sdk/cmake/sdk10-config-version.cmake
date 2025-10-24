include("${CMAKE_CURRENT_LIST_DIR}/sdk10-version.cmake")

if (PACKAGE_FIND_VERSION)
	string(REGEX MATCH "^10\\.[^.]+\\.[^.]+\\.([0-9]+)$" version_match "${PACKAGE_FIND_VERSION}")
	if (NOT version_match)
		return()
	endif()
	if (NOT "${CMAKE_MATCH_1}" EQUAL "${SDK10_VERSION}")
		return()
	endif()
endif()

set(PACKAGE_VERSION_COMPATIBLE TRUE)
