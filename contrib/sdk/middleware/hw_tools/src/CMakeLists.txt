sdk10_sources(
	PULSE.S
	Xtal_TRIM.c
)

sdk10_sources_ifdef(DA1459X
	xtal32m_block_calib.c
)
