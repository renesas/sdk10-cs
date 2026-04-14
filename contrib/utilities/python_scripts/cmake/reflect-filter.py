from sys import stdin, stdout
from re import sub

for line in stdin.readlines():
	if len(line.strip()) == 0:
		continue

	symbol, value = line.split(maxsplit=1)

	symbol = symbol.replace("\"", "")

	value = value.strip()
	value = sub("\\b[A-Za-z_][A-Za-z0-9_]*\\b", "0", value)
	value = eval(value, {}, {})

	stdout.write(f"set({symbol} {value})\n")

stdout.flush()
