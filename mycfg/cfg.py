import json	# To read input in JSON format
import sys	# To read input from standard input(stdin)

# Instructions which terminate a basic block
TERMINATORS = 'jmp' , 'br' , 'ret'

def form_blocks(body):

	# Initialize an empty list to store the current block of instructions
	cur_block = []

	# Loops through each instruction in the function body
	for instr in body:

		# Check if this is an actual instructions (not a label)
		if 'op' in instr:
			cur_block.append(instr)		# Add the instrs to the end of the list i.e end of the curent block

			# Check if the instruction is a terminator
			if instr['op'] in TERMINATORS:
				yield cur_block		# Specifies that the current block is over
				cur_block = []		# Start a new empty block

		# 'op' is not an instruction which means it is a label
		else:
			yield cur_block			# End the current block before the label
			cur_block = [instr]		# Start a new block beginning with the name as the label

	yield cur_block		# In case of no terminator, end the current block

def block_map(blocks, counter):

	out = {}	# Create a 'out' dictionary to map block names to block contents

	# Loop through each block generated earlier
	for block in blocks:

		# Skip empty blocks
		if not block:
			continue

		# Check if the block starts with a label
		if 'label' in block[0]:
			name = block[0]['label']	# Use the label as the block name
			block = block[1:]		# Making a new list that is like the old one, except it skips the first element
		else:
			# Creates a string using an f-string (formatted string)
			name = f"b{counter}"		# 'b' is prefix and '{counter}' will be replaced by value of var 'counter'
			counter += 1
#			name = 'b{}'.format(len(out))	# Getting the number from the length of the out map so far
							# the first time it will be b0 and continues wheneevr we add something new

		out[name] = block	# Store the block in the dictionary with its name

	return out	# Return the completed mapping

def mycfg():
	prog = json.load(sys.stdin)	# Read the JSON program from standard input
	label_number = 0;

	# Loop through each function in the program
	for func in prog['functions']:
		name2block = block_map(form_blocks(func['instrs']), label_number)	# Create blocks and map them to names

		# Iterate through each block in the dictionary
		for name, block in name2block.items():
			print(f"{name}: {block}")	# Print the block name and its corresponding list of instructions
		label_number += 1
#		print(name2block)

if __name__ == '__main__':
	mycfg()
