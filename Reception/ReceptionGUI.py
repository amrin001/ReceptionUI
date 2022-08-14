import customtkinter
import pandas as pd

from DataFrame import ReceptionConfig


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("850x520")
        self.title("Reception: Guest Lists")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.inner_frame = customtkinter.CTkFrame(master=self)
        self.inner_frame.pack()
        self.inner_frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=(20, 0), columnspan=3)

        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        # self.header = customtkinter.CTkLabel(master=self, text="GUEST LIST")
        # self.header.grid(row=0, column=2, padx=20, pady=20, sticky="ew")

        # first row - Search function to find the name of the guests
        self.name_label = customtkinter.CTkLabel(master=self.inner_frame, text="Guest Name: ")
        self.name_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.name_entry = customtkinter.CTkEntry(master=self.inner_frame, width=350)
        self.name_entry.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.search_button = customtkinter.CTkButton(master=self.inner_frame, width=100,
                                                     command=self.search_button_callback, text="Search")
        self.search_button.grid(row=0, column=2, padx=20, pady=20, sticky="ew")

        # second row - display the name, table number and attendance
        self.textbox = customtkinter.CTkTextbox(master=self.inner_frame)
        self.textbox.grid(row=1, column=1, padx=20, pady=(20, 0), sticky="nsew")
        self.clear_button = customtkinter.CTkButton(master=self.inner_frame, text="Clear",
                                                    command=self.clear_button_callback, width=5)
        self.clear_button.grid(row=1, column=2, padx=20, pady=20, sticky="ew")

        # Third row - Update the attendance and clear the text box
        self.update_label = customtkinter.CTkLabel(master=self.inner_frame, text="Attendance: ")
        self.update_label.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.update_attendance = customtkinter.CTkComboBox(master=self.inner_frame, values=["1", "0"])
        self.update_attendance.grid(row=2, column=1, padx=20, pady=20, sticky="ew")
        self.update_button = customtkinter.CTkButton(master=self.inner_frame,
                                                     command=self.update_button_callback, text="Update")
        self.update_button.grid(row=2, column=2, padx=20, pady=20, sticky="ew")

        # fourth row - Confirmation of the changes being made
        self.update_confirmation = customtkinter.CTkLabel(master=self.inner_frame, text="")
        self.update_confirmation.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

        # fifth row - Exit the application
        self.exit_button = customtkinter.CTkButton(master=self, text="Exit", command=self.exit_button_callback, width=5)
        self.exit_button.grid(row=3, column=2, padx=20, pady=20, sticky="ew")
        # settings_image = tkinter.PhotoImage(file='./images/settings-icon.png', height=50, width=50)
        self.setting_button = customtkinter.CTkButton(master=self, text="Settings",
                                                      width=5, command=self.setting_button_callback)
        self.setting_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        self.temp_df = pd.DataFrame()

    def get_guest(self):
        text = self.name_entry.get()
        display_table = ReceptionConfig.get_namelist()[["Names", "Tables", "Present"]].where(
            ReceptionConfig.get_namelist()["Names"].str.contains(str(text.title())))
        searched_name = display_table.dropna()
        return searched_name

    def search_button_callback(self):
        self.textbox.insert("insert", self.get_guest().to_string(header=False) + "\n")
        self.temp_df = self.temp_df.append(self.get_guest())
        print(self.temp_df)
        self.name_entry.delete(0, 'end')

    def update_button_callback(self):
        self.temp_df["Present"] = int(self.update_attendance.get())
        print(self.temp_df)
        ReceptionConfig.get_namelist().update(self.temp_df)
        source = ReceptionConfig.ReceptionConfig.usr_input.title()
        selected_wks = ReceptionConfig.update_table_number().get_worksheet(ReceptionConfig.wks_data().get(source))
        selected_wks.delete_rows(2, 100)
        selected_wks.append_rows(ReceptionConfig.get_namelist().values.tolist())
        self.update_confirmation.configure(text="The record have been updated!")
        self.clear_dataframe()
        self.textbox.textbox.delete('1.0', 'end')

    def exit_button_callback(self):
        self.destroy()

    def clear_button_callback(self):
        self.textbox.textbox.delete('1.0', 'end')
        self.clear_dataframe()
        print("Textbox has been cleared.")

    def clear_dataframe(self):
        self.temp_df.drop(self.temp_df.index, inplace=True)

    def setting_button_callback(self):
        return "Settings"
