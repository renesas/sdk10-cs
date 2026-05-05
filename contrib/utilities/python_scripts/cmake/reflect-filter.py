from sys import stdin, stdout
from re import sub

for line in stdin.readlines():
	if len(line.strip()) == 0:
		continue

	pair = line.split(maxsplit=1)
	# defined but no value -> assign empty string
	if len(pair) == 1:
		pair.append("")
	symbol, value = pair

	symbol = symbol.replace("\"", "")

	value = value.strip()
	if symbol == value:
		continue
	value = sub("\\b[A-Za-z_][A-Za-z0-9_]*\\b", "0", value)
	if len(value) > 0:
		value = eval(value, {}, {})
	else:
		value = "\"\""

	stdout.write(f"set({symbol} {value})\n")

stdout.flush()
