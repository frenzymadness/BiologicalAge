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

        # Positions
        self.openFileBtn.grid(column=1, row=1)
        self.statusBar.grid(column=1, row=2)

    def openFileDialog(self):
        filetypes = [('DiCOM files', '*.dcm'),
                     ('All files', '*')]
        dialog = filedialog.Open(self.master, filetypes=filetypes)
        self.file = dialog.show()
        print('Opening', self.file)


def main():
    root = tk.Tk()
    app = MainWindow(root) # noqa
    root.mainloop()


if __name__ == '__main__':
    main()
