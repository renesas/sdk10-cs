--- !patchspec
processors:
  - id: jinja
...
sdk10_include_directories(config)

add_subdirectory(adapters)
{% if DA1459X and VERSION > 86 %}
add_subdirectory(asymmetric_suota)
{% endif %}
add_subdirectory(cli)
add_subdirectory(console)
add_subdirectory(dgtl)
add_subdirectory(haptics)
add_subdirectory(hw_tools)
add_subdirectory(intrinsic)
add_subdirectory(osal)
add_subdirectory(segger_tools)
