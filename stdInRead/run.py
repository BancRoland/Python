import sys
from struct import *

for line in sys.stdin:
	if 'q' == line.rstrip():
		break
	num=float(line)/31557600
	print(num)
	sys.stdout.write(line)
	 
print("Exit")
