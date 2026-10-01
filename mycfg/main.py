import json
import sys

from dce import dead_code_elimination
from lvn import local_value_numbering

def main():
	# Read Bril JSON from stdin
	prog = json.load(sys.stdin)

	# Run DCE
	prog = dead_code_elimination(prog)

	# Run LVN
	prog = local_value_numbering(prog)

	# WRITE OUTPUT
	with open("output.json", "w") as f:
		json.dump(prog, f, indent=2)

if __name__ == "__main__":
	main()
