import os
import tkinter
from tkinter import Tk, filedialog, Button, Scale, HORIZONTAL, messagebox
from PIL import Image
import ctypes


class Error(Exception):
    """Base class for other exceptions"""
    pass


class wrongMargin(Error):
    """Raised when the input margin is smaller than the left percentage"""
    pass
class ImageCutter(object):
    def __init__(self):
        self.stop = False
        self.percentage = 100
        self.percentageR = None
        self.margeL = None

    def split(self, imgPath):
        img = Image.open(imgPath)
        w, h = img.size
        try:
            if self.percentageR.get() > self.margeL.get():
                raise wrongMargin
            else:
                imgA = img.crop((0, 0, w * (self.percentageR.get() / 100), h))
                imgB = img.crop((w * self.percentageR.get() / 100, 0, w * self.margeL.get() / 100, h))
                return imgA, imgB
        except wrongMargin:
            messagebox.showerror(":c error", "marge must be bigger than percentage")


    def stop_program(self):
        self.stop = True
        ctypes.windll.user32.MessageBoxW(0, "Programa Detenido", "Programa Detenido", 0)

    def select_directory(self):
        self.stop = False
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.process_images(directory_path)

    def process_images(self, directory):
        splitted_directory = os.path.join(directory, "splitted_images")
        os.makedirs(splitted_directory, exist_ok=True)

        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) and not self.stop:
                img_path = os.path.join(directory, filename)
                imgA, imgB = self.split(img_path)
                base_filename = os.path.splitext(filename)[0]
                imgA.save(os.path.join(splitted_directory, f"{base_filename}_A.png"))
                imgB.save(os.path.join(splitted_directory, f"{base_filename}_B.png"))

    def createWindow(self):
        root = Tk()
        root.title("Image cutter")

        select_button = Button(root, text="Select directory to cut images from", command=self.select_directory)
        select_button.pack(pady=20)

        Tp = tkinter.Text(root, height=1, width=40)
        Tp.insert(tkinter.END, "Percentage of image cut from the right")
        Tp.config(state='disabled')
        Tp.pack(pady=21)

        self.percentageR = Scale(root, from_=0, to=self.percentage, orient=HORIZONTAL)
        self.percentageR.pack(pady=22)

        Tmarge = tkinter.Text(root, height=1, width=11)
        Tmarge.insert(tkinter.END, "Right marge")
        Tmarge.config(state='disabled')
        Tmarge.pack(pady=23)

        self.margeL = Scale(root, from_=self.percentage, to=0, orient=HORIZONTAL)
        self.margeL.set(100)
        self.margeL.pack(pady=24)

        stop_button = Button(root, text="Parar acción", command=self.stop_program)
        stop_button.pack(pady=25)

        root.mainloop()


def run():
    # GUI setup
    cutter = ImageCutter()
    cutter.createWindow()


if __name__ == "__main__":
    run()
