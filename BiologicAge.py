#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join
from collections import OrderedDict
from functools import partial
import json

from PyQt5 import QtWidgets, uic, QtGui
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier


class DecisionTree():
    def __init__(self, type='b'):
        self.data = pd.read_csv(join('data', type, 'data.csv'))
        Y = self.data.values[:, -1].astype('float64')
        self.groups = self.calculate_groups(Y)
        with open(join('data', 'questions.json')) as fh:
            self.questions = json.load(fh)
        self.current_question = 0
        self.answers = []

    def train(self):
        X = self.data.values[:, 1:self.current_question+1].astype('float64')
        Y = self.data.values[:, -1].astype('float64')
        clf = DecisionTreeClassifier(min_samples_split=5)
        self.dt = clf.fit(X, Y)

    def calculate_groups(self, Y):
        groups = []
        list_of_groups = list(Y)
        for x in set(Y):
            groups.append(list_of_groups.count(x))

        return groups

    def get_question(self):
        self.current_question += 1
        print('current question', self.current_question, self.answers)
        return self.questions[self.current_question-1]

    def predict(self):
        self.train()
        prediction = self.dt.predict(np.array(self.answers).reshape(1, -1))
        print('prediction array', prediction)
        prediction = int(prediction[0]) - 1
        print('prediction integer', prediction)
        lower = sum(self.groups[:prediction])
        upper = lower + self.groups[prediction]
        print('bounds', lower, upper)
        return lower, upper

    def save_answer(self, answer):
        self.answers.append(answer)
        return self.predict()


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

        self.window.numberQuestionCombo.currentIndexChanged[int].connect(
            self.save_answer
        )
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
        print('limits', lower, upper)
        print('images subset', sorted_files[lower:upper])
        for name in sorted_files[lower:upper]:
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

        # Start asking questions
        self.restart_decision_tree()

    def next_question(self):
        try:
            question, type, folder = self.dt.get_question()
        except IndexError:
            self.disable_question_inputs()
            return

        print('next question', question, type, folder)
        self.disable_question_inputs()
        self.toggle_question_input(type=type, enabled=True)
        if type == 'image':
            path = join('images', 'patterns', folder)
            for n in range(1, 9):
                widget = getattr(self.window, 'twImg' + str(n))
                self._load_image(join(path, str(n) + '.png'), widget)
        widget = getattr(self.window, type + 'Question')
        widget.setText(question)

    def toggle_question_input(self, type='number', enabled=True):
        if type == 'number':
            widgets_names = ['numberQuestion', 'numberQuestionCombo']
        else:
            widgets_names = []
            for n in range(1, 9):
                widgets_names.append('twAnswer' + str(n))

        widgets = [getattr(self.window, w) for w in widgets_names]

        for w in widgets:
            w.setEnabled(enabled)

    def disable_question_inputs(self):
        self.toggle_question_input(type='image', enabled=False)
        self.toggle_question_input(type='number', enabled=False)

    def restart_decision_tree(self):
        self.window.numberQuestionCombo.setCurrentIndex(-1)
        self.dt = DecisionTree(type=self.sex)
        self.load_ref_img_list()
        self.next_question()

    def save_answer(self, index):
        print('save answer', index)
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
