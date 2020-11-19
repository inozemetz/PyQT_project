import sys
import math
import sqlite3
import random
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtCore, QtGui, QtWidgets


# класс для обработки уравнений
class Equation():
    def __init__(self, eq):
        self.str_eq = eq
        self.coefficents = self.find_coefficents()

    # функция для превращения уравнения из строки в набор коэффициентов 
    def find_coefficents(self):
        self.str_eq = ''.join([i for i in self.str_eq if i != ' '])
        mn = self.str_eq[0:self.str_eq.index('=')]
        degrees = []
        for i in range(len(mn)):
            if mn[i] == '^':
                degrees.append(int(mn[i + 1]))
        if 'x' in mn and not degrees:
            coefficents = [0, 0]
            if '+' in mn:
                if 'x' in mn.split('+')[0]:
                    if mn.split('+')[0][0:mn.split('+')[0].index('x')] == '':
                        coefficents[0] = 1
                    elif mn.split('+')[0][0:mn.split('+')[0].index('x')] == '-':
                        coefficents[0] = -1
                    else:
                        coefficents[0] = float(mn.split('+')[0][0:mn.split('+')[0].index('x')])
                    coefficents[1] = float(mn.split('+')[1])
                else:
                    if mn.split('+')[1][0:mn.split('+')[1].index('x')] == '':
                        coefficents[0] = 1
                    else:
                        coefficents[0] = float(mn.split('+')[1][0:mn.split('+')[1].index('x')])
                    coefficents[1] = float(mn.split('+')[0])
            elif '-' in mn and mn[0] != '-':
                if 'x' in mn.split('-')[0]:
                    if mn.split('-')[0][0:mn.split('-')[0].index('x')] == '':
                        coefficents[0] = 1
                    elif mn.split('-')[0][0:mn.split('-')[0].index('x')] == '-':
                        coefficents[0] = -1
                    else:
                        coefficents[0] = float(mn.split('-')[0][0:mn.split('-')[0].index('x')])
                    coefficents[1] = -float(mn.split('-')[1])
                else:
                    coefficents[0] = -float(mn.split('-')[1][0:mn.split('-')[1].index('x')])
                    coefficents[1] = float(mn.split('-')[0])
            elif mn[0] == '-' and mn.count('-') == 2:
                terms = mn.split('-')[1:]
                if 'x' in terms[0]:
                    if terms[0][0:terms[0].index('x')] == '':
                        coefficents[0] = -1
                    else:
                        coefficents[0] = -float(terms[0][0:terms[0].index('x')])
                    coefficents[1] = -float(terms[1])
                else:
                    coefficents[0] = -float(terms[1][0:terms[1].index('x')])
                    coefficents[1] = -float(terms[0])
            elif mn[0] == '-' and mn.count('-') == 1 and mn.count('+') == 0:
                if mn[0:mn.index('x')] == '-':
                    coefficents[0] = -1
                else:
                    coefficents[0] = float(mn[0:mn.index('x')])
                coefficents[1] = 0
            elif mn.count('-') == 0 and mn.count('+') == 0:
                if mn[0:mn.index('x')] == '':
                    coefficents[0] = 1
                else:
                    coefficents[0] = float(mn[0:mn.index('x')])
                coefficents[1] = 0
        elif 'x' not in mn and not degrees:
            coefficents = [float(mn)]
        else:
            coefficents = [0 for i in range(max(degrees) + 1)]
            for i in range(len(mn)):
                if mn[i] == '^':
                    for j in range(i, -1, -1):
                        if mn[j] == '+':
                            if mn[j + 1:i - 1] == '':
                                coefficents[-int(mn[i + 1]) - 1] = 1
                            else:
                                coefficents[-int(mn[i + 1]) - 1] = float(mn[j + 1:i - 1])
                            break
                        elif mn[j] == '-':
                            if mn[j + 1:i - 1] == '':
                                coefficents[-int(mn[i + 1]) - 1] = -1
                            else:
                                coefficents[-int(mn[i + 1]) - 1] = -float(mn[j + 1:i - 1])
                            break
                        elif j == 0:
                            if mn[0:i - 1] == '':
                                coefficents[-int(mn[i + 1]) - 1] = 1
                            else:
                                coefficents[-int(mn[i + 1]) - 1] = float(mn[0:i - 1])
            for i in range(len(mn)):
                if mn[i] == 'x' and (i + 1 == len(mn) or (mn[i + 1] != '^')):
                    for j in range(i, -1, -1):
                        if mn[j] == '+':
                            if mn[j + 1: i] == '':
                                coefficents[-2] = 1
                            else:
                                coefficents[-2] = float(mn[j + 1:i])
                            break
                        elif mn[j] == '-':
                            if mn[j + 1: i] == '':
                                coefficents[-2] = -1
                            else:
                                coefficents[-2] = -float(mn[j + 1:i])
                            break
                        elif j == 0:
                            if mn[0:i] == '':
                                coefficents[-2] = 1
                            else:
                                coefficents[-2] = float(mn[0:i])
                            break
            for i in range(len(mn)):
                if mn[i].isdigit() and mn[i - 1] != '^':
                    substr = mn[i:]
                    if 'x' not in substr[0:] and mn[i - 1] != '^':
                        if mn[i - 1] == '-':
                            coefficents[-1] = -float(substr[:])
                        else:
                            coefficents[-1] = float(substr[:])
                        break
                    elif '+' in substr and 'x' not in substr[0: substr.index('+')] \
                            and mn[i - 1] != '^':
                        if mn[i - 1] == '-':
                            coefficents[-1] = -float(substr[: substr.index('+')])
                        else:
                            coefficents[-1] = float(substr[: substr.index('+')])
                        break
                    elif '-' in substr and 'x' not in substr[0: substr.index('-')] \
                            and mn[i - 1] != '^':
                        if mn[i - 1] == '-':
                            coefficents[-1] = -float(substr[: substr.index('-')])
                        else:
                            coefficents[-1] = float(substr[: substr.index('-')])
                        break
        for i in range(len(coefficents)):
            if coefficents[i] == int(coefficents[i]):
                coefficents[i] = int(coefficents[i])
        return coefficents

    # возвращает коэффициенты
    def get_coefficents(self):
        return self.coefficents

    # распределяет коэффициенты по уравнениям  
    def get_equation_type(self):
        if len(self.coefficents) == 1:
            return NoneArgumentEquation
        elif len(self.coefficents) == 2:
            return LineumEquation
        elif len(self.coefficents) == 3:
            return SecondDegreeEquation
        else:
            return ThirdDegreeEquation


# класс для уравнений без переменной
class NoneArgumentEquation():
    def __init__(self, coeffs):
        self.coeffs = coeffs
        if self.coeffs[0] == int(self.coeffs[0]):
            self.coeffs[0] = int(self.coeffs[0])
        self.solution = []
        self.radical = []
        self.coords = []

    def solve(self):
        if self.coeffs[0] == 0:
            self.radical = 'верное равенство'
        else:
            self.radical = 'неверное равенство'

    def get_solution(self):
        self.solve()
        if self.radical == 'верное равенство':
            solution = ['верное равенство. любое число']
        else:
            solution = ['неверное равенство. нет корней']
        return solution

    def get_radicals(self):
        self.solve()
        return [str(self.radical)], [str(self.radical)]

    # создает и возвращает координаты для графика
    def get_coords_for_graphic(self):
        i = -24
        while i < 24:
            self.coords.append([i, self.coeffs[0]])
            i += 0.1
        return self.coords


class LineumEquation:
    def __init__(self, coeffs):
        self.coeffs = coeffs
        for i in range(len(self.coeffs)):
            if self.coeffs[i] == int(self.coeffs[i]):
                self.coeffs[i] = int(self.coeffs[i])
        self.solution = []
        self.radical = []
        self.pretty_radical = []
        self.coords = []

    # решает уравнение и приводит его корни в красивый вид
    def solve(self):
        self.radical = -self.coeffs[1] / self.coeffs[0]
        a, b = self.coeffs[0], self.coeffs[1]
        for i in range(1, max([int(abs(a)), int(abs(b))])):
            if a % i == 0 and b % i == 0:
                a = a // i
                b = b // i
        if self.radical == int(self.radical):
            self.radical = int(self.radical)
        if a > 0 and b > 0:
            self.pretty_radical = [f'{-b}/{a}']
        elif a > 0 and b < 0:
            self.pretty_radical = [f'{-b}/{a}']
        elif a < 0 and b > 0:
            self.pretty_radical = [f'{b}/{-a}']
        else:
            self.pretty_radical = [f'{b}/{-a}']
        self.radicals = [str(self.radical)]

    # создает текст решения уравнения
    def get_solution(self):
        self.solve()
        solution = ['линейное уравнение решается по формуле ',
                    'x = -b/a, где а - коэффицент при x, b - ',
                    'свободный коэффицент, подставим и ',
                    f'получим х = {self.pretty_radical[0]}']
        return solution

    # возвращает корни в десятичных и обычных дробях
    def get_radicals(self):
        self.solve()
        return self.radicals, self.pretty_radical

    # создает и возвращает координаты уравнения
    def get_coords_for_graphic(self):
        i = -24
        while i < 24:
            self.coords.append([i, self.coeffs[0] * i + self.coeffs[1]])
            i += 0.1
        return self.coords


# класс для решения квадратных уравнений
class SecondDegreeEquation():
    def __init__(self, coeffs):
        self.coeffs = coeffs
        for i in range(len(self.coeffs)):
            if self.coeffs[i] == int(self.coeffs[i]):
                self.coeffs[i] = int(self.coeffs[i])
        self.solution = []
        self.radicals = []
        self.pretty_radicals = []
        self.coords = []

    # решает квадратное уравнение и приводит корни в красивый вид
    def solve(self):
        discriminant = self.coeffs[1] ** 2 - 4 * self.coeffs[0] * self.coeffs[2]
        if discriminant == int(discriminant):
            discriminant = int(discriminant)
        if ((self.coeffs[0] > 0 and self.coeffs[1] == 0 and self.coeffs[2] < 0) or \
            (self.coeffs[0] < 0 and self.coeffs[1] == 0 and self.coeffs[2] > 0)) and discriminant > 0:
            a = 2 * self.coeffs[0]
            b = discriminant
            new_b = b
            b_mn = 1
            # выносит множитель из под корня
            for i in range(2, int(b)):
                if int(b / i ** 2) == b / i ** 2:
                    b_mn = i
                    new_b = b / i ** 2
            a1, c1 = abs(a), abs(b_mn)
            while a1 != 0 and c1 != 0:
                if a1 > c1:
                    a1 %= c1
                else:
                    c1 %= a1
            gcd_2 = a1 + c1
            a = a // gcd_2
            b_mn = b_mn // gcd_2
            if int(a) == a:
                a = int(a)
            if int(b_mn) == b_mn:
                b_mn = int(b_mn)
            if int(new_b) == new_b:
                new_b = int(new_b)
            self.radicals = [-math.sqrt(discriminant) / 2 / self.coeffs[0],
                             math.sqrt(discriminant) / 2 / self.coeffs[0]]
            if b_mn != 1:
                self.pretty_radicals = [f'±{b_mn}√{new_b}/{abs(a)}']
            else:
                self.pretty_radicals = [f'±√{new_b}/{abs(a)}']
        else:
            # находит НОД 3х чисел
            def gcd(a, b, c=None):
                return ((a if b == 0 else gcd(b, a % b)) if c is None
                        else gcd(gcd(a, b), gcd(a, c)))

            # распределяет корни в зависимости от дискриминанта
            if discriminant > 0:
                self.radicals = [(-self.coeffs[1] + math.sqrt(discriminant)) / 2 / self.coeffs[0],
                                 (-self.coeffs[1] - math.sqrt(discriminant)) / 2 / self.coeffs[0]]
                if len(str(math.sqrt(discriminant))) > 8:
                    a, b, c = -self.coeffs[1], discriminant, 2 * self.coeffs[0]
                    new_b = b
                    b_mn = 1
                    # выносит множитель из под корня
                    for i in range(1, int(b)):
                        if int(b / i ** 2) == b / i ** 2:
                            b_mn = i
                            new_b = b / i ** 2
                    nod = gcd(abs(a), abs(b_mn), abs(c))
                    a = a // nod
                    b_mn = b_mn // nod
                    c = c // nod
                    new_b = int(new_b)
                    if c < 0:
                        c = abs(c)
                        a = -a
                    if b_mn != 1:
                        if c != 1:
                            self.pretty_radicals = [f'({a}±{b_mn}√{new_b})/{c}']
                        else:
                            self.pretty_radicals = [f'{a}±{b_mn}√{new_b}']
                    else:
                        if c != 1:
                            self.pretty_radicals = [f'({a}±√{new_b})/{c}']
                        else:
                            self.pretty_radicals = [f'{a}±√{new_b}']
                else:
                    self.pretty_radicals = ['', '']
                    a = -self.coeffs[1] + math.sqrt(discriminant)
                    c = 2 * self.coeffs[0]
                    a1, c1 = abs(a), abs(c)
                    # сокращает дробные корни
                    while a1 != 0 and c1 != 0:
                        if a1 > c1:
                            a1 %= c1
                        else:
                            c1 %= a1
                    gcd_2 = a1 + c1
                    a = a // gcd_2
                    c = c // gcd_2
                    if int(a) == a:
                        a = int(a)
                    if int(c) == c:
                        c = int(c)
                    if c < 0:
                        c = abs(c)
                        a = -a
                    if len(f'{a}/{c}') > 20:
                        self.pretty_radicals[0] = f'...'
                    else:
                        self.pretty_radicals[0] = f'{a}/{c}'

                    b = -self.coeffs[1] - math.sqrt(discriminant)
                    c = 2 * self.coeffs[0]
                    b1, c1 = abs(b), abs(c)
                    while b1 != 0 and c1 != 0:
                        if b1 > c1:
                            b1 %= c1
                        else:
                            c1 %= b1
                    gcd_2 = b1 + c1
                    b = b // gcd_2
                    c = c // gcd_2
                    if int(b) == b:
                        b = int(b)
                    if int(c) == c:
                        c = int(c)
                    if c < 0:
                        c = abs(c)
                        b = -b
                    if len(f'{b}/{c}') > 20:
                        self.pretty_radicals[1] = f''
                    else:
                        self.pretty_radicals[1] = f'{b}/{c}'

            elif discriminant == 0:
                self.radicals = [-self.coeffs[1] / 2 / self.coeffs[0]]
                a, b = -self.coeffs[1], 2 * self.coeffs[0]
                a1, b1 = abs(a), abs(b)
                while a1 != 0 and b1 != 0:
                    if a1 > b1:
                        a1 %= b1
                    else:
                        b1 %= a1
                gcd_2 = b1 + a1
                a = a // gcd_2
                b = b // gcd_2
                if b < 0:
                    b = abs(b)
                    a = -a
                self.pretty_radicals = [f'{a}/{b}']
            else:
                self.radicals = []
        for i in range(len(self.radicals)):
            if self.radicals[i] == int(self.radicals[i]):
                self.radicals[i] = int(self.radicals[i])
            self.radicals[i] = str(self.radicals[i])
        self.radicals = tuple(self.radicals)
        self.pretty_radicals = tuple(self.pretty_radicals)
        self.discriminant = discriminant

    # создает и возвращает текст решения
    def get_solution(self):
        self.solve()
        # теорема виета
        if len(self.radicals) == 2 and \
                len(self.radicals[0]) == 1 and len(self.radicals[1]) == 1:
            solution = ['решается по теореме виета x1+x2 = -b ',
                        'x1*x2 = c, угадав корни получаем ',
                        f'x1 = {self.radicals[0]}, x2 = {self.radicals[1]}']
        # по дискриминанту
        else:
            if self.discriminant > 0:
                solution = ['решается по формуле квадратного ',
                            'уравнения x = (-b±√D)/2a ',
                            'D = b^2-4ac D >= 0 значит корни есть',
                            f'x=({-self.coeffs[1]}±√{self.discriminant}) / {2 * self.coeffs[0]}']
            elif self.discriminant == 0:
                solution = ['решается по формуле квадратного ',
                            'уравнения x = (-b±√D)/2a ',
                            'D = b^2-4ac D >= 0 значит корни есть',
                            f'x={-self.coeffs[1]}/{2 * self.coeffs[0]}']
            else:
                solution = ['решается по формуле квадратного ',
                            'уравнения x = (-b±√D)/2a ',
                            'D = b^2-4ac D < 0 значит корней нет']
        return solution

    # возвращает корни в виде десятичной и обычной дроби
    def get_radicals(self):
        self.solve()
        if self.radicals:
            return (self.radicals, self.pretty_radicals)
        else:
            return (['нет корней'], ['нет корней'])

    # создает и возвращает координаты для графика
    def get_coords_for_graphic(self):
        i = -24
        while i < 24:
            self.coords.append([i, self.coeffs[0] * (i ** 2) + self.coeffs[1] * i + self.coeffs[2]])
            i += 0.1
        return self.coords


# класс для решения уравнений 3 степени
class ThirdDegreeEquation():
    def __init__(self, coeffs):
        self.coeffs = coeffs
        for i in range(len(self.coeffs)):
            if self.coeffs[i] == int(self.coeffs[i]):
                self.coeffs[i] = int(self.coeffs[i])
        self.pretty_radicals = []
        self.solution = []
        self.radicals = []
        self.coords = []

    # находит корни подбором по теореме виета
    def solve(self):
        if len(self.coeffs) == 4:
            a3, a2, a1, a0 = tuple(self.coeffs)
            for x1 in range(-10, 10):
                for x2 in range(-10, 10):
                    for x3 in range(-10, 10):
                        if x1 + x2 + x3 == -a2 / a3 and x1 * x2 + x1 * x3 + x2 * x3 == a1 / a3 \
                                and x1 * x2 * x3 == -a0 / a3:
                            self.radicals = [str(x1), str(x2), str(x3)]
        self.radicals = set(self.radicals)
        self.radicals = [i for i in self.radicals]
        self.pretty_radicals = [i for i in self.radicals]
        if not self.radicals:
            self.radicals = ['не решить']
            self.pretty_radicals = ['не решить']

    # создает и возвращает текст решения
    def get_solution(self):
        self.solve()
        if self.radicals:
            solution = ['подобрать корни по теореме виета 3 степени',
                        'x1 + x2 + x3 = -a2/a3',
                        'x1x2 + x1x3 + x2x3 = a1/a3',
                        'x1x2x3 = -a0/a3']
        else:
            solution = ['']
        return solution

    # возвращает корни
    def get_radicals(self):
        self.solve()
        return (self.radicals, self.pretty_radicals)

    # создает и возвращает координаты для графика
    def get_coords_for_graphic(self):
        i = -24
        while i < 24:
            summ = 0
            for j in range(len(self.coeffs)):
                summ += self.coeffs[j] * (i ** (len(self.coeffs) - 1 - j))
            self.coords.append([i, summ])
            i += 0.1
        return self.coords


# класс для графического вывода и обработки реакций кнопок
class MyWidget(QMainWindow):

    # создание реакций на кнопки
    def __init__(self):
        super().__init__()
        self.could_repaint = False
        self.DB_NAME = 'equations.db'
        self.actual_radicals = ''
        self.equation = ''
        self.setupUi(self)
        self.Build_btn.clicked.connect(self.build)
        self.Solve_btn.clicked.connect(self.solve)
        self.EquationType_box.addItems(['линейное', 'квадратное', 'высших степеней'])
        self.Check_btn.clicked.connect(self.check)
        self.EquationGet_btn.clicked.connect(self.get_equation)
        self.Square_btn.clicked.connect(self.put_square)
        self.PlusMinus_btn.clicked.connect(self.put_plus_minus)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(921, 737)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 50, 121, 31))
        self.label.setObjectName("label")
        self.EquationPut_ln = QtWidgets.QLineEdit(self.centralwidget)
        self.EquationPut_ln.setGeometry(QtCore.QRect(140, 50, 261, 31))
        self.EquationPut_ln.setObjectName("EquationPut_ln")
        self.Solve_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Solve_btn.setGeometry(QtCore.QRect(140, 110, 131, 41))
        self.Solve_btn.setObjectName("Solve_btn")
        self.Build_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Build_btn.setGeometry(QtCore.QRect(270, 110, 131, 41))
        self.Build_btn.setObjectName("Build_btn")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(410, 50, 141, 31))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 160, 101, 31))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 250, 101, 20))
        self.label_5.setObjectName("label_5")
        self.Solution_lwd = QtWidgets.QListWidget(self.centralwidget)
        self.Solution_lwd.setGeometry(QtCore.QRect(140, 260, 256, 192))
        self.Solution_lwd.setObjectName("Solution_lwd")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(430, 50, 151, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 490, 91, 31))
        self.label_7.setObjectName("label_7")
        self.EquationType_box = QtWidgets.QComboBox(self.centralwidget)
        self.EquationType_box.setGeometry(QtCore.QRect(120, 490, 171, 31))
        self.EquationType_box.setObjectName("EquationType_box")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(310, 490, 91, 31))
        self.label_8.setObjectName("label_8")
        self.RadicalsPut_ln = QtWidgets.QLineEdit(self.centralwidget)
        self.RadicalsPut_ln.setGeometry(QtCore.QRect(710, 490, 191, 31))
        self.RadicalsPut_ln.setObjectName("RadicalsPut_ln")
        self.EquationGet_btn = QtWidgets.QPushButton(self.centralwidget)
        self.EquationGet_btn.setGeometry(QtCore.QRect(120, 540, 141, 31))
        self.EquationGet_btn.setObjectName("EquationGet_btn")
        self.EquationRandom_lbl = QtWidgets.QLabel(self.centralwidget)
        self.EquationRandom_lbl.setGeometry(QtCore.QRect(380, 490, 221, 31))
        self.EquationRandom_lbl.setObjectName("EquationRandom_lbl")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(610, 490, 91, 31))
        self.label_10.setObjectName("label_10")
        self.Check_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Check_btn.setGeometry(QtCore.QRect(770, 540, 131, 31))
        self.Check_btn.setObjectName("Check_btn")
        self.Reply_lbl = QtWidgets.QLabel(self.centralwidget)
        self.Reply_lbl.setGeometry(QtCore.QRect(610, 600, 291, 21))
        self.Reply_lbl.setObjectName("Reply_lbl")
        self.Radicals_lbl = QtWidgets.QLabel(self.centralwidget)
        self.Radicals_lbl.setGeometry(QtCore.QRect(140, 210, 241, 21))
        self.Radicals_lbl.setObjectName("Radicals_lbl")
        self.Square_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Square_btn.setGeometry(QtCore.QRect(610, 540, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Square_btn.setFont(font)
        self.Square_btn.setObjectName("Square_btn")
        self.PlusMinus_btn = QtWidgets.QPushButton(self.centralwidget)
        self.PlusMinus_btn.setGeometry(QtCore.QRect(670, 540, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PlusMinus_btn.setFont(font)
        self.PlusMinus_btn.setObjectName("PlusMinus_btn")
        self.PrettyRadicals_lbl = QtWidgets.QLabel(self.centralwidget)
        self.PrettyRadicals_lbl.setGeometry(QtCore.QRect(140, 170, 241, 21))
        self.PrettyRadicals_lbl.setObjectName("PrettyRadicals_lbl")
        self.Error_lbl = QtWidgets.QLabel(self.centralwidget)
        self.Error_lbl.setGeometry(QtCore.QRect(70, 650, 341, 21))
        self.Error_lbl.setText("")
        self.Error_lbl.setObjectName("Error_lbl")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(510, 630, 391, 21))
        self.label_4.setObjectName("label_4")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(510, 660, 341, 16))
        self.label_9.setObjectName("label_9")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(20, 20, 381, 16))
        self.label_11.setObjectName("label_11")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 921, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Введите уравнение"))
        self.Solve_btn.setText(_translate("MainWindow", "Решить"))
        self.Build_btn.setText(_translate("MainWindow", "Построить"))
        self.label_3.setText(_translate("MainWindow", "Корни уравнения"))
        self.label_5.setText(_translate("MainWindow", "Решение уравнения"))
        self.label_6.setText(_translate("MainWindow", "График уравнения"))
        self.label_7.setText(_translate("MainWindow", "Выберите тип"))
        self.label_8.setText(_translate("MainWindow", "уравнение"))
        self.EquationGet_btn.setText(_translate("MainWindow", "Получить уравнение"))
        self.EquationRandom_lbl.setText(_translate("MainWindow", "..."))
        self.label_10.setText(_translate("MainWindow", "Введите корни"))
        self.Check_btn.setText(_translate("MainWindow", "Проверить"))
        self.Reply_lbl.setText(_translate("MainWindow", "..."))
        self.Radicals_lbl.setText(_translate("MainWindow", "..."))
        self.Square_btn.setText(_translate("MainWindow", "√"))
        self.PlusMinus_btn.setText(_translate("MainWindow", "±"))
        self.PrettyRadicals_lbl.setText(_translate("MainWindow", "..."))
        self.label_4.setText(_translate("MainWindow", "Ответы надо указать через пробел, максимально упрощенными"))
        self.label_9.setText(_translate("MainWindow", "Если корней нет, напишите \"нет корней\""))
        self.label_11.setText(_translate("MainWindow", "справа в уравнении должен быть 0. Переменная - x"))

    # запрашивает уравнение из БД
    def get_equation(self):
        equation_type = self.EquationType_box.currentText()
        con = sqlite3.connect(self.DB_NAME)
        cur = con.cursor()
        equations = cur.execute("""SELECT * FROM equations WHERE equation_type=?""",
                                (equation_type,)).fetchall()
        equation = random.choice(equations)

        self.EquationRandom_lbl.setText(equation[0])
        self.equation = equation[0]
        self.actual_radicals = str(equation[2])

    # напечатать ±
    def put_plus_minus(self):
        text = self.RadicalsPut_ln.text()
        text = text + '±'
        self.RadicalsPut_ln.setText(text)

    # напечатать √
    def put_square(self):
        text = self.RadicalsPut_ln.text()
        text = text + '√'
        self.RadicalsPut_ln.setText(text)

    # сверить корни
    def check(self):
        try:
            self.Error_lbl.setText('')
            input_radicals = ' '.join(self.RadicalsPut_ln.text().strip().split())
            if self.equation:
                if '_' in self.actual_radicals:
                    pretty_radicals = self.actual_radicals.split('_')[1]
                    radicals = self.actual_radicals.split('_')[0]
                    if pretty_radicals == 'нет корней':
                        if input_radicals == 'нет корней':
                            self.Reply_lbl.setText('Верно!')
                        else:
                            self.Reply_lbl.setText(f'Неверно! Корней нет!')
                    else:
                        if len(radicals.split(',')) == 1 and len(pretty_radicals.split(',')) == 1:
                            if input_radicals == radicals or input_radicals == pretty_radicals:
                                self.Reply_lbl.setText('Верно!')
                            else:
                                if float(radicals) in [i for i in range(-10, 10)]:
                                    self.Reply_lbl.setText(f'Неверно! Корни: {radicals}')
                                else:
                                    self.Reply_lbl.setText(f'Неверно! Корни: {pretty_radicals}')
                        elif len(pretty_radicals.split(',')) == 1 and len(radicals.split(',')) == 2:
                            if pretty_radicals == input_radicals:
                                self.Reply_lbl.setText('Верно!')
                            else:
                                self.Reply_lbl.setText(f'Неверно! Корни: {pretty_radicals}')
                else:
                    radicals = self.actual_radicals.split(',')
                    radicals.sort()
                    radicals = ' '.join(radicals)
                    input_radicals = input_radicals.split()
                    input_radicals.sort()
                    input_radicals = ' '.join(input_radicals)
                    if input_radicals == radicals:
                        self.Reply_lbl.setText('Верно!')
                    else:
                        self.Reply_lbl.setText(f'Неверно! корни: {radicals}')
        except Exception:
            self.Error_lbl.setText('Что-то пошло не так!')
            self.Error_lbl.setStyleSheet('color:#ff0000')

    # реакция кнопки "решить"
    def solve(self):
        try:
            self.Error_lbl.setText('')
            equation = Equation(self.EquationPut_ln.text())
            typed_equation = equation.get_equation_type()
            self.Solution_lwd.clear()
            radicals, pretty_radicals = typed_equation(equation.get_coefficents()).get_radicals()
            self.Solution_lwd.addItems(typed_equation(equation.get_coefficents()).get_solution())
            self.PrettyRadicals_lbl.setText(', '.join(pretty_radicals))
            self.Radicals_lbl.setText(', '.join(radicals))
        except Exception:
            self.Error_lbl.setText('Что-то пошло не так!')
            self.Error_lbl.setStyleSheet('color:#ff0000')

    # функция рисования
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_graphic_axes(qp)
        if self.could_repaint:
            try:
                equation = Equation(self.EquationPut_ln.text())
                typed_equation = equation.get_equation_type()
                points = typed_equation(equation.get_coefficents()).get_coords_for_graphic()
                for i in range(len(points)):
                    points[i][0] = int(points[i][0] * 10 + 650)
                    points[i][1] = -int(points[i][1] * 10 - 270)
                self.draw_graphic(qp, points)
                self.could_repaint = False
            except Exception:
                self.Error_lbl.setText('Что-то пошло не так!')
                self.Error_lbl.setStyleSheet('color:#ff0000')
        qp.end()

    # реакция кнопки построения графика
    def build(self):
        try:
            self.could_repaint = True
            self.repaint()
        except Exception:
            self.could_repaint = False
            self.Error_lbl.setText('Что-то пошло не так!')
            self.Error_lbl.setStyleSheet('color:#ff0000')

    # отрисовка осей графика
    def draw_graphic_axes(self, qp):
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(430, 70, 450, 400)
        qp.setBrush(QColor(0, 0, 0))
        qp.drawLine(430, 270, 880, 270)
        qp.drawLine(650, 70, 650, 470)
        for i in range(430, 880, 10):
            qp.drawLine(i, 268, i, 272)
        for i in range(70, 470, 10):
            qp.drawLine(652, i, 648, i)

    # отрисовка графика
    def draw_graphic(self, qp, points):
        try:
            for i in range(len(points)):
                if points[i][1] > 470:
                    points[i][1] = 470
                elif points[i][1] < 70:
                    points[i][1] = 70
            for i in range(len(points)):
                if points[i][1] >= 70 and i + 1 < len(points) and points[i + 1][0] > 430 \
                        and points[i + 1][0] < 880:
                    qp.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])
        except Exception:
            self.Error_lbl.setText('Что-то пошло не так!')
            self.Error_lbl.setStyleSheet('color:#ff0000')


# запуск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
