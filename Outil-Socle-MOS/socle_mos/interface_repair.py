# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_repair.ui'
#
# Created: Fri Nov  9 10:02:47 2018
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_interface_repair(object):
    def setupUi(self, interface_repair):
        interface_repair.setObjectName(_fromUtf8("interface_repair"))
        interface_repair.resize(406, 222)
        self.verticalLayout = QtGui.QVBoxLayout(interface_repair)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(interface_repair)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.cb_connexion = QtGui.QComboBox(interface_repair)
        self.cb_connexion.setObjectName(_fromUtf8("cb_connexion"))
        self.horizontalLayout.addWidget(self.cb_connexion)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pb_connect = QtGui.QPushButton(interface_repair)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_connect.sizePolicy().hasHeightForWidth())
        self.pb_connect.setSizePolicy(sizePolicy)
        self.pb_connect.setObjectName(_fromUtf8("pb_connect"))
        self.verticalLayout.addWidget(self.pb_connect)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_6 = QtGui.QLabel(interface_repair)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.cb_schema = QtGui.QComboBox(interface_repair)
        self.cb_schema.setObjectName(_fromUtf8("cb_schema"))
        self.horizontalLayout_3.addWidget(self.cb_schema)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_13 = QtGui.QLabel(interface_repair)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_2.addWidget(self.label_13)
        self.cb_table = QtGui.QComboBox(interface_repair)
        self.cb_table.setObjectName(_fromUtf8("cb_table"))
        self.horizontalLayout_2.addWidget(self.cb_table)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pb_repair = QtGui.QPushButton(interface_repair)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_repair.sizePolicy().hasHeightForWidth())
        self.pb_repair.setSizePolicy(sizePolicy)
        self.pb_repair.setObjectName(_fromUtf8("pb_repair"))
        self.verticalLayout.addWidget(self.pb_repair)
        self.lbl_etat = QtGui.QLabel(interface_repair)
        self.lbl_etat.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_etat.setObjectName(_fromUtf8("lbl_etat"))
        self.verticalLayout.addWidget(self.lbl_etat)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(interface_repair)
        QtCore.QMetaObject.connectSlotsByName(interface_repair)

    def retranslateUi(self, interface_repair):
        interface_repair.setWindowTitle(_translate("interface_repair", "Réparation des géométries invalides", None))
        self.label.setText(_translate("interface_repair", "Sélectionner la connexion à la base de donnée", None))
        self.pb_connect.setText(_translate("interface_repair", "Connecter", None))
        self.label_6.setText(_translate("interface_repair", "Sélectionner le schéma", None))
        self.label_13.setText(_translate("interface_repair", "Sélectionner la table", None))
        self.pb_repair.setText(_translate("interface_repair", "Réparer", None))
        self.lbl_etat.setText(_translate("interface_repair", "TextLabel", None))

