import re
from os import path
from typing import cast
from patchtree import Header, Context, ProcessJinja2
from argparse import ArgumentParser
from subprocess import run

PATCH_LICENSE = f"""
Copyright (C) 2025 Renesas Electronics Corporation and/or its affiliates.
All rights reserved. Confidential Information.

This software ("Software") is supplied by Renesas Electronics Corporation and/or its
affiliates ("Renesas"). Renesas grants you a personal, non-exclusive, non-transferable,
revocable, non-sub-licensable right and license to use the Software, solely if used in
or together with Renesas products. You may make copies of this Software, provided this
copyright notice and disclaimer ("Notice") is included in all such copies. Renesas
reserves the right to change or discontinue the Software at any time without notice.

THE SOFTWARE IS PROVIDED "AS IS". RENESAS DISCLAIMS ALL WARRANTIES OF ANY KIND,
WHETHER EXPRESS, IMPLIED, OR STATUTORY, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. TO THE
MAXIMUM EXTENT PERMITTED UNDER LAW, IN NO EVENT SHALL RENESAS BE LIABLE FOR ANY DIRECT,
INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE, EVEN IF RENESAS HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES. USE OF THIS SOFTWARE MAY BE SUBJECT TO TERMS AND CONDITIONS CONTAINED IN
AN ADDITIONAL AGREEMENT BETWEEN YOU AND RENESAS. IN CASE OF CONFLICT BETWEEN THE TERMS
OF THIS NOTICE AND ANY SUCH ADDITIONAL LICENSE AGREEMENT, THE TERMS OF THE AGREEMENT
SHALL TAKE PRECEDENCE. BY CONTINUING TO USE THIS SOFTWARE, YOU AGREE TO THE TERMS OF
THIS NOTICE.IF YOU DO NOT AGREE TO THESE TERMS, YOU ARE NOT PERMITTED TO USE THIS
SOFTWARE.
"""

class SDK10Header(Header):
	name = "SDK10 patchtree"
	license = PATCH_LICENSE

	def write_version_extra(self):
		version_cmd = ("git", "describe", "--tags", "--always", "--dirty",)
		version_proc = run(version_cmd, text=True, capture_output=True)
		version = version_proc.stdout.strip()

		self.context.output.write(f"sdk10-cs version {version}\n")

class SDK10ArgumentParser(ArgumentParser):
	def __init__(self, *args, **kwargs):
		super(SDK10ArgumentParser, self).__init__(*args, **kwargs)

		self.add_argument(
			'--sdk10-version',
			help="specify SDK10 version (i.e. 86, 104, 108)",
			type=int,
		)
		self.add_argument(
			'--sdk10-target',
			help="specify device target (i.e. DA1459X)",
			type=str,
		)

class SDK10ProcessJinja2(ProcessJinja2):
	def get_template_vars(self):
		context = cast(SDK10Context, self.context)
		return {
			"SDK_VERSION": context.sdk_version,
			"SDK_TARGET": context.sdk_target,
		}

class SDK10Context(Context):
	"""
	Generic "context" struct that Diff and the main() function depend on for
	application context.
	"""

	sdk_version: int | None = None
	sdk_target: str | None = None

	SDKROOT_SET = set(('doc', 'sdk', 'projects', 'utilities',))

	def __init__(self, options):
		super(SDK10Context, self).__init__(options)

		found = self.find_root()
		if not found:
			raise Exception(f"not an SDK10 folder or archive")

		version_str = self.get_content("doc/VERSION.txt")
		if version_str is not None:
			git_tag, self.sdk_target = version_str.split()
			git_tag = git_tag.replace("sdk10_", "")
			git_tag = git_tag.replace("bismuth_", "")
			git_tag = re.sub(r'^10\.\d+\.\d+.', "", git_tag)
			match = re.search(r'\d+', git_tag)
			assert match is not None
			self.sdk_version = int(match.group())

		if options.sdk10_target is not None:
			context.sdk_target = options.sdk10_target.upper()
		if options.sdk10_version is not None:
			context.sdk_version = options.sdk10_version

		if self.sdk_version is None:
			raise ValueError("no SDK version specified or detected")

	def find_root(self, root: str = "", maxdepth: int = 3) -> bool:
		if maxdepth < 0:
			return False
		here = self.fs.joinpath(root)
		ls = list(here.iterdir())
		ls = [path for path in ls if path != here]

		names = set(path.name for path in ls)
		if names.issuperset(self.SDKROOT_SET):
			self.fs = here
			return True

		for entry in ls:
			if not entry.is_dir():
				continue
			found = self.find_root(path.join(root, entry.name), maxdepth - 1)
			if found:
				return found
		return False

context = SDK10Context
argument_parser = SDK10ArgumentParser
processors = {
	"jinja": SDK10ProcessJinja2,
}
header = SDK10Header
