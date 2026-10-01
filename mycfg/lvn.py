def local_value_numbering(prog):

        # ============================================================
        # value number -> information about that value
        #
	# definitions[3] = {
	#     "index": 3,
	#     "expression": {
	#         "operation": "add",
	#         "var1": 1,
	#         "var2": 2
	#     },
	#     "variable_name": "c"
	# }
	# ============================================================
	definitions = {}

	# ============================================================
	# variable name -> value number
	#
	# a -> 1
	# b -> 2
	# c -> 3
	# d -> 3
	# ============================================================
	value_numbers = {}

	# ============================================================
	# expression -> value number
	#
	# ("add", 1, 2) -> 3
	# ============================================================
	expression_table = {}

	# ============================================================
	# Keeps track of how many times each variable has been defined.
	#
	# a -> 1
	# after another definition
	# a -> 2
	# ============================================================
	variable_versions = {}

	# ============================================================
	# Keeps track of the currently active version of every variable.
	#
	# current_variable = {
	#	"a":"a2",
	#	"b":"b1"
	# }
	# ============================================================
	current_variable = {}

	# Next value number
	next_index = 1

	def get_value_number(variable):

		nonlocal next_index

		# Use the current version of the variable, if available
		if variable in current_variable:
			variable = curent_variable[variable]

		# Return the existing value number if the variable
		# already has one.
		if variable in value_numbers:
			return value_numbers[variable]

		# Variable does not have a value number yet.
		# Create a new value number and treat it as an INPUT.
		index = next_index
		next_index += 1

		definitions[index] = {
			"index": index,
			"expression": {
				"operation": "INPUT",
				"var1": variable,
				"var2": None
			},
			"variable_name": variable
		}

		value_numbers[variable] = index

		return index

	# ============================================================
	# Process each function
	# ============================================================
	for function in prog["functions"]:

		for instruction in function["instrs"]:

			operation = instruction["op"]

			# Skip instructions that do not define a variable.
			if "dest" not in instruction:
				continue

			variable = instruction["dest"]

			# Create a new version whenever a variable is defined.
			#     a -> a1
			#     a -> a2
			#     a -> a3
			if variable in variable_versions:
				variable_versions[variable] += 1

			else:
				variable_versions[variable] = 1

			versioned_variable = (
				variable + str(variable_versions[variable])
			)

			# Make this the currently active version
			current_variable[variable] = versioned_variable


			#---------------------------------------------------------
			# CASE 1: CONSTANT
			#---------------------------------------------------------
			if operation == "const":

				value = instruction["value"]

				expression = ("const", value)

				# Check whether this constant already exists

				if expression in expression_table:

					index = expression_table[expression]

				else:

					# New value number
					index = next_index
					next_index += 1

					# Store expression -> value number
					expression_table[expression] = index

					# Store information about the value
					definitions[index] = {
						"index": index,
						"expression": {
						"operation": "const",
							"var1": value,
							"var2": None
						},
						"variable_name": versioned_variable
					}

				# Associate the versioned variable with its
				# value number
				value_numbers[versioned_variable] = index

			#---------------------------------------------------------
			# CASE 2: NORMAL OPERATION
			#---------------------------------------------------------
			else:

				# Get the operands
				#
				# c = add a b
				#
				# args = ["a", "b"]
				args = instruction.get("args", [])

				# Currently handling binary operations only.

				if len(args) != 2:
					continue

				var1 = args[0]
				var2 = args[1]


				# Replace operands with their current versions.
				#
				#     a1 = const 5
				#     a2 = const 10
				#
				#     c = add a b
				#
				# becomes:
				#
				#     c1 = add a2 b1
				if var1 in current_variable:
					var1 = current_variable[var1]

				if var2 in current_variable:
					var2 = current_variable[var2]


				# Convert operands into value numbers.
				var1_index = get_value_number(var1)
				var2_index = get_value_number(var2)

				# Create expression key
				#
				# add a b
				#
				# if:
				#
				# a -> 1
				# b -> 2
				#
				# expression becomes:
				#
				# ("add", 1, 2)

				expression = (
					operation,
					var1_index,
					var2_index
				)

 				# Check whether this expression already exists

				if expression in expression_table:

					# Existing expression:
					# reuse its value number.

					index = expression_table[expression]

				else:

					# New expression
					# create a new value number.
					index = next_index
					next_index += 1

					# Store expression -> value number
					expression_table[expression] = index

					# Store complete information about the value.
					definitions[index] = {
						"index": index,
						"expression": {
							"operation": operation,
							"var1": var1_index,
							"var2": var2_index
						},
						"variable_name": versioned_variable
					}

				# Associate the versioned variable with its
				# value number.
				value_numbers[versioned_variable] = index

	# ============================================================
	# ADD LVN INFORMATION TO OUTPUT
	# ============================================================
	prog["definitions"] = definitions
	prog["value_numbers"] = value_numbers

	return prog
