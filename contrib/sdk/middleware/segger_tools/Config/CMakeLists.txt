sdk10_include_directories(.)

sdk10_sources_ifdef(DA1469X
	SEGGER_SYSVIEW_Config_FreeRTOS.c
	SEGGER_SYSVIEW_Config_FreeRTOS_da1469x.c
)

sdk10_sources_ifdef(DA1459X
	SEGGER_SYSVIEW_Config_FreeRTOS_da1459x.c
)
