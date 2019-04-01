import numpy as np
import calhelper
import getanglelist
from getanglelist import *
from calhelper import CalHelper
from calhelper import CalHelperMultiprocess
import time

for N in range(2,16):
    print(N,'handling')
    util = CalHelperMultiprocess(N,Ctimes=2)
    tic = time.time()
    util.run_all('results/N_{}.txt'.format(N))
    print(N,'time is',time.time()-tic)