--- !patchspec
processors:
  - id: jinja
...
cmake_minimum_required(VERSION 3.20.0)

{{ find_config_headers() }}

find_package(SDK10 REQUIRED HINTS "$ENV{SDK10_ROOT}")

project(audio_demo)

target_include_directories(app PRIVATE includes)
add_subdirectory(src)
