import sys

fin = open(sys.argv[1], 'r')

key = fin.read()
key = key.split(' ')
key = key.split('\n')

print (key)
print (len(key))
for i in range(len(key)):
    if i % 4 == 0:
        print('\n\t\t\t\t', end='')

    print('0x'+key[i].strip()+', ', end='') 

print()
