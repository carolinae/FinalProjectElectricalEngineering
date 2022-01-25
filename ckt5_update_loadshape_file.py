def update_loadshape_ckt5_file():
    OUTPUT_FILE = 'C:/ck5/Loadshapes_ckt5.dss'
    numOfLoads = 1379
    with open(OUTPUT_FILE, 'w') as f:
        for i in range(1, numOfLoads + 1, 1):
            f.write('New LoadShape.LS' + str(i) + ' npts=8760 interval=1.0 Pmult=(File=LS' + str(
                i) + '.csv) Qmult=(File=LS_Q' + str(i) + '.csv)' + '\n')


    # create loads file:ffa
    load_count = 0
    with open(r'C:\OpenDSS\EPRITestCircuits\ckt5\Loads_ckt5.dss') as f:
        with open('C:/ck5/Loads_ckt5.dss', 'w') as f_out:
            raw_file_lines = f.readlines()
            for i in range(0, len(raw_file_lines), 1):
                if raw_file_lines[i].find('Residential') != -1 or raw_file_lines[i].find('Commercial_SM') != -1 or \
                        raw_file_lines[i].find('Commercial_MD') != -1:
                    load_count = load_count + 1
                raw_file_lines[i] = raw_file_lines[i].replace('Residential', 'LS' + str(load_count))
                raw_file_lines[i] = raw_file_lines[i].replace('Commercial_SM', 'LS' + str(load_count))
                raw_file_lines[i] = raw_file_lines[i].replace('Commercial_MD', 'LS' + str(load_count))
                f_out.write(raw_file_lines[i])

