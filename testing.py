import re

code = 'def fib(num):\\n\\t#insert code here\\n\\tnumbers = [1, 2, 3]\\n\\tfor n in numbers:\\n\\tprint(n + \\"\\\\n\\")'


# code = code.replace("\\n", "\n")
code = re.sub(r'(\\)+n'), '\n', code)

print(code)
