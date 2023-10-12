import os
import tkinter as tk
from PIL import Image, ImageTk


class ImageSlideshow(tk.Toplevel):
    def __init__(self, root, image_paths):
        super().__init__(root)
        self.attributes('-fullscreen', True)

        self.image_paths = image_paths  # ImageSlideshow.get_file_paths("images")
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

    @staticmethod
    def resize_image_with_fixed_ratio(image: Image, target_dimension: tuple[int, int]) -> Image:
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height

        target_width = min(target_dimension[0], target_dimension[1] * aspect_ratio)
        target_height = min(target_dimension[1], target_dimension[0] / aspect_ratio)

        new_image = Image.new("RGB", (target_dimension[0], target_dimension[1]), "#a4a4a4")

        left = int((target_dimension[0] - target_width) // 2)
        top = int((target_dimension[1] - target_height) // 2)
        right = int(left + target_width)
        bottom = int(top + target_height)

        resized_image = image.resize((int(target_width), int(target_height)), Image.ANTIALIAS)
        new_image.paste(resized_image, (left, top, right, bottom))
        return new_image

    def load_images(self):
        if 0 <= self.current_image_index < len(self.image_paths):
            current_image_path = self.image_paths[self.current_image_index]
            next_image_index = (self.current_image_index + 1) % len(self.image_paths)
            next_image_path = self.image_paths[next_image_index]

            self.current_image = ImageSlideshow.resize_image_with_fixed_ratio(Image.open(current_image_path), (
                self.winfo_screenwidth(), self.winfo_screenheight()))
            self.next_image = ImageSlideshow.resize_image_with_fixed_ratio(Image.open(next_image_path), (
                self.winfo_screenwidth(), self.winfo_screenheight()))

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
    display = ImageSlideshow(root, ["images/Screenshot_20230226_002333.png", "images/yt_profile.png"])
    root.mainloop()
