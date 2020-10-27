import sys

fin = open(sys.argv[1], 'r')

key = fin.read()
key = key.split(' ')

for i in range(len(key)):
    if i % 8 == 0:
        print('\n\t\t\t\t', end='')

    print('0x'+key[i].strip()+', ', end='') 

print()
