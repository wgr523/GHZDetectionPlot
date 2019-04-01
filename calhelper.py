import numpy as np
from getanglelist import *
from multiprocessing import Process, Queue
import json
import os

class CalHelper():
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
    def a1anphi(self,k,angle,C,step=0.1):
        N = self.N
        if type(angle) is list:
            Theta = np.array(angle) * np.pi / N
        else:
            return -1,()
        ### Theta should have shape (S,)
        S = Theta.shape[0]
        res=0
        record=None
        for alpha in np.arange(0,np.pi/2,step):
            a1mo = np.cos(alpha)
            for beta in np.arange(0,np.pi/2,step):
                anmo = np.sin(alpha) * np.cos(beta)
                for phi in np.arange(0,np.pi,step):# phi is difference of phase
                    x=a1mo*a1mo
                    y=anmo*anmo

                    z = np.zeros((S,2))
                    tmp = 2*a1mo*anmo*np.cos(phi-k*Theta)
                    z[:,0] = tmp + (1-x-y)
                    z[:,1] = tmp - (1-x-y)
                    zu = np.max(np.abs(z),axis=-1)
                    zue = zu * np.exp(1j*(N-k)*Theta)
                    mat_withphase = self.MatSign[S].dot(zue)
                    f = np.max(np.abs(mat_withphase)) / C


                    lamu = (x + y)/2 + np.sqrt(f*f + (x - y)*(x - y)/4)
                    if lamu > res:
                        res = lamu
                        record = a1mo,anmo,phi
        return res, record
    def run_all(self,output):
        #step = 0.1
        N = self.N
        Ctimes = self.Ctimes
        if type(output) is not str:
            print('Output error')
            return
        outputfilename = output
        output = open(outputfilename,'w')
        for angle in getanglelist(N):
            S = len(angle)
            for C in range(S,S*Ctimes+1):
                for k in range(1,N):
                    res, record = self.a1anphi(k,angle,C)
                    self.output_helper(output,res,angle,k,C,record)

        output.close()

        self.read_results(outputfilename)

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

class CalHelperMultiprocess(CalHelper):
    queue = None
    NumPros = 15
    def put_queue(self):
        N = self.N
        Ctimes = self.Ctimes
        for angle in getanglelist(N):
            S = len(angle)
            for C in range(S,S*Ctimes+1):
                for k in range(1,N):
                    #print(k,angle,C)
                    self.queue.put(json.dumps([k,angle,C]))
        for i in range(2*self.NumPros+5):
            self.queue.put('[-1,[],-1]')
    def get_queue(self,output):
        N = self.N
        if type(output) is not str:
            print('Output error')
            return
        output = open(output,'w')
        k,angle,C = json.loads(self.queue.get())
        while k!=-1:
            #print(k,angle,C)
            res, record = self.a1anphi(k,angle,C)
            self.output_helper(output,res,angle,k,C,record)
            k,angle,C = json.loads(self.queue.get())
        output.close()
    def run_all(self,output):
        # start one process, put sth into queue
        # start many pros, read queue
        self.queue = Queue()
        p0 = Process(target=self.put_queue,args=())
        p0.start()
        #self.put_queue()
        #print('------------------')
        #self.get_queue('tmp.txt')
        pros = []
        if type(output) is str:
            for i in range(1,self.NumPros+1):
                p = Process(target=self.get_queue,args=(output+str(i).zfill(2),))
                pros.append(p)
                p.start()
        p0.join()
        for p in pros:
            p.join()
        self.queue.close()
        command_cat='cat'
        for i in range(1,self.NumPros+1):
            command_cat += ' '+output+str(i).zfill(2)
        command_cat += ' > '+output
        os.system(command_cat)
        for i in range(1,self.NumPros+1):
            command_del = 'rm '+output+str(i).zfill(2)
            os.system(command_del)
        self.read_results(output)
        self.analyze_results()

class CalHelperSimple(CalHelper):
    def __init__(self,N):
        self.N = N
        self.Results = {}
        for S in range(1,N+1):
            for k in range(1,N):
                self.Results[(S,k)]=[]
        self.Analysis = np.zeros((N,N-1))
    def a1anphi(self,k,angle,C,step=0.1):
        pass
    def run_all(self,output):
        pass
