from pathlib import Path

class ReflectTxt:
	symbols = dict()

	def __init__(self, path: Path):
		for line in path.read_text().splitlines():
			if not line.startswith("\""):
				continue
			line = line.removeprefix("\"")

			key, value = line.split("\" ", 1)

			# if the value is the same as the key, the name was not expanded so must
			# be undefined and therefore left untouched by the preprocessor
			if key == value:
				continue

			self.symbols[key] = value

	def get_symbol(self, name: str) -> str | None:
		return self.symbols.get(name)

	def get_symbol_preprocessor(self, name: str) -> str:
		return self.symbols.get(name, "0")
