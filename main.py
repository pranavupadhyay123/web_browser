import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QFont

class TabWidget(QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.new_tab()

    def new_tab(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl('https://google.com'))
        index = self.addTab(browser, 'New Tab')
        self.setCurrentIndex(index)
        browser.urlChanged.connect(lambda q, browser=browser: self.update_url(q, browser))

    def close_tab(self, index):
        if self.count() > 1:
            widget = self.widget(index)
            widget.deleteLater()
            self.removeTab(index)

    def update_url(self, q, browser):
        index = self.indexOf(browser)
        self.setTabText(index, q.toString())

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tabs = TabWidget()
        self.setCentralWidget(self.tabs)
        self.showMaximized()

        # Navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('<<', self)
        back_btn.triggered.connect(self.active_browser().back)
        navbar.addAction(back_btn)

        reload_btn = QAction('O', self)
        reload_btn.triggered.connect(self.active_browser().reload)
        navbar.addAction(reload_btn)

        forward_btn = QAction('>>', self)
        forward_btn.triggered.connect(self.active_browser().forward)
        navbar.addAction(forward_btn)

        home_btn = QAction('Youtube', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        new_tab_btn = QAction('+', self)
        new_tab_btn.triggered.connect(self.tabs.new_tab)
        navbar.addAction(new_tab_btn)

        font = QFont()
        font.setPointSize(14)  # Change the point size as needed
        back_btn.setFont(font)
        forward_btn.setFont(font)
        reload_btn.setFont(font)
        home_btn.setFont(font)

        new_tab_font = QFont()
        new_tab_font.setPointSize(25)  # Change the point size as needed for the new_tab_btn
        new_tab_btn.setFont(new_tab_font)

        self.tabs.currentChanged.connect(self.tab_changed)

    def navigate_home(self):
        self.active_browser().setUrl(QUrl('https://youtube.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.active_browser().setUrl(QUrl(url))

    def tab_changed(self):
        self.url_bar.setText(self.active_browser().url().toString())

    def active_browser(self):
        return self.tabs.currentWidget()

app = QApplication(sys.argv)
QApplication.setApplicationName('My Cool Browser')
window = MainWindow()
app.exec_()
