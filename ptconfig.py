import re
from os import path
from pathlib import Path
from typing import cast
from patchtree import Header, Context, Jinja2Process
from argparse import ArgumentParser
from subprocess import run
from stat import S_ISDIR

from patchtree.target import TargetFileInputSpec

PATCH_LICENSE = f"""
Copyright (C) 2025 Renesas Electronics Corporation and/or its affiliates.
All rights reserved. Confidential Information.

This software ("Software") is supplied by Renesas Electronics Corporation and/or
its affiliates ("Renesas"). Renesas grants you a personal, non-exclusive,
non-transferable, revocable, non-sub-licensable right and license to use the
Software, solely if used in or together with Renesas products. You may make
copies of this Software, provided this copyright notice and disclaimer ("Notice")
is included in all such copies. Renesas reserves the right to change or
discontinue the Software at any time without notice.

THE SOFTWARE IS PROVIDED "AS IS". RENESAS DISCLAIMS ALL WARRANTIES OF ANY KIND,
WHETHER EXPRESS, IMPLIED, OR STATUTORY, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NON-INFRINGEMENT. TO THE MAXIMUM EXTENT PERMITTED UNDER LAW, IN NO EVENT SHALL
RENESAS BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL
DAMAGES ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE, EVEN IF RENESAS
HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. USE OF THIS SOFTWARE MAY BE
SUBJECT TO TERMS AND CONDITIONS CONTAINED IN AN ADDITIONAL AGREEMENT BETWEEN YOU
AND RENESAS. IN CASE OF CONFLICT BETWEEN THE TERMS OF THIS NOTICE AND ANY SUCH
ADDITIONAL LICENSE AGREEMENT, THE TERMS OF THE AGREEMENT SHALL TAKE PRECEDENCE.
BY CONTINUING TO USE THIS SOFTWARE, YOU AGREE TO THE TERMS OF THIS NOTICE.IF YOU
DO NOT AGREE TO THESE TERMS, YOU ARE NOT PERMITTED TO USE THIS SOFTWARE.
"""

class SDK10Header(Header):
	name = "SDK10 patchtree"
	license = PATCH_LICENSE

	def write_version_extra(self):
		version_cmd = ("git", "describe", "--tags", "--always", "--dirty",)
		version_proc = run(version_cmd, text=True, capture_output=True)
		version = version_proc.stdout.strip()

		context = cast(SDK10Context, self.context)
		return f"sdk10-cs version {version} for SDK10 version {context.sdk_version}\n"

class SDK10ArgumentParser(ArgumentParser):
	def __init__(self, *args, **kwargs):
		super(SDK10ArgumentParser, self).__init__(*args, **kwargs)

		extras = self.add_argument_group('SDK10 options')
		extras.add_argument(
			'--sdk-version',
			metavar="VERSION",
			help="specify SDK version (i.e. 86, 104, 108)",
			type=int,
		)
		extras.add_argument(
			'--sdk-target',
			metavar="TARGET",
			help="specify device target (i.e. DA1459X)",
			type=str,
		)

class SDK10Jinja2Process(Jinja2Process):
	def get_template_vars(self):
		context = cast(SDK10Context, self.target.context)
		vars = {
			"VERSION": context.sdk_version,
			"TARGET": context.sdk_target,
		}

		TARGETS = ("DA1459X", "DA1469X", "DA1470X",)
		if context.sdk_target is not None:
			target = context.sdk_target.upper()
			if target in TARGETS:
				vars[target] = True
		return vars

class SDK10Context(Context):
	"""
	Generic "context" struct that Diff and the main() function depend on for
	application context.
	"""

	sdk_version: int | None = None
	sdk_target: str | None = None

	SDKROOT_SET = set(('doc', 'sdk', 'projects', 'utilities',))

	def __init__(self, config, options):
		super(SDK10Context, self).__init__(config, options)

		found = self.find_root()
		if not found:
			raise Exception(f"not an SDK10 folder or archive")

		version = self.get_file(TargetFileInputSpec(path=Path("doc/VERSION.txt")))
		version_str = version.get_str()
		if version_str is not None:
			git_tag, self.sdk_target = version_str.split()
			git_tag = git_tag.replace("sdk10_", "")
			git_tag = git_tag.replace("bismuth_", "")
			git_tag = re.sub(r'^10\.\d+\.\d+.', "", git_tag)
			match = re.search(r'\d+', git_tag)
			assert match is not None
			self.sdk_version = int(match.group())

		if options.sdk_target is not None:
			context.sdk_target = options.sdk_target
		if options.sdk_version is not None:
			context.sdk_version = options.sdk_version

		if self.sdk_version is None:
			raise ValueError("no SDK version specified or detected")

	def find_root(self, root: Path = Path(), maxdepth: int = 3) -> bool:
		if maxdepth < 0:
			return False

		names = set(path.name for path in self.target_fs.get_dir(root))

		if names.issuperset(self.SDKROOT_SET):
			self.target_fs.root = root
			return True

		for name in names:
			mode = self.get_file(TargetFileInputSpec(path=Path(root.joinpath(name)))).mode
			if not S_ISDIR(mode):
				continue
			found = self.find_root(root.joinpath(name), maxdepth - 1)
			if found:
				return found
		return False

context = SDK10Context
argument_parser = SDK10ArgumentParser
processors = {
	"jinja": SDK10Jinja2Process,
}
header = SDK10Header
diff_context = 0
output_shebang = True
default_root = "contrib"
