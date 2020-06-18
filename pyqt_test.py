# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 17:10:55 2020

@author: Jerry
"""

import bs4 as bs
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    page = Page('https://www.ratebeer.com/brewers/avondale-brewing-company/12890/')
    soup = bs.BeautifulSoup(page.html, 'html.parser')
#    js_test = soup.find('p', class_='jstest')
    print(soup.text)

if __name__ == '__main__': main()