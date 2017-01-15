import PyQt5.QtWidgets
from PyQt5.QtWidgets import QFileDialog
import math
from TabelModel import Model
import form2
from itertools import groupby
import mainwindow
import sys
import re


class Form(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.ui = form2.Ui_Form()
        self.ui.setupUi(self)


class MainWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.text1 = ""
        self.text2 = ""


# FOR TABLE -> columns, rows = 3, 5


columns, rows = 3, 5
app = PyQt5.QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
form = Form()


def show_second_form():
    if len(main_window.text1) == 0 or len(main_window.text2) == 0 or len(main_window.ui.text_edit.toPlainText()) == 0:
        return False
    # main_window.hide()
    form.show()

    text1 = main_window.text1
    text2 = main_window.text2
    word_search = main_window.ui.text_edit.toPlainText()

    def cook_text(input_text, search):
        text = re.compile('\w+').findall(input_text)
        text_words_count = len(text)
        duplicates_in_text = [0] * (math.ceil(text_words_count / 1000))

        for idx, val in enumerate(text):
            if search.lower() == val.lower():
                duplicates_in_text[int(idx / 1000)] += 1
        # duplicates_in_text = list(filter((0).__ne__, duplicates_in_text))
        return sorted(duplicates_in_text)

    def cook_matrix(elms):
        c1 = sorted(list(set(elms)))
        c2 = [len(list(group)) for key, group in groupby(elms)]
        c3 = list(map(lambda x, y: x * y, c1, c2))
        matrix = [["" for x in range(6)] for y in c1]
        ser = sum(c3) / sum(c2)
        for idx in range(len(c1)):
            matrix[idx][0] = c1[idx]
            matrix[idx][1] = c2[idx]
            matrix[idx][2] = c3[idx]
            matrix[idx][3] = c1[idx] - ser

        return matrix, ser

    matrix1, ser1 = cook_matrix(cook_text(text1, word_search))
    matrix2, ser2 = cook_matrix(cook_text(text2, word_search))
    form.ui.tableView.setModel(Model(form, matrix=matrix1))
    form.ui.tableView_2.setModel(Model(form, matrix=matrix2))
    form.ui.label_7.setText(str(ser1))
    form.ui.label_12.setText(str(ser2))

    # form.ui.pushButton.clicked.connect(form.hide)


def OpenFirstFile(self):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilters(["Text files (*.txt)"])

    if dlg.exec_():
        filenames = dlg.selectedFiles()
        f = open(filenames[0], 'r')

        with f:
            data = f.read()
            main_window.ui.textBrowser.setText(data)
            main_window.text1 = data


def OpenSecondFile(self):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilters(["Text files (*.txt)"])

    if dlg.exec_():
        filenames = dlg.selectedFiles()
        f = open(filenames[0], 'r')

        with f:
            data = f.read()
            main_window.ui.textBrowser_2.setText(data)
            main_window.text2 = data


main_window.ui.pushButton.clicked.connect(show_second_form)
main_window.ui.pushButton_2.clicked.connect(OpenFirstFile)
main_window.ui.pushButton_3.clicked.connect(OpenSecondFile)
main_window.show()

sys.exit(app.exec_())
