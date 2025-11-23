from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from qfluentwidgets import *

class AboutInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initUI()
        self.setObjectName('aboutInterface')

    def initUI(self):
        """初始化用户界面，使用自适应布局"""
        self.setObjectName('aboutInterface')