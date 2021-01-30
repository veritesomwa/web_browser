from PyQt5.QtWidgets import (QApplication, QFrame, QWidget,
                             QVBoxLayout, QHBoxLayout, QStackedLayout,
                             QPushButton, QLineEdit, QTabBar, QLabel)

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QImage, QFont

import sys, os

from PyQt5.QtWebEngineWidgets import QWebEngineView

class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()

class App(QFrame):
    def __init__(self):
        super().__init__()
        self.AppSettings()
        self.CreateApplication()

    def AppSettings(self):
        self.setWindowTitle('Web Browser')
        self.setMinimumSize(840, 620)

    def CreateApplication(self):
        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        # Variables
        self.tab_count = 0
        self.tabs = []

        self.tabbar = QTabBar(tabsClosable=True, movable=True)
        self.tabbar.tabCloseRequested.connect(self.CloseTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)

        self.tabbar.setElideMode(Qt.ElideLeft)
        self.tabbar.setExpanding(False)

        # ToolBar
        self.ToolBar = QWidget()
        self.toolbar_layout = QHBoxLayout()
        
        # Tools
        self.btnAddTab = QPushButton('+')
        self.btnAddTab.clicked.connect(self.AddTab)

        self.address_bar =  AddressBar()
        self.address_bar.returnPressed.connect(self.BrowseTo)

        self.btn_back = QPushButton('<')
        self.btn_back.clicked.connect(self.Back)

        self.btn_forward = QPushButton('>')
        self.btn_forward.clicked.connect(self.Forward)

        self.btn_refresh = QPushButton('F5')
        self.btn_refresh.clicked.connect(self.Refresh)

        # Add Tools to ToolBar layout
        self.toolbar_layout.addWidget(self.btn_back)
        self.toolbar_layout.addWidget(self.btn_forward)
        self.toolbar_layout.addWidget(self.btn_refresh)
        self.toolbar_layout.addWidget(self.address_bar)
        self.toolbar_layout.addWidget(self.btnAddTab)


        # Container
        self.container = QWidget()
        self.container_layout = QStackedLayout()
        self.container.setLayout(self.container_layout)

        # addLayout to toolbar
        self.ToolBar.setLayout(self.toolbar_layout)

        
        # Adding Widgets to Main Layout
        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.ToolBar)
        self.layout.addWidget(self.container)

        self.AddTab()

        self.setLayout(self.layout)
        self.show()


    def CloseTab(self, i):
        self.tabbar.removeTab(i)

    def AddTab(self):
        if len(self.tabs):
            self.tab_count += 1
        i = self.tab_count

        self.tabs.append(QWidget())
        self.tabs[i].layout  = QHBoxLayout()
        self.tabs[i].setObjectName('tab'+str(i))


        self.tabs[i].layout.setContentsMargins(0,0,0,0)

        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.titleChanged.connect(lambda: self.setTabTitle(i))
        self.tabs[i].content.iconChanged.connect(lambda: self.setTabIcon(i))
        self.tabs[i].content.urlChanged.connect(lambda: self.setAddressBar(i))


        self.tabs[i].content.load(QUrl.fromUserInput('http://www.google.com'))

        self.tabs[i].layout.addWidget(self.tabs[i].content)
        
        self.container_layout.addWidget(self.tabs[i])
        self.tabs[i].setLayout(self.tabs[i].layout)

        self.tabbar.addTab('New Tab')
        self.tabbar.setTabData(i, 'tab'+str(i))
        self.tabbar.setCurrentIndex(i)
        self.container_layout.setCurrentWidget(self.tabs[i])

        self.address_bar.selectAll()
        self.address_bar.setFocus()

    
    def SwitchTab(self, i):

        if self.tabs[i]:
            self.tabbar.currentIndex()
            tabName = self.tabbar.tabData(i)
            tabObj = self.findChild(QWidget, tabName)
            self.container_layout.setCurrentWidget(tabObj)

            url = tabObj.content.url().toString()
            self.address_bar.setText(url)

    def BrowseTo(self):
        text = self.address_bar.text()
        url = ""
        if 'http' not in text:
            if '.' not in text:
                if 'localhost' in text:
                    url = 'http://'+text
                else:
                    url = 'http://google.com/search?q='+text
            else:
                url = 'http://'+text
        else:
            url = text

        i = self.tabbar.currentIndex()
        self.object = self.findChild(QWidget, self.tabbar.tabData(i))
        self.object.content.load(QUrl.fromUserInput(url))
        

    def setTabTitle(self, i):
        tabName = self.tabbar.tabData(i)
        TabObj = self.findChild(QWidget, tabName)
        self.tabbar.setTabText(i, TabObj.content.title())

    def setAddressBar(self, i):
        tabName = self.tabbar.tabData(i)
        url = self.findChild(QWidget, tabName).content.url().toString()

        self.address_bar.setText(url)

    def setTabIcon(self, i):
        tabName = self.tabbar.tabData(i)
        icon = self.findChild(QWidget, tabName).content.icon()
        self.tabbar.setTabIcon(i, icon)

    def Back(self):
        i = self.tabbar.currentIndex()
        self.tabs[i].content.back()

    def Forward(self):
        i = self.tabbar.currentIndex()
        self.tabs[i].content.forward()

    def Refresh(self):
        i = self.tabbar.currentIndex()
        self.tabs[i].content.reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    

    with open('material.css') as style:
        app.setStyleSheet(style.read())

    window = App()

    sys.exit(app.exec_())