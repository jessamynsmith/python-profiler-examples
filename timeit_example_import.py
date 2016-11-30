import timeit


print('Plus', timeit.timeit("import uuid; ['Hello world: ' + str(uuid.uuid1()) for n in range(100)]", number=1000))

print('Format', timeit.timeit("import uuid; ['Hello world: {0}'.format(uuid.uuid1()) for n in range(100)]", number=1000))

print('Percent', timeit.timeit("import uuid; ['Hello world: %s' % uuid.uuid1() for n in range(100)]", number=1000))
