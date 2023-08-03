import tkinter as tk
import customtkinter as ct
from ImageSlideshow import ImageSlideshow
from TimePicker import TimePicker
import datetime

from Timer import Timer


class Launcher(ct.CTk):
    start_button: ct.CTkButton
    current_timer: datetime.datetime
    time_picker: TimePicker = None
    timer: Timer = None
    image_slideshow: ImageSlideshow = None

    def __init__(self):
        super().__init__()
        ct.set_appearance_mode("dark")
        self.title("Time Selector")
        self.geometry(f"200x50+{int(self.winfo_screenwidth() / 2)}+{int(self.winfo_screenheight() / 2)}")

        self.hour_var = tk.IntVar()
        self.minute_var = tk.IntVar()

        self.display_menu()

    def handle_timer_end(self):
        if self.image_slideshow:
            self.image_slideshow.destroy()

    def start_timer(self):
        self.timer = Timer(self, self.current_timer, self.handle_timer_end)
        self.image_slideshow = ImageSlideshow(self)

    def set_current_timer(self, target_time: datetime.datetime):
        self.current_timer = target_time
        self.time_picker.window.destroy()
        self.start_timer()

    def start_countdown(self):
        self.time_picker = TimePicker(self, self.set_current_timer)

    def display_menu(self):
        self.start_button = ct.CTkButton(self, text="Start Countdown", command=self.start_countdown)
        self.start_button.pack()


if __name__ == '__main__':
    launcher = Launcher()
    launcher.mainloop()
