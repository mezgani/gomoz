fd = open('phps.txt', 'r')
data=fd.readlines()

for s in data:
	print s[s.index('/'):].strip()
