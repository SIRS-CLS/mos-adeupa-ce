# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_socle.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_interface_socle(object):
    def setupUi(self, interface_socle):
        interface_socle.setObjectName("interface_socle")
        interface_socle.resize(844, 842)
        interface_socle.setMaximumSize(QtCore.QSize(16777215, 16777215))
        interface_socle.setSizeGripEnabled(True)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(interface_socle)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(interface_socle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.cb_connexion = QtWidgets.QComboBox(interface_socle)
        self.cb_connexion.setObjectName("cb_connexion")
        self.horizontalLayout_2.addWidget(self.cb_connexion)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.pb_dbConnect = QtWidgets.QPushButton(interface_socle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_dbConnect.sizePolicy().hasHeightForWidth())
        self.pb_dbConnect.setSizePolicy(sizePolicy)
        self.pb_dbConnect.setObjectName("pb_dbConnect")
        self.verticalLayout_6.addWidget(self.pb_dbConnect)
        self.gb_destination = QtWidgets.QGroupBox(interface_socle)
        self.gb_destination.setObjectName("gb_destination")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.gb_destination)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.gb_destination)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.cb_schema = QtWidgets.QComboBox(self.gb_destination)
        self.cb_schema.setObjectName("cb_schema")
        self.horizontalLayout.addWidget(self.cb_schema)
        self.label_13 = QtWidgets.QLabel(self.gb_destination)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout.addWidget(self.label_13)
        self.le_destination = QtWidgets.QLineEdit(self.gb_destination)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_destination.sizePolicy().hasHeightForWidth())
        self.le_destination.setSizePolicy(sizePolicy)
        self.le_destination.setObjectName("le_destination")
        self.horizontalLayout.addWidget(self.le_destination)
        self.label_2 = QtWidgets.QLabel(self.gb_destination)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.le_annee = QtWidgets.QLineEdit(self.gb_destination)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_annee.sizePolicy().hasHeightForWidth())
        self.le_annee.setSizePolicy(sizePolicy)
        self.le_annee.setObjectName("le_annee")
        self.horizontalLayout.addWidget(self.le_annee)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_6.addWidget(self.gb_destination)
        self.gb_data = QtWidgets.QScrollArea(interface_socle)
        self.gb_data.setEnabled(True)
        self.gb_data.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gb_data.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gb_data.setWidgetResizable(True)
        self.gb_data.setObjectName("gb_data")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, -125, 807, 618))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_14 = QtWidgets.QLabel(self.groupBox_5)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 1, 0, 1, 1)
        self.cb_parcelle_bdtopo = QtWidgets.QComboBox(self.groupBox_5)
        self.cb_parcelle_bdtopo.setObjectName("cb_parcelle_bdtopo")
        self.gridLayout_5.addWidget(self.cb_parcelle_bdtopo, 1, 1, 1, 1)
        self.cb_parcellaire = QtWidgets.QComboBox(self.groupBox_5)
        self.cb_parcellaire.setObjectName("cb_parcellaire")
        self.gridLayout_5.addWidget(self.cb_parcellaire, 2, 1, 1, 1)
        self.label_60 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_60.sizePolicy().hasHeightForWidth())
        self.label_60.setSizePolicy(sizePolicy)
        self.label_60.setObjectName("label_60")
        self.gridLayout_5.addWidget(self.label_60, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 1, 0, 1, 1)
        self.cb_parcelle = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_parcelle.sizePolicy().hasHeightForWidth())
        self.cb_parcelle.setSizePolicy(sizePolicy)
        self.cb_parcelle.setObjectName("cb_parcelle")
        self.gridLayout_4.addWidget(self.cb_parcelle, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 2, 0, 1, 1)
        self.cb_subparc = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_subparc.sizePolicy().hasHeightForWidth())
        self.cb_subparc.setSizePolicy(sizePolicy)
        self.cb_subparc.setObjectName("cb_subparc")
        self.gridLayout_4.addWidget(self.cb_subparc, 2, 1, 1, 1)
        self.cb_tronroute = QtWidgets.QComboBox(self.groupBox)
        self.cb_tronroute.setObjectName("cb_tronroute")
        self.gridLayout_4.addWidget(self.cb_tronroute, 3, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 3, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 4, 0, 1, 1)
        self.cb_tronfluv = QtWidgets.QComboBox(self.groupBox)
        self.cb_tronfluv.setObjectName("cb_tronfluv")
        self.gridLayout_4.addWidget(self.cb_tronfluv, 4, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 5, 0, 1, 1)
        self.cb_tsurf = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_tsurf.sizePolicy().hasHeightForWidth())
        self.cb_tsurf.setSizePolicy(sizePolicy)
        self.cb_tsurf.setObjectName("cb_tsurf")
        self.gridLayout_4.addWidget(self.cb_tsurf, 5, 1, 1, 1)
        self.cb_geobati = QtWidgets.QComboBox(self.groupBox)
        self.cb_geobati.setObjectName("cb_geobati")
        self.gridLayout_4.addWidget(self.cb_geobati, 6, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 6, 0, 1, 1)
        self.cb_section = QtWidgets.QComboBox(self.groupBox)
        self.cb_section.setObjectName("cb_section")
        self.gridLayout_4.addWidget(self.cb_section, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.cb_res_sport = QtWidgets.QComboBox(self.groupBox_3)
        self.cb_res_sport.setObjectName("cb_res_sport")
        self.gridLayout_3.addWidget(self.cb_res_sport, 6, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_3)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 2, 0, 1, 1)
        self.cb_ipli = QtWidgets.QComboBox(self.groupBox_3)
        self.cb_ipli.setObjectName("cb_ipli")
        self.gridLayout_3.addWidget(self.cb_ipli, 2, 1, 1, 1)
        self.label_57 = QtWidgets.QLabel(self.groupBox_3)
        self.label_57.setObjectName("label_57")
        self.gridLayout_3.addWidget(self.label_57, 5, 0, 1, 1)
        self.label_58 = QtWidgets.QLabel(self.groupBox_3)
        self.label_58.setObjectName("label_58")
        self.gridLayout_3.addWidget(self.label_58, 6, 0, 1, 1)
        self.cb_finess = QtWidgets.QComboBox(self.groupBox_3)
        self.cb_finess.setObjectName("cb_finess")
        self.gridLayout_3.addWidget(self.cb_finess, 5, 1, 1, 1)
        self.label_61 = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_61.sizePolicy().hasHeightForWidth())
        self.label_61.setSizePolicy(sizePolicy)
        self.label_61.setObjectName("label_61")
        self.gridLayout_3.addWidget(self.label_61, 0, 0, 1, 1)
        self.cb_ff_parcelle = QtWidgets.QComboBox(self.groupBox_3)
        self.cb_ff_parcelle.setObjectName("cb_ff_parcelle")
        self.gridLayout_3.addWidget(self.cb_ff_parcelle, 0, 1, 1, 1)
        self.label_56 = QtWidgets.QLabel(self.groupBox_3)
        self.label_56.setObjectName("label_56")
        self.gridLayout_3.addWidget(self.label_56, 1, 0, 1, 1)
        self.cb_rpga = QtWidgets.QComboBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_rpga.sizePolicy().hasHeightForWidth())
        self.cb_rpga.setSizePolicy(sizePolicy)
        self.cb_rpga.setObjectName("cb_rpga")
        self.gridLayout_3.addWidget(self.cb_rpga, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_4 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.rb_geom = QtWidgets.QRadioButton(self.groupBox_4)
        self.rb_geom.setChecked(True)
        self.rb_geom.setObjectName("rb_geom")
        self.btgr_geom = QtWidgets.QButtonGroup(interface_socle)
        self.btgr_geom.setObjectName("btgr_geom")
        self.btgr_geom.addButton(self.rb_geom)
        self.horizontalLayout_3.addWidget(self.rb_geom)
        self.rb_the_geom = QtWidgets.QRadioButton(self.groupBox_4)
        self.rb_the_geom.setObjectName("rb_the_geom")
        self.btgr_geom.addButton(self.rb_the_geom)
        self.horizontalLayout_3.addWidget(self.rb_the_geom)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.label_26 = QtWidgets.QLabel(self.groupBox_4)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 1, 0, 1, 1)
        self.cb_pai_cult = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_pai_cult.setObjectName("cb_pai_cult")
        self.gridLayout.addWidget(self.cb_pai_cult, 1, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.groupBox_4)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 2, 0, 1, 1)
        self.cb_paitransp = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_paitransp.setObjectName("cb_paitransp")
        self.gridLayout.addWidget(self.cb_paitransp, 2, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.groupBox_4)
        self.label_28.setObjectName("label_28")
        self.gridLayout.addWidget(self.label_28, 3, 0, 1, 1)
        self.cb_paisante = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_paisante.setObjectName("cb_paisante")
        self.gridLayout.addWidget(self.cb_paisante, 3, 1, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.groupBox_4)
        self.label_29.setObjectName("label_29")
        self.gridLayout.addWidget(self.label_29, 4, 0, 1, 1)
        self.cb_pairel = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_pairel.setObjectName("cb_pairel")
        self.gridLayout.addWidget(self.cb_pairel, 4, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBox_4)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 5, 0, 1, 1)
        self.cb_paimilit = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_paimilit.setObjectName("cb_paimilit")
        self.gridLayout.addWidget(self.cb_paimilit, 5, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 6, 0, 1, 1)
        self.cb_paiens = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_paiens.setObjectName("cb_paiens")
        self.gridLayout.addWidget(self.cb_paiens, 6, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 7, 0, 1, 1)
        self.cb_paicom = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_paicom.setObjectName("cb_paicom")
        self.gridLayout.addWidget(self.cb_paicom, 7, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.groupBox_4)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 8, 0, 1, 1)
        self.cb_paisport = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_paisport.setObjectName("cb_paisport")
        self.gridLayout.addWidget(self.cb_paisport, 8, 1, 1, 1)
        self.label_53 = QtWidgets.QLabel(self.groupBox_4)
        self.label_53.setObjectName("label_53")
        self.gridLayout.addWidget(self.label_53, 9, 0, 1, 1)
        self.cb_paitransfo = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_paitransfo.setObjectName("cb_paitransfo")
        self.gridLayout.addWidget(self.cb_paitransfo, 9, 1, 1, 1)
        self.label_54 = QtWidgets.QLabel(self.groupBox_4)
        self.label_54.setObjectName("label_54")
        self.gridLayout.addWidget(self.label_54, 10, 0, 1, 1)
        self.cb_cime = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_cime.setObjectName("cb_cime")
        self.gridLayout.addWidget(self.cb_cime, 10, 1, 1, 1)
        self.label_55 = QtWidgets.QLabel(self.groupBox_4)
        self.label_55.setObjectName("label_55")
        self.gridLayout.addWidget(self.label_55, 11, 0, 1, 1)
        self.cb_terrainsport = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_terrainsport.setObjectName("cb_terrainsport")
        self.gridLayout.addWidget(self.cb_terrainsport, 11, 1, 1, 1)
        self.label_59 = QtWidgets.QLabel(self.groupBox_4)
        self.label_59.setObjectName("label_59")
        self.gridLayout.addWidget(self.label_59, 12, 0, 1, 1)
        self.cb_zoneveget = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_zoneveget.setObjectName("cb_zoneveget")
        self.gridLayout.addWidget(self.cb_zoneveget, 12, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 13, 0, 1, 1)
        self.cb_route = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_route.setObjectName("cb_route")
        self.gridLayout.addWidget(self.cb_route, 13, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox_4)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 14, 0, 1, 1)
        self.cb_remarquable = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_remarquable.setObjectName("cb_remarquable")
        self.gridLayout.addWidget(self.cb_remarquable, 14, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox_4)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 15, 0, 1, 1)
        self.cb_indust = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_indust.setObjectName("cb_indust")
        self.gridLayout.addWidget(self.cb_indust, 15, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBox_4)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 16, 0, 1, 1)
        self.cb_indif = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_indif.setObjectName("cb_indif")
        self.gridLayout.addWidget(self.cb_indif, 16, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.groupBox_4)
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 17, 0, 1, 1)
        self.cb_surf_eau = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_surf_eau.setObjectName("cb_surf_eau")
        self.gridLayout.addWidget(self.cb_surf_eau, 17, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.groupBox_4)
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 18, 0, 1, 1)
        self.cb_pt_eau = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_pt_eau.setObjectName("cb_pt_eau")
        self.gridLayout.addWidget(self.cb_pt_eau, 18, 1, 1, 1)
        self.label_50 = QtWidgets.QLabel(self.groupBox_4)
        self.label_50.setObjectName("label_50")
        self.gridLayout.addWidget(self.label_50, 19, 0, 1, 1)
        self.cb_surf_acti = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_surf_acti.setObjectName("cb_surf_acti")
        self.gridLayout.addWidget(self.cb_surf_acti, 19, 1, 1, 1)
        self.label_51 = QtWidgets.QLabel(self.groupBox_4)
        self.label_51.setObjectName("label_51")
        self.gridLayout.addWidget(self.label_51, 20, 0, 1, 1)
        self.cb_triage = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_triage.setObjectName("cb_triage")
        self.gridLayout.addWidget(self.cb_triage, 20, 1, 1, 1)
        self.label_52 = QtWidgets.QLabel(self.groupBox_4)
        self.label_52.setObjectName("label_52")
        self.gridLayout.addWidget(self.label_52, 21, 0, 1, 1)
        self.cb_voiefer = QtWidgets.QComboBox(self.groupBox_4)
        self.cb_voiefer.setObjectName("cb_voiefer")
        self.gridLayout.addWidget(self.cb_voiefer, 21, 1, 1, 1)
        self.label_23.raise_()
        self.cb_paicom.raise_()
        self.label_29.raise_()
        self.cb_paitransp.raise_()
        self.label_59.raise_()
        self.cb_paiens.raise_()
        self.cb_pai_cult.raise_()
        self.label_24.raise_()
        self.cb_cime.raise_()
        self.cb_pairel.raise_()
        self.cb_paimilit.raise_()
        self.label_55.raise_()
        self.cb_zoneveget.raise_()
        self.label_54.raise_()
        self.label_27.raise_()
        self.cb_paisport.raise_()
        self.cb_paitransfo.raise_()
        self.label_22.raise_()
        self.cb_paisante.raise_()
        self.label_28.raise_()
        self.label_26.raise_()
        self.label_25.raise_()
        self.cb_terrainsport.raise_()
        self.label_53.raise_()
        self.cb_route.raise_()
        self.label_15.raise_()
        self.cb_remarquable.raise_()
        self.label_19.raise_()
        self.cb_indust.raise_()
        self.label_20.raise_()
        self.cb_indif.raise_()
        self.label_21.raise_()
        self.cb_surf_eau.raise_()
        self.label_30.raise_()
        self.cb_pt_eau.raise_()
        self.label_31.raise_()
        self.cb_surf_acti.raise_()
        self.label_50.raise_()
        self.cb_triage.raise_()
        self.label_51.raise_()
        self.cb_voiefer.raise_()
        self.label_52.raise_()
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.gb_data.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_6.addWidget(self.gb_data)
        self.gb_genere = QtWidgets.QGroupBox(interface_socle)
        self.gb_genere.setEnabled(True)
        self.gb_genere.setObjectName("gb_genere")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gb_genere)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_16 = QtWidgets.QLabel(self.gb_genere)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_5.addWidget(self.label_16)
        self.cb_schema_geom = QtWidgets.QComboBox(self.gb_genere)
        self.cb_schema_geom.setObjectName("cb_schema_geom")
        self.horizontalLayout_5.addWidget(self.cb_schema_geom)
        self.label_17 = QtWidgets.QLabel(self.gb_genere)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_5.addWidget(self.label_17)
        self.cb_couche_geom = QtWidgets.QComboBox(self.gb_genere)
        self.cb_couche_geom.setObjectName("cb_couche_geom")
        self.horizontalLayout_5.addWidget(self.cb_couche_geom)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.verticalLayout_6.addWidget(self.gb_genere)
        self.groupBox_2 = QtWidgets.QGroupBox(interface_socle)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cbx_etape1 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cbx_etape1.setChecked(True)
        self.cbx_etape1.setTristate(False)
        self.cbx_etape1.setObjectName("cbx_etape1")
        self.horizontalLayout_4.addWidget(self.cbx_etape1)
        self.cbx_etape2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cbx_etape2.setChecked(True)
        self.cbx_etape2.setObjectName("cbx_etape2")
        self.horizontalLayout_4.addWidget(self.cbx_etape2)
        self.cbx_etape3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.cbx_etape3.setChecked(True)
        self.cbx_etape3.setObjectName("cbx_etape3")
        self.horizontalLayout_4.addWidget(self.cbx_etape3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.pb_start = QtWidgets.QPushButton(interface_socle)
        self.pb_start.setObjectName("pb_start")
        self.verticalLayout_6.addWidget(self.pb_start)
        self.lbl_etape = QtWidgets.QLabel(interface_socle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_etape.sizePolicy().hasHeightForWidth())
        self.lbl_etape.setSizePolicy(sizePolicy)
        self.lbl_etape.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_etape.setObjectName("lbl_etape")
        self.verticalLayout_6.addWidget(self.lbl_etape)
        self.pb_avancement = QtWidgets.QProgressBar(interface_socle)
        self.pb_avancement.setProperty("value", 24)
        self.pb_avancement.setObjectName("pb_avancement")
        self.verticalLayout_6.addWidget(self.pb_avancement)
        self.pb_start.raise_()
        self.pb_avancement.raise_()
        self.lbl_etape.raise_()
        self.pb_dbConnect.raise_()
        self.gb_data.raise_()
        self.groupBox_2.raise_()
        self.gb_genere.raise_()
        self.gb_destination.raise_()

        self.retranslateUi(interface_socle)
        QtCore.QMetaObject.connectSlotsByName(interface_socle)

    def retranslateUi(self, interface_socle):
        _translate = QtCore.QCoreApplication.translate
        interface_socle.setWindowTitle(_translate("interface_socle", "Création d\'un socle (t0)"))
        self.label.setText(_translate("interface_socle", "Sélectionner la connexion à la base de données"))
        self.pb_dbConnect.setText(_translate("interface_socle", "Connecter"))
        self.gb_destination.setTitle(_translate("interface_socle", "Destination"))
        self.label_6.setText(_translate("interface_socle", "Schema destination"))
        self.label_13.setText(_translate("interface_socle", "Couche destination"))
        self.label_2.setText(_translate("interface_socle", "Année"))
        self.groupBox_5.setTitle(_translate("interface_socle", "EMPRISE"))
        self.label_14.setText(_translate("interface_socle", "Communes BD Topo"))
        self.label_60.setText(_translate("interface_socle", "Communes BD Parcellaire"))
        self.groupBox.setTitle(_translate("interface_socle", "EDIGEO"))
        self.label_7.setText(_translate("interface_socle", "Parcelles"))
        self.label_8.setText(_translate("interface_socle", "Subdivisions"))
        self.label_9.setText(_translate("interface_socle", "Tronçon route"))
        self.label_10.setText(_translate("interface_socle", "Tronçon fleuve"))
        self.label_11.setText(_translate("interface_socle", "Tsurf"))
        self.label_12.setText(_translate("interface_socle", "Bâtiments"))
        self.label_4.setText(_translate("interface_socle", "Sections"))
        self.groupBox_3.setTitle(_translate("interface_socle", "AUTRE"))
        self.label_18.setText(_translate("interface_socle", "IPLI"))
        self.label_57.setText(_translate("interface_socle", "FINESS"))
        self.label_58.setText(_translate("interface_socle", "RES sportif"))
        self.label_61.setText(_translate("interface_socle", "FF pnb10_parcelle"))
        self.label_56.setText(_translate("interface_socle", "RPGA"))
        self.groupBox_4.setTitle(_translate("interface_socle", "IGN"))
        self.label_5.setText(_translate("interface_socle", "Champ geom"))
        self.rb_geom.setText(_translate("interface_socle", "geom"))
        self.rb_the_geom.setText(_translate("interface_socle", "the_geom"))
        self.label_26.setText(_translate("interface_socle", "PAI culture/loisirs"))
        self.label_27.setText(_translate("interface_socle", "PAI transport"))
        self.label_28.setText(_translate("interface_socle", "PAI santé"))
        self.label_29.setText(_translate("interface_socle", "PAI religieux"))
        self.label_22.setText(_translate("interface_socle", "PAI administratif militaire"))
        self.label_23.setText(_translate("interface_socle", "PAI science/enseignement"))
        self.label_24.setText(_translate("interface_socle", "PAI industrie/commerce"))
        self.label_25.setText(_translate("interface_socle", "PAI sport"))
        self.label_53.setText(_translate("interface_socle", "Poste transformation"))
        self.label_54.setText(_translate("interface_socle", "Cimetière"))
        self.label_55.setText(_translate("interface_socle", "Terrain sport"))
        self.label_59.setText(_translate("interface_socle", "Zone végétation"))
        self.label_15.setText(_translate("interface_socle", "Routes"))
        self.label_19.setText(_translate("interface_socle", "Bâti remarquable"))
        self.label_20.setText(_translate("interface_socle", "Bâti industriel"))
        self.label_21.setText(_translate("interface_socle", "Bâti indifférencié"))
        self.label_30.setText(_translate("interface_socle", "Surface eau"))
        self.label_31.setText(_translate("interface_socle", "Point eau"))
        self.label_50.setText(_translate("interface_socle", "Surface activité"))
        self.label_51.setText(_translate("interface_socle", "Aire de triage"))
        self.label_52.setText(_translate("interface_socle", "Voie ferrée"))
        self.gb_genere.setTitle(_translate("interface_socle", "COUCHE GENEREE"))
        self.label_16.setText(_translate("interface_socle", "Schéma de la couche destination"))
        self.label_17.setText(_translate("interface_socle", "Couche destination"))
        self.groupBox_2.setTitle(_translate("interface_socle", "Sélection des phases de calcul"))
        self.cbx_etape1.setText(_translate("interface_socle", "Création du socle géométrique"))
        self.cbx_etape2.setText(_translate("interface_socle", "Analyse du taux de recouvrement"))
        self.cbx_etape3.setText(_translate("interface_socle", "Calcul des code4 à attribuer"))
        self.pb_start.setText(_translate("interface_socle", "Start"))
        self.lbl_etape.setText(_translate("interface_socle", "TextLabel"))

