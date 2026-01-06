sdk10_include_directories(.)
sdk10_sources(
	SEGGER_RTT.c
	SEGGER_RTT_printf.c
	SEGGER_SYSVIEW.c
)

sdk10_sources_ifdef(DA1459X
	SEGGER_RTT_ASM_ARMv7M.S
)
