#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.file = None

        # Widgets
        self.openFileBtn = ttk.Button(self.master, text="Open file",
                                      command=self.openFileDialog)
        self.statusBar = ttk.Label(self.master, relief=tk.SUNKEN,
                                   anchor="w", text='Biological age app')
        self.canvas = tk.Canvas(self.master, width=512, height=512)
        self.canvas.create_text(256, 256, text="Open file first",
                                anchor='center')

        # Positions
        self.canvas.grid(column=1, row=1)
        self.openFileBtn.grid(column=2, row=1, sticky='n')
        self.statusBar.grid(column=1, row=2, columnspan=2, sticky='we')

    def openFileDialog(self):
        filetypes = [('DiCOM files', '*.dcm'),
                     ('All files', '*')]
        dialog = filedialog.Open(self.master, filetypes=filetypes)
        self.file = dialog.show()
        print('Opening', self.file)
        self.statusBar['text'] = 'File {} opened'.format(self.file)


def main():
    root = tk.Tk()
    app = MainWindow(root) # noqa
    root.mainloop()


if __name__ == '__main__':
    main()
