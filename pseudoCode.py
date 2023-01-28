# import libraries

# initialize
# establish ports and pins
# establish easily changed variables
Threshold1 = 300
Threshold2 = 1100
mode = 0
AllowO2 = 0
AllowN2 = 0
AllowH2O = 0

# main loop
while True:
    # read all sensors
    # map sensor values to temps
    # read user inputs

    # determine user input modes
    if F1Select == 0 and F2Select == 0:
        mode = 0
        Bubbler = 0  # turn off bubbler
        AllowO2 = 0
        AllowN2 = 0
        print("No furnaces or gasses selected.")
    elif F1Select == 1 and DrySelect == 1:
        mode = 1
        WetOrDry = 1
        print("Mode 1: Dry Oxidation in Furnace 1.")
    elif F1Select == 1 and DrySelect == 0 and WetSelect == 0:
        mode = 2
        WetOrDry = 1
        print("Mode 2: Diffusion not recommended for Furnace 1.")
    elif F1Select == 1 and WetSelect == 1:
        mode = 3
        WetOrDry = 0
        Bubbler = 1  # begin heating bubbler
        print("Mode 3: Wet Oxidation in Furnace 1")
    elif F2Select == 1 and DrySelect == 1:
        mode = 4
        WetOrDry = 1
        print("Mode 4: Oxidation (dry) not recommended for Furnace 2.")
    elif F2Select == 1 and DrySelect == 0 and WetSelect == 0:
        mode = 5
        WetOrDry = 1
        print("Mode 5: Furnace 2 diffusion selected.")
    elif F2Select == 1 and WetSelect == 1:
        mode = 6
        WetOrDry = 0
        Bubbler = 1  # begin preheating water
        print("Mode 6: Oxidation (wet) not recommended for Furnace 2.")

    # check temperatures and trigger relays
    if T1 < Threshold1 and T2 < Threshold1:
        AllowN2 = 0
        O2Relay = 0
    elif Threshold1 <= T1 < Threshold2:
        if mode == 0:
            print("Furnace 1 heating without gasses selected.")
            delay(5)
        elif 1 <= mode <= 3:
            AllowN2 = 1
            AllowO2 = 0
            FurnaceSelect = 0
        else:
            print("Furnace 1 heating but Furnace 2 selected by user.")
            delay(5)
    elif T1 > Threshold2:
        # capture oxidation time
        if T1OxiSet == 0:
            T1OxiTime = time()
            T1OxiSet = 1
        if mode == 0:
            print("Furnace 1 at temperature without gasses selected.")
            delay(5)
        elif mode == 1 or mode == 3:
            AllowN2 = 0  # turn off N2
            AllowO2 = 1  # turn on O2
        elif mode == 2:
            AllowN2 = 1
        else:
            print("Furnace 1 heating but Furnace 2 selected by user.")
            delay(5)
    elif Threshold1 <= T2 < Threshold2:
        if mode == 0:
            print("Furnace 2 heating without gasses selected.")
            delay(5)
        elif 1 <= mode <= 3:
            AllowN2 = 1
            AllowO2 = 0
            FurnaceSelect = 1
        else:
            print("Furnace 2 heating but Furnace 2 selected by user.")
            delay(5)
    elif T2 > Threshold2:
        if mode == 0:
            print("Furnace 2 at temperature without gasses selected.")
            delay(5)
        elif mode == 4 or mode == 6:
            AllowN2 = 0  # turn off N2
            AllowO2 = 1  # turn on O2
            # capture oxidation time
            if T2OxiSet == 0:
                T2OxiTime = time()
                T2OxiSet = 1
        elif mode == 5:
            AllowN2 = 1
        else:
            print("Furnace 2 heating but Furnace 1 selected by user.")
            delay(5)
    else:
        print("Error: Both furnaces are heating.")

    # check bubbler float
    if Float == 1:
        AllowH20 = 1
        delay(10)
        AllowH2O = 0

    # check for gas flow
    if AllowN2 == 1 and N2Flow == 0:
        print("Error: N2 requested but no flow detected.")
    if AllowO2 == 1 and O2Flow == 0:
        print("Error: O2 requested but no flow detected.")
    if AllowH2O == 1 and H2OFlow == 0:
        print("Error: H2O requested but no flow detected.")

    # update user display
        # plot update T1, T2
        # update user inputs
        # update systemDiagram
        # update oxidation time if T1 or T2 > Threshold2



