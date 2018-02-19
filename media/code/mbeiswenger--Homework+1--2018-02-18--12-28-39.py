def function(num):
	#insert code here
	return num

import sys

def Main():
	with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
		for line in input:
			output.write(str(function(int(line))) + '\n')

if __name__ == '__main__':
	Main()