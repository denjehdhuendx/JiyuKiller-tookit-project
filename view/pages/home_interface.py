
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme)
from PyQt5 import uic
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF, NavigationItemPosition



########################################
# He1l0Wor1d-ice ©️ 2025               #
# home_interface.py  ,ITLTookit的一部分。#                            #
########################################

class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget)
      
        self.home_Label = QLabel(self.tr('主页｜HOME'),self)

        self.oftenuseGroup = SettingCardGroup(self.tr('常用功能'), self.scrollWidget)
        self.launcherCard = PushSettingCard(
            self.tr('启动器'),
            FIF.PLAY,
            self.tr('启动器'),
            parent=self.oftenuseGroup
        )   
        self.__initWidget()  
    def __initWidget(self):
         self.resize(1000, 800)
         self.setWidget(self.scrollWidget)
         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
         self.setWidgetResizable(True)
         self.setViewportMargins(0, 0, 0, 0)
         
         self.setObjectName('homeInterface')
         # 设置纯白色背景
         self.setStyleSheet('''
             QScrollArea#homeInterface {
                 background-color: #ffffff;
                 border: none;
             }
         ''')

         self.scrollWidget.setObjectName('homeInterfaceScrollWidget')   
         self.home_Label.setObjectName('homeInterfaceHomeLabel')
         self.home_Label.setStyleSheet('''
          QLabel#homeInterfaceHomeLabel{
              font-size: 30px;
              font-weight: bold;
              color: #333333;
              margin-left: 3px;
              margin-top: 3px;
          }
          ''')
         self.scrollWidget.setStyleSheet('''
            QWidget#homeInterfaceScrollWidget{
             background-color: #F7F9FC;
             border: none;
            }
         ''')
         self.expandLayout.setSpacing(0)
         
         self.__initLayout()
    def __initLayout(self):  
      # 重新调整布局，避免标题重叠
      # 将主标题放置在适当位置
      self.home_Label.move(26, 26)
      
      # 移除oftenuseGroup的移动设置，让expandLayout控制其位置
      self.oftenuseGroup.addSettingCard(self.launcherCard)
      
      # 调整expandLayout的边距和间距，确保标题不重叠
      self.expandLayout.setSpacing(28)
      # 增加顶部边距，确保与home_Label有足够距离
      self.expandLayout.setContentsMargins(36, 70, 36, 0)
      self.expandLayout.addWidget(self.oftenuseGroup)
     


      
      


      




   

   

      


