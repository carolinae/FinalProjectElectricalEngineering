import math
import win32com
import sys
import csv

from win32com.client import makepy
import numpy as np
from ctypes import cdll

# cdll.msvcrt.controlfp(0x10000, 0x30000)

sys.argv = ["makepy", "OpenDSSEngine.DSS"]
makepy.main()
DSSObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
DSSObj.AllowForms = True
DSSText = DSSObj.Text  # Used for all text interfacing from matlab to opendss
DSSCircuit = DSSObj.ActiveCircuit  # active circuit

DSSText.Command = 'compile "C:\\Program Files\\OpenDSS\\IEEETestCases\\123Bus\\IEEE123Master.dss"'  # Path where Master and its associated files are stored.
nodeNames = DSSCircuit.YNodeOrder

lineNames = DSSCircuit.Lines.AllNames
transformerNames = DSSCircuit.Transformers.AllNames
voltageNames = DSSCircuit.AllNodeNames

DSSText.Command = 'Batchedit Load..* vmin=0.7'  # Loadshape PQmult
nt = 17520
TimeArray = [1, nt]

# solve first a 24-hr period to get the regulator and capacitor controls synchronized.

DSSText.Command = 'set mode=daily stepsize=1h number=24'  # we want 1 day-24 hour period
DSSText.Command = 'Solve'
DSSText.Command = 'set mode=yearly stepsize=1h number=1'  # number - Number of solutions or time steps to perform for each Solve command
DSSText.Command = 'set hour=0'  # Start at second 0 of hour 5

loadnames: list = DSSCircuit.Loads.AllNames
new_loadnames: list = []
balancedLoads: list = []
for name in loadnames:
    if 'a' not in name and 'b' not in name and 'c' not in name:
        new_loadnames.append(name[1:] + ".1")
        new_loadnames.append(name[1:] + ".2")
        new_loadnames.append(name[1:] + ".3")
        balancedLoads.append(loadnames.index(name))
    else:
        new_loadnames.append((name[1:]).replace('a', '.1').replace('b', '.2').replace('c', '.3'))

lines = 0
Ibase = (5 * 10 ^ 3) / (math.sqrt(3) * 4.16)

SfactorToPU = 3 / (5 * 10 ^ 3)

DSSObj.AllowForms = False  # true
countOutliar = 0
totc = 0
atime = 0
columns = np.size(DSSCircuit.AllBusVmagPu)

v_mag = np.zeros((nt, columns))
v_ang_matrix = np.zeros((nt, columns))

powers = np.zeros((nt, len(new_loadnames) * 2))
for i in range(nt):
    totc = totc + 1
    DSSText.Command = "get hour"
    hour = DSSText.Result

    DSSText.Command = 'Solve'
    DSSText.Command = 'get steptime'
    atime = atime + float(DSSText.Result)

    v = DSSCircuit.AllBusVolts
    comp_v = []
    for r in range(0, len(v)-1, 2):
        comp_v.append(complex(v[r], v[r+1]))
    ang_new_v = []
    for m in range(len(comp_v)):
        ang_new_v.append(np.angle(comp_v[m]))

    for j in range(len(DSSCircuit.AllBusVmagPu)):
        v_mag[i][j] = DSSCircuit.AllBusVmagPu[j]

    for j in range(len(ang_new_v)):
        v_ang_matrix[i][j]=ang_new_v[j]

    loadCount = 1
    AllPowers = []  # *(len(new_loadnames) * 2)
    while loadCount <= len(new_loadnames):
        EPowers = list(DSSObj.ActiveCircuit.ActiveElement.Powers)
        if loadCount in balancedLoads:
            for j in range(len(EPowers)):
                if EPowers[j] != 0:
                    AllPowers.append(EPowers[j])
                else:
                    continue

        elif DSSObj.ActiveCircuit.ActiveElement.NumConductors == 2 and loadCount not in balancedLoads:
            for j in range(len(EPowers)):
                if EPowers[j] != 0:
                    AllPowers.append(EPowers[j])
                else:
                    continue

        elif DSSObj.ActiveCircuit.ActiveElement.NumConductors == 4:
                AllPowers.append(EPowers[1] + EPowers[3] + EPowers[5])
                AllPowers.append(EPowers[2] + EPowers[4] + EPowers[6])


        else:
            print(DSSObj.ActiveCircuit.ActiveElement.NumConductors)
        loadCount = loadCount + 1

    for l in range(len(AllPowers)):
        powers[i][l] = AllPowers[l]
    # powers[i, :] = AllPowers
    # AllPowers = []
    ll = 6

# nodes 150-150r-149 are all the source hence have constant voltages. don't include them in the ANN simulations: (9 since each one of them has 3 phases)

# voltageNames(1:9) = []
# ang(:,1:9) = []
# mag(:,1:9) = []

DSSText.Command = 'get Totaltime'
tot_time = DSSText.Result

in_outSetsStart = math.floor(nt * 0.8)
trainSetStop = in_outSetsStart - 1

annInput = powers[in_outSetsStart:nt, :]
annOutput = v_mag[in_outSetsStart:nt, :], v_ang_matrix[in_outSetsStart:nt, :]  # only voltages
training = powers[1:trainSetStop, :], v_mag[1:trainSetStop, :], v_ang_matrix[1:trainSetStop, :]

with open('C:\\Program Files\\OpenDSS\\IEEETestCases\\123Bus\\csv\\training.csv', 'w') as training:
    writer = csv.writer(training)
    writer.writerows(training)
with open('C:\\Program Files\\OpenDSS\\IEEETestCases\\123Bus\\csv\\annInput.csv', 'w') as annInput:
    writer = csv.writer(annInput)
    writer.writerows(annInput)
with open('C:\\Program Files\\OpenDSS\\IEEETestCases\\123Bus\\csv\\annOutput.csv', 'w') as annOutput:
    writer = csv.writer(annOutput)
    writer.writerows(annOutput)
