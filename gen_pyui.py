from PyQt5 import uic

with open("form2.py", "w+") as f:
    uic.compileUi('form2.ui', f)
    f.close()

with open("mainwindow.py", "w+") as f:
    uic.compileUi('mainwindow.ui', f)
    f.close()
