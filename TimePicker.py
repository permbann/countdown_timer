import tkinter as tk
from typing import Callable
from tktimepicker import AnalogPicker, AnalogThemes, constants
import customtkinter as ct
import datetime


class TimePicker:
    time_picker: AnalogPicker
    confirm_button: ct.CTkButton
    update_function: Callable

    def __init__(self, root, on_time_change: Callable):
        self.update_function = on_time_change
        self.window = ct.CTkToplevel(root)
        self.window.geometry(f"+{int(self.window.winfo_screenwidth() / 2)}+{int(self.window.winfo_screenheight() / 2 + 50)}")
        self.setup_picker()
        self.setup_confirm_button()

    def setup_picker(self):
        self.time_picker = AnalogPicker(self.window, type=constants.HOURS24)
        theme = AnalogThemes(self.time_picker)
        theme.setDracula()
        self.time_picker.pack(expand=True, fill="both")

    def handle_update(self):
        time = self.time_picker.time()
        self.update_function(TimePicker.tuple_to_timestamp((time[0], time[1])))

    def setup_confirm_button(self):
        self.confirm_button = ct.CTkButton(self.window, text="Confirm Timer",
                                           command=self.handle_update)
        self.confirm_button.pack()

    @staticmethod
    def tuple_to_timestamp(hours_minutes_tuple):
        current_date = datetime.date.today()
        hours, minutes = hours_minutes_tuple
        timestamp = datetime.datetime.combine(current_date, datetime.time(hours, minutes))
        return timestamp


if __name__ == '__main__':
    root = ct.CTk()


    def set_time(time):
        print(time)


    TimePicker(root, set_time)

    root.mainloop()
