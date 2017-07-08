# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/initwindow.ui'
#
# Created: Fri Jul  7 11:51:13 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(342, 114)
        Dialog.setWindowTitle(_fromUtf8(""))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_nombre = QtGui.QLabel(Dialog)
        self.label_nombre.setObjectName(_fromUtf8("label_nombre"))
        self.horizontalLayout.addWidget(self.label_nombre)
        self.lineedit_project_name = QtGui.QLineEdit(Dialog)
        self.lineedit_project_name.setObjectName(_fromUtf8("lineedit_project_name"))
        self.horizontalLayout.addWidget(self.lineedit_project_name)
        self.label_group = QtGui.QLabel(Dialog)
        self.label_group.setObjectName(_fromUtf8("label_group"))
        self.horizontalLayout.addWidget(self.label_group)
        self.combobox_term_group = QtGui.QComboBox(Dialog)
        self.combobox_term_group.setObjectName(_fromUtf8("combobox_term_group"))
        self.horizontalLayout.addWidget(self.combobox_term_group)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.lineedit_log_path = QtGui.QLineEdit(Dialog)
        self.lineedit_log_path.setMouseTracking(True)
        self.lineedit_log_path.setAutoFillBackground(True)
        self.lineedit_log_path.setReadOnly(True)
        self.lineedit_log_path.setObjectName(_fromUtf8("lineedit_log_path"))
        self.horizontalLayout_2.addWidget(self.lineedit_log_path)
        self.button_log_path = QtGui.QPushButton(Dialog)
        self.button_log_path.setObjectName(_fromUtf8("button_log_path"))
        self.horizontalLayout_2.addWidget(self.button_log_path)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.label_nombre.setText(_translate("Dialog", "Project name:", None))
        self.label_group.setText(_translate("Dialog", "Terminals group:", None))
        self.label.setText(_translate("Dialog", "Logs path: ", None))
        self.button_log_path.setText(_translate("Dialog", "&Select", None))

