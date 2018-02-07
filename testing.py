import subprocess

process = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
result = process.communicate()[0]

print(result)
