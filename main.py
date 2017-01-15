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

    def closeEvent(self, event):
        main_window.show()
        event.accept()


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


def show_second_form():
    if len(main_window.text1) == 0 or len(main_window.text2) == 0 or len(main_window.ui.textEdit.toPlainText()) == 0:
        return False
    form = Form()
    form.show()
    main_window.hide()
    text1 = main_window.text1
    text2 = main_window.text2
    word_search = main_window.ui.textEdit.toPlainText()

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
        sumc2 = sum(c2)
        ser = sum(c3) / sumc2
        sumc5 = 0
        for idx in range(len(c1)):
            matrix[idx][0] = c1[idx]
            matrix[idx][1] = c2[idx]
            matrix[idx][2] = c3[idx]
            matrix[idx][3] = c1[idx] - ser
            matrix[idx][4] = (c1[idx] - ser) ** 2
            matrix[idx][5] = ((c1[idx] - ser) ** 2) * c2[idx]
            sumc5 += matrix[idx][5]
        vid = math.sqrt(sumc5/sumc2)
        mira = vid/math.sqrt(sumc2)
        var = vid/ser
        stab = 1 - (var/(math.sqrt(sumc2-1)))
        return matrix, ser, vid, mira, var, stab

    matrix1, ser1, vid1, mira1, var1, stab1 = cook_matrix(cook_text(text1, word_search))
    matrix2, ser2, vid2, mira2, var2, stab2 = cook_matrix(cook_text(text2, word_search))
    form.ui.tableView.setModel(Model(form, matrix=matrix1))
    form.ui.tableView_2.setModel(Model(form, matrix=matrix2))
    form.ui.label_7.setText(str(ser1))
    form.ui.label_12.setText(str(ser2))
    form.ui.label_8.setText(str(vid1))
    form.ui.label_13.setText(str(vid2))
    form.ui.label_9.setText(str(mira1))
    form.ui.label_14.setText(str(mira2))
    form.ui.label_10.setText(str(var1))
    form.ui.label_17.setText(str(var2))
    form.ui.label_11.setText(str(stab1))
    form.ui.label_21.setText(str(stab2))

    def compare():
        smuga1 = ser1 + (mira1 * 2)
        smuga2 = ser2 - (mira2 * 2)
        smuga3 = ser2 + (mira2 * 2)
        smuga4 = ser2 - (mira2 * 2)
        st1 = 'від {0} до{1}'.format(smuga2, smuga1)
        st2 = 'від {0} до{1}'.format(smuga4, smuga3)
        form.ui.label_26.setText(str(st1))
        form.ui.label_27.setText(str(st2))


    form.ui.pushButton.clicked.connect(compare)

        # form.ui.pushButton.clicked.connect(form.hide)


def OpenDialog():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilters(["Text files (*.txt)"])
    return dlg


def OpenFirstFile(self):
    dlg = OpenDialog()
    if dlg.exec_():
        with open(dlg.selectedFiles()[0], 'r') as f:
            data = f.read()
            main_window.ui.textBrowser.setText(data)
            main_window.text1 = data


def OpenSecondFile(self):
    dlg = OpenDialog()
    if dlg.exec_():
        with open(dlg.selectedFiles()[0], 'r') as f:
            data = f.read()
            main_window.ui.textBrowser_2.setText(data)
            main_window.text2 = data




main_window.ui.pushButton.clicked.connect(show_second_form)
main_window.ui.pushButton_2.clicked.connect(OpenFirstFile)
main_window.ui.pushButton_3.clicked.connect(OpenSecondFile)
main_window.show()

sys.exit(app.exec_())
