import sys
from PyQt5.QtWidgets import QApplication
from classes import *

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)
    
window = Interface_presentation()
window.show()
sys.exit(app.exec())