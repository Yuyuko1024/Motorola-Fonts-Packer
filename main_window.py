# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 520)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 40, 681, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.edit_font_name = LineEdit(self.horizontalLayoutWidget)
        self.edit_font_name.setObjectName("edit_font_name")
        self.horizontalLayout.addWidget(self.edit_font_name)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(60, 90, 681, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edit_ttf_path = LineEdit(self.horizontalLayoutWidget_2)
        self.edit_ttf_path.setObjectName("edit_ttf_path")
        self.horizontalLayout_2.addWidget(self.edit_ttf_path)
        self.btn_choose_file = PushButton(self.horizontalLayoutWidget_2)
        self.btn_choose_file.setObjectName("btn_choose_file")
        self.horizontalLayout_2.addWidget(self.btn_choose_file)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(430, 200, 311, 51))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_clear = PushButton(self.horizontalLayoutWidget_3)
        self.btn_clear.setObjectName("btn_clear")
        self.horizontalLayout_3.addWidget(self.btn_clear)
        self.btn_pack = PushButton(self.horizontalLayoutWidget_3)
        self.btn_pack.setObjectName("btn_pack")
        self.horizontalLayout_3.addWidget(self.btn_pack)
        self.btn_exit = PushButton(self.horizontalLayoutWidget_3)
        self.btn_exit.setObjectName("btn_exit")
        self.horizontalLayout_3.addWidget(self.btn_exit)
        self.build_output = QtWidgets.QTextBrowser(self.centralwidget)
        self.build_output.setGeometry(QtCore.QRect(50, 270, 690, 190))
        self.build_output.setObjectName("build_output")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(60, 140, 681, 41))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.edit_font_target_name = LineEdit(self.horizontalLayoutWidget_4)
        self.edit_font_target_name.setObjectName("edit_font_target_name")
        self.horizontalLayout_4.addWidget(self.edit_font_target_name)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.edit_pkg_version = LineEdit(self.horizontalLayoutWidget_4)
        self.edit_pkg_version.setObjectName("edit_pkg_version")
        self.horizontalLayout_4.addWidget(self.edit_pkg_version)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menuLanguage = QtWidgets.QMenu(self.menubar)
        self.menuLanguage.setObjectName("menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open_workspace = QtWidgets.QAction(MainWindow)
        self.action_open_workspace.setObjectName("action_open_workspace")
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_Qt = QtWidgets.QAction(MainWindow)
        self.action_Qt.setObjectName("action_Qt")
        self.action_open_tempdir = QtWidgets.QAction(MainWindow)
        self.action_open_tempdir.setObjectName("action_open_tempdir")
        self.actionLangEnglish = QtWidgets.QAction(MainWindow)
        self.actionLangEnglish.setObjectName("actionLangEnglish")
        self.actionLangChs = QtWidgets.QAction(MainWindow)
        self.actionLangChs.setObjectName("actionLangChs")
        self.menu.addAction(self.action_open_workspace)
        self.menu.addSeparator()
        self.menu.addAction(self.action_exit)
        self.menu_2.addAction(self.action_about)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_Qt)
        self.menuLanguage.addAction(self.actionLangEnglish)
        self.menuLanguage.addAction(self.actionLangChs)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())

        self.retranslateUi(MainWindow)
        self.btn_exit.clicked.connect(MainWindow.close) # type: ignore
        self.action_exit.triggered.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Motorola Font Packer"))
        self.label.setText(_translate("MainWindow", "字体包名称"))
        self.label_2.setText(_translate("MainWindow", "选择.ttf字体文件"))
        self.btn_choose_file.setText(_translate("MainWindow", "选择文件"))
        self.btn_clear.setText(_translate("MainWindow", "清除输出"))
        self.btn_pack.setText(_translate("MainWindow", "打包"))
        self.btn_exit.setText(_translate("MainWindow", "退出"))
        self.label_3.setText(_translate("MainWindow", "目标字体名"))
        self.label_4.setText(_translate("MainWindow", "版本号"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "关于"))
        self.menuLanguage.setTitle(_translate("MainWindow", "Language"))
        self.action_open_workspace.setText(_translate("MainWindow", "打开工作目录"))
        self.action_about.setText(_translate("MainWindow", "关于软件"))
        self.action_exit.setText(_translate("MainWindow", "退出"))
        self.action_Qt.setText(_translate("MainWindow", "关于Qt"))
        self.action_open_tempdir.setText(_translate("MainWindow", "打开临时目录"))
        self.actionLangEnglish.setText(_translate("MainWindow", "English"))
        self.actionLangChs.setText(_translate("MainWindow", "简体中文"))
from qfluentwidgets import LineEdit, PushButton
