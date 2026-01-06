sdk10_sources_ifdef(DA1469X
	qspi_automode.c
	qspi_internal.h
	qspi_memory_config_table_internal.h
)

sdk10_sources_ifdef(DA1459X
	eflash_automode.c
	qspi_automode_v2.c
)
