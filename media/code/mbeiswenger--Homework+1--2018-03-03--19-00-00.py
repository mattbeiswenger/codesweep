def monkey_trouble(a_smile, b_smile):
	#insert code here
	if a_smile and b_smile:
	    return True
	elif not a_smile and not b_smile:
	    return True
	else:
	    return False

import sys

def bool(v):
	return v.lower() in ("true")

def Main():
	with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
		output.write(str(monkey_trouble(True, True)) + '\n')
		output.write(str(monkey_trouble(False, False)) + '\n')
		output.write(str(monkey_trouble(True, False)) + '\n')
		

if __name__ == '__main__':
	Main()