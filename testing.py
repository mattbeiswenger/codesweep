f = open('inputs.txt', 'r')
lines = f.readlines()

#
# def Main():
# 	with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
# 		for line in input:
# 			if line[0] == '"' and line[-1] == '"':
# 				output.write(str(function(line)) + '\n')
# 			else:
# 				output.write(str(function(int(line))) + '\n')
#
# if __name__ == '__main__':
	# Main()



# assume that we are not in double quotes
inDoubleQuotes = False

variable = ""
numVariable = ""
variableList = []

for line in lines:



    for index, c in enumerate(line):

        if inDoubleQuotes:
            if line[index] == "\\" and line[index + 1] == "\"":
                continue
            else:
                variable += c

        if not inDoubleQuotes and c.isdigit():
            numVariable += c

        if not inDoubleQuotes and line[index:index + 5] == "False":
            variableList.append("False")

        if not inDoubleQuotes and line[index:index + 4] == "True":
            variableList.append("True")

        # account for the beginning of iteration
        if index == 0 and line[index] == "\"":
            inDoubleQuotes = not inDoubleQuotes


        # if we come across an unescaped quote, toggle inDoubleQuotes
        if index != 0 and line[index - 1] != "\\" and line[index] == "\"":
            inDoubleQuotes = not inDoubleQuotes

        if index == len(line) - 1:
            # save each variable in a dictionary, specifiying the type.
            # at the end of each line, call the function, specifying the
            # variable type



    # ------- four instances in which we write to file -------- #

    # (1) if we are not in double quotes and we come across a ","
    #     append the variable and make it empty for the next variable
        if not inDoubleQuotes and line[index] == ",":
            if variable:
                variableList.append(variable[:-1])
                variable = ""
            if numVariable:
                variableList.append(numVariable)
                numVariable = ""

    # (2) if we are at the last index and we are accounting for an integer
        if not inDoubleQuotes and index == len(line) - 1:
            if numVariable:
                variableList.append(numVariable)
                numVariable = ""

    # (3) if we are at the last index of a string with closing double quote
        if not inDoubleQuotes and line[index] == "\"" and index == len(line) - 1:
            if variable:
                variableList.append(variable[:-1])
                variable = ""


    # (4) if we are at the last index of a string with closing double quote and newline
        if not inDoubleQuotes and index == len(line) - 1 and line[index] == "\n" and line[index - 1] == "\"":
            if variable:
                variableList.append(variable[:-1])
                variable = ""


for item in variableList:
    print("item:  " + item)
