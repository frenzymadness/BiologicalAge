#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from libs.DicomImage import Dicom
from PIL import ImageTk


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.filename = None
        self.dicom = None

        # Control variables
        self.contrast = tk.DoubleVar()
        self.brightness = tk.DoubleVar()

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

        # Info table
        self.table = ttk.Treeview(self.master, columns=('value'))
        self.table.heading('#0', text='Key')
        self.table.heading('#1', text='Value')
        self.table.column('#0', stretch=tk.YES)
        self.table.column('#1', stretch=tk.YES)

        # Positions
        self.canvas.grid(column=1, row=1, columnspan=2, rowspan=2,
                         sticky='nswe')
        self.contrastLabel.grid(column=1, row=2, sticky='swe')
        self.contrastScale.grid(column=1, row=3, sticky='we')
        self.brightnessLabel.grid(column=2, row=2, sticky='swe')
        self.brightnessScale.grid(column=2, row=3, sticky='we')
        self.openFileBtn.grid(column=3, row=1, sticky='nw')
        self.table.grid(row=2, column=3, columnspan=2, rowspan=2,
                        sticky='nsew')
        self.statusBar.grid(column=1, row=4, columnspan=3, sticky='we')

    def openFileDialog(self):
        filetypes = [('DiCOM files', '*.dcm'),
                     ('All files', '*')]
        dialog = filedialog.Open(self.master, filetypes=filetypes)
        self.filename = dialog.show()
        self.dicom = Dicom(self.filename)
        self.drawImage(self.dicom.image)
        self.reset()
        self.fillInfoTable()
        self.setStatus('File {} opened'.format(self.filename))

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
        contrast = self.contrast.get()
        brightness = self.brightness.get()
        image = self.dicom.get_enhanced_image(contrast, brightness)
        self.drawImage(image)
        self.setStatus('Image enhanced. Contrast: {:.2f}, Brightness: {:.2f}'
                       .format(contrast, brightness))

    def setStatus(self, status):
        self.statusBar['text'] = status

    def reset(self):
        self.contrast.set(1.0)
        self.brightness.set(1.0)
        self.setStatus('')
        self.table.delete(*self.table.get_children())

    def fillInfoTable(self):
        important_data = ['DeviceSerialNumber',
                          'Manufacturer',
                          'Modality',
                          'InstitutionName',
                          'PatientName',
                          'PatientBirthDate',
                          'PatientSex',
                          'BodyPartExamined',
                          'ViewPosition',
                          ]

        for attr in important_data:
            value = getattr(self.dicom.data, attr)
            self.table.insert('', 'end', text=attr, values=(value))


def main():
    root = tk.Tk()
    root.title('Biological age of patient')
    app = MainWindow(root) # noqa
    root.mainloop()


if __name__ == '__main__':
    main()
