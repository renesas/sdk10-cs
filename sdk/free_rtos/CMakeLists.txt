sdk10_include_directories(include)

sdk10_sources(
	croutine.c
	event_groups.c
	list.c
	queue.c
	stream_buffer.c
	tasks.c
	timers.c
)

add_subdirectory(portable)

