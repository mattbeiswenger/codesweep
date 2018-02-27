f = open('inputs.txt', 'r')
line = f.readlines()


line = "".join(line)
print(line)
line = line[:-1]
print(line)




# assume that we are not in double quotes
inDoubleQuotes = False

variable = ""
numVariable = ""
variableList = []

for index, c in enumerate(line):

    if inDoubleQuotes:
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

    # if we are not in double quotes and we come across a ","
    # append the variable and make it empty for the next variable
    if not inDoubleQuotes and line[index] == ",":
        if variable:
            variableList.append(variable[:-1])
            variable = ""
        if numVariable:
            variableList.append(numVariable)
            numVariable = ""



    if not inDoubleQuotes and index == len(line) - 1:
        if numVariable:
            variableList.append(numVariable)
            numVariable = ""

    # if we are at the end of the last string parameter
    if not inDoubleQuotes and line[index] == "\"" and index == len(line) - 1:
        if variable:
            variableList.append(variable[:-1])
            variable = ""

    # if we are at the end of the line and there is a newline character after
    if not inDoubleQuotes and index == len(line) and line[index - 1] == "\"" and line[index] == "\\" and line[index + 1] == "n":
        if variable:
            variableList.append(variable[:-1])
            variable = ""




for item in variableList:
    print(item)
