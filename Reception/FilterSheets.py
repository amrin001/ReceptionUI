import gspread
import pandas as pd

sa = gspread.service_account()
sh = sa.open("Sample Names")

wks = sh.get_worksheet(0)
display_names = wks.get_all_records()

records_df = pd.DataFrame.from_dict(display_names)
records_df.index += 1
# print(records_df)
#
while True:
    print("\nPlease enter name here: ")
    name = input()
    if name.casefold() == "exit" or name == "":
        break
    display_table = records_df[["Names", "Tables", "Present"]].where(records_df["Names"].str.contains(str(name.title())))
    print(display_table.dropna())
    print("\nUpdate Present column?")
    update_attendance = input()
    if update_attendance.lower() in ["n", "no"]:
        continue
    elif update_attendance.lower() in ["y", "yes"]:
        display_table["Present"] = 1
        print(display_table.dropna())
        records_df.update(display_table.dropna())
        # print(records_df)
        sh.get_worksheet(1).update(records_df.values.tolist())
