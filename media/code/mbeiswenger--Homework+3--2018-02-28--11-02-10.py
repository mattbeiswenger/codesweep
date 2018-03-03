def blah(num):
	#insert code here
	return num

import sys

def Main():
	with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
		output.write(str(blah(int(1))) + '\n')
		output.write(str(blah(int(1))) + '\n')
		output.write(str(blah(int(2))) + '\n')
		