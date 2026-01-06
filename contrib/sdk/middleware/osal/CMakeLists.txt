sdk10_include_directories(.)

sdk10_sources(
	msg_queues.c
	resmgmt.c
)

sdk10_sources_ifdef(DA1469X
	usb_osal_wrapper.c
)
