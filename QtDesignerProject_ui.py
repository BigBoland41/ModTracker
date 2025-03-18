# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'QtDesignerProject.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1000)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tableWidget = QTableWidget(self.centralwidget)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        font = QFont()
        font.setPointSize(14)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget.rowCount() < 5):
            self.tableWidget.setRowCount(5)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        self.tableWidget.setItem(0, 0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setItem(0, 1, __qtablewidgetitem4)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        brush1 = QBrush(QColor(0, 255, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setBackground(brush1);
        __qtablewidgetitem5.setForeground(brush);
        self.tableWidget.setItem(0, 2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setItem(1, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setItem(1, 1, __qtablewidgetitem7)
        brush2 = QBrush(QColor(255, 85, 0, 255))
        brush2.setStyle(Qt.SolidPattern)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setBackground(brush2);
        __qtablewidgetitem8.setForeground(brush);
        self.tableWidget.setItem(1, 2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget.setItem(2, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget.setItem(2, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setBackground(brush1);
        __qtablewidgetitem11.setForeground(brush);
        self.tableWidget.setItem(2, 2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget.setItem(3, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget.setItem(3, 1, __qtablewidgetitem13)
        brush3 = QBrush(QColor(255, 255, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setBackground(brush3);
        __qtablewidgetitem14.setForeground(brush);
        self.tableWidget.setItem(3, 2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget.setItem(4, 0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget.setItem(4, 1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setBackground(brush1);
        __qtablewidgetitem17.setForeground(brush);
        self.tableWidget.setItem(4, 2, __qtablewidgetitem17)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(0, -10, 1000, 900))
        self.tableWidget.setFont(font)
        self.addModTextField = QLineEdit(self.centralwidget)
        self.addModTextField.setObjectName(u"addModTextField")
        self.addModTextField.setGeometry(QRect(0, 900, 800, 70))
        font1 = QFont()
        font1.setPointSize(12)
        self.addModTextField.setFont(font1)
        self.addModBtn = QPushButton(self.centralwidget)
        self.addModBtn.setObjectName(u"addModBtn")
        self.addModBtn.setGeometry(QRect(800, 900, 200, 70))
        font2 = QFont()
        font2.setPointSize(18)
        self.addModBtn.setFont(font2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mod Tracker", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Mod Name", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Latest Version", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Ready/Priority", None));

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem3 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Sodium", None));
        ___qtablewidgetitem4 = self.tableWidget.item(0, 1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"1.21.4", None));
        ___qtablewidgetitem5 = self.tableWidget.item(0, 2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Ready", None));
        ___qtablewidgetitem6 = self.tableWidget.item(1, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Continuity", None));
        ___qtablewidgetitem7 = self.tableWidget.item(1, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"1.20.6", None));
        ___qtablewidgetitem8 = self.tableWidget.item(1, 2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"High Priority", None));
        ___qtablewidgetitem9 = self.tableWidget.item(2, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Entity Culling", None));
        ___qtablewidgetitem10 = self.tableWidget.item(2, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"1.21.4", None));
        ___qtablewidgetitem11 = self.tableWidget.item(2, 2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Ready", None));
        ___qtablewidgetitem12 = self.tableWidget.item(3, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Fabric Skyboxes", None));
        ___qtablewidgetitem13 = self.tableWidget.item(3, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"1.21.1", None));
        ___qtablewidgetitem14 = self.tableWidget.item(3, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Non-essential", None));
        ___qtablewidgetitem15 = self.tableWidget.item(4, 0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Enhanced Block Entities", None));
        ___qtablewidgetitem16 = self.tableWidget.item(4, 1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"1.21.4", None));
        ___qtablewidgetitem17 = self.tableWidget.item(4, 2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Ready", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.addModTextField.setText(QCoreApplication.translate("MainWindow", u"Enter mod URL here", None))
        self.addModBtn.setText(QCoreApplication.translate("MainWindow", u"Add Mod", None))
    # retranslateUi

