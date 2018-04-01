from os.path import join
import json

from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np


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
        return self.questions[self.current_question-1]

    def predict(self):
        self.train()
        prediction = self.dt.predict(np.array(self.answers).reshape(1, -1))
        prediction = int(prediction[0]) - 1
        lower = sum(self.groups[:prediction])
        upper = lower + self.groups[prediction]
        return lower, upper

    def save_answer(self, answer):
        self.answers.append(answer)
        return self.predict()
