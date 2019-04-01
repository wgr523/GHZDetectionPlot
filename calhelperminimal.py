import numpy as np
from getanglelist import *
import json
import os

class CalHelperMinimal():
    def __init__(self,N,Ctimes=1):
        self.N = N
        self.Ctimes = int(Ctimes)
        self.MatSign = {}
        for S in range(1,N+1):
            mat_sign = []
            for binary in range(0,2**(S-1)):
                b=bin(binary)[2:].zfill(S)
                sign=np.array(list(b), dtype=int)
                mat_sign.append(1-2*sign)
            self.MatSign[S]=np.array(mat_sign)
        self.Results = {}
        self.AnglesStr = {}
        self.Analysis = np.zeros((N,N-1))

    def output_helper(self,output,res,angle,k,C,record):
        print(res,angle,k,C,record[0],record[1],record[2],file=output,sep=';')

    def read_results(self,filename):
        N = self.N
        self.Results = {}
        self.AnglesStr = {}
        for S in range(1,N+1):
            self.AnglesStr[S]=set()
        with open(filename) as fin:
            for line in fin:
                splits = line.split(';')
                res,angle,k,C,record0,record1,record2 = float(splits[0]),json.loads(splits[1]),int(splits[2]),int(splits[3]),float(splits[4]),float(splits[5]),float(splits[6])
                key = (len(angle),json.dumps(angle)+'C'+str(C),k)
                self.AnglesStr[key[0]].add(key[1])
                if key not in self.Results:
                    self.Results[key]=[]
                self.Results[key].append([1-res/(1+len(angle)/C),record0,record1,record2])
        self.analyze_results()
    def analyze_results(self):
        N = self.N
        max_len = 0
        for S,v in self.AnglesStr.items():
            if max_len < len(v):
                max_len = len(v)
            self.AnglesStr[S] = sorted(list(v))
        self.Analysis = np.zeros((N,max_len,N-1))

        for S,angleC,k in self.Results:
            results = self.Results[(S,angleC,k)]
            if len(results) > 0:
                res,a1mo,anmo,phi = max(results)
                self.Analysis[S-1,self.AnglesStr[S].index(angleC),k-1] = res

    def write_points(self,output=None):
        N = self.N
        nok = np.min(self.Analysis,axis=-1)
        to_plot_1Cmin = np.zeros(N)
        to_plot_1Cmax = np.zeros(N)
        to_plot_2C = np.zeros(N)

        to_plot_allC = np.zeros(N)
        index_C = np.zeros(N,dtype=np.int)
        for S in range(N):# real S is S+1
            #a_c = {}
            Cidxs = []
            Cidxs2 = []
            Cidxs3 = []
            for idx in range(len(self.AnglesStr[S+1])):
                ss = self.AnglesStr[S+1][idx].split('C')
                angles = ss[0]
                C = int(ss[1])
                if C==S+1:
                    Cidxs.append(idx)
                if C==2*(S+1):
                    Cidxs2.append(idx)
            nozero_1C = nok[S,Cidxs]
            nozero_2C = nok[S,Cidxs2]
            nozero = nok[S,range(len(self.AnglesStr[S+1]))]
            #nozero = nozero[np.nonzero(nozero)]
            to_plot_allC[S]=np.max(nozero)
            idx=np.argmax(nozero)
            ss = self.AnglesStr[S+1][idx].split('C')
            index_C[S]=int(ss[1])
            to_plot_1Cmax[S] = np.max(nozero_1C)
            to_plot_1Cmin[S] = np.min(nozero_1C)
            to_plot_2C[S] = np.max(nozero_2C)
            #idx = np.argmax(nozero)
            #ss = self.AnglesStr[S+1][idx].split('C')
            ## real S is S+1...
            #angles = ss[0]
            #C = int(ss[1])
            #to_plot_max[S] = nozero[idx]
        x = np.arange(1,N+1)
        if output is None:
            outputfilename = 'to_plot.dat'
        else:
            outputfilename = output.strip('.dat')+'.dat'
        with open(outputfilename,'w') as fout:
            for i in range(N):
                print(x[i],to_plot_allC[i],to_plot_1Cmax[i],sep = '\t',file = fout)
