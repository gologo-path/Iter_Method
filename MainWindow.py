from tkinter import messagebox

from IterMethod import IterMethod
from WindowPattern import WindowPattern
import tkinter as tk


class MainWindow(WindowPattern):
    number_var = 0
    accuracy = 0.0
    destroy_objects = []

    def __init__(self):
        super().__init__("Iteration Method")

    def _new_command(self):
        self._clear_frame()
        self.dialog_window = tk.Tk()
        self.dialog_window.geometry("300x100")
        self.dialog_window.resizable(False, False)
        label = tk.Label(self.dialog_window, text="Введите размер матрицы\n"
                                                  "Размер должен быть не больше 10",
                         font=("Times new Roman", 10))
        label.pack(side=tk.TOP)
        self.spinbox = tk.Spinbox(self.dialog_window, from_=2, to=10, width=7, font="10")
        self.spinbox.bind('<Return>', self._set_number_var)

        self.spinbox.pack()
        button = tk.Button(self.dialog_window, text="Ввод", command=self._set_number_var, font="10")
        button.pack(side=tk.BOTTOM)

    def _open_command(self):
        super()._open_command()
        self._read_from_file()
        self._start_calculations(True)

    def _clear_frame(self):
        for obj in self.destroy_objects:
            obj.destroy()

    def _set_accuracy(self):
        inp_str = self.spinbox.get()
        try:
            float(inp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Ожидается число")
        self.accuracy = float(inp_str)
        self.dialog_window_accuracy.destroy()

    def _set_dialog_accuracy(self):
        self.dialog_window_accuracy = tk.Tk()
        self.dialog_window_accuracy.geometry("300x100")
        self.dialog_window_accuracy.resizable(False, False)
        label = tk.Label(self.dialog_window_accuracy, text="Введите точность E\n",
                         font=("Times new Roman", 10))
        label.pack(side=tk.TOP)

        self.spinbox = tk.Spinbox(self.dialog_window_accuracy, from_=0, to=10, width=7, font="10", increment=.001)
        self.spinbox.bind('<Return>', self._set_accuracy)
        self.spinbox.pack()
        button = tk.Button(self.dialog_window_accuracy, text="Ввод", command=self._set_accuracy, font="10")
        button.pack(side=tk.BOTTOM)

    def _set_number_var(self, event=None):
        inp_str = self.spinbox.get()
        if not inp_str.isdigit():
            messagebox.showerror("Ошибка", "Ожидается ввод числа")
        elif int(inp_str) > 10 or int(inp_str) < 2:
            messagebox.showerror("Ошибка", "Ожидается число в диапазоне от 2 до 10")
        else:
            self.number_var = int(inp_str)
            self.dialog_window.destroy()
            self._build_matrix()
            self._set_dialog_accuracy()

    def _build_matrix(self):
        self._matrix = [[None for _ in range(0, self.number_var)] for _ in range(0, self.number_var)]
        self._answers = [None for _ in range(0, self.number_var)]
        self._approximation = [None for _ in range(0, self.number_var)]

        for y in range(0, self.number_var):
            for x in range(0, self.number_var):
                self._matrix[y][x] = tk.StringVar()
                tmp = tk.Entry(textvariable=self._matrix[y][x], width=10)
                tmp.grid(row=y, column=x, padx=5, pady=5)
                self.destroy_objects.append(tmp)

            self._answers[y] = tk.StringVar()
            tmp = tk.Entry(textvariable=self._answers[y], width=10)
            tmp.grid(row=y, column=self.number_var, padx=20, pady=5)
            self.destroy_objects.append(tmp)

            self._approximation[y] = tk.StringVar()
            tmp = tk.Entry(textvariable=self._approximation[y], width=10)
            tmp.grid(row=y, column=self.number_var + 1, padx=20, pady=5)
            self.destroy_objects.append(tmp)

        tmp = tk.Button(text="Расчет", command=self._start_calculations, width=20)
        tmp.grid(row=self.number_var, columnspan=self.number_var)
        self.destroy_objects.append(tmp)

    def _start_calculations(self, valid=False):
        if not valid:
            valid = self._check_valid()
        if valid:
            method = IterMethod(self._float_matrix, self._float_answers, self._float_approximation, self.accuracy)
            conditions = method.check_conditions()
            if conditions[0] == 0:
                tmp = tk.Label(text="det = {}".format(round(conditions[1], 3))).grid(row=self.number_var + 1,
                                                                                     columnspan=3)
                self.destroy_objects.append(tmp)
                final = method.calculate()
                for i in range(0, len(final)):
                    tmp = tk.Label(text="x{0} = {1}".format(i + 1, final[i])).\
                        grid(row=self.number_var + 2 + i, columnspan=3)
                    self.destroy_objects.append(tmp)
            elif conditions[0] == 1:
                messagebox.showerror("Ошибка", "det = 0")
            elif conditions[0] == 2:
                messagebox.showerror("Ошибка", "Строка {} не отвечает требованиям".format(conditions[1]))
            else:
                messagebox.showerror("Ошибка", "Непредвиденная ошибка")
        else:
            messagebox.showerror("Ошибка", "Ожидается ввод числа")

    def _read_from_file(self):
        with open(self.file, "r") as f:
            first_l = f.readline().strip().split(',')
            self._float_approximation = [0.0 for _ in range(0,len(first_l)-1)]
            for i in range(0, len(first_l)):
                try:
                    tmp = float(first_l[i])
                except ValueError:
                    messagebox.showerror("Ошибка", "Данные в файле повреждены")
                    return None
                if i == 0:
                    self.accuracy = tmp
                else:
                    self._float_approximation[i-1] = tmp

            lines = f.readlines()
            size = len(lines)
            self._float_matrix = [[0.0 for _ in range(0, size)] for _ in range(0, size)]
            self._float_answers = []
            for line in range(0, len(lines)):
                l = lines[line].strip().split(',')
                for i in range(0, len(l) - 1):
                    try:
                        tmp = float(l[i])
                    except ValueError:
                        messagebox.showerror("Ошибка", "Данные в файле повреждены")
                        return None
                    self._float_matrix[line][i] = tmp

                try:
                    tmp = float(l[len(l) - 1])
                except ValueError:
                    return None
                self._float_answers.append(tmp)

    def _check_valid(self):
        self._float_matrix = [[0.0 for _ in range(0, self.number_var)] for _ in range(0, self.number_var)]
        self._float_answers = [0.0 for _ in range(0, self.number_var)]
        self._float_approximation = [0.0 for _ in range(0, self.number_var)]
        for y in range(0, len(self._matrix)):
            for x in range(0, len(self._matrix[y])):
                try:
                    tmp = float(self._matrix[y][x].get())
                except ValueError:
                    return False
                self._float_matrix[y][x] = tmp

        for i in range(0, len(self._answers)):
            try:
                tmp = float(self._answers[i].get())
            except ValueError:
                return False
            self._float_answers[i] = tmp

        for i in range(0, len(self._approximation)):
            try:
                tmp = float(self._approximation[i].get())
            except ValueError:
                return False
            self._float_approximation[i] = tmp

        return True
