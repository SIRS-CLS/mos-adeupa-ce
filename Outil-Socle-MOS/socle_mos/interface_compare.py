# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_compare.ui'
#
# Created: Tue Nov 13 13:50:03 2018
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_interface_compare(object):
    def setupUi(self, interface_compare):
        interface_compare.setObjectName(_fromUtf8("interface_compare"))
        interface_compare.resize(578, 309)
        interface_compare.setMaximumSize(QtCore.QSize(16777215, 16777215))
        interface_compare.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(interface_compare)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(interface_compare)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.cb_connexion = QtGui.QComboBox(interface_compare)
        self.cb_connexion.setObjectName(_fromUtf8("cb_connexion"))
        self.horizontalLayout_2.addWidget(self.cb_connexion)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pb_dbConnect = QtGui.QPushButton(interface_compare)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_dbConnect.sizePolicy().hasHeightForWidth())
        self.pb_dbConnect.setSizePolicy(sizePolicy)
        self.pb_dbConnect.setObjectName(_fromUtf8("pb_dbConnect"))
        self.verticalLayout.addWidget(self.pb_dbConnect)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(interface_compare)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.cb_schema_desti = QtGui.QComboBox(interface_compare)
        self.cb_schema_desti.setObjectName(_fromUtf8("cb_schema_desti"))
        self.horizontalLayout.addWidget(self.cb_schema_desti)
        self.label_3 = QtGui.QLabel(interface_compare)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.le_table_desti = QtGui.QLineEdit(interface_compare)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_table_desti.sizePolicy().hasHeightForWidth())
        self.le_table_desti.setSizePolicy(sizePolicy)
        self.le_table_desti.setObjectName(_fromUtf8("le_table_desti"))
        self.horizontalLayout.addWidget(self.le_table_desti)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtGui.QScrollArea(interface_compare)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 541, 112))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_5 = QtGui.QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_5.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.cb_schema_t1 = QtGui.QComboBox(self.groupBox_5)
        self.cb_schema_t1.setObjectName(_fromUtf8("cb_schema_t1"))
        self.gridLayout_5.addWidget(self.cb_schema_t1, 1, 1, 1, 1)
        self.cb_table_t1 = QtGui.QComboBox(self.groupBox_5)
        self.cb_table_t1.setObjectName(_fromUtf8("cb_table_t1"))
        self.gridLayout_5.addWidget(self.cb_table_t1, 2, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_5.addWidget(self.label_14, 1, 0, 1, 1)
        self.label_60 = QtGui.QLabel(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_60.sizePolicy().hasHeightForWidth())
        self.label_60.setSizePolicy(sizePolicy)
        self.label_60.setObjectName(_fromUtf8("label_60"))
        self.gridLayout_5.addWidget(self.label_60, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_4 = QtGui.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_26 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout.addWidget(self.label_26, 0, 0, 1, 1)
        self.label_27 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.gridLayout.addWidget(self.label_27, 1, 0, 1, 1)
        self.cb_schema_t0 = QtGui.QComboBox(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_schema_t0.sizePolicy().hasHeightForWidth())
        self.cb_schema_t0.setSizePolicy(sizePolicy)
        self.cb_schema_t0.setObjectName(_fromUtf8("cb_schema_t0"))
        self.gridLayout.addWidget(self.cb_schema_t0, 0, 1, 1, 1)
        self.cb_table_t0 = QtGui.QComboBox(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_table_t0.sizePolicy().hasHeightForWidth())
        self.cb_table_t0.setSizePolicy(sizePolicy)
        self.cb_table_t0.setObjectName(_fromUtf8("cb_table_t0"))
        self.gridLayout.addWidget(self.cb_table_t0, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        self.pb_start = QtGui.QPushButton(interface_compare)
        self.pb_start.setObjectName(_fromUtf8("pb_start"))
        self.verticalLayout.addWidget(self.pb_start)
        self.lbl_etape = QtGui.QLabel(interface_compare)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_etape.sizePolicy().hasHeightForWidth())
        self.lbl_etape.setSizePolicy(sizePolicy)
        self.lbl_etape.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_etape.setObjectName(_fromUtf8("lbl_etape"))
        self.verticalLayout.addWidget(self.lbl_etape)
        self.pb_avancement = QtGui.QProgressBar(interface_compare)
        self.pb_avancement.setProperty("value", 24)
        self.pb_avancement.setObjectName(_fromUtf8("pb_avancement"))
        self.verticalLayout.addWidget(self.pb_avancement)

        self.retranslateUi(interface_compare)
        QtCore.QMetaObject.connectSlotsByName(interface_compare)

    def retranslateUi(self, interface_compare):
        interface_compare.setWindowTitle(_translate("interface_compare", "Création de MOS", None))
        self.label.setText(_translate("interface_compare", "Sélectionner la connexion à la base de donnée", None))
        self.pb_dbConnect.setText(_translate("interface_compare", "Connecter", None))
        self.label_2.setText(_translate("interface_compare", "Schéma destination", None))
        self.label_3.setText(_translate("interface_compare", "Table destination", None))
        self.groupBox_5.setTitle(_translate("interface_compare", "Socle T-1", None))
        self.label_14.setText(_translate("interface_compare", "Schéma T-1", None))
        self.label_60.setText(_translate("interface_compare", "Table T-1", None))
        self.groupBox_4.setTitle(_translate("interface_compare", "Socle T0", None))
        self.label_26.setText(_translate("interface_compare", "Schéma T0", None))
        self.label_27.setText(_translate("interface_compare", "Table T0", None))
        self.pb_start.setText(_translate("interface_compare", "Start", None))
        self.lbl_etape.setText(_translate("interface_compare", "TextLabel", None))

