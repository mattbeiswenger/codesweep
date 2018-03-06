def function(num):
	#insert code here
	return num _ 1

import sys

def Main():
	with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
		output.write(str(function(int(1))) + '\n')
		output.write(str(function(int(1))) + '\n')
		output.write(str(function(int(2))) + '\n')
		

if __name__ == '__main__':
	Main()