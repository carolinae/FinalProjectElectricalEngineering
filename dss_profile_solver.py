import math
import win32com
import sys
import numpy as np
from win32com.client import makepy
from ckt5_update_loadshape_file import update_loadshape_ckt5_file
import time

# cdll.msvcrt.controlfp(0x10000, 0x30000)
CIRCUIT_PROFILE_IEEE123 = "ieee123"
CIRCUIT_PROFILE_CK5 = "ckt5"


def run(profile, examination_period, selected_include_caps, pu_value, load_model, model_inputs):
    sys.argv = ["makepy", "OpenDSSEngine.DSS"]
    makepy.main()
    DSSObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
    DSSObj.AllowForms = True
    DSSText = DSSObj.Text  # Used for all text interfacing from matlab to opendss
    DSSCircuit = DSSObj.ActiveCircuit  # active circuit

    # Declare pu of the circuit:
    # DSSText.Command = 'Circuit.' + profile + '.pu=' + pu_value
    # if profile == CIRCUIT_PROFILE_CK5:
    #     DSSText.Command = "Clear"
    #     DSSText.Command = "Set DefaultBaseFrequency = 60"
    #     DSSText.Command = "New Circuit." + profile + " pu=" + pu_value + " r1 = 0 x1 = 0.001 r0 = 0 x0 = 0.001"
    # else:
    #     DSSText.Command = "Clear"
    #     # DSSText.Command = "New object=circuit." + profile
    #     # DSSText.Command = "~ basekv=4.16 Bus1=150" + " pu=" + pu_value + " R1=0 X1=0.0001 R0=0 X0=0.0001"
    #     DSSText.Command = "New Circuit." + profile + " pu=" + pu_value + " R1=0 X1=0.0001 R0=0 X0=0.0001"

    if profile == CIRCUIT_PROFILE_CK5:
        update_loadshape_ckt5_file()


    if profile == CIRCUIT_PROFILE_CK5:
        DSSText.Command = 'compile "C:\\ck5\\Run_ckt5.DSS"'  # Path where Master and its associated files are stored.
    else:
        DSSText.Command = 'compile "C:\\ieee123\\Run_IEEE123Bus.DSS"'  # Path where Master and its associated files are stored.



    nodeNames = DSSCircuit.YNodeOrder
    lineNames = DSSCircuit.Lines.AllNames
    transformerNames = DSSCircuit.Transformers.AllNames
    voltageNames = DSSCircuit.AllNodeNames
    print(len(voltageNames))

    ####################################################################################################################
    # User's choice: use or not use capacitors during tha calculations
    Cindex = DSSCircuit.Capacitors.First
    while Cindex != 0:
        if selected_include_caps == 0:
            DSSText.Command = DSSCircuit.ActiveElement.Name + '.kVar=0'
        Cindex = DSSCircuit.Capacitors.Next

    ####################################################################################################################

    ####################################################################################################################
    # User's choice: change Load's model (1/2/3/4/5/6/7/8):
    num_of_loads = len(DSSCircuit.Loads.AllNames)
    Lindex = DSSCircuit.Loads.First
    while Lindex != 0 and Lindex < 0.25 * num_of_loads:
        loadName = DSSCircuit.ActiveElement.Name
        DSSText.Command = loadName + ".model=" + load_model
        if load_model == "1":
            DSSText.Command = loadName + ".Vminpu=" + model_inputs['Vminpu_model1']
            DSSText.Command = loadName + ".Vlowpu=" + model_inputs['Vmaxpu']

        if load_model == "2":
            DSSText.Command = loadName + ".Vlowpu=" + model_inputs['Vlowpu']
            DSSText.Command = loadName + ".Vminpu=" + model_inputs['Vminpu_model2']

        if load_model == "3":
            DSSText.Command = loadName + ".Pvfactor=" + model_inputs['Pvfactor']

        if load_model == "4":
            DSSText.Command = loadName + ".CVRwatts=" + model_inputs['CVRwatts']
            DSSText.Command = loadName + ".CVRvars=" + model_inputs['CVRvars']

        # if load_model == "5":
        #     DSSText.Command = loadName + ".Vminpu=" + model_inputs['Vminpu_model1']
        #     DSSText.Command = loadName + ".Vlowpu=" + model_inputs['Vmaxpu']

        # if load_model == "6":
        #     DSSText.Command = loadName + ".Xd=" + model_inputs['Xd']
        #
        # if load_model == "7":
        #     DSSText.Command = loadName + ".Balanced=" + model_inputs['Balanced']

        if load_model == "8":
            DSSText.Command = loadName + ".Vminpu=" + model_inputs['Vminpu_model8']
            DSSText.Command = loadName + ".ZIPV=" + model_inputs['ZIPV']

        Lindex = DSSCircuit.Loads.Next

    ####################################################################################################################

    DSSText.Command = 'Batchedit Load..* vmin=0.7'  # Loadshape PQmult
    nt = examination_period
    TimeArray = [1, nt]

    # solve first a 24-hr period to get the regulator and capacitor controls synchronized.
    DSSText.Command = 'set mode=daily stepsize=1h number=24'  # we want 1 day-24 hour period
    DSSText.Command = 'Solve'
    DSSText.Command = 'set mode=yearly stepsize=1h number=1'  # number - Number of solutions or time steps to perform for each Solve command
    DSSText.Command = 'set hour=0'  # Start at second 0 of hour 5

    DSSParallel = DSSCircuit.Parallel  # Habdler for Parallel processing functions
    CPUs = DSSParallel.NumCPUs - 1  # Gets how many CPUs this PC has
    # By default one actor is created, if you want more than one
    # parallel instance you will have to create them. Try to leave at least
    # One CPU available to handle the rest of windows, otherwise will block
    # Everything
    # Prepares everything for a yearly simulation using temporal parallelization
    DSSText.Command = 'Clone ' + str(CPUs - 2)  # Creates the other actors completing #CPUs-1 actors
    YDelta = nt / (CPUs - 1)
    print('Compiling and creating Actors')

    for i in range(1, CPUs):
        DSSParallel.ActiveActor = i
        if i == (CPUs - 1):
            YDelta = nt - (CPUs - 2) * YDelta
        DSSText.Command = 'set mode=Yearly stepsize=1h number=1 hour=' + str((i - 1) * YDelta)

    # Now the actors are solved
    DSSText.Command = 'Set Parallel=Yes'  # Activates parallel processing

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

    # Edid load powers
    found_kVA = 0
    kVA = 0
    Lindex = DSSCircuit.Loads.First
    while Lindex != 0:
        loadName = DSSCircuit.ActiveElement.Name
        DSSText.Command = '? ' + loadName + '.Bus1'  # Bus1=Bus to which the load is connected. May include specific node specification. This is the secondary bus of a transformer
        loadBusNameWithPhase = DSSText.Result

        Tindex = DSSCircuit.Transformers.First
        while Tindex != 0:
            transName = DSSCircuit.ActiveElement.Name
            DSSText.Command = '? ' + transName + '.buses'
            trans_sec_bus = DSSText.Result

            if (loadBusNameWithPhase.split('.')[0] == trans_sec_bus.split(',')[1][1:].split('.')[0]):
                DSSText.Command = '? ' + transName + '.kVA'  # under the assumption that kVA is identical in both windings.
                kVA = DSSText.Result
                found_kVA = 1
                break
            Tindex = DSSCircuit.Transformers.Next

        if (found_kVA == 1):
            S = float(kVA) * 0.8
            P = S * 0.9
            # Q = np.sqrt(np.square(S) - np.square(P))
            DSSText.Command = loadName + '.kW=' + str(P)
            # DSSText.Command = loadName + '.kvar=' + str(Q)

        Lindex = DSSCircuit.Loads.Next

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

    #################################start of "for i in range(nt)" loop#################################################
    for i in range(nt):
        # start = time.time()
        totc = totc + 1
        DSSText.Command = "get hour"
        hour = DSSText.Result

        DSSText.Command = 'Solve'
        DSSText.Command = 'get steptime'
        atime = atime + float(DSSText.Result)

        v = DSSCircuit.AllBusVolts
        comp_v = []
        for r in range(0, len(v) - 1, 2):
            comp_v.append(complex(v[r], v[r + 1]))

        ang_new_v = []
        for m in range(len(comp_v)):
            ang_new_v.append(np.angle(comp_v[m]))

        all_vbus_pu = DSSCircuit.AllBusVmagPu
        for j in range(len(all_vbus_pu)):
            v_mag[i][j] = all_vbus_pu[j]

        for j in range(len(ang_new_v)):
            v_ang_matrix[i][j] = ang_new_v[j]

        Lindex = DSSCircuit.Loads.First
        loadCount = 0
        AllPowers = []  # *(len(new_loadnames) * 2)
        while Lindex != 0:
            EPowers = DSSObj.ActiveCircuit.ActiveElement.Powers
            if loadCount in balancedLoads:
                for j in range(len(EPowers)):
                    if EPowers[j] != 0:
                        AllPowers.append(EPowers[j])
                    else:
                        continue

            elif DSSObj.ActiveCircuit.ActiveElement.NumConductors == 2 and loadCount not in balancedLoads:
                AllPowers.append(EPowers[0])
                AllPowers.append(EPowers[1])

            elif DSSObj.ActiveCircuit.ActiveElement.NumConductors == 4:
                AllPowers.append(EPowers[0] + EPowers[2] + EPowers[4])
                AllPowers.append(EPowers[1] + EPowers[3] + EPowers[5])
            else:
                print(DSSObj.ActiveCircuit.ActiveElement.NumConductors)
            loadCount = loadCount + 1
            Lindex = DSSCircuit.Loads.Next

        for l in range(len(AllPowers)):
            powers[i][l] = AllPowers[l]

        ll = 6
        print(i)
    ###################################end of "for i in range(nt)" loop#################################################

    # nodes 150-150r-149 are all the source hence have constant voltages. don't include them in the ANN simulations: (9 since each one of them has 3 phases)

    # voltageNames(1:9) = []
    # ang(:,1:9) = []
    # mag(:,1:9) = []

    DSSText.Command = 'get Totaltime'
    tot_time = DSSText.Result

    in_outSetsStart = math.floor(nt * 0.8)
    trainSetStop = in_outSetsStart - 1

    if CIRCUIT_PROFILE_CK5 == profile:
        annInput_path = 'C:\\ck5\\annInput.csv'
    else:
        annInput_path = 'C:\\ieee123\\annInput.csv'
    annInput = np.zeros((nt - in_outSetsStart, len(new_loadnames) * 2))
    annInputA = open(annInput_path, 'w', newline='')
    for row in powers[in_outSetsStart - 1:nt][:]:
        for column in row:
            annInputA.write('%.8f,' % column)
        annInputA.write('\n')

    if CIRCUIT_PROFILE_CK5 == profile:
        annOutput_path = 'C:\\ck5\\annOutput.csv'
    else:
        annOutput_path = 'C:\\ieee123\\annOutput.csv'
    annOutput = np.zeros((nt - in_outSetsStart, len(DSSCircuit.AllBusVolts) + len(DSSCircuit.AllBusVmagPu)))
    matrix = np.hstack((v_mag, v_ang_matrix))
    annOutputA = open(annOutput_path, 'w', newline='')
    for row in matrix[in_outSetsStart - 1:nt][:]:
        for column in row:
            annOutputA.write('%.8f,' % column)
        annOutputA.write('\n')

    if CIRCUIT_PROFILE_CK5 == profile:
        training_path = 'C:\\ck5\\training.csv'
    else:
        training_path = 'C:\\ieee123\\training.csv'
    training = np.zeros(
        (trainSetStop - 1, (len(new_loadnames) * 2) + len(DSSCircuit.AllBusVolts) + len(DSSCircuit.AllBusVmagPu)))
    matrix = np.hstack((powers, v_mag, v_ang_matrix))
    trainingA = open(training_path, 'w', newline='')
    for row in matrix[0:trainSetStop][:]:
        for column in row:
            trainingA.write('%.8f,' % column)
        trainingA.write('\n')

#
# if __name__ == '__main__':
#     run(PROFILE_IEEE123)
