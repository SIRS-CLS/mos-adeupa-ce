# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import os

from main_dialog import *

class SocleMos:
    def __init__(self, iface):
        self.interface = iface


    def initGui(self):
        iconMain = QIcon(os.path.dirname(__file__) + "/icons/icon_socle.png")
        self.actionMain = QAction(iconMain, u"Réaliser un socle", self.interface.mainWindow())
        QObject.connect(self.actionMain, SIGNAL("triggered()"), self.gereActionMain)

        self.menuSocle = QMenu(u"Socle MOS")
        self.menuSocle.setIcon(QIcon(os.path.dirname(__file__) + "/icons/icon.png"))
        self.menuSocle.addAction(self.actionMain)
        self.interface.pluginMenu().addMenu(self.menuSocle)

        self.toolbarSocle = self.interface.addToolBar(u"Socle MOS");
        self.toolbarSocle.setObjectName("barreOutilSocleMOS")
        self.toolbarSocle.addAction(self.actionMain)

    def unload(self):
        self.interface.mainWindow().menuBar().removeAction(self.menuSocle.menuAction())
        self.interface.mainWindow().removeToolBar(self.toolbarSocle)

    def gereActionMain(self):
        dlg = MainDialog(self.interface)
        # dlg.show() # ligne à mettre en commentaire pour avoir une fenêtre modale
        result = dlg.exec_()
        if result:
            pass
