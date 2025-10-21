SDK10 CMake package
###################

This repository contains source files and patches to make SDK10 an installable
CMake package. It allows you use CMake and ezFlashCLI for building and flashing
code that would normally be built and flashed as part of an e² studio project.

.. contents::
   :depth: 1
   :local:

Installation
************

.. _toolchain: https://developer.arm.com/downloads/-/gnu-rm/7-2018-q2-update
.. _ezflashcli: https://github.com/ezflash/ezFlashCLI#installation
.. _cmake: https://cmake.org/download
.. _git: https://git-scm.com/install

Prerequisites:

* `Git <git_>`_
* `CMake <cmake_>`_
* `ezFlashCLI <ezflashcli_>`_
* GNU ARM toolchain (`7-2018-q2-update <toolchain_>`_ recommended)

The installation procedure consists of the following steps:

* Download the .patch file corresponding to your SDK10 version
* ``git apply`` the changes
* Install the CMake package by running ``cmake -P
  /dir/to/sdk10/sdk/cmake/sdk10_export.cmake``

Usage
*****

.. _59x_examples: https://github.com/renesas/ble-sdk10-da1459x-examples

After following the installation instructions, all projects in the SDK10 folder
can be built as standard CMake projects. The `DA1459X examples repository
<59x_examples_>`_ contains additional examples and empty template projects that
can be used as starting points for developing new applications.

Because projects may not require specific devices or toolchain versions, these
*should* be left out of the project's CMakeLists.txt when possible. In order to
allow these options to be configured on a per-user basis, environment variables
are used. See `options`_ for more details on which options are supported and/or
required by the SDK10 CMake package.

.. _options:

Options
*******

Most regular CMake options still apply (e.g. ``CMAKE_BUILD_TYPE``,
``CMAKE_EXPORT_COMPILE_COMMANDS``, etc.). SDK10 specific variables can be set in
the project CMakeLists.txt *before* importing the SDK10 CMake package, and are
listed below.

``DEVICE``
  Device identifier (e.g. ``DA14592``, ``DA14594``). Required to be defined.
  The value of ``DEVICE`` is sourced from:

  * the project's CMakeLists.txt if ``DEVICE`` is explicitly set
  * the ``SDK10_DEVICE`` environment variable if it is set

``TOOLCHAIN_HOME``
  Path to toolchain home (e.g. ``C:/Program Files (x86)/GNU Tools Arm
  Embedded/7 2018-q2-update``,
  ``/opt/renesas/toolchains/gcc_arm/7_2018q2/gcc-arm-none-eabi-7-2018-q2-update``)
  . An ARM toolchain is *required*, but setting
  ``TOOLCHAIN_HOME`` is only required if the arm-none-eabi toolchain is not
  available in ``$PATH``.

``SDK10_INCLUDE_FILES``
  List of file(s) included for ALL sources (including SDK10 sources). Optional,
  but likely required to build most projects (i.e. ``custom_config_eflash.h``).

``CONFIG_USE_BLE``
  Enable BLE support (boolean). Off by default (must mirror C macro equivalent).

License
*******

Since this repository deliberately does not include *any* SDK10 source code, all
of the code in this repository is licensed with the MIT-0 license. This choice
was made so modified copies of SDK10 can be used under the same terms as the
original proprietary license it is released under.

.. TODO: specify what license the released .diff files fall under (check if
   these can be released w/o including any SDK10 source code)

Development
***********

Under construction

