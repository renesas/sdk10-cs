.. |>=| unicode:: U+2265
   :rtrim:

.. |<=| unicode:: U+2264
   :rtrim:

######################
Known Limitations List
######################

More comprehensive lists of limitations (including those not related to the SDK10 source) can be found below:

* `DA1459X <https://lpccs-docs.renesas.com/da1459x_kll/index.html>`_ (SDK10.1)
* `DA1469X <https://lpccs-docs.renesas.com/da1469x_kll/index.html>`_ (SDK10.0)

The following known limitations are resolved by the patchset in this repository:

.. contents::
   :depth: 1
   :local:

*****************
SDK10CS-CRYPTO-CB
*****************

:Version:
  DA1459X |>=| 106
:Symptoms:
  The device crashes with a bus fault after calling ``ad_crypto_perform_operation``.
  Printing a backtrace with a debugger reveals an infinite recursive loop of ``aes_hash_irq_cb`` similar to::

    #0  0x00006e84 in BusFault_Handler ()
    #1  <signal handler called>
    #2  0x00000038 in __isr_vector ()
    #3  0x00005e4e in aes_hash_irq_cb ()
    #4  0x00005e4e in aes_hash_irq_cb ()
    #5  0x00005e4e in aes_hash_irq_cb ()

:Root cause:
  A subtle bug was introduced where the crypto engine user callback pointer is overwritten multiple times, resulting in it becoming equal to the internal callback handler.
  This causes an infinite recursive loop when the AES operation finishes, crashing the system.
:Resolution:
  The ``ad_crypto_configure`` method now only updates the callback pointer if the user has configured it.

*****************
SDK10CS-UTIL-MODE
*****************

:Versions: \-
:Symptoms: ::

  . ERROR:
  . /path/to/sdk/binaries/mkimage is not application file.
  . Please build mkimage and try again.

:Root cause:
  Some releases of SDK10 were packaged on Windows, while others were packaged on UNIX(-like) systems.
  The .zip files packaged on Windows do not preserve the executable permissions of the binaries.
:Resolution:
  The modes of the binaries bundled with the SDK are set to 755 (executable) for \*NIX filesystems.

*****************
SDK10CS-PY-SYNTAX
*****************

:Versions: \-
:Symptoms: ::

  /path/to/sdk/utilities/python_scripts/api/jlink.py: SyntaxWarning: invalid escape sequence

:Root cause:
  String literals containing Windows-style paths incorrectly omit the raw string prefix in the released Python scripts.
:Resolution:
  The syntax is corrected and no longer causes SyntaxWarnings.
