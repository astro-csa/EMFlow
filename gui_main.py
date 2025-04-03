import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QApplication, QPushButton
from gui.forms.all_programs_form import AllProgramsForm
from utils.loader import get_programs

class EMFlow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EMFlow – Configuration Generator")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AllProgramsForm()
    window.show()

    app.exec_()
