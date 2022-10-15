#!/bin/python -B

from cProfile import label
#import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy

norm_labels = ["No normalisation", "Area normalisation", "Population normalisation"]

def avg(x):
    if len(x) == 0:
        return 0
    return sum(x)/len(x)

class Did_Sets:
    def __init__(self):
        self.name = ""
        self.group = False
        self.area = 0
        self.pop = []
        self.vals = []
    
    def printSet(self):
        print("Name: " + self.name)
        print("Group: " + ("Treatment" if self.group else "Control"))
        print("Area: " + str(self.area) + " km2")
        print("Population: " + str(self.pop))
        print("Values: " + str(self.vals))

class DiD_Solver:
    def __init__(self, filename, mode=0):
        # mode 0 - direto
        # mode 1 - area
        # mode 2 - população
        self.mode = mode
        self.fname = filename
        self.sets = []
        self.norm_label = norm_labels[mode]
        with open(filename, "r") as fp:
            data = fp.readline()
            self.dates = [int(elem) for elem in data.split(",")]
            for line in fp:
                # Create new data set
                self.sets.append(Did_Sets())
                # Get name
                self.sets[-1].name = line.rstrip('\n')
                # Get group and area
                data = fp.readline().split(",")
                self.sets[-1].group = bool(int(data[0]))
                self.sets[-1].area = float(data[1])
                # Get population
                self.sets[-1].pop = [int(elem) for elem in fp.readline().split(',')]
                # Get values and normalisation
                if mode == 2:
                    self.sets[-1].vals = [1000*float(elem1)/elem2 for elem1,elem2 in zip(fp.readline().split(','), self.sets[-1].pop)]
                else:
                    norm = self.sets[-1].area if mode else 1
                    self.sets[-1].vals = [float(elem)/norm for elem in fp.readline().split(',')]
        self.solved = False
        self.b1 = []

    def solveDiD(self):
        for i in range(len(self.dates)-1):
            y11 = []
            y12 = []
            y21 = []
            y22 = []
            for _set in self.sets:
                if _set.group == False: # if data is in control group
                    y11.append(_set.vals[i])
                    y12.append(_set.vals[i+1])
                else: # if data is in treatment group
                    y21.append(_set.vals[i])
                    y22.append(_set.vals[i+1])
            y11 = avg(y11)
            y12 = avg(y12)
            y21 = avg(y21)
            y22 = avg(y22)

            self.b1.append((y11 - y12) - (y21 - y22))

        self.solved = True

    def printSets(self):
        for _set in self.sets:
            _set.printSet()
            print("\n")

    def plotPop(self):
        plt.figure()
        plt.title("População")
        for _set in self.sets:
            plt.plot(self.dates, _set.pop, label=_set.name)
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.legend(loc="upper right")

    def plotVals(self):
        plt.figure()
        plt.title(self.fname.split('.')[0].split('/')[-1].replace('_',' '))
        for _set in self.sets:
            plt.plot(self.dates, [val for val in _set.vals], label=_set.name)
        plt.xlabel("Year")
        if self.mode == 0:
            lbl = "€"
        elif self.mode == 1:
            lbl = "€/km2"
        else:
            lbl = "€/1000 hab."
        plt.ylabel("Custo - " + lbl)
        plt.legend(loc="upper right")

    def plotDiDEstimator(self):
        if not self.solved:
            return
        plt.figure()
        plt.title("Estimador DiD " + self.fname.split('.')[0].split('/')[-1].replace('_',' '))
        plt.plot([0.5*(self.dates[k]+self.dates[k+1]) for k in range(len(self.dates)-1)], [val for val in self.b1])
        plt.xlabel("Year")
        if self.mode == 0:
            lbl = "€"
        elif self.mode == 1:
            lbl = "€/km2"
        else:
            lbl = "€/1000 hab."
        plt.ylabel("Custo - " + lbl)


# mode 0 - direto
# mode 1 - area
# mode 2 - população

if __name__ == "__main__":
    #did = DiD_Solver("test.csv")
    did = DiD_Solver("data/csv/Saldo_para_a_gerência_seguinte.csv", 2)
    did.printSets()
    did.solveDiD()
    #did.plotPop()
    did.plotVals()
    did.plotDiDEstimator()
    plt.show()