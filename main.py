import youtube_dl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os


class Ui_MainWindow(object):
    def __init__(self):
        print("noo it initing")
        self.downloadQueueList = []
        self.downloadedList = []
        print(self.downloadQueueList)

        self.ydl_opts = {
            'format': 'mp4',
            'writethumbnail': True,
        }

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(430, 350)
        MainWindow.setWindowOpacity(0.99)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.downloadAll = QtWidgets.QPushButton(self.centralwidget)
        self.downloadAll.setGeometry(QtCore.QRect(290, 90, 141, 81))
        self.downloadAll.setObjectName("downloadAll")
        self.urlHere = QtWidgets.QLineEdit(self.centralwidget)
        self.urlHere.setGeometry(QtCore.QRect(10, 10, 371, 31))
        self.urlHere.setObjectName("urlHere")
        self.add = QtWidgets.QPushButton(self.centralwidget)
        self.add.setGeometry(QtCore.QRect(290, 50, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.add.setFont(font)
        self.add.setObjectName("add")
        self.lbList = QtWidgets.QListWidget(self.centralwidget)
        self.lbList.setGeometry(QtCore.QRect(10, 50, 281, 131))
        self.lbList.setObjectName("lbList")
        self.lblthumbnail = QtWidgets.QLabel(self.centralwidget)
        self.lblthumbnail.setGeometry(QtCore.QRect(290, 170, 141, 101))
        self.lblthumbnail.setToolTipDuration(-9)
        self.lblthumbnail.setFrameShape(QtWidgets.QFrame.Box)
        self.lblthumbnail.setLineWidth(0)
        self.lblthumbnail.setText("")
        self.lblthumbnail.setObjectName("lblthumbnail")
        self.lbldownloaded = QtWidgets.QListWidget(self.centralwidget)
        self.lbldownloaded.setGeometry(QtCore.QRect(10, 190, 281, 131))
        self.lbldownloaded.setObjectName("lbldownloaded")
        self.outOf = QtWidgets.QLabel(self.centralwidget)
        self.outOf.setGeometry(QtCore.QRect(350, 280, 81, 41))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.outOf.setFont(font)
        self.outOf.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.outOf.setFrameShape(QtWidgets.QFrame.Box)
        self.outOf.setLineWidth(0)
        self.outOf.setScaledContents(False)
        self.outOf.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.outOf.setWordWrap(False)
        self.outOf.setObjectName("outOf")
        self.quicdl = QtWidgets.QPushButton(self.centralwidget)
        self.quicdl.setGeometry(QtCore.QRect(380, 0, 51, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.quicdl.setFont(font)
        self.quicdl.setText("")
        self.quicdl.setIcon(QIcon('quicDownloadBtn.png'))
        self.quicdl.setObjectName("quicdl")
        self.relaunch = QtWidgets.QPushButton(self.centralwidget)
        self.relaunch.setGeometry(QtCore.QRect(290, 280, 71, 41))
        self.relaunch.setObjectName("relaunch")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 430, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.add.clicked.connect(self.addItem)
        self.relaunch.clicked.connect(self.restart_program)
        self.quicdl.clicked.connect(self.quic_download)
        self.downloadAll.clicked.connect(self.download_all)

    def restart_program(self):
        """Restarts the current program, with file objects and descriptors
           cleanup
        """
        os.execl(sys.executable, *([sys.executable] + sys.argv))

    def quic_download(self):
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([self.urlHere.text()])

            self.urlHere.clear()

        except:
            self.urlHere.setText(("please inpiut a valid url"))

    def download_all(self):
        print("starting all download")
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            for x in self.downloadQueueList:
                ydl.download([x])

        items = []
        for index in range(self.lbList.count()):
            items.append(self.lbList.item(index))

        for item in items:
            self.lbldownloaded.addItem(item.text())

        self.downloadedList.append(self.downloadQueueList)
        self.downloadQueueList = []
        self.lbList.clear()

    def addItem(self):
        try:
            url = self.urlHere.text()
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                meta = ydl.extract_info(url, download=False)
                formats = meta.get('name', [meta])

            expo = None
            for f in formats:
                expo = str(f['title'])

            self.downloadQueueList.append(url)

            self.lbList.addItem(expo)
            self.urlHere.clear()

        except:
            self.urlHere.setText(("please inpiut a valid url"))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.downloadAll.setText(_translate("MainWindow", "Download all"))
        self.urlHere.setToolTip(_translate("MainWindow", "put url inside and hit add"))
        self.urlHere.setText(_translate("MainWindow", "url here:"))
        self.add.setText(_translate("MainWindow", "add to list"))
        self.outOf.setText(_translate("MainWindow", "0/0"))
        self.relaunch.setText(_translate("MainWindow", "restart"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
