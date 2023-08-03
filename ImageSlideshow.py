import os
import tkinter as tk
from PIL import Image, ImageTk


class ImageSlideshow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.attributes('-fullscreen', True)

        self.image_paths = ImageSlideshow.get_file_paths("images")
        self.current_image_index = 0

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.current_image = None
        self.next_image = None
        self.blended_image = None
        self.blended_photo = None

        self.load_images()
        self.fade_in_next_image()
        self.bind("<Escape>", self.quit_slideshow)

    @staticmethod
    def get_file_paths(folder_path):
        file_paths = []

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        return file_paths

    def load_images(self):
        if 0 <= self.current_image_index < len(self.image_paths):
            current_image_path = self.image_paths[self.current_image_index]
            next_image_index = (self.current_image_index + 1) % len(self.image_paths)
            next_image_path = self.image_paths[next_image_index]

            self.current_image = Image.open(current_image_path).resize(
                (self.winfo_screenwidth(), self.winfo_screenheight()))
            self.next_image = Image.open(next_image_path).resize((self.winfo_screenwidth(), self.winfo_screenheight()))

    def fade_in_next_image(self, alpha=0):
        self.blended_image = Image.blend(self.current_image, self.next_image, alpha)
        self.blended_photo = ImageTk.PhotoImage(self.blended_image)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.blended_photo)

        if alpha < 1:
            self.after(20, self.fade_in_next_image, alpha + 0.01)
        else:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.current_image = self.next_image
            self.load_images()
            self.after(10000, self.fade_in_next_image)

    def quit_slideshow(self):
        self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    display = ImageSlideshow(root)
    root.mainloop()
