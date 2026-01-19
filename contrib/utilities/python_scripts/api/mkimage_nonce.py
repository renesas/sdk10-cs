import sys
import libcst as cst

name = "read_nonce_from_xml"

replacement = cst.parse_module(f"""
def {name}():
	from secure_image.generate_nonce import generate_nonce
	return generate_nonce()
""")

class ReplaceFunc(cst.CSTTransformer):
	def leave_FunctionDef(self, original_node, updated_node):
		if original_node.name.value == name:
			return replacement.body[0]
		return original_node

source = sys.stdin.read()
original_module = cst.parse_module(source)
updated_module = original_module.visit(ReplaceFunc())
sys.stdout.write(updated_module.code)
sys.stdout.flush()
