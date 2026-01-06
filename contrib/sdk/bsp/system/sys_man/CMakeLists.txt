sdk10_include_directories(
	.
	include
)

sdk10_sources(
	sys_adc.c
	sys_audio_mgr.c
	sys_bsr.c
	sys_timer.c
	sys_watchdog.c
)

sdk10_sources_ifdef(DA1469X
	sys_charger_da1469x.c
	sys_clock_mgr_da1469x.c
	sys_power_mgr_da1469x.c
	sys_rc_clocks_calibration.c
	sys_tcs_da1469x.c
	sys_trng.c
	sys_usb_da1469x.c
)

sdk10_sources_ifdef(DA1459X
	sys_adc_da1459x.c
	sys_boot.c
	sys_clock_mgr_da1459x.c
	sys_drbg.c
	sys_power_mgr_da1459x.c
	sys_rcx_calibrate.c
	sys_tcs.c
	sys_tcs_da1459x.c
	sys_trng_v2.c
)
