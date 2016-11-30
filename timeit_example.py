import timeit


print('Plus:', timeit.timeit("['Hello world: ' + str(n) for n in range(100)]", number=1000))

print('Format:', timeit.timeit("['Hello world: {0}'.format(n) for n in range(100)]", number=1000))

print('Percent:', timeit.timeit("['Hello world: %s' % n for n in range(100)]", number=1000))
