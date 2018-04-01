#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic, QtGui
from os import listdir
from os.path import isfile, join
from collections import OrderedDict


class MainWindow():
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QMainWindow()
        with open('mainwindow.ui') as f:
            uic.loadUi(f, self.window)

        # Clear
        self.window.refList.clear()

        # Connections
        self.window.sexCombo.currentIndexChanged[int].connect(
            self.load_ref_img_list
        )
        self.window.refList.currentItemChanged.connect(self.open_ref_image)
        self.window.openFileButton.clicked.connect(self.open_rtg_image)

    def load_ref_img_list(self):
        # 0 -> Boy, 1 -> Girl
        index = self.window.sexCombo.currentIndex()
        # Create path to folder with RTGs
        folder = 'B' if index == 0 else 'G'
        path = join('images', 'RTG', folder)
        # List, everything, extract files and sort them
        all = listdir(path)
        files = [name for name in all if isfile(join(path, name))]
        sorted_files = sorted(files,
                              key=lambda n: [int(x) for x in n.split('_')[:2]])
        # Create dictionary with files and paths and insert item to the list
        self.window.refList.clear()
        self.ref_images = OrderedDict()
        for name in sorted_files:
            filename = name
            y, m = name.split('_')[:2]
            y, m = int(y), int(m)
            name = '{} years {} months'.format(y, m)
            self.ref_images[name] = join(path, filename)
            self.window.refList.addItem(name)

    def _load_image(self, filename, widget):
        image = QtGui.QPixmap(filename)
        image = image.scaledToWidth(widget.width())
        widget.setPixmap(image)

    def open_ref_image(self):
        item = self.window.refList.currentItem()
        if item is None:
            return
        name = item.text()
        filename = self.ref_images[name]
        self._load_image(filename, self.window.refImgLabel)

    def open_rtg_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window, "Open RTG file", "",
            "Images (*.png *.PNG *.jpg *.jpeg *.JPG);;All Files (*);;")
        if filename is None:
            return
        self._load_image(filename, self.window.rtgImgLabel)

    def toggle_question_input(self, type='number', enabled=True):
        if type == 'number':
            widgets_names = ['numberQuestionLabel', 'numberQuestionCombo']
        else:
            widgets_names = []
            for n in range(1, 9):
                for t in 'twImg', 'twAnswer':
                    widgets_names.append(t + str(n))

        widgets = [getattr(self.window, w) for w in widgets_names]

        for w in widgets:
            w.setEnabled(enabled)

    def run(self):
        self.window.show()
        return self.app.exec()


def main():
    app = MainWindow()
    app.run()


main()
