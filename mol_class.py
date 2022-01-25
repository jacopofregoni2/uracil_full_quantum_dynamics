import qutip
import numpy as np
from jftools.fedvr import fedvr_grid
from scipy.interpolate import interp2d

class mol:
    def __init__(self,n,path): #prende numero stati, path cartella con le matrici, dimensione della matrice quadrata
        self.n=n
        self.path=path
        myvars = {}
        with open(self.path+"grid_metadata.txt") as myfile:
            for line in myfile:
                name, var = line.partition("=")[::2]
                myvars[name.strip()] = float(var.strip())
        self.Y = np.linspace(myvars["xmin0"],myvars["xmax0"],int(myvars["N0"]))#[:120] #reads the coordinates file and builds the first grid
        self.X = np.linspace(myvars["xmin1"],myvars["xmax1"],int(myvars["N1"]))
        self.s_orig = []
        self.s_interp = []
        self.tdm_orig = []
        self.tdm_interp = []
        self.nacx_orig = []
        self.nacx_interp = []
        self.nacy_orig = []
        self.nacy_interp = []

        for i in range(self.n):
            s = np.loadtxt(self.path+"/s"+str(i)+"_pes.txt")#[:120]
            self.s_orig.append(s)
            assert s.shape == (len(self.Y),len(self.X))
            self.s_interp.append(interp2d(self.X,self.Y,s))
        for i in range(self.n):
            self.tdm_orig.append([])
            self.tdm_interp.append([])
            for j in range(i+1,self.n):
                s = np.loadtxt(self.path+"/tdm_"+str(i)+str(j)+".txt")#[:120]
                self.tdm_orig[i].append(s)
                assert s.shape == (len(self.Y),len(self.X))
                self.tdm_interp[i].append(interp2d(self.X,self.Y,s))
        for i in range(self.n):
            self.nacx_orig.append([])
            self.nacx_interp.append([])
            for j in range(i+1,self.n):
                s = np.loadtxt(self.path+"/coup"+str(i)+str(j)+"_x.txt")
                self.nacx_orig[i].append(s) # Check
                assert s.shape == (len(self.Y),len(self.X))
                self.nacx_interp[i].append(interp2d(self.X,self.Y,np.transpose(s)))
        for i in range(self.n):
            self.nacy_orig.append([])
            self.nacy_interp.append([])
            for j in range(i+1,self.n):
                s = np.loadtxt(self.path+"/coup"+str(i)+str(j)+"_y.txt")
                self.nacy_orig[i].append(s) # check 
                assert s.shape == (len(self.Y),len(self.X))
                self.nacy_interp[i].append(interp2d(self.X,self.Y,np.transpose(s)))


    def gen_coords(self,xnew=0,ynew=0):  #takes the two new coordinates arrays as input
        from scipy.interpolate import interp2d
        self.s = [interp(xnew,ynew) for interp in self.s_interp]
        self.tdm = [[interp(xnew,ynew) for interp in tt] for tt in self.tdm_interp]
        self.nacx = [[interp(xnew,ynew) for interp in tt] for tt in self.nacx_interp]
        self.nacy = [[interp(xnew,ynew) for interp in tt] for tt in self.nacy_interp]


