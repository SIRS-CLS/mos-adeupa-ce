# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_socle.ui'
#
# Created: Fri Nov 16 12:33:40 2018
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

class Ui_interface_socle(object):
    def setupUi(self, interface_socle):
        interface_socle.setObjectName(_fromUtf8("interface_socle"))
        interface_socle.resize(815, 576)
        interface_socle.setMaximumSize(QtCore.QSize(16777215, 16777215))
        interface_socle.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(interface_socle)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(interface_socle)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.cb_connexion = QtGui.QComboBox(interface_socle)
        self.cb_connexion.setObjectName(_fromUtf8("cb_connexion"))
        self.horizontalLayout_2.addWidget(self.cb_connexion)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pb_dbConnect = QtGui.QPushButton(interface_socle)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_dbConnect.sizePolicy().hasHeightForWidth())
        self.pb_dbConnect.setSizePolicy(sizePolicy)
        self.pb_dbConnect.setObjectName(_fromUtf8("pb_dbConnect"))
        self.verticalLayout.addWidget(self.pb_dbConnect)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_6 = QtGui.QLabel(interface_socle)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.cb_schema = QtGui.QComboBox(interface_socle)
        self.cb_schema.setObjectName(_fromUtf8("cb_schema"))
        self.horizontalLayout.addWidget(self.cb_schema)
        self.label_13 = QtGui.QLabel(interface_socle)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout.addWidget(self.label_13)
        self.le_destination = QtGui.QLineEdit(interface_socle)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_destination.sizePolicy().hasHeightForWidth())
        self.le_destination.setSizePolicy(sizePolicy)
        self.le_destination.setObjectName(_fromUtf8("le_destination"))
        self.horizontalLayout.addWidget(self.le_destination)
        self.label_2 = QtGui.QLabel(interface_socle)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.le_annee = QtGui.QLineEdit(interface_socle)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_annee.sizePolicy().hasHeightForWidth())
        self.le_annee.setSizePolicy(sizePolicy)
        self.le_annee.setObjectName(_fromUtf8("le_annee"))
        self.horizontalLayout.addWidget(self.le_annee)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtGui.QScrollArea(interface_socle)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 778, 618))
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
        self.label_14 = QtGui.QLabel(self.groupBox_5)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_5.addWidget(self.label_14, 1, 0, 1, 1)
        self.cb_parcelle_bdtopo = QtGui.QComboBox(self.groupBox_5)
        self.cb_parcelle_bdtopo.setObjectName(_fromUtf8("cb_parcelle_bdtopo"))
        self.gridLayout_5.addWidget(self.cb_parcelle_bdtopo, 1, 1, 1, 1)
        self.cb_parcellaire = QtGui.QComboBox(self.groupBox_5)
        self.cb_parcellaire.setObjectName(_fromUtf8("cb_parcellaire"))
        self.gridLayout_5.addWidget(self.cb_parcellaire, 2, 1, 1, 1)
        self.label_60 = QtGui.QLabel(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_60.sizePolicy().hasHeightForWidth())
        self.label_60.setSizePolicy(sizePolicy)
        self.label_60.setObjectName(_fromUtf8("label_60"))
        self.gridLayout_5.addWidget(self.label_60, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox = QtGui.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_4.addWidget(self.label_7, 1, 0, 1, 1)
        self.cb_parcelle = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_parcelle.sizePolicy().hasHeightForWidth())
        self.cb_parcelle.setSizePolicy(sizePolicy)
        self.cb_parcelle.setObjectName(_fromUtf8("cb_parcelle"))
        self.gridLayout_4.addWidget(self.cb_parcelle, 1, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 2, 0, 1, 1)
        self.cb_subparc = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_subparc.sizePolicy().hasHeightForWidth())
        self.cb_subparc.setSizePolicy(sizePolicy)
        self.cb_subparc.setObjectName(_fromUtf8("cb_subparc"))
        self.gridLayout_4.addWidget(self.cb_subparc, 2, 1, 1, 1)
        self.cb_tronroute = QtGui.QComboBox(self.groupBox)
        self.cb_tronroute.setObjectName(_fromUtf8("cb_tronroute"))
        self.gridLayout_4.addWidget(self.cb_tronroute, 3, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 4, 0, 1, 1)
        self.cb_tronfluv = QtGui.QComboBox(self.groupBox)
        self.cb_tronfluv.setObjectName(_fromUtf8("cb_tronfluv"))
        self.gridLayout_4.addWidget(self.cb_tronfluv, 4, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_4.addWidget(self.label_11, 5, 0, 1, 1)
        self.cb_tsurf = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_tsurf.sizePolicy().hasHeightForWidth())
        self.cb_tsurf.setSizePolicy(sizePolicy)
        self.cb_tsurf.setObjectName(_fromUtf8("cb_tsurf"))
        self.gridLayout_4.addWidget(self.cb_tsurf, 5, 1, 1, 1)
        self.cb_geobati = QtGui.QComboBox(self.groupBox)
        self.cb_geobati.setObjectName(_fromUtf8("cb_geobati"))
        self.gridLayout_4.addWidget(self.cb_geobati, 6, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_4.addWidget(self.label_12, 6, 0, 1, 1)
        self.cb_section = QtGui.QComboBox(self.groupBox)
        self.cb_section.setObjectName(_fromUtf8("cb_section"))
        self.gridLayout_4.addWidget(self.cb_section, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.cb_res_sport = QtGui.QComboBox(self.groupBox_3)
        self.cb_res_sport.setObjectName(_fromUtf8("cb_res_sport"))
        self.gridLayout_3.addWidget(self.cb_res_sport, 6, 1, 1, 1)
        self.label_18 = QtGui.QLabel(self.groupBox_3)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_3.addWidget(self.label_18, 2, 0, 1, 1)
        self.cb_ipli = QtGui.QComboBox(self.groupBox_3)
        self.cb_ipli.setObjectName(_fromUtf8("cb_ipli"))
        self.gridLayout_3.addWidget(self.cb_ipli, 2, 1, 1, 1)
        self.label_57 = QtGui.QLabel(self.groupBox_3)
        self.label_57.setObjectName(_fromUtf8("label_57"))
        self.gridLayout_3.addWidget(self.label_57, 5, 0, 1, 1)
        self.label_58 = QtGui.QLabel(self.groupBox_3)
        self.label_58.setObjectName(_fromUtf8("label_58"))
        self.gridLayout_3.addWidget(self.label_58, 6, 0, 1, 1)
        self.cb_finess = QtGui.QComboBox(self.groupBox_3)
        self.cb_finess.setObjectName(_fromUtf8("cb_finess"))
        self.gridLayout_3.addWidget(self.cb_finess, 5, 1, 1, 1)
        self.label_61 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_61.sizePolicy().hasHeightForWidth())
        self.label_61.setSizePolicy(sizePolicy)
        self.label_61.setObjectName(_fromUtf8("label_61"))
        self.gridLayout_3.addWidget(self.label_61, 0, 0, 1, 1)
        self.cb_ff_parcelle = QtGui.QComboBox(self.groupBox_3)
        self.cb_ff_parcelle.setObjectName(_fromUtf8("cb_ff_parcelle"))
        self.gridLayout_3.addWidget(self.cb_ff_parcelle, 0, 1, 1, 1)
        self.label_56 = QtGui.QLabel(self.groupBox_3)
        self.label_56.setObjectName(_fromUtf8("label_56"))
        self.gridLayout_3.addWidget(self.label_56, 1, 0, 1, 1)
        self.cb_rpga = QtGui.QComboBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_rpga.sizePolicy().hasHeightForWidth())
        self.cb_rpga.setSizePolicy(sizePolicy)
        self.cb_rpga.setObjectName(_fromUtf8("cb_rpga"))
        self.gridLayout_3.addWidget(self.cb_rpga, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
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
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_3.addWidget(self.label_5)
        self.rb_geom = QtGui.QRadioButton(self.groupBox_4)
        self.rb_geom.setObjectName(_fromUtf8("rb_geom"))
        self.btgr_geom = QtGui.QButtonGroup(interface_socle)
        self.btgr_geom.setObjectName(_fromUtf8("btgr_geom"))
        self.btgr_geom.addButton(self.rb_geom)
        self.horizontalLayout_3.addWidget(self.rb_geom)
        self.rb_the_geom = QtGui.QRadioButton(self.groupBox_4)
        self.rb_the_geom.setObjectName(_fromUtf8("rb_the_geom"))
        self.btgr_geom.addButton(self.rb_the_geom)
        self.horizontalLayout_3.addWidget(self.rb_the_geom)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.label_26 = QtGui.QLabel(self.groupBox_4)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout.addWidget(self.label_26, 1, 0, 1, 1)
        self.cb_pai_cult = QtGui.QComboBox(self.groupBox_4)
        self.cb_pai_cult.setObjectName(_fromUtf8("cb_pai_cult"))
        self.gridLayout.addWidget(self.cb_pai_cult, 1, 1, 1, 1)
        self.label_27 = QtGui.QLabel(self.groupBox_4)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.gridLayout.addWidget(self.label_27, 2, 0, 1, 1)
        self.cb_paitransp = QtGui.QComboBox(self.groupBox_4)
        self.cb_paitransp.setObjectName(_fromUtf8("cb_paitransp"))
        self.gridLayout.addWidget(self.cb_paitransp, 2, 1, 1, 1)
        self.label_28 = QtGui.QLabel(self.groupBox_4)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.gridLayout.addWidget(self.label_28, 3, 0, 1, 1)
        self.cb_paisante = QtGui.QComboBox(self.groupBox_4)
        self.cb_paisante.setObjectName(_fromUtf8("cb_paisante"))
        self.gridLayout.addWidget(self.cb_paisante, 3, 1, 1, 1)
        self.label_29 = QtGui.QLabel(self.groupBox_4)
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.gridLayout.addWidget(self.label_29, 4, 0, 1, 1)
        self.cb_pairel = QtGui.QComboBox(self.groupBox_4)
        self.cb_pairel.setObjectName(_fromUtf8("cb_pairel"))
        self.gridLayout.addWidget(self.cb_pairel, 4, 1, 1, 1)
        self.label_22 = QtGui.QLabel(self.groupBox_4)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridLayout.addWidget(self.label_22, 5, 0, 1, 1)
        self.cb_paimilit = QtGui.QComboBox(self.groupBox_4)
        self.cb_paimilit.setObjectName(_fromUtf8("cb_paimilit"))
        self.gridLayout.addWidget(self.cb_paimilit, 5, 1, 1, 1)
        self.label_23 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout.addWidget(self.label_23, 6, 0, 1, 1)
        self.cb_paiens = QtGui.QComboBox(self.groupBox_4)
        self.cb_paiens.setObjectName(_fromUtf8("cb_paiens"))
        self.gridLayout.addWidget(self.cb_paiens, 6, 1, 1, 1)
        self.label_24 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.gridLayout.addWidget(self.label_24, 7, 0, 1, 1)
        self.cb_paicom = QtGui.QComboBox(self.groupBox_4)
        self.cb_paicom.setObjectName(_fromUtf8("cb_paicom"))
        self.gridLayout.addWidget(self.cb_paicom, 7, 1, 1, 1)
        self.label_25 = QtGui.QLabel(self.groupBox_4)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridLayout.addWidget(self.label_25, 8, 0, 1, 1)
        self.cb_paisport = QtGui.QComboBox(self.groupBox_4)
        self.cb_paisport.setObjectName(_fromUtf8("cb_paisport"))
        self.gridLayout.addWidget(self.cb_paisport, 8, 1, 1, 1)
        self.label_53 = QtGui.QLabel(self.groupBox_4)
        self.label_53.setObjectName(_fromUtf8("label_53"))
        self.gridLayout.addWidget(self.label_53, 9, 0, 1, 1)
        self.cb_paitransfo = QtGui.QComboBox(self.groupBox_4)
        self.cb_paitransfo.setObjectName(_fromUtf8("cb_paitransfo"))
        self.gridLayout.addWidget(self.cb_paitransfo, 9, 1, 1, 1)
        self.label_54 = QtGui.QLabel(self.groupBox_4)
        self.label_54.setObjectName(_fromUtf8("label_54"))
        self.gridLayout.addWidget(self.label_54, 10, 0, 1, 1)
        self.cb_cime = QtGui.QComboBox(self.groupBox_4)
        self.cb_cime.setObjectName(_fromUtf8("cb_cime"))
        self.gridLayout.addWidget(self.cb_cime, 10, 1, 1, 1)
        self.label_55 = QtGui.QLabel(self.groupBox_4)
        self.label_55.setObjectName(_fromUtf8("label_55"))
        self.gridLayout.addWidget(self.label_55, 11, 0, 1, 1)
        self.cb_terrainsport = QtGui.QComboBox(self.groupBox_4)
        self.cb_terrainsport.setObjectName(_fromUtf8("cb_terrainsport"))
        self.gridLayout.addWidget(self.cb_terrainsport, 11, 1, 1, 1)
        self.label_59 = QtGui.QLabel(self.groupBox_4)
        self.label_59.setObjectName(_fromUtf8("label_59"))
        self.gridLayout.addWidget(self.label_59, 12, 0, 1, 1)
        self.cb_zoneveget = QtGui.QComboBox(self.groupBox_4)
        self.cb_zoneveget.setObjectName(_fromUtf8("cb_zoneveget"))
        self.gridLayout.addWidget(self.cb_zoneveget, 12, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 13, 0, 1, 1)
        self.cb_route = QtGui.QComboBox(self.groupBox_4)
        self.cb_route.setObjectName(_fromUtf8("cb_route"))
        self.gridLayout.addWidget(self.cb_route, 13, 1, 1, 1)
        self.label_19 = QtGui.QLabel(self.groupBox_4)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout.addWidget(self.label_19, 14, 0, 1, 1)
        self.cb_remarquable = QtGui.QComboBox(self.groupBox_4)
        self.cb_remarquable.setObjectName(_fromUtf8("cb_remarquable"))
        self.gridLayout.addWidget(self.cb_remarquable, 14, 1, 1, 1)
        self.label_20 = QtGui.QLabel(self.groupBox_4)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout.addWidget(self.label_20, 15, 0, 1, 1)
        self.cb_indust = QtGui.QComboBox(self.groupBox_4)
        self.cb_indust.setObjectName(_fromUtf8("cb_indust"))
        self.gridLayout.addWidget(self.cb_indust, 15, 1, 1, 1)
        self.label_21 = QtGui.QLabel(self.groupBox_4)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout.addWidget(self.label_21, 16, 0, 1, 1)
        self.cb_indif = QtGui.QComboBox(self.groupBox_4)
        self.cb_indif.setObjectName(_fromUtf8("cb_indif"))
        self.gridLayout.addWidget(self.cb_indif, 16, 1, 1, 1)
        self.label_30 = QtGui.QLabel(self.groupBox_4)
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.gridLayout.addWidget(self.label_30, 17, 0, 1, 1)
        self.cb_surf_eau = QtGui.QComboBox(self.groupBox_4)
        self.cb_surf_eau.setObjectName(_fromUtf8("cb_surf_eau"))
        self.gridLayout.addWidget(self.cb_surf_eau, 17, 1, 1, 1)
        self.label_31 = QtGui.QLabel(self.groupBox_4)
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.gridLayout.addWidget(self.label_31, 18, 0, 1, 1)
        self.cb_pt_eau = QtGui.QComboBox(self.groupBox_4)
        self.cb_pt_eau.setObjectName(_fromUtf8("cb_pt_eau"))
        self.gridLayout.addWidget(self.cb_pt_eau, 18, 1, 1, 1)
        self.label_50 = QtGui.QLabel(self.groupBox_4)
        self.label_50.setObjectName(_fromUtf8("label_50"))
        self.gridLayout.addWidget(self.label_50, 19, 0, 1, 1)
        self.cb_surf_acti = QtGui.QComboBox(self.groupBox_4)
        self.cb_surf_acti.setObjectName(_fromUtf8("cb_surf_acti"))
        self.gridLayout.addWidget(self.cb_surf_acti, 19, 1, 1, 1)
        self.label_51 = QtGui.QLabel(self.groupBox_4)
        self.label_51.setObjectName(_fromUtf8("label_51"))
        self.gridLayout.addWidget(self.label_51, 20, 0, 1, 1)
        self.cb_triage = QtGui.QComboBox(self.groupBox_4)
        self.cb_triage.setObjectName(_fromUtf8("cb_triage"))
        self.gridLayout.addWidget(self.cb_triage, 20, 1, 1, 1)
        self.label_52 = QtGui.QLabel(self.groupBox_4)
        self.label_52.setObjectName(_fromUtf8("label_52"))
        self.gridLayout.addWidget(self.label_52, 21, 0, 1, 1)
        self.cb_voiefer = QtGui.QComboBox(self.groupBox_4)
        self.cb_voiefer.setObjectName(_fromUtf8("cb_voiefer"))
        self.gridLayout.addWidget(self.cb_voiefer, 21, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        self.pb_start = QtGui.QPushButton(interface_socle)
        self.pb_start.setObjectName(_fromUtf8("pb_start"))
        self.verticalLayout.addWidget(self.pb_start)
        self.lbl_etape = QtGui.QLabel(interface_socle)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_etape.sizePolicy().hasHeightForWidth())
        self.lbl_etape.setSizePolicy(sizePolicy)
        self.lbl_etape.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_etape.setObjectName(_fromUtf8("lbl_etape"))
        self.verticalLayout.addWidget(self.lbl_etape)
        self.pb_avancement = QtGui.QProgressBar(interface_socle)
        self.pb_avancement.setProperty("value", 24)
        self.pb_avancement.setObjectName(_fromUtf8("pb_avancement"))
        self.verticalLayout.addWidget(self.pb_avancement)

        self.retranslateUi(interface_socle)
        QtCore.QMetaObject.connectSlotsByName(interface_socle)

    def retranslateUi(self, interface_socle):
        interface_socle.setWindowTitle(_translate("interface_socle", "Création d\'un socle (t0)", None))
        self.label.setText(_translate("interface_socle", "Sélectionner la connexion à la base de données", None))
        self.pb_dbConnect.setText(_translate("interface_socle", "Connecter", None))
        self.label_6.setText(_translate("interface_socle", "Schema destination", None))
        self.label_13.setText(_translate("interface_socle", "Couche destination", None))
        self.label_2.setText(_translate("interface_socle", "Année", None))
        self.groupBox_5.setTitle(_translate("interface_socle", "Emprise", None))
        self.label_14.setText(_translate("interface_socle", "Limite communes BD Topo", None))
        self.label_60.setText(_translate("interface_socle", "Limite communes BD Parcellaire", None))
        self.groupBox.setTitle(_translate("interface_socle", "Edigeo", None))
        self.label_7.setText(_translate("interface_socle", "Parcelles", None))
        self.label_8.setText(_translate("interface_socle", "Sous-parcelles", None))
        self.label_9.setText(_translate("interface_socle", "Tronçon Route", None))
        self.label_10.setText(_translate("interface_socle", "Tronçon fleuve", None))
        self.label_11.setText(_translate("interface_socle", "Tsurf", None))
        self.label_12.setText(_translate("interface_socle", "Bâtiments", None))
        self.label_4.setText(_translate("interface_socle", "Sections", None))
        self.groupBox_3.setTitle(_translate("interface_socle", "Autre", None))
        self.label_18.setText(_translate("interface_socle", "IPLI", None))
        self.label_57.setText(_translate("interface_socle", "FINESS", None))
        self.label_58.setText(_translate("interface_socle", "RES sportif", None))
        self.label_61.setText(_translate("interface_socle", "FF pnb10_parcelle", None))
        self.label_56.setText(_translate("interface_socle", "RPGA", None))
        self.groupBox_4.setTitle(_translate("interface_socle", "IGN", None))
        self.label_5.setText(_translate("interface_socle", "Champ geom", None))
        self.rb_geom.setText(_translate("interface_socle", "geom", None))
        self.rb_the_geom.setText(_translate("interface_socle", "the_geom", None))
        self.label_26.setText(_translate("interface_socle", "PAI culture/loisirs", None))
        self.label_27.setText(_translate("interface_socle", "PAI transport", None))
        self.label_28.setText(_translate("interface_socle", "PAI sante", None))
        self.label_29.setText(_translate("interface_socle", "PAI religieux", None))
        self.label_22.setText(_translate("interface_socle", "PAI militaire", None))
        self.label_23.setText(_translate("interface_socle", "PAI science/enseignement", None))
        self.label_24.setText(_translate("interface_socle", "PAI indust/commer", None))
        self.label_25.setText(_translate("interface_socle", "PAI sport", None))
        self.label_53.setText(_translate("interface_socle", "Poste transformation", None))
        self.label_54.setText(_translate("interface_socle", "Cimetiere", None))
        self.label_55.setText(_translate("interface_socle", "Terrain sport", None))
        self.label_59.setText(_translate("interface_socle", "Zone végétation", None))
        self.label_15.setText(_translate("interface_socle", "Routes", None))
        self.label_19.setText(_translate("interface_socle", "Bâti remarquable", None))
        self.label_20.setText(_translate("interface_socle", "Bâti industriel", None))
        self.label_21.setText(_translate("interface_socle", "Bâti indiferencie", None))
        self.label_30.setText(_translate("interface_socle", "Surface eau", None))
        self.label_31.setText(_translate("interface_socle", "Point eau", None))
        self.label_50.setText(_translate("interface_socle", "Surface activité", None))
        self.label_51.setText(_translate("interface_socle", "Aitre triage", None))
        self.label_52.setText(_translate("interface_socle", "Voie ferré", None))
        self.pb_start.setText(_translate("interface_socle", "Start", None))
        self.lbl_etape.setText(_translate("interface_socle", "TextLabel", None))

