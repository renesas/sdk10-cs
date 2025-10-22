#!/bin/python3

import re
from pathlib import Path as DiskPath
from typing import Union
from zipfile import is_zipfile, Path as ZipPath
from jinja2 import Environment
from difflib import unified_diff
from os import path
from subprocess import run, PIPE
from sys import argv, stdout, stderr
from shutil import which
from argparse import ArgumentParser
from typing import IO

PATCH_LICENSE = f"""\
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

JINJA_ENV = Environment(
	trim_blocks=True,
	lstrip_blocks=True,
)

class Context:
	"""
	Generic "context" struct that Diff and the main() function depend on for
	application context.
	"""

	fs: Union[DiskPath, ZipPath]

	sdk_version: int | None = None
	sdk_target: str | None = None

	patch_root: str
	output: IO

	SDKROOT_SET = set(('doc', 'sdk', 'projects', 'utilities',))

	def __init__(self, sdk: str):
		if not path.exists(sdk):
			raise Exception(f"cannot open `{sdk}'")

		if path.isdir(sdk):
			self.fs = DiskPath(sdk)
		elif is_zipfile(sdk):
			self.fs = ZipPath(sdk)
		else:
			raise Exception("cannot read `{sdk}'")

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

	def get_dir(self, dir: str) -> list[str]:
		here = self.fs.joinpath(dir)
		print(here)
		return [path.name for path in here.iterdir()]

	def get_content(self, file: str) -> str | None:
		here = self.fs.joinpath(file)
		if not here.exists():
			return None
		return here.read_bytes().decode()

	def validate(self):
		if self.sdk_version is None:
			raise ValueError("no SDK version specified or detected")

def parse_arguments() -> Context:
	parser = ArgumentParser(
		prog='mkpatch',
		description='SDK10 CMake patch file generator',
	)
	parser.add_argument(
		'-v', '--version',
		help="specify SDK10 version (i.e. 86, 104, 108)",
		type=int,
	)
	parser.add_argument(
		'-t', '--target',
		help="specify device target (i.e. DA1459X)",
		type=str,
	)
	parser.add_argument(
		'sdk',
		help="SDK10 directory or archive",
	)

	options = parser.parse_args()

	for dependency in ("git",):
		if which(dependency) is None:
			parser.error(f"missing dependency: {dependency}")

	patch_root_cmd = ("git", "rev-parse", "--show-toplevel",)
	patch_root_cwd = path.dirname(path.realpath(argv[0]))
	patch_root_proc = run(patch_root_cmd, stdout=PIPE, cwd=patch_root_cwd)
	patch_root = patch_root_proc.stdout.decode().strip()

	try:
		ctx = Context(options.sdk)

		if options.target is not None:
			ctx.sdk_target = options.target.upper()
		if options.version is not None:
			ctx.sdk_version = options.version
		ctx.patch_root = patch_root

		ctx.validate()

		return ctx
	except Exception as e:
		parser.error(str(e))

class Diff:
	"""
	The base Diff class just produces a regular diff from the (possibly absent)
	SDK10 file. This effectively adds a new file or replaces the SDK10 source file
	with the file in the patch directory.
	"""

	ctx: Context
	file: str

	content_a: str | None
	content_b: str = ""

	def __init__(self, ctx: Context, file: str):
		self.ctx = ctx
		self.file = file

	def compare(self):
		a = [] if self.content_a is None else self.content_a.splitlines()
		fromfile = "/dev/null" if self.content_a is None else f"a/{self.file}"

		b = self.content_b.strip().splitlines()
		b = [line.rstrip() for line in b]
		tofile = f"b/{self.file}"

		diff = unified_diff(a, b, fromfile, tofile, n=0, lineterm="")
		self.ctx.output.write("\n".join(diff) + "\n")

	def diff(self):
		self.compare()

class IgnoreDiff(Diff):
	"""
	IgnoreDiff is slightly different and is used to ensure all the lines in the
	patch source ignore file are present in the SDK version. This ensures no
	duplicate ignore lines exist after patching.
	"""

	def diff(self):
		if self.content_a is None:
			self.content_a = ""
		lines_a = self.content_a.splitlines()
		lines_b = self.content_b.splitlines()

		add_lines = set(lines_b) - set(lines_a)

		self.content_b = "\n".join((*lines_a, *add_lines,))

		self.compare()

def get_diff_class(file: str) -> type[Diff]:
	file_name = path.basename(file)
	match = re.match(r'.*?\.(.+)', file_name)
	file_type = file_name if match is None else match.group(1)

	if file_type == "gitignore": return IgnoreDiff
	return Diff

def main():
	ctx = parse_arguments()
	ctx.output = stdout

	mkpatch_version_cmd = ("git", "describe", "--tags", "--always", "--dirty",)
	mkpatch_version_proc = run(mkpatch_version_cmd, stdout=PIPE, cwd=ctx.patch_root)
	mkpatch_version = mkpatch_version_proc.stdout.decode().strip()

	files_cmd = ("git", "ls-files", "--", "sdk",)
	files_proc = run(files_cmd, stdout=PIPE, cwd=ctx.patch_root)
	files = files_proc.stdout.decode().strip().splitlines()

	if len(files) == 0:
		print("no files to patch!", file=stderr)
		return 0

	ctx.output.write(f"sdk10-cmake mkpatch {mkpatch_version} for " +\
		f"{ctx.sdk_target} SDK10 version {ctx.sdk_version}.\n\n")
	ctx.output.write(f"{PATCH_LICENSE}\n---\n\n")

	template_vars = {
		"SDK_VERSION": ctx.sdk_version,
		"SDK_TARGET": ctx.sdk_target,
	}

	for file in files:
		real_file = file
		file = file.removesuffix(".in")
		template = real_file != file

		diff_class = get_diff_class(file)

		diff = diff_class(ctx, file)

		# read file A contents
		diff.content_a = ctx.get_content(real_file)
	
		# read file B contents
		path_b = path.join(ctx.patch_root, real_file)
		if path.exists(path_b):
			file_b = open(path_b, 'rb', buffering=0)
			content_b = file_b.read().decode()
			if template:
				content_b = JINJA_ENV.from_string(content_b).render(**template_vars)
			diff.content_b = content_b
		diff.diff()
	
	ctx.output.flush()
	ctx.output.close()
	
	return 0

if __name__ == "__main__":
	exit(main())

