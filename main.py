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
        vid = math.sqrt(sumc5 / sumc2)
        mira = vid / math.sqrt(sumc2)
        var = vid / ser
        stab = 1 - (var / (math.sqrt(sumc2 - 1)))
        return matrix, ser, vid, mira, var, stab

    cooked_text1 = cook_text(text1, word_search)
    cooked_text2 = cook_text(text1, word_search)

    t_text1 = list(filter((0).__ne__, cooked_text1))
    t_text2 = list(filter((0).__ne__, cooked_text2))
    f_sk = list((map(lambda x, y: x + y, t_text1, t_text2)))
    f_N = sum(t_text1) + sum(t_text2)
    f_sm = [sum(t_text1), sum(t_text2), f_N]
    s_m_1 = sum(map(lambda x, y: (x ** 2) / (y * f_sm[0]), t_text1, f_sk))
    s_m_2 = sum(map(lambda x, y: (x ** 2) / (y * f_sm[1]), t_text2, f_sk))
    f_result = f_N * ((s_m_1 + s_m_2) - 1)

    matrix1, ser1, vid1, mira1, var1, stab1 = cook_matrix(cooked_text1)
    matrix2, ser2, vid2, mira2, var2, stab2 = cook_matrix(cooked_text2)
    form.ui.tableView.setModel(Model(form, matrix=matrix1))
    form.ui.tableView_2.setModel(Model(form, matrix=matrix2))

    form.ui.label_7.setText(format(ser1, '.4f'))
    form.ui.label_12.setText(format(ser2, '.4f'))
    form.ui.label_8.setText(format(vid1, '.4f'))
    form.ui.label_13.setText(format(vid2, '.4f'))
    form.ui.label_9.setText(format(mira1, '.4f'))
    form.ui.label_14.setText(format(mira2, '.4f'))
    form.ui.label_10.setText(format(var1, '.4f'))
    form.ui.label_17.setText(format(var2, '.4f'))
    form.ui.label_11.setText(format(stab1, '.4f'))
    form.ui.label_21.setText(format(stab2, '.4f'))

    def compare():
        smuga1 = ser1 + (mira1 * 2)
        smuga2 = ser1 - (mira2 * 2)
        smuga3 = ser2 + (mira2 * 2)
        smuga4 = ser2 - (mira2 * 2)
        st1 = 'від {0:.2f} до {1:.2f}'.format(smuga2, smuga1)
        st2 = 'від {0:.2f} до {1:.2f}'.format(smuga4, smuga3)
        form.ui.label_26.setText(format(st1, '.4f'))
        form.ui.label_27.setText(format(st2, '.4f'))

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
