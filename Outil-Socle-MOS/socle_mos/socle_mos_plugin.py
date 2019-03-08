# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import os
import resources
from create_socle import *
from repair_socle import *
from analyse_socle import *
from compare_socle import *
from evolution_socle import *
from evolution_geometrie import *

class socle_mos:
    def __init__(self, iface):
        self.interface = iface


    def initGui(self):
        iconCreateSocle = QIcon(os.path.dirname(__file__) + "/icon_socle.png")
        self.createSocle = QAction(iconCreateSocle, u"Réaliser un socle", self.interface.mainWindow())
        QObject.connect(self.createSocle, SIGNAL("triggered()"), self.gereActionCreate)

        iconCompare = QIcon(os.path.dirname(__file__) + "/compare.png")
        self.compareSocle = QAction(iconCompare, u"Comparer les socles", self.interface.mainWindow())
        QObject.connect(self.compareSocle, SIGNAL("triggered()"), self.gereActionCompare)

        iconanalyse = QIcon(os.path.dirname(__file__) + "/analyse.png")
        self.analyseSocle = QAction(iconanalyse, u"Réaliser une rétroévolution", self.interface.mainWindow())
        QObject.connect(self.analyseSocle, SIGNAL("triggered()"), self.gereActionAnalyse)
        
        iconRepair = QIcon(os.path.dirname(__file__) + "/repair.png")
        self.repairSocle = QAction(iconRepair, u"Réparer les géométries", self.interface.mainWindow())
        QObject.connect(self.repairSocle, SIGNAL("triggered()"), self.gereActionRepair)
        
        iconEvol = QIcon(os.path.dirname(__file__) + "/evol.png")
        self.evolSocle = QAction(iconEvol, u"Réaliser une évolution attributaire", self.interface.mainWindow())
        QObject.connect(self.evolSocle, SIGNAL("triggered()"), self.gereActionEvol)

        iconEvol = QIcon(os.path.dirname(__file__) + "/geomevol.png")
        self.evolGeomSocle = QAction(iconEvol, u"Réaliser une évolution géométrique", self.interface.mainWindow())
        QObject.connect(self.evolGeomSocle, SIGNAL("triggered()"), self.gereActionEvolGeom)

        self.menuSocle = QMenu(u"Socle MOS")
        self.menuSocle.setIcon(QIcon(os.path.dirname(__file__) + "/icon.png"))
        self.menuSocle.addAction(self.createSocle)
        self.menuSocle.addAction(self.compareSocle)
        self.menuSocle.addAction(self.analyseSocle)
        self.menuSocle.addAction(self.repairSocle)
        self.menuSocle.addAction(self.evolSocle)
        self.menuSocle.addAction(self.evolGeomSocle)
        self.interface.pluginMenu().addMenu(self.menuSocle)


        self.toolbarSocle = self.interface.addToolBar(u"socle_mos");
        self.toolbarSocle.setObjectName("barreOutilsocle__mos")
        self.toolbarSocle.addAction(self.createSocle)
        self.toolbarSocle.addAction(self.compareSocle)
        self.toolbarSocle.addAction(self.analyseSocle)
        self.toolbarSocle.addAction(self.repairSocle)
        self.toolbarSocle.addAction(self.evolSocle)
        self.toolbarSocle.addAction(self.evolGeomSocle)

    def unload(self):
        self.interface.mainWindow().menuBar().removeAction(self.menuSocle.menuAction())
        self.interface.mainWindow().removeToolBar(self.toolbarSocle)

    def gereActionCreate(self):
        dlg = Createsocle__mos(self.interface)
        # dlg.show() # ligne à mettre en commentaire pour avoir une fenêtre modale
        result = dlg.exec_()
        if result:
            pass

    def gereActionRepair(self):
        dlg = RepairSocle(self.interface)
        # dlg.show() # ligne à mettre en commentaire pour avoir une fenêtre modale
        result = dlg.exec_()
        if result:
            pass

    def gereActionCompare(self):
        dlg = Compare_mos(self.interface)
        # dlg.show() # ligne à mettre en commentaire pour avoir une fenêtre modale
        result = dlg.exec_()
        if result:
            pass

    def gereActionAnalyse(self):
        dlg = Analyse_mos(self.interface)
        # dlg.show() # ligne à mettre en commentaire pour avoir une fenêtre modale
        result = dlg.exec_()
        if result:
            pass

    def gereActionEvol(self):
        dlg = Evolution_mos(self.interface)
        # dlg.show() # ligne à mettre en commentaire pour avoir une fenêtre modale
        result = dlg.exec_()
        if result:
            pass

    def gereActionEvolGeom(self):
        dlg = EvolGeom_mos(self.interface)
        # dlg.show() # ligne à mettre en commentaire pour avoir une fenêtre modale
        result = dlg.exec_()
        if result:
            pass