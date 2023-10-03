import tkinter as tk
import customtkinter as ct
from ImageSlideshow import ImageSlideshow
from TimePicker import TimePicker
import datetime
from tkinter import filedialog
from functools import partial

from Timer import Timer


class Launcher(ct.CTk):
    start_button1: ct.CTkButton
    start_button2: ct.CTkButton
    current_timer: datetime.datetime
    time_picker: TimePicker = None
    timer: Timer = None
    image_slideshow: ImageSlideshow = None
    displayed_images: list[str]

    def __init__(self):
        super().__init__()
        ct.set_appearance_mode("dark")
        self.title("Time Selector")
        self.geometry(f"300x80+{int(self.winfo_screenwidth() / 2)}+{int(self.winfo_screenheight() / 2)}")

        self.hour_var = tk.IntVar()
        self.minute_var = tk.IntVar()

        self.display_menu()

    def handle_timer_end(self):
        if self.image_slideshow:
            self.image_slideshow.destroy()

    def start_timer(self):
        self.timer = Timer(self, self.current_timer, self.handle_timer_end)
        self.image_slideshow = ImageSlideshow(self, self.displayed_images)

    def set_current_timer(self, target_time: datetime.datetime):
        self.current_timer = target_time
        self.time_picker.window.destroy()
        self.start_timer()

    def start_countdown(self, open_image_picker: bool):
        if open_image_picker:
            self.displayed_images = list(filedialog.askopenfilenames(
                title="Select PNG files",
                filetypes=(("PNG files", "*.png"), ("All files", "*.*")),
                initialdir="images"
            ))
        else:
            self.displayed_images = ImageSlideshow.get_file_paths("images")
        self.time_picker = TimePicker(self, self.set_current_timer)

    def display_menu(self):
        self.start_button1 = ct.CTkButton(self, text="Start Countdown (with images dir)",
                                          command=partial(self.start_countdown, False), )
        # self.start_button1.pack()
        self.start_button2 = ct.CTkButton(self, text="Start Countdown (pick images)",
                                          command=partial(self.start_countdown, True))
        # self.start_button2.pack()
        self.start_button1.grid(row=0, column=0, padx=(5, 2.5), pady=5, sticky="ew")
        self.start_button2.grid(row=1, column=0, padx=(2.5, 5), pady=5, sticky="ew")

        self.columnconfigure(0, weight=1)


if __name__ == '__main__':
    launcher = Launcher()
    launcher.mainloop()
