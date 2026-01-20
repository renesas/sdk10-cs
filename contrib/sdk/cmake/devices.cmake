include_guard(GLOBAL)

if(NOT DEVICE)
	message(FATAL_ERROR "No DEVICE configured!")
endif()
set("${DEVICE}" TRUE)

macro(sdk10_device_version_mismatch)
	message(FATAL_ERROR "`${DEVICE}' is not supported by SDK10 version ${SDK10_VERSION} (${SDK10_TARGET})")
endmacro()

if("${DEVICE}" MATCHES "^DA1459[24]$")
	if(NOT SDK10_TARGET STREQUAL "DA1459x")
		sdk10_device_version_mismatch()
	endif()

	sdk10_compile_definitions(dg_configDEVICE=${DEVICE}_00)
	set(DA1459X TRUE)

	set(PRODUCT_ID "DA1459x-00")

	return()
endif()

if("${DEVICE}" MATCHES "^DA1469[1579]$")
	if(NOT SDK10_TARGET STREQUAL "DA1469x")
		sdk10_device_version_mismatch()
	endif()

	sdk10_compile_definitions(dg_configDEVICE=DA14699_00)
	set(DA1469X TRUE)

	# default devkit flash name
	sdk10_def_option(DEVICE_FLASH_NAME "MX25U3235F")
	set(PRODUCT_ID "DA1469x-00")

	return()
endif()

message(FATAL_ERROR "DEVICE `${DEVICE}' is not supported!")
