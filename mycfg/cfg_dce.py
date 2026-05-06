import json	# To read input in JSON format
import sys	# To read input from standard input(stdin)

def dead_code_elimination():

	prog = json.load(sys.stdin)     # Read the JSON program from standard input

	# Run repeatedly until no more instructions are removed
	while True:

		definitions = {}
		used_lines = set()
		used_labels = set()
		label_to_line = {}

		changed = False
		line_no = 1

		# Loop through each function in the program
		for func in prog['functions']:

			for instr in func['instrs']:
				instr['_id'] = line_no

				# If instruction uses variables
				if 'args' in instr:
					for arg in instr['args']:

						# If variable was defined earlier,
						# mark that definiton as used
						if arg in definitions:
							used_lines.add(definitions[arg])

				# Mark important ops as used
				if instr.get('op') in ['call', 'return', 'ret', 'print']:
					used_lines.add(line_no)

				# Handling jump and br
				elif instr.get('op') in ['jmp', 'br']:
					used_lines.add(line_no)
					for lbl in instr.get('labels', []):
						used_labels.add(lbl)

						# If label already seen,
						# mark label instruction as used
						if lbl in label_to_line:
							used_lines.add(label_to_line[lbl])

				# Handling Label definition
				elif 'label' in instr:
					label_to_line[instr['label']] = line_no
					if instr['label'] in used_labels:
						used_lines.add(line_no)

				# Record definition
				if 'dest' in instr:
					definitions[instr['dest']] = line_no

				line_no += 1

#		print("Used line numbers:", used_lines)
#		print("Used labels:", used_labels)
#		print("Labels defined:", label_to_line)

# -------- Second pass: remove unused instructions --------
			for func in prog['functions']:

				new_instrs = []
				for instr in func['instrs']:

					# Keep used instructions
					if instr['_id'] in used_lines:

						# Remove unused labels
						if 'label' in instr:
							if instr['label'] not in used_labels and instr['label'] != first_label:
								continue

						new_instrs.append(instr)
					else:
						changed = True

				func['instrs'] = new_instrs

		# Stop is nothing removed
		if not changed:
			break

# -------- Write output to file --------
	with open("output.json", "w") as f:
		json.dump(prog, f, indent=2)

if __name__ == '__main__':	
	dead_code_elimination()
