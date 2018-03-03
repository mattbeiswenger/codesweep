def blah(num):
	#insert code here
	return num


import sys

def Main():
 	with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
	    # assume that we are not in double quotes
	    inDoubleQuotes = False

	    variable = ""
	    numVariable = ""
	    variableList = []

	    def bool(v):
	        return v in ("True")

	    for line in input:
	        for index, c in enumerate(line):

	            if inDoubleQuotes:
	                if line[index] == "\\" and line[index + 1] == "\"":
	                    continue
	                else:
	                    variable += c

	            if not inDoubleQuotes and c.isdigit():
	                numVariable += c

	            if not inDoubleQuotes and line[index:index + 5] == "False":
	                variableList.append("bool(False)")

	            if not inDoubleQuotes and line[index:index + 4] == "True":
	                variableList.append("bool(True)")

	            # account for the beginning of iteration
	            if index == 0 and line[index] == "\"":
	                inDoubleQuotes = not inDoubleQuotes


	            # if we come across an unescaped quote, toggle inDoubleQuotes
	            if index != 0 and line[index - 1] != "\\" and line[index] == "\"":
	                inDoubleQuotes = not inDoubleQuotes


	        # ------- four instances in which we write to file -------- #

	        # (1) if we are not in double quotes and we come across a ","
	        #     append the variable and make it empty for the next variable
	            if not inDoubleQuotes and line[index] == ",":
	                if variable:
	                    variableList.append("str(" + variable[:-1] + ")")
	                    variable = ""
	                if numVariable:
	                    variableList.append("int(" + numVariable + ")")
	                    numVariable = ""

	        # (2) if we are at the last index and we are accounting for an integer
	            if not inDoubleQuotes and index == len(line) - 1:
	                if numVariable:
	                    variableList.append("int(" + numVariable + ")")
	                    numVariable = ""

	        # (3) if we are at the last index of a string with closing double quote
	            if not inDoubleQuotes and line[index] == "\"" and index == len(line) - 1:
	                if variable:
	                    variableList.append("str(" + variable[:-1] + ")")
	                    variable = ""


	        # (4) if we are at the last index of a string with closing double quote and newline
	            if not inDoubleQuotes and index == len(line) - 1 and line[index] == "\n" and line[index - 1] == "\"":
	                if variable:
	                    variableList.append("str(" + variable[:-1] + ")")
	                    variable = ""

		variableList = ', '.join(variableList)
		output.write(str(blah(variableList)))
		variableList = []

if __name__ == '__main__':
		Main()