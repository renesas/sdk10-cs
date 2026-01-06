--- !patchspec
processors:
  - id: jinja
...
set(SDK10_VERSION {{ VERSION }})
set(SDK10_TARGET {{ TARGET }})

set(PACKAGE_VERSION 10.X.X.${SDK10_VERSION})
