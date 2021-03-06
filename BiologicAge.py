#!/usr/bin/env python3
from os import listdir, chdir
from os.path import isfile, join, basename
from collections import OrderedDict
from functools import partial
import sys

from libs.DecisionTree import DecisionTree
from libs.DicomImage import Dicom

from PyQt5 import QtWidgets, uic, QtGui, QtCore

# Change CWD to temp directory if we run in pyinstalled bundle mode
if hasattr(sys, '_MEIPASS'):
    chdir(sys._MEIPASS)


class MainWindow():
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QMainWindow()
        with open('mainwindow.ui') as f:
            uic.loadUi(f, self.window)

        # Add logo
        self._load_image(join('images', 'BME.jpg'), self.window.logo)

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
        """Loads list of reference images"""
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
        """Load image to the specified widget with proper size"""
        if filename is not None:
            if filename.endswith('.dcm'):
                dicom_file = Dicom(filename)
                pixmap = QtGui.QPixmap.fromImage(dicom_file.image)
            else:
                pixmap = QtGui.QPixmap(filename)
            w = min(pixmap.width(), widget.maximumWidth())
            h = min(pixmap.height(), widget.maximumHeight())
            pixmap = pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio,
                                   QtCore.Qt.SmoothTransformation)
            # Try to put image name to the name label if exists
            try:
                widget_name = widget.objectName()
                name_widget = getattr(self.window, widget_name + 'Name')
                if widget_name == 'refImg':
                    prefix = 'Referrence image: '
                elif widget_name == 'rtgImg':
                    prefix = 'Clinical image: '
                name_widget.setText(prefix + basename(filename))
            except AttributeError:
                pass
        else:
            # Use empty pixmap if no file given
            pixmap = QtGui.QPixmap()
        widget.setPixmap(pixmap)

    def open_ref_image(self):
        """Open and show choosen reference image"""
        item = self.window.refList.currentItem()
        if item is None:
            return
        name = item.text()
        filename = self.ref_images[name]
        self._load_image(filename, self.window.refImg)

    def open_rtg_image(self):
        """Open and show RTG image and start assesment"""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.window, "Open RTG file", "",
            "Images (*.png *.PNG *.jpg *.jpeg *.JPG *.JPEG *.DCM *.dcm);;\
            All Files (*);;")
        if filename is None:
            return
        self._load_image(filename, self.window.rtgImg)

        # Start asking questions
        self.restart_decision_tree()

        # Enable button to reset evaluation
        self.window.resetEvaluation.setEnabled(True)

    def next_question(self):
        """Process next question in assesment process"""
        # Disable inputs if last question reached
        try:
            question, folder = self.dt.get_question()
        except IndexError:
            self.toggle_question_input(enable=False)
            return

        self.toggle_question_input(enable=True)

        # Load images of TW patterns or empty images if question is about
        # number and not bone status
        for n in range(1, 9):
            widget = getattr(self.window, 'twImg' + str(n))
            if folder is not None:
                path = join('images', 'patterns', folder)
                self._load_image(join(path, str(n) + '.png'), widget)
            else:
                self._load_image(None, widget)

        self.window.questionLabel.setText(question)

    def toggle_question_input(self, enable=True):
        """Enable/Disable question input buttons"""
        widgets_names = []
        for n in range(1, 9):
            widgets_names.append('twAnswer' + str(n))

        widgets = [getattr(self.window, w) for w in widgets_names]

        for w in widgets:
            w.setEnabled(enable)

    def restart_decision_tree(self):
        """Restart decision tree process"""
        self.dt = DecisionTree(type=self.sex)
        self.load_ref_img_list()
        self.next_question()

    def save_answer(self, index):
        """Save answer after button click and go to next"""
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
