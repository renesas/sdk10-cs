.. _toolchain: https://developer.arm.com/downloads/-/gnu-rm/7-2018-q2-update
.. _ezflashcli: https://github.com/ezflash/ezFlashCLI#installation
.. _cmake: https://cmake.org/download

.. |E2S| replace:: e\ :sup:`2` studio

###################
SDK10 CMake package
###################

This repository contains source files and patches to make SDK10 an installable CMake package.
It allows you use CMake together with ezFlashCLI for building and flashing code instead of SmartSnippets studio or |E2S|.

*************
Prerequisites
*************

Make sure you have `patched the SDK <../readme.md#installation>`_ and have working installations of--

* `CMake <cmake_>`_
* `ezFlashCLI <ezflashcli_>`_
* GNU ARM toolchain (`7-2018-q2-update <toolchain_>`_ recommended).

************
Installation
************

The CMake package can be installed by running

::

  $ cmake -P /dir/to/sdk10/sdk/cmake/sdk10-export.cmake

After installing, SDK10 CMake projects should build like any other CMake project.

.. note::

   At this point, any IDE with CMake support can be used to build SDK10 projects, including Visual Studio Code with the CMake extension.
   Make sure to set the toolchain detection to unspecified so the SDK10 toolchain detection script is used instead of CMake's built-in mechanism.

*****
Usage
*****

.. _59x_examples: https://github.com/renesas/ble-sdk10-da1459x-examples

After following the installation instructions, all projects in the SDK10 folder can be built as standard CMake projects.
The `DA1459X examples repository <59x_examples_>`_ contains additional examples and empty template projects that can be used as starting points for developing new applications.

In order to flash the target, build the ``flash`` utility target.
This target automatically builds the raw binary and calls ezFlashCLI to flash the target device.

Because projects may not require specific devices or toolchain versions, these *should* be left out of the project's CMakeLists.txt when possible.
In order to allow these options to be configured on a per-user basis, environment variables are used.
See `options`_ for more details on which options are supported and/or required by the SDK10 CMake package.

.. _options:

*******
Options
*******

Most regular CMake options still apply (e.g. ``CMAKE_BUILD_TYPE``, ``CMAKE_EXPORT_COMPILE_COMMANDS``, etc.).
SDK10 specific variables can be set in the project CMakeLists.txt *before* importing the SDK10 CMake package, and are listed below.

``DEVICE`` (string)
  Device identifier (e.g. ``DA14592``, ``DA14594``).
  Required to be defined.
  The value of ``DEVICE`` is sourced from:

  * the project's CMakeLists.txt if ``DEVICE`` is explicitly set
  * the ``SDK10_DEVICE`` environment variable if it is set

``TOOLCHAIN_HOME`` (path)
  Path to toolchain home (e.g. ``C:/Program Files (x86)/GNU Tools Arm Embedded/7 2018-q2-update``, ``/opt/toolchains/gcc_arm/7_2018q2/gcc-arm-none-eabi-7-2018-q2-update``).
  An ARM toolchain is *required*, but setting ``TOOLCHAIN_HOME`` is only required if the arm-none-eabi toolchain is not available in ``$PATH``.

``SDK10_INCLUDE_FILES`` (path list)
  List of files included for all SDK sources (i.e. through the ``-include`` compiler flag).
  Optional, but likely required to build most projects (i.e. ``custom_config_eflash.h``).

``SDK10_INCLUDE_DIRECTORIES`` (path list)
  List of directories to add to the SDK10 sources' include path.
  Optional, but required for some projects (i.e. ``app_nvparam.h``).

``CONFIG_USE_BLE`` (boolean)
  Enable BLE support (must mirror C macro equivalent).
  Off by default.
