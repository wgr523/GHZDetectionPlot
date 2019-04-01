import numpy as np
def getanglelist(N):
    for i in range(0,2**(N-2)):
        ret = np.array(list('10'+bin(i)[2:].zfill(N-2)),dtype=int)
        #print(ret)
        rel=[int(i) for i in np.nonzero(ret)[0]]
        yield rel
        rel[0]=1
        yield rel
        rel.insert(0,0)
        yield rel
def getanglelistS2(N):
    for i0 in range(2,N):
        yield ([0,i0])
        yield ([1,i0])
    yield ([0,1])
def getanglelistS3(N):
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            yield ([0,i0,i1])
            yield ([1,i0,i1])
    for i0 in range(2,N):
        yield ([0,1,i0])
def getanglelistS4(N):
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                yield ([0,i0,i1,i2])
                yield ([1,i0,i1,i2])
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            yield ([0,1,i0,i1])
def getanglelistS5(N):
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                for i3 in range(i2+1,N):
                    yield ([0,i0,i1,i2,i3])
                    yield ([1,i0,i1,i2,i3])
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                yield ([0,1,i0,i1,i2])
def getanglelistS5_zero(N):
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                for i3 in range(i2+1,N):
                    yield ([0,i0,i1,i2,i3])
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                yield ([0,1,i0,i1,i2])
def getanglelistS5_one(N):
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                for i3 in range(i2+1,N):
                    yield ([1,i0,i1,i2,i3])
def getanglelistS6(N,split=None,splitstep=None):
    if split is None or splitstep is None:
        for i0 in range(2,N):
            for i1 in range(i0+1,N):
                for i2 in range(i1+1,N):
                    for i3 in range(i2+1,N):
                        for i4 in range(i3+1,N):
                            yield ([0,i0,i1,i2,i3,i4])
                            yield ([1,i0,i1,i2,i3,i4])
        for i0 in range(2,N):
            for i1 in range(i0+1,N):
                for i2 in range(i1+1,N):
                    for i3 in range(i2+1,N):
                        yield ([0,1,i0,i1,i2,i3])
    else:
        for i0 in range(6+split,N,splitstep):
            for i1 in range(i0+2,N,2):
                for i2 in range(i1+2,N,2):
                    yield ([0,2,4,i0,i1,i2])
def getanglelistS7(N):
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                for i3 in range(i2+1,N):
                    for i4 in range(i3+1,N):
                        for i5 in range(i4+1,N):
                            yield ([0,i0,i1,i2,i3,i4,i5])
                            yield ([1,i0,i1,i2,i3,i4,i5])
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                for i3 in range(i2+1,N):
                    for i4 in range(i3+1,N):
                        yield ([0,1,i0,i1,i2,i3,i4])
def getanglelistS8(N):
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                for i3 in range(i2+1,N):
                    for i4 in range(i3+1,N):
                        for i5 in range(i4+1,N):
                            for i6 in range(i5+1,N):
                                yield ([0,i0,i1,i2,i3,i4,i5,i6])
                                yield ([1,i0,i1,i2,i3,i4,i5,i6])
    for i0 in range(2,N):
        for i1 in range(i0+1,N):
            for i2 in range(i1+1,N):
                for i3 in range(i2+1,N):
                    for i4 in range(i3+1,N):
                        for i5 in range(i4+1,N):
                            yield ([0,1,i0,i1,i2,i3,i4,i5])
