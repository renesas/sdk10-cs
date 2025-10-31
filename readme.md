# SDK10 Community Support

This repository contains a [patchtree] patchset with bugfixes and additional features for SDK10.

[patchtree]: https://github.com/renesas/patchtree
[git]: https://git-scm.com/install

## Patch content

- [SDK10 CMake package](doc/cmake.rst)
- [Known limitations list workarounds](doc/kll.rst)

## Installation

1. Download the .patch file corresponding to your SDK10 version from the [releases](releases/).
2. Place the downloaded `.patch` file in the SDKROOT directory (the one that contains `binaries`, `config`, `doc`, `projects`, `sdk` and `utilities` subdirectories) under the name `.patchtree.diff`.
3. Open a terminal in the SDKROOT directory and run `git apply --unidiff-zero .patchtree.diff`.

## Roadmap

The following functionality is not yet implemented or tested

- DA1469X SDK10 support
- DA1470X SDK10 support

## License

Since this repository deliberately does not include *any* SDK10 source code, all of the code in this repository is licensed with the MIT-0 license.
This choice was made so modified copies of SDK10 can be used under the same terms as the original proprietary license it is released under.

> [!NOTE]
>
> The .patch files under the releases tab *are* licensed under the same license as the SDK10 sources themselves.

## Development

Patches for supported SDK10 versions are built using the makefile in this repository.
This patchset makes use of Coccinelle patches, so it must be installed in order to build successfully.

Contributions to this repository are actively welcomed.
Please see the [patchtree developer documentation][pt-dev] for more info on developing patchsets.

[pt-dev]: https://patchtree.readthedocs.io/en/latest/dev/index.html
