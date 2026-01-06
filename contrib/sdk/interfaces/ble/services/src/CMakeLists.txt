--- !patchspec
processors:
  - id: jinja
...
sdk10_sources_ifdef(CONFIG_USE_BLE
	bas.c
	bcs.c
	ble_service.c
	bls.c
	bms.c
	{% if DA1459X and VERSION > 86 %}
	ctes.c
	{% endif %}
	cts.c
	dis.c
	dlg_debug.c
	dlg_suota.c
	hids.c
	hrs.c
	ias.c
	lls.c
	scps.c
	sps.c
	tps.c
	uds.c
	wss.c
)
