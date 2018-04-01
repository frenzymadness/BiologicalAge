#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
from collections import OrderedDict
from functools import partial

from libs.DecisionTree import DecisionTree

from PyQt5 import QtWidgets, uic, QtGui


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
        self.window.resetEvaluation.clicked.connect(self.restart_decision_tree)

        for n in range(1, 9):
            widget = getattr(self.window, 'twAnswer' + str(n))
            widget.clicked.connect(partial(self.save_answer, n))

    def load_ref_img_list(self, _=None, subset=None):
        # 0 -> Boy, 1 -> Girl
        index = self.window.sexCombo.currentIndex()
        # Create path to folder with RTGs
        folder = 'B' if index == 0 else 'G'
        self.sex = folder.lower()
        path = join('images', 'RTG', folder)
        # List, everything, extract files and sort them
        all = listdir(path)
        files = [name for name in all if isfile(join(path, name))]
        sorted_files = sorted(files,
                              key=lambda n: [int(x) for x in n.split('_')[:2]])
        # Process given subset or all images if no subset is given
        if subset is None:
            lower, upper = 0, len(sorted_files)
        else:
            lower, upper = subset

        self.window.openFileButton.setEnabled(True)
        # Create dictionary with files and paths and insert item to the list
        self.window.refList.clear()
        self.ref_images = OrderedDict()
        for name in sorted_files[lower:upper]:
            filename = name
            y, m = name.split('_')[:2]
            y, m = int(y), int(m)
            name = '{} years {} months'.format(y, m)
            self.ref_images[name] = join(path, filename)
            self.window.refList.addItem(name)

    def _load_image(self, filename, widget):
        if filename is not None:
            image = QtGui.QPixmap(filename)
            image = image.scaledToWidth(widget.width())
            try:
                widget_name = widget.objectName()
                name_widget = getattr(self.window, widget_name + 'Name')
                name_widget.setText(filename)
            except AttributeError:
                pass
        else:
            image = QtGui.QPixmap()
        widget.setPixmap(image)

    def open_ref_image(self):
        item = self.window.refList.currentItem()
        if item is None:
            return
        name = item.text()
        filename = self.ref_images[name]
        self._load_image(filename, self.window.refImg)

    def open_rtg_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window, "Open RTG file", "",
            "Images (*.png *.PNG *.jpg *.jpeg *.JPG);;All Files (*);;")
        if filename is None:
            return
        self._load_image(filename, self.window.rtgImg)

        # Start asking questions
        self.restart_decision_tree()

        # Enable button to reset evaluation
        self.window.resetEvaluation.setEnabled(True)

    def next_question(self):
        try:
            question, folder = self.dt.get_question()
        except IndexError:
            self.toggle_question_input(enable=False)
            return

        self.toggle_question_input(enable=True)

        for n in range(1, 9):
            widget = getattr(self.window, 'twImg' + str(n))
            if folder is not None:
                path = join('images', 'patterns', folder)
                self._load_image(join(path, str(n) + '.png'), widget)
            else:
                self._load_image(None, widget)

        self.window.questionLabel.setText(question)

    def toggle_question_input(self, enable=True):
        widgets_names = []
        for n in range(1, 9):
            widgets_names.append('twAnswer' + str(n))

        widgets = [getattr(self.window, w) for w in widgets_names]

        for w in widgets:
            w.setEnabled(enable)

    def restart_decision_tree(self):
        self.dt = DecisionTree(type=self.sex)
        self.load_ref_img_list()
        self.next_question()

    def save_answer(self, index):
        subset = self.dt.save_answer(index)
        self.load_ref_img_list(None, subset)
        self.next_question()

    def run(self):
        self.window.show()
        return self.app.exec()


def main():
    app = MainWindow()
    app.run()


main()
