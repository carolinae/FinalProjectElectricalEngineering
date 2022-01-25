# hello_psg.py

import PySimpleGUI as sg

from dss_profile_solver import CIRCUIT_PROFILE_IEEE123, CIRCUIT_PROFILE_CK5, run
from functions import add_samplings_according_users_decision, EXAMINE_EVERY_30_MINUTES, EXAMINE_EVERY_HOUR, \
    EXAMINE_EVERY_15_MINUTES, create_powers_input_P_and_Q_according_users_decesion
from initial_data_vector_normalized import RESIDENTIAL, \
    YEARLY_COMMERCIAL_PROFILE, YEARLY_APPARTMENTS_PROFILE, YEARLY_COMMERCIAL_APPARTMENTS_PROFILE


circuit_types = {
    'IEEE123': CIRCUIT_PROFILE_IEEE123,
    'ckt5': CIRCUIT_PROFILE_CK5
}

profiles = {
    'apartments': YEARLY_APPARTMENTS_PROFILE, 'commercial': YEARLY_COMMERCIAL_PROFILE,
    'commercial combined with apartments': YEARLY_COMMERCIAL_APPARTMENTS_PROFILE,
    'residential': RESIDENTIAL,
}

examinations_periods = {"Examine every hour": EXAMINE_EVERY_HOUR, "Examine every 30 minutes": EXAMINE_EVERY_30_MINUTES,
                        "Examine every 15 minutes": EXAMINE_EVERY_15_MINUTES}

include_caps_dict = {'True_Value': 1, 'False_value': 0}

load_model_dict = {'1_model': [".model=1", ".Vminpu=0.2", ".Vmaxpu=1.2"],
                   '2_model': [".model=2", ".Vlowpu=0.5", ".Vminpu=0.95"],
                   '3_model': [".model=3", ".pvfactor=0.1"],
                   '4_model': [".model=4", ".CVRwatts=0.8", ".CVRvars=2.0"],
                   '5_model': [".model=5", ""],
                   '6_model': [".model=6", ".Xd=1.0"],
                   '7_model': [".model=7", ".Balanced=No"],
                   '8_model': [".model=8", "Vminpu=0.8", {'ZIPV': [0.5, 0, 0.5, 1, 0, 0, 0.93]}]}

layout = [[sg.Text("Choose circuit profile")],
          [sg.Combo(['IEEE123', 'ckt5'], key='circuit_type')],
          [sg.Text('Please choose PU value of the circuit:')],
          [sg.Input(key='PU_Value')],
          [sg.Text("Choose Load model")],
          [sg.Combo(['1', '2', '3', '4', '5', '6', '7', '8'],
                    key='Load_Model', enable_events=True)],

          # Model = 1
          [sg.Text('Vminpu:', key='Vminpu_txt_model1', visible=False)],
          [sg.Input(key='Vminpu_model1', visible=False, default_text='0.2')],
          [sg.Text('Vmaxpu:', key='Vmaxpu_txt', visible=False)],
          [sg.Input(key='Vmaxpu', visible=False, default_text='1.2')],

          # Model = 2
          [sg.Text('Vlowpu:', key='Vlowpu_txt', visible=False)],
          [sg.Input(key='Vlowpu', visible=False, default_text='0.5')],
          [sg.Text('Vminpu:', key='Vminpu_txt_model2', visible=False)],
          [sg.Input(key='Vminpu_model2', visible=False, default_text='0.95')],

          # Model = 3
          [sg.Text('Pvfactor:', key='Pvfactor_txt', visible=False)],
          [sg.Input(key='Pvfactor', visible=False, default_text='0.1')],
          # [sg.Text('Maxkvar:', key='Maxkvar_txt', visible=False)],
          # [sg.Input(key='Maxkvar', visible=False, default_text='0.1')],
          # [sg.Text('Minkvar:', key='Minkvar_txt', visible=False)],
          # [sg.Input(key='Minkvar', visible=False, default_text='0.1')],

          # Model = 4
          [sg.Text('CVRwatts:', key='CVRwatts_txt', visible=False)],
          [sg.Input(key='CVRwatts', visible=False, default_text='0.8')],
          [sg.Text('CVRvars:', key='CVRvars_txt', visible=False)],
          [sg.Input(key='CVRvars', visible=False, default_text='2.0')],

          # # Model = 5
          # [sg.Text('Vminpu:', key='Vminpu_txt', visible=False)],
          # [sg.Input(key='Vminpu', visible=False, default_text='0.2')],
          # [sg.Text('Vmaxpu:', key='Vmaxpu_txt', visible=False)],
          # [sg.Input(key='Vmaxpu', visible=False, default_text='1.2')],

          # # Model = 6
          # [sg.Text('xd:', key='Xd_txt', visible=False)],
          # [sg.Input(key='Xd', visible=False, default_text='1.0')],
          #
          # # Model = 7
          # [sg.Text('Balanced:', key='Balanced_txt', visible=False)],
          # [sg.Input(key='Balanced', visible=False, default_text='No')],

          # Model = 8
          [sg.Text('Vminpu:', key='Vminpu_txt_model8', visible=False)],
          [sg.Input(key='Vminpu_model8', visible=False, default_text='0.8')],
          [sg.Text('Please insert 7 numbers of ZIPV:', key='ZIPV_instructions', visible=False)],
          [sg.Input(key='ZIPV', visible=False, default_text='(0.5, 0, 0.5, 1, 0, 0, 0.93)')],

          [sg.Text("Do you want to include capacitors in your data calculations?")],
          [sg.Combo(['True_Value', 'False_value'], key='include_caps')],
          [sg.Text("Choose profile data")],
          [sg.Combo(['apartments', 'commercial', 'commercial combined with apartments', 'residential'], key='profile')],
          [sg.Text("Choose examinations period")],
          [sg.Combo(['Examine every hour', 'Examine every 30 minutes', 'Examine every 15 minutes'],
                    key='examination_period')], [sg.Button("Create samples")]
          ]

window = sg.Window("Demo", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == 'Load_Model':
        window['Load_Model'].update(disabled=True)
        if values['Load_Model'] == '1':
            window['Vminpu_model1'].update(visible=True)
            window['Vminpu_txt_model1'].update(visible=True)
            window['Vmaxpu'].update(visible=True)
            window['Vmaxpu_txt'].update(visible=True)

        if values['Load_Model'] == '2':
            window['Vlowpu'].update(visible=True)
            window['Vlowpu_txt'].update(visible=True)
            window['Vminpu_model2'].update(visible=True)
            window['Vminpu_txt_model2'].update(visible=True)

        if values['Load_Model'] == '3':
            window['Pvfactor'].update(visible=True)
            window['Pvfactor_txt'].update(visible=True)

        if values['Load_Model'] == '4':
            window['CVRwatts'].update(visible=True)
            window['CVRwatts_txt'].update(visible=True)
            window['CVRvars'].update(visible=True)
            window['CVRvars_txt'].update(visible=True)

        # if values['Load_Model'] == '5_model':
        #     window['Vminpu'].update(visible=True)
        #     window['Vminpu_txt'].update(visible=True)
        #     window['Vmaxpu'].update(visible=True)
        #     window['Vmaxpu_txt'].update(visible=True)

        # if values['Load_Model'] == '6':
        #     window['Xd'].update(visible=True)
        #     window['Xd_txt'].update(visible=True)
        #
        # if values['Load_Model'] == '7':
        #     window['Balanced'].update(visible=True)
        #     window['Balanced_txt'].update(visible=True)

        if values['Load_Model'] == '8':
            window['Vminpu_model8'].update(visible=True)
            window['Vminpu_txt_model8'].update(visible=True)
            window['ZIPV'].update(visible=True)
            window['ZIPV_instructions'].update(visible=True)

    if event == "Create samples":
        circuit_type = values['circuit_type']
        examination_period = values['examination_period']
        profile = values['profile']
        include_caps = values['include_caps']
        pu_value = values['PU_Value']
        load_model = values['Load_Model']
        model_inputs = {
            # model = 1
            'Vminpu_model1': values['Vminpu_model1'],
            'Vmaxpu': values['Vmaxpu'],

            # model = 2
            'Vlowpu': values['Vlowpu'],
            'Vminpu_model2': values['Vminpu_model2'],

            # model = 3
            'Pvfactor': values['Pvfactor'],

            # model = 4
            'CVRwatts': values['CVRwatts'],
            'CVRvars': values['CVRvars'],

            # # model = 5
            # 'Vminpu_model1': values['Vminpu_model1'],
            # 'Vmaxpu': values['Vmaxpu'],

            # # model = 6
            # 'Xd': values['Xd'],
            #
            # # model = 7
            # 'Balanced': values['Balanced'],

            # model = 8
            'Vminpu_model8': values['Vminpu_model8'],
            'ZIPV': values['ZIPV']
        }

        selected_include_caps = include_caps_dict[include_caps]
        selected_circuit_type = circuit_types[circuit_type]
        selected_examination_period = examinations_periods[examination_period]
        selected_profile = profiles[profile]

        samples_according_users_decision = add_samplings_according_users_decision(selected_profile,
                                                                                  selected_examination_period)
        create_powers_input_P_and_Q_according_users_decesion(selected_examination_period,
                                                             samples_according_users_decision, selected_circuit_type)
        sg.popup("Successfully created csv files!!! ")
        run(selected_circuit_type, selected_examination_period, selected_include_caps, pu_value, load_model, model_inputs)
        sg.popup("Successfully solved profile!!! ")
        exit(0)

window.close()
