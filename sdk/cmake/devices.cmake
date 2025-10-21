include_guard(GLOBAL)

if (NOT DEVICE) 
	message(FATAL_ERROR "No DEVICE configured!")
endif()

if("${DEVICE}" MATCHES "^DA1459[24]$")
	sdk10_compile_definitions(dg_configDEVICE=${DEVICE}_00)
	set(DA1459X TRUE)

	if (DEVICE STREQUAL "DA14594")
		set(LIBBLE_STACK_VER da14594)
	elseif(DEVICE STREQUAL "DA14592")
		set(LIBBLE_STACK_VER da14592)
	endif()

	return()
endif()

message(FATAL_ERROR "DEVICE `${DEVICE}' is not supported!")

