import gspread
import pandas as pd


class ReceptionConfig:
    sa = gspread.service_account()
    sh = sa.open("Guest List")

    wks_data = {"Sample": 0, "Amrin": 2, "Hannah": 3}

    print("Who's guest list will you be referring from?")
    # print(wks_data.keys())
    usr_input = input()
    wks_num = 0
    if usr_input.title() in wks_data.keys():
        wks_num = wks_data.get(usr_input.title())
    else:
        exit(1)

    wks = sh.get_worksheet(wks_num)
    display_names = wks.get_all_records()

    records_df = pd.DataFrame.from_dict(display_names)
    records_df.index += 1


def get_namelist():
    return ReceptionConfig.records_df


def update_table_number():
    return ReceptionConfig.sh


def app_settings(input_key):
    return ReceptionConfig.wks_data[input_key]


def wks_data():
    return ReceptionConfig.wks_data
