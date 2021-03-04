import copy

import numpy as np


class IterMethod:
    def __init__(self, matrix, answers, approximation, accuracy):
        self._accuracy = accuracy
        self._approximation = approximation
        self._matrix = matrix
        self._answers = answers

    def check_conditions(self):
        det = np.linalg.det(self._matrix)
        if det == 0:
            return 1, None
        else:
            for y in range(0, len(self._matrix)):
                tmp = 0
                for x in range(0, len(self._matrix[y])):
                    if x != y:
                        tmp += abs(self._matrix[y][x])
                if not tmp < abs(self._matrix[y][y]):
                    return 2, y

        return 0, det

    def calculate(self):
        start = copy.deepcopy(self._matrix)
        while not self._check_accuracy():
            self._last = self._approximation.copy()
            for y in range(0, len(self._matrix)):
                sum_ = 0
                for x in range(0, len(self._matrix)):
                    if y != x:
                        sum_ += self._approximation[x]

                self._matrix[y][y] = (self._answers[y] - sum_) / start[y][y]
                # self._approximation[y] = self._matrix[y][y]
            for i in range(0, len(self._approximation)):
                self._approximation[i] = self._matrix[i][i]
        return self._approximation

    def _check_accuracy(self):
        try:
            acc = []
            for i in range(0, len(self._last)):
                acc.append(abs(self._approximation[i] - self._last[i]))
            if max(acc) > self._accuracy:
                return False
            else:
                return True
        except AttributeError:
            return False
