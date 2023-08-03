from typing import Callable

import customtkinter as ct
import datetime

main_color = "#0074D9"
secondary_color = "#B10DC9"
transparent_color = "red"


class Timer(ct.CTkToplevel):

    def __init__(self, root, target_time: datetime.datetime, on_timer_end: Callable):
        super().__init__(root)
        # self = ct.CTkToplevel(root)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.attributes("-alpha", 1)
        self.wm_attributes("-transparentcolor", transparent_color)
        self.target_time = target_time
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}+0+0")
        self.canvas = ct.CTkCanvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.on_timer_end = on_timer_end
        self.text = None

        self.start_countdown()
        # self.bind("<Escape>", self.quit_timer)

    def center_text(self, text):
        self.text = self.canvas.create_text(int(self.width / 2), int(self.height / 2), text=text,
                                            font=("fixedsys", 80), tags="text", justify="center", fill=main_color)

    def draw_progress_bar(self, percentage):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=transparent_color, tags="bg")
        radius = 400
        x = int(self.width / 2)
        y = int(self.height / 2)
        start_angle = 0
        end_angle = start_angle + (percentage * 360 / 100)

        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=main_color, width=2, tags="progress"
        )

        self.canvas.create_arc(
            x - radius, y - radius, x + radius, y + radius,
            start=start_angle, extent=-end_angle,
            fill=secondary_color, width=2, tags="progress"
        )
        inner_radius = radius - 40

        self.canvas.create_oval(
            x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius,
            fill=transparent_color, stipple="gray12", tags="inner"
        )

    def update_progress(self, start_time, selected_timestamp):
        current_timestamp = datetime.datetime.now()
        elapsed_time = current_timestamp - start_time
        total_time = selected_timestamp - start_time

        if elapsed_time <= total_time:
            elapsed_percentage = (elapsed_time / total_time) * 100
            self.draw_progress_bar(elapsed_percentage)
            self.center_text(f"Continuing at:\n{selected_timestamp.strftime('%H:%M')}")
            self.after(10, self.update_progress, start_time, selected_timestamp)
        else:
            self.on_timer_end()
            self.destroy()

    @staticmethod
    def calculate_time_difference(target_time: tuple[int, int]):
        current_time = datetime.datetime.now()

        target_hour, target_minute = target_time
        target_datetime = current_time.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

        time_difference = target_datetime - current_time

        return time_difference

    def start_countdown(self):
        current_time = datetime.datetime.now()
        self.update_progress(current_time, self.target_time)

    def quit_timer(self, _):
        self.destroy()


if __name__ == '__main__':
    def get_datetime_plus_one_minute():
        current_datetime = datetime.datetime.now()
        one_minute = datetime.timedelta(minutes=1)
        new_datetime = current_datetime + one_minute
        return new_datetime


    root = ct.CTk()
    Timer(root, get_datetime_plus_one_minute(), lambda: print("ended"))
    root.mainloop()
