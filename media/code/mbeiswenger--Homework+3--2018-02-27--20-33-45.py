def blah(num):
	#insert code here
	return num + 1

import sys

def Main():
	with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
		for line in input:
			if line[0] == '"' and line[-1] == '"':
				output.write(str(function(line)) + '\n')
			else:
				output.write(str(function(int(line))) + '\n')

if __name__ == '__main__':
	Main()
