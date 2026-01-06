sdk10_sources(
	sdk_crc16.c
	sdk_list.c
	sdk_queue.c
)

sdk10_sources_ifdef(DA1459X
	chacha20.c
)
