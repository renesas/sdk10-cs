sdk10_include_directories(
	.
	include
)

sdk10_sources(
	sys_adc.c
	sys_audio_mgr.c
	sys_boot.c
	sys_bsr.c
	sys_drbg.c
	sys_rcx_calibrate.c
	sys_tcs.c
	sys_timer.c
	sys_trng_v2.c
	sys_watchdog.c
)

sdk10_sources_ifdef(DA1459X
	sys_adc_da1459x.c
	sys_clock_mgr_da1459x.c
	sys_power_mgr_da1459x.c
	sys_tcs_da1459x.c
)

