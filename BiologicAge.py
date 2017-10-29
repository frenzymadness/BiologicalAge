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

        # Widgets
        self.openFileBtn = ttk.Button(self.master, text="Open file",
                                      command=self.openFileDialog)
        self.statusBar = ttk.Label(self.master, relief=tk.SUNKEN,
                                   anchor="w", text='Biological age app')
        self.canvas = tk.Canvas(self.master, width=1024, height=768)

        # Positions
        self.canvas.grid(column=1, row=1)
        self.openFileBtn.grid(column=2, row=1, sticky='n')
        self.statusBar.grid(column=1, row=2, columnspan=2, sticky='we')

    def openFileDialog(self):
        filetypes = [('DiCOM files', '*.dcm'),
                     ('All files', '*')]
        dialog = filedialog.Open(self.master, filetypes=filetypes)
        self.filename = dialog.show()
        self.file = DicomImage(self.filename)
        self.drawImage()
        self.statusBar['text'] = 'File {} opened'.format(self.filename)

    def drawImage(self):
        # Canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        # Convert, resize and draw in canvas
        self.image = self.file.image.convert('L')
        self.image.thumbnail((canvas_width, canvas_height))
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image((canvas_width / 2, canvas_height / 2),
                                 image=self.image)


def main():
    root = tk.Tk()
    root.title('Biological age of patient')
    app = MainWindow(root) # noqa
    root.mainloop()


if __name__ == '__main__':
    main()
