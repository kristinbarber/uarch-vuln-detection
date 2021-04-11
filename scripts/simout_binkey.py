import re, sys

txt = open(sys.argv[1], 'r').read()

key = ''
for match in re.finditer('====== Round [0-9]+, e=([0|1])  ======', txt):
    key += match.group(1)

print(key)
#print(hex(int(key[::-1],2))[2:])
