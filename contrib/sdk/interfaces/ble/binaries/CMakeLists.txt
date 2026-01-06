--- !patchspec
processors:
  - id: jinja
...
if(NOT CONFIG_USE_BLE)
	return()
endif()

{% if VERSION < 99 %}
add_subdirectory(DA1459x-Release)
{% else %}
add_subdirectory(DA14592-Release)
add_subdirectory(DA14594-Release)
{% endif %}

add_subdirectory(DA1469x-Release)
