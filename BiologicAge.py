#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from libs.DicomImage import DicomImage
from PIL import ImageTk


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.filename = None
        self.file = None

        # Control variables
        self.contrast = tk.DoubleVar()
        self.contrast.set(1.0)
        self.brightness = tk.DoubleVar()
        self.brightness.set(1.0)

        # Widgets
        self.openFileBtn = ttk.Button(self.master, text="Open file",
                                      command=self.openFileDialog)
        self.statusBar = ttk.Label(self.master, relief=tk.SUNKEN,
                                   anchor="w", text='Biological age app')
        self.canvas = tk.Canvas(self.master, width=1024, height=768)
        self.contrastScale = ttk.Scale(self.master, from_=0, to=10.0,
                                       orient=tk.HORIZONTAL,
                                       variable=self.contrast,
                                       command=self.enhanceImage)
        self.contrastLabel = ttk.Label(self.master, text='Contrast level')
        self.brightnessScale = ttk.Scale(self.master, from_=0, to=10.0,
                                         orient=tk.HORIZONTAL,
                                         variable=self.brightness,
                                         command=self.enhanceImage)
        self.brightnessLabel = ttk.Label(self.master, text='Brightness level')

        # Positions
        self.canvas.grid(column=1, row=1, columnspan=2)
        self.contrastLabel.grid(column=1, row=2, sticky='we')
        self.contrastScale.grid(column=1, row=3, sticky='we')
        self.brightnessLabel.grid(column=2, row=2, sticky='we')
        self.brightnessScale.grid(column=2, row=3, sticky='we')
        self.openFileBtn.grid(column=3, row=1, sticky='n')
        self.statusBar.grid(column=1, row=4, columnspan=3, sticky='we')

    def openFileDialog(self):
        filetypes = [('DiCOM files', '*.dcm'),
                     ('All files', '*')]
        dialog = filedialog.Open(self.master, filetypes=filetypes)
        self.filename = dialog.show()
        self.file = DicomImage(self.filename)
        self.drawImage(self.file.image)
        self.statusBar['text'] = 'File {} opened'.format(self.filename)

    def drawImage(self, image):
        # Canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        # Convert, resize and draw in canvas
        image.thumbnail((canvas_width, canvas_height))
        self.image = ImageTk.PhotoImage(image)
        self.canvas.create_image((canvas_width / 2, canvas_height / 2),
                                 image=self.image)

    def enhanceImage(self, event):
        image = self.file.get_enhanced_image(self.contrast.get(),
                                             self.brightness.get())
        self.drawImage(image)


def main():
    root = tk.Tk()
    root.title('Biological age of patient')
    app = MainWindow(root) # noqa
    root.mainloop()


if __name__ == '__main__':
    main()
