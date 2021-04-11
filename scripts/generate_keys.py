import numpy

def write_weighted_key_bytes(population, num):
    for weight in numpy.arange(0.1, 1, 0.1):
        for version in range(num):
            fout = open('keys/rand-'+"{:.2f}".format(round(weight, 1))+'_'+"{:.2f}".format(round(1-weight, 1))+'.v'+str(version)+'.key', 'w')
            samples = numpy.random.choice(population, size=1024, p=[weight, 1-weight])
            fout.write(hex(int(''.join(samples), 2))[2:])

write_weighted_key_bytes(['0', '1'], 10)
