# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.PyQt.QtWidgets import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *
import os, sys
import psycopg2
import time
from db_manager.db_plugins.plugin import (
    DBPlugin,
    Schema,
    Table,
    BaseError
)
from db_manager.db_plugins import createDbPlugin
from db_manager.dlg_db_error import DlgDbError
from db_manager.db_plugins.postgis.connector import PostGisDBConnector

from interface_socle import *

class Createsocle__mos(QDialog, Ui_interface_socle):
    def __init__(self, interface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.host = None
        self.port = None
        self.database = None
        self.username = None
        self.pwd = None

        self.geom = None

        self.schema_geom = None

        self.pb_avancement.setValue(False)
        self.lbl_etape.setText(None)
        self.gb_genere.setEnabled(False)
        
            #Déclenchement de la création du socle
        self.connect(self.pb_start, SIGNAL("clicked()"), self.start)

            #initialisation du bouton de commencement en inclickable
        self.pb_start.setEnabled(False)
        self.rb_geom.setChecked(True)

            #Déclenchement du chargement des données de la base dans les combobox
        self.connect(self.pb_dbConnect, SIGNAL("clicked()"), self.charge)

        self.connect(self.cb_schema_geom, SIGNAL("activated(int)"), self.chargeTableGeom)
            #Lancement de la liste des connexions QGIS au lancement de la fenêtre
        self.updateConnectionList()

        self.connect(self.cbx_etape1, SIGNAL("stateChanged(int)"), self.blockGroupBox)
        self.connect(self.cbx_etape2, SIGNAL("stateChanged(int)"), self.blockGroupBox)
        self.connect(self.cbx_etape3, SIGNAL("stateChanged(int)"), self.blockGroupBox)


            #Déclenchement de la vérification de la totalité des champs rentrés pour lancer le programme
        self.connect(self.cb_parcelle, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_subparc, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_tronroute, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_tronfluv, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_tsurf, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_geobati, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_rpga, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_finess, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_res_sport, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_ff_parcelle, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_parcellaire, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_pai_cult, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_paitransp, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_paisante, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_pairel, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_paimilit, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_paiens, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_paicom, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_paisport, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_paitransfo, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_cime, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_terrainsport, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_zoneveget, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_parcelle_bdtopo, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_route, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_ipli, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_remarquable, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_indust, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_indif, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_surf_eau, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_pt_eau, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_surf_acti, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_triage, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_voiefer, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_schema, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_section, SIGNAL("currentIndexChanged(int)"), self.canStart)
        self.connect(self.cb_couche_geom, SIGNAL("currentIndexChanged(int)"), self.canStart)


        self.connect(self.le_destination, SIGNAL("textChanged(QString)"), self.canStart)
        self.connect(self.le_annee, SIGNAL("textChanged(QString)"), self.canStart)

    def connexion(self):
        #Fonction de récupération des données de connexion à la base
        #Renvois la base contenant les paramètres propre à sa connexion
        #Récupère les données de la connexion QGIS
        s = QSettings()

        self.getConInfo()

        db = QSqlDatabase.addDatabase("QPSQL", "adeupa1")
        db.setHostName(self.host)
        db.setPort(int(self.port))
        db.setDatabaseName(self.database)
        db.setUserName(self.username)
        db.setPassword(self.pwd)
        return db


    def updateConnectionList(self):
        #Fonction récupérant les connexion aux base de données de qgis
        #Lancée à l'ouverture de la fenêtre, affiche les connexion dans un combo box
        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.cb_connexion.clear()


        dbType = 'postgis'
        self.dbType = dbType
        # instance of db_manager plugin class
        dbpluginclass = createDbPlugin( dbType )
        self.dbpluginclass = dbpluginclass

        # fill the connections combobox
        self.connectionDbList = []
        for c in dbpluginclass.connections():
            self.cb_connexion.addItem( str(c.connectionName()))
            self.connectionDbList.append(str(c.connectionName()))



        QApplication.restoreOverrideCursor()

    def getConInfo(self):
        #Fonction de récupération des données des connexions

        QApplication.setOverrideCursor(Qt.WaitCursor)
        connectionName = self.cb_connexion.currentText()
        self.connectionName = connectionName
        dbType = 'postgis'

        connection = None
        if connectionName:
            # Get schema list
            dbpluginclass = createDbPlugin( dbType, connectionName )
            self.dbpluginclass = dbpluginclass
            try:
                connection = dbpluginclass.connect()
            except BaseError as e:

                DlgDbError.showError(e, self)
                self.go = False
                self.updateLog(e.msg)
                QApplication.restoreOverrideCursor()
                return
            except:
                self.go = False
                msg = u"Impossible de récupérer les schémas de la base. Vérifier les informations de connexion."
                self.updateLog(msg)
                QApplication.restoreOverrideCursor()
                return
            finally:
                QApplication.restoreOverrideCursor()

        if connection:
            self.connection = connection
            db = dbpluginclass.database()
            #db1 = dbpluginclass.database().connector()
            if db:
                settings = QSettings()
                settings.beginGroup(u"/%s/%s" % (dbpluginclass.connectionSettingsKey(), connectionName))
                
                settingsList = ["service", "host", "port", "database", "username", "password", "authcfg"]
                self.service, self.host, self.port, self.database, self.username, self.pwd, self.authcfg = [settings.value(x, "", type=str) for x in settingsList]
        QApplication.restoreOverrideCursor()


    def chargeTableGeom(self):
        #Fonction de chargement des données des tables lorsque le schéma T0 est changé
        self.cb_couche_geom.clear()
        db = self.connexion()
            #Connexion à la base de données
        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

                    #Initialisation de la combo box schema avec la liste des schemas de la base
            queryTable = QSqlQuery(db)
            wschema = self.cb_schema_geom.currentText()
            queryTable.prepare("Select distinct table_name from information_schema.tables where table_schema = '" + wschema + "' order by table_name;")
            if queryTable.exec_():
                while queryTable.next():
                    self.cb_couche_geom.addItem(queryTable.value(0))


    def charge(self):
        #Fonction de chargement des données de la base dans les combo box
        #initialise les combo box avec la liste des schema + table de la base

            #Initialisation vide des combobox
        self.cb_parcelle.clear()
        self.cb_subparc.clear()
        self.cb_tronroute.clear()
        self.cb_tronfluv.clear()
        self.cb_tsurf.clear()
        self.cb_geobati.clear()
        self.cb_rpga.clear()
        self.cb_finess.clear()
        self.cb_res_sport.clear()
        self.cb_ff_parcelle.clear()
        self.cb_parcellaire.clear()
        self.cb_pai_cult.clear()
        self.cb_paitransp.clear()
        self.cb_paisante.clear()
        self.cb_pairel.clear()
        self.cb_paimilit.clear()
        self.cb_paiens.clear()
        self.cb_paicom.clear()
        self.cb_paisport.clear()
        self.cb_paitransfo.clear()
        self.cb_cime.clear()
        self.cb_terrainsport.clear()
        self.cb_zoneveget.clear()
        self.cb_parcelle_bdtopo.clear()
        self.cb_route.clear()
        self.cb_ipli.clear()
        self.cb_remarquable.clear()
        self.cb_indust.clear()
        self.cb_indif.clear()
        self.cb_surf_eau.clear()
        self.cb_pt_eau.clear()
        self.cb_surf_acti.clear()
        self.cb_triage.clear()
        self.cb_voiefer.clear()
        self.cb_schema.clear()
        self.cb_schema_geom.clear()
        self.cb_section.clear()

        db = self.connexion()

            #Connexion à la base de données
        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

                #Attribution des text schema + table aux combo box des tables
            self.relation_district = QSqlTableModel(self, db)

            queryTable = QSqlQuery(db)
            queryTable.prepare("Select f_table_schema || '.' || f_table_name as tname from geometry_columns order by f_table_schema, f_table_name;")
            if queryTable.exec_():       
                while queryTable.next():
                    self.cb_parcelle.addItem(queryTable.value(0))
                    self.cb_subparc.addItem(queryTable.value(0))
                    self.cb_tronroute.addItem(queryTable.value(0))
                    self.cb_tronfluv.addItem(queryTable.value(0))
                    self.cb_tsurf.addItem(queryTable.value(0))
                    self.cb_geobati.addItem(queryTable.value(0))
                    self.cb_rpga.addItem(queryTable.value(0))
                    self.cb_finess.addItem(queryTable.value(0))
                    self.cb_res_sport.addItem(queryTable.value(0))
                    self.cb_ff_parcelle.addItem(queryTable.value(0))
                    self.cb_parcellaire.addItem(queryTable.value(0))
                    self.cb_pai_cult.addItem(queryTable.value(0))
                    self.cb_paitransp.addItem(queryTable.value(0))
                    self.cb_paisante.addItem(queryTable.value(0))
                    self.cb_pairel.addItem(queryTable.value(0))
                    self.cb_paimilit.addItem(queryTable.value(0))
                    self.cb_paiens.addItem(queryTable.value(0))
                    self.cb_paicom.addItem(queryTable.value(0))
                    self.cb_paisport.addItem(queryTable.value(0))
                    self.cb_paitransfo.addItem(queryTable.value(0))
                    self.cb_cime.addItem(queryTable.value(0))
                    self.cb_terrainsport.addItem(queryTable.value(0))
                    self.cb_zoneveget.addItem(queryTable.value(0))
                    self.cb_parcelle_bdtopo.addItem(queryTable.value(0))
                    self.cb_route.addItem(queryTable.value(0))
                    self.cb_ipli.addItem(queryTable.value(0))
                    self.cb_remarquable.addItem(queryTable.value(0))
                    self.cb_indust.addItem(queryTable.value(0))
                    self.cb_indif.addItem(queryTable.value(0))
                    self.cb_surf_eau.addItem(queryTable.value(0))
                    self.cb_pt_eau.addItem(queryTable.value(0))
                    self.cb_surf_acti.addItem(queryTable.value(0))
                    self.cb_triage.addItem(queryTable.value(0))
                    self.cb_voiefer.addItem(queryTable.value(0))
                    self.cb_section.addItem(queryTable.value(0))


                    #Initialisation de la combo box schema avec la liste des schemas de la base
            querySchema = QSqlQuery(db)
            querySchema.prepare("Select distinct schema_name from information_schema.schemata where schema_name not like 'pg%' order by schema_name;")
            if querySchema.exec_():
                while querySchema.next():
                    self.cb_schema.addItem(querySchema.value(0))
                    self.cb_schema_geom.addItem(querySchema.value(0))
            
            """          
                    #A ENLEVER /!\
            self.cb_parcelle.setCurrentIndex(self.cb_parcelle.findText('cadastre_edigeo.geo_parcelle'))
            self.cb_subparc.setCurrentIndex(self.cb_subparc.findText('cadastre_edigeo.geo_subdfisc'))
            self.cb_tronroute.setCurrentIndex(self.cb_tronroute.findText('cadastre_edigeo.geo_tronroute'))
            self.cb_tronfluv.setCurrentIndex(self.cb_tronfluv.findText('cadastre_edigeo.geo_tronfluv'))
            self.cb_tsurf.setCurrentIndex(self.cb_tsurf.findText('cadastre_edigeo.geo_tsurf'))
            self.cb_geobati.setCurrentIndex(self.cb_geobati.findText('cadastre_edigeo.geo_batiment'))
            self.cb_rpga.setCurrentIndex(self.cb_rpga.findText('data_exo.rpga_29_2015'))
            self.cb_finess.setCurrentIndex(self.cb_finess.findText('data_exo.extraction_finess_dep29'))
            self.cb_res_sport.setCurrentIndex(self.cb_res_sport.findText('data_exo.equipements_sportifs_res_dep_29'))
            self.cb_ff_parcelle.setCurrentIndex(self.cb_ff_parcelle.findText('ff_d29_2015.d29_2015_pnb10_parcelle'))
            self.cb_parcellaire.setCurrentIndex(self.cb_parcellaire.findText('sandbox.emprise_d29'))
            self.cb_pai_cult.setCurrentIndex(self.cb_pai_cult.findText('ref_ign.pai_culture_loisirs'))
            self.cb_paitransp.setCurrentIndex(self.cb_paitransp.findText('ref_ign.pai_transport'))
            self.cb_paisante.setCurrentIndex(self.cb_paisante.findText('ref_ign.pai_sante'))
            self.cb_pairel.setCurrentIndex(self.cb_pairel.findText('ref_ign.pai_religieux'))
            self.cb_paimilit.setCurrentIndex(self.cb_paimilit.findText('ref_ign.pai_administratif_militaire'))
            self.cb_paiens.setCurrentIndex(self.cb_paiens.findText('ref_ign.pai_science_enseignement'))
            self.cb_paicom.setCurrentIndex(self.cb_paicom.findText('ref_ign.pai_industirel_commercial'))
            self.cb_paisport.setCurrentIndex(self.cb_paisport.findText('ref_ign.pai_sport'))
            self.cb_paitransfo.setCurrentIndex(self.cb_paitransfo.findText('ref_ign.poste_transformation'))
            self.cb_terrainsport.setCurrentIndex(self.cb_terrainsport.findText('ref_ign.terrain_sport'))
            self.cb_cime.setCurrentIndex(self.cb_cime.findText('ref_ign.cimetiere'))
            self.cb_zoneveget.setCurrentIndex(self.cb_zoneveget.findText('ref_ign.zone_vegetation'))
            self.cb_parcelle_bdtopo.setCurrentIndex(self.cb_parcelle_bdtopo.findText('sandbox.emprise_d29_bdtopo'))
            self.cb_route.setCurrentIndex(self.cb_route.findText('ref_ign.route'))
            self.cb_ipli.setCurrentIndex(self.cb_ipli.findText('data_exo.ipli_n_occ_sol_lit_region'))
            self.cb_remarquable.setCurrentIndex(self.cb_remarquable.findText('ref_ign.bati_remarquable'))
            self.cb_indust.setCurrentIndex(self.cb_indust.findText('ref_ign.bati_industirel'))
            self.cb_indif.setCurrentIndex(self.cb_indif.findText('ref_ign.bati_indifferencie'))
            self.cb_surf_eau.setCurrentIndex(self.cb_surf_eau.findText('ref_ign.surface_eau'))
            self.cb_pt_eau.setCurrentIndex(self.cb_pt_eau.findText('ref_ign.point_eau'))
            self.cb_surf_acti.setCurrentIndex(self.cb_surf_acti.findText('ref_ign.surface_activite'))
            self.cb_triage.setCurrentIndex(self.cb_triage.findText('ref_ign.aire_triage'))
            self.cb_voiefer.setCurrentIndex(self.cb_voiefer.findText('ref_ign.troncon_voie_ferree'))
            self.cb_section.setCurrentIndex(self.cb_voiefer.findText('cadastre_edigeo.geo_section'))

            self.cb_schema.setCurrentIndex(self.cb_schema.findText('sandbox'))
            self.cb_schema_geom.setCurrentIndex(self.cb_schema_geom.findText('sandbox'))

            """           
            
            self.cb_parcelle.setCurrentIndex(self.cb_parcelle.findText('cadastre_edigeo_22.geo_parcelle'))
            self.cb_subparc.setCurrentIndex(self.cb_subparc.findText('cadastre_edigeo_22.geo_subdfisc'))
            self.cb_tronroute.setCurrentIndex(self.cb_tronroute.findText('cadastre_edigeo_22.geo_tronroute'))
            self.cb_tronfluv.setCurrentIndex(self.cb_tronfluv.findText('cadastre_edigeo_22.geo_tronfluv'))
            self.cb_tsurf.setCurrentIndex(self.cb_tsurf.findText('cadastre_edigeo_22.geo_tsurf'))
            self.cb_geobati.setCurrentIndex(self.cb_geobati.findText('cadastre_edigeo_22.geo_batiment'))
            self.cb_rpga.setCurrentIndex(self.cb_rpga.findText('exo_guimgamp.rpga_2019'))
            self.cb_finess.setCurrentIndex(self.cb_finess.findText('exo_guimgamp.finess'))
            self.cb_res_sport.setCurrentIndex(self.cb_res_sport.findText('exo_guimgamp.res_sport_22_29'))
            self.cb_ff_parcelle.setCurrentIndex(self.cb_ff_parcelle.findText('ff_d22_2016.d22_2016_pnb10_parcelle'))
            self.cb_parcellaire.setCurrentIndex(self.cb_parcellaire.findText('exo_guimgamp.emprise_bd_parcellaire'))
            self.cb_pai_cult.setCurrentIndex(self.cb_pai_cult.findText('ign_guimgamp.pai_culture_loisirs'))
            self.cb_paitransp.setCurrentIndex(self.cb_paitransp.findText('ign_guimgamp.pai_transport'))
            self.cb_paisante.setCurrentIndex(self.cb_paisante.findText('ign_guimgamp.pai_sante'))
            self.cb_pairel.setCurrentIndex(self.cb_pairel.findText('ign_guimgamp.pai_religieux'))
            self.cb_paimilit.setCurrentIndex(self.cb_paimilit.findText('ign_guimgamp.pai_administratif_militaire'))
            self.cb_paiens.setCurrentIndex(self.cb_paiens.findText('ign_guimgamp.pai_science_enseignement'))
            self.cb_paicom.setCurrentIndex(self.cb_paicom.findText('ign_guimgamp.pai_industriel_commercial'))
            self.cb_paisport.setCurrentIndex(self.cb_paisport.findText('ign_guimgamp.pai_sport'))
            self.cb_paitransfo.setCurrentIndex(self.cb_paitransfo.findText('ign_guimgamp.poste_transformation'))
            self.cb_terrainsport.setCurrentIndex(self.cb_terrainsport.findText('ign_guimgamp.terrain_sport'))
            self.cb_cime.setCurrentIndex(self.cb_cime.findText('ign_guimgamp.cimetiere'))
            self.cb_zoneveget.setCurrentIndex(self.cb_zoneveget.findText('ign_guimgamp.zone_vegetation'))
            self.cb_parcelle_bdtopo.setCurrentIndex(self.cb_parcelle_bdtopo.findText('exo_guimgamp.emprise_bd_topo'))
            self.cb_route.setCurrentIndex(self.cb_route.findText('ign_guimgamp.route'))
            self.cb_ipli.setCurrentIndex(self.cb_ipli.findText('exo_guimgamp.ipli_1977'))
            self.cb_remarquable.setCurrentIndex(self.cb_remarquable.findText('ign_guimgamp.bati_remarquable'))
            self.cb_indust.setCurrentIndex(self.cb_indust.findText('ign_guimgamp.bati_industriel'))
            self.cb_indif.setCurrentIndex(self.cb_indif.findText('ign_guimgamp.bati_indifferencie'))
            self.cb_surf_eau.setCurrentIndex(self.cb_surf_eau.findText('ign_guimgamp.surface_eau'))
            self.cb_pt_eau.setCurrentIndex(self.cb_pt_eau.findText('ign_guimgamp.point_eau'))
            self.cb_surf_acti.setCurrentIndex(self.cb_surf_acti.findText('ign_guimgamp.surface_activite'))
            self.cb_triage.setCurrentIndex(self.cb_triage.findText('ign_guimgamp.aire_triage'))
            self.cb_voiefer.setCurrentIndex(self.cb_voiefer.findText('ign_guimgamp.troncon_voie_ferree'))
            self.cb_section.setCurrentIndex(self.cb_voiefer.findText('cadastre_edigeo_22.geo_section'))

            self.cb_schema.setCurrentIndex(self.cb_schema.findText('sandbox'))
            #self.le_destination.setText('mos_guimgamp')
            
            #self.cb_parcelle_bdtopo.setCurrentIndex(self.cb_parcelle_bdtopo.findText('sandbox.emprise_g1_bdtopo'))
            #self.cb_parcellaire.setCurrentIndex(self.cb_parcellaire.findText('sandbox.emprise_g1_parc'))

            
            """
          
                #initialisation des combo box avec la valeur nulle, pour pouvoir voir l'avancement de notre saisie
            self.cb_parcelle.setCurrentIndex(self.cb_subparc.findText(None))
            self.cb_subparc.setCurrentIndex(self.cb_subparc.findText(None))
            self.cb_tronroute.setCurrentIndex(self.cb_tronroute.findText(None))
            self.cb_tronfluv.setCurrentIndex(self.cb_tronfluv.findText(None))
            self.cb_tsurf.setCurrentIndex(self.cb_tsurf.findText(None))
            self.cb_geobati.setCurrentIndex(self.cb_geobati.findText(None))
            self.cb_rpga.setCurrentIndex(self.cb_rpga.findText(None))
            self.cb_finess.setCurrentIndex(self.cb_finess.findText(None))
            self.cb_res_sport.setCurrentIndex(self.cb_res_sport.findText(None))
            self.cb_ff_parcelle.setCurrentIndex(self.cb_ff_parcelle.findText(None))
            self.cb_parcellaire.setCurrentIndex(self.cb_parcellaire.findText(None))
            self.cb_pai_cult.setCurrentIndex(self.cb_pai_cult.findText(None))
            self.cb_paitransp.setCurrentIndex(self.cb_paitransp.findText(None))
            self.cb_paisante.setCurrentIndex(self.cb_paisante.findText(None))
            self.cb_pairel.setCurrentIndex(self.cb_pairel.findText(None))
            self.cb_paimilit.setCurrentIndex(self.cb_paimilit.findText(None))
            self.cb_paiens.setCurrentIndex(self.cb_paiens.findText(None))
            self.cb_paicom.setCurrentIndex(self.cb_paicom.findText(None))
            self.cb_paisport.setCurrentIndex(self.cb_paisport.findText(None))
            self.cb_paitransfo.setCurrentIndex(self.cb_paitransfo.findText(None))
            self.cb_terrainsport.setCurrentIndex(self.cb_terrainsport.findText(None))
            self.cb_cime.setCurrentIndex(self.cb_cime.findText(None))
            self.cb_zoneveget.setCurrentIndex(self.cb_zoneveget.findText(None))
            self.cb_parcelle_bdtopo.setCurrentIndex(self.cb_parcelle_bdtopo.findText(None))
            self.cb_route.setCurrentIndex(self.cb_route.findText(None))
            self.cb_ipli.setCurrentIndex(self.cb_ipli.findText(None))
            self.cb_remarquable.setCurrentIndex(self.cb_remarquable.findText(None))
            self.cb_indust.setCurrentIndex(self.cb_indust.findText(None))
            self.cb_indif.setCurrentIndex(self.cb_indif.findText(None))
            self.cb_surf_eau.setCurrentIndex(self.cb_surf_eau.findText(None))
            self.cb_pt_eau.setCurrentIndex(self.cb_pt_eau.findText(None))
            self.cb_surf_acti.setCurrentIndex(self.cb_surf_acti.findText(None))
            self.cb_triage.setCurrentIndex(self.cb_triage.findText(None))
            self.cb_voiefer.setCurrentIndex(self.cb_voiefer.findText(None))
            self.cb_section.setCurrentIndex(self.cb_voiefer.findText(None))

            self.cb_schema.setCurrentIndex(self.cb_schema.findText(None))"""

    def blockGroupBox(self):
        if self.cbx_etape1.isChecked():
            if self.cbx_etape2.isChecked():
                self.gb_genere.setEnabled(False)
                self.gb_destination.setEnabled(True)
                self.gb_data.setEnabled(True)

                self.cb_parcelle_bdtopo.setEnabled(True)
                self.cb_parcellaire.setEnabled(True)

                self.cb_section.setEnabled(True)
                self.cb_parcelle.setEnabled(True)
                self.cb_subparc.setEnabled(True)
                self.cb_tronroute.setEnabled(True)
                self.cb_tronfluv.setEnabled(True)
                self.cb_tsurf.setEnabled(True)
                self.cb_geobati.setEnabled(True)

                self.cb_ff_parcelle.setEnabled(True)
                self.cb_rpga.setEnabled(True)
                self.cb_ipli.setEnabled(True)
                self.cb_finess.setEnabled(True)
                self.cb_res_sport.setEnabled(True)

                self.cb_pai_cult.setEnabled(True)
                self.cb_paitransp.setEnabled(True)
                self.cb_paisante.setEnabled(True)
                self.cb_pairel.setEnabled(True)
                self.cb_paimilit.setEnabled(True)
                self.cb_paiens.setEnabled(True)
                self.cb_paicom.setEnabled(True)
                self.cb_paisport.setEnabled(True)
                self.cb_paitransfo.setEnabled(True)
                self.cb_cime.setEnabled(True)
                self.cb_terrainsport.setEnabled(True)
                self.cb_zoneveget.setEnabled(True)
                self.cb_route.setEnabled(True)
                self.cb_remarquable.setEnabled(True)
                self.cb_indust.setEnabled(True)
                self.cb_indif.setEnabled(True)
                self.cb_surf_eau.setEnabled(True)
                self.cb_pt_eau.setEnabled(True)
                self.cb_surf_acti.setEnabled(True)
                self.cb_triage.setEnabled(True)
                self.cb_voiefer.setEnabled(True)
            else:
                self.gb_genere.setEnabled(False)
                self.gb_destination.setEnabled(False)
                self.gb_data.setEnabled(True)

                self.cb_parcelle_bdtopo.setEnabled(True)
                self.cb_parcellaire.setEnabled(True)

                self.cb_section.setEnabled(True)
                self.cb_parcelle.setEnabled(True)
                self.cb_subparc.setEnabled(True)
                self.cb_tronroute.setEnabled(False)
                self.cb_tronfluv.setEnabled(False)
                self.cb_tsurf.setEnabled(False)
                self.cb_geobati.setEnabled(False)

                self.cb_ff_parcelle.setEnabled(False)
                self.cb_rpga.setEnabled(True)
                self.cb_ipli.setEnabled(True)
                self.cb_finess.setEnabled(False)
                self.cb_res_sport.setEnabled(False)

                self.cb_pai_cult.setEnabled(False)
                self.cb_paitransp.setEnabled(False)
                self.cb_paisante.setEnabled(False)
                self.cb_pairel.setEnabled(False)
                self.cb_paimilit.setEnabled(False)
                self.cb_paiens.setEnabled(False)
                self.cb_paicom.setEnabled(False)
                self.cb_paisport.setEnabled(False)
                self.cb_paitransfo.setEnabled(False)
                self.cb_cime.setEnabled(False)
                self.cb_terrainsport.setEnabled(False)
                self.cb_zoneveget.setEnabled(True)
                self.cb_route.setEnabled(True)
                self.cb_remarquable.setEnabled(False)
                self.cb_indust.setEnabled(False)
                self.cb_indif.setEnabled(False)
                self.cb_surf_eau.setEnabled(False)
                self.cb_pt_eau.setEnabled(False)
                self.cb_surf_acti.setEnabled(False)
                self.cb_triage.setEnabled(False)
                self.cb_voiefer.setEnabled(False)


        elif self.cbx_etape2.isChecked():
            self.gb_genere.setEnabled(False)
            self.gb_destination.setEnabled(True)
            self.gb_data.setEnabled(True)

            self.cb_parcelle_bdtopo.setEnabled(True)
            self.cb_parcellaire.setEnabled(True)

            self.cb_section.setEnabled(True)
            self.cb_parcelle.setEnabled(True)
            self.cb_subparc.setEnabled(True)
            self.cb_tronroute.setEnabled(True)
            self.cb_tronfluv.setEnabled(True)
            self.cb_tsurf.setEnabled(True)
            self.cb_geobati.setEnabled(True)

            self.cb_ff_parcelle.setEnabled(True)
            self.cb_rpga.setEnabled(True)
            self.cb_ipli.setEnabled(True)
            self.cb_finess.setEnabled(True)
            self.cb_res_sport.setEnabled(True)

            self.cb_pai_cult.setEnabled(True)
            self.cb_paitransp.setEnabled(True)
            self.cb_paisante.setEnabled(True)
            self.cb_pairel.setEnabled(True)
            self.cb_paimilit.setEnabled(True)
            self.cb_paiens.setEnabled(True)
            self.cb_paicom.setEnabled(True)
            self.cb_paisport.setEnabled(True)
            self.cb_paitransfo.setEnabled(True)
            self.cb_cime.setEnabled(True)
            self.cb_terrainsport.setEnabled(True)
            self.cb_zoneveget.setEnabled(True)
            self.cb_route.setEnabled(True)
            self.cb_remarquable.setEnabled(True)
            self.cb_indust.setEnabled(True)
            self.cb_indif.setEnabled(True)
            self.cb_surf_eau.setEnabled(True)
            self.cb_pt_eau.setEnabled(True)
            self.cb_surf_acti.setEnabled(True)
            self.cb_triage.setEnabled(True)
            self.cb_voiefer.setEnabled(True)

        elif self.cbx_etape3.isChecked():
            self.gb_genere.setEnabled(True)
            self.gb_destination.setEnabled(False)
            self.gb_data.setEnabled(False)
            self.le_annee.setEnabled(True)
        else:
            self.gb_destination.setEnabled(True)
            self.gb_genere.setEnabled(True)
            self.gb_data.setEnabled(True)

    def canStart(self):
        #Fonction analysant si le programme peu être exécuté (tous les champs sont remplis) ou non
        if self.cbx_etape1.isChecked():
            if self.cbx_etape2.isChecked():
                if self.cb_parcelle.currentText() == '' or self.cb_subparc.currentText() == '' or self.cb_tronroute.currentText() == '' or self.cb_tronfluv.currentText() == '' or self.cb_tsurf.currentText() == '' or self.cb_rpga.currentText() == '' or self.cb_finess.currentText() == '' or self.cb_res_sport.currentText() == '' or self.cb_ff_parcelle.currentText() == '' or self.cb_parcellaire.currentText() == '' or self.cb_pai_cult.currentText() == '' or self.cb_paitransp.currentText() == '' or self.cb_paisante.currentText() == '' or self.cb_pairel.currentText() == '' or self.cb_paimilit.currentText() == '' or self.cb_paiens.currentText() == '' or self.cb_paicom.currentText() == '' or self.cb_paitransfo.currentText() == '' or self.cb_terrainsport.currentText() == '' or self.cb_cime.currentText() == '' or self.cb_zoneveget.currentText() == '' or self.cb_parcelle_bdtopo.currentText() == '' or self.cb_route.currentText() == '' or self.cb_remarquable.currentText() == '' or self.cb_indust.currentText() == '' or self.cb_indif.currentText() == '' or self.cb_surf_eau.currentText() == '' or self.cb_pt_eau.currentText() == '' or  self.cb_surf_acti.currentText() == '' or self.cb_triage.currentText() == '' or self.cb_voiefer.currentText() == '' or self.cb_paisport.currentText() == '' or self.cb_paisport.currentText() == '' or self.cb_schema.currentText() == '' or self.le_destination.text() == '' or self.le_annee.text() == '' :
                    self.pb_start.setEnabled(False)
                else:
                    self.pb_start.setEnabled(True)
            else:
                if  self.cb_parcelle.currentText() == '' or self.cb_subparc.currentText() == '' or self.cb_parcelle_bdtopo.currentText() == '' or self.cb_parcellaire.currentText() == '' or self.cb_section.currentText() == '' or self.cb_rpga.currentText() == '' or self.cb_ipli.currentText() == ''  or self.cb_zoneveget.currentText() == '' or self.cb_route.currentText() == '':
                    self.pb_start.setEnabled(False)
                else: 
                    self.pb_start.setEnabled(True)
        elif self.cbx_etape2.isChecked():
                if self.cb_parcelle.currentText() == '' or self.cb_subparc.currentText() == '' or self.cb_tronroute.currentText() == '' or self.cb_tronfluv.currentText() == '' or self.cb_tsurf.currentText() == '' or self.cb_rpga.currentText() == '' or self.cb_finess.currentText() == '' or self.cb_res_sport.currentText() == '' or self.cb_ff_parcelle.currentText() == '' or self.cb_parcellaire.currentText() == '' or self.cb_pai_cult.currentText() == '' or self.cb_paitransp.currentText() == '' or self.cb_paisante.currentText() == '' or self.cb_pairel.currentText() == '' or self.cb_paimilit.currentText() == '' or self.cb_paiens.currentText() == '' or self.cb_paicom.currentText() == '' or self.cb_paitransfo.currentText() == '' or self.cb_terrainsport.currentText() == '' or self.cb_cime.currentText() == '' or self.cb_zoneveget.currentText() == '' or self.cb_parcelle_bdtopo.currentText() == '' or self.cb_route.currentText() == '' or self.cb_remarquable.currentText() == '' or self.cb_indust.currentText() == '' or self.cb_indif.currentText() == '' or self.cb_surf_eau.currentText() == '' or self.cb_pt_eau.currentText() == '' or  self.cb_surf_acti.currentText() == '' or self.cb_triage.currentText() == '' or self.cb_voiefer.currentText() == '' or self.cb_paisport.currentText() == '' or self.cb_paisport.currentText() == '' or self.cb_schema.currentText() == '' or self.le_destination.text() == '' or self.le_annee.text() == '' :
                    self.pb_start.setEnabled(False)
                else:
                    self.pb_start.setEnabled(True)
        elif self.cbx_etape3.isChecked():
            if self.cb_couche_geom.currentText() == '':
                self.pb_start.setEnabled(False)
            else:
                self.pb_start.setEnabled(True)  


    def start(self):
        #Fonction de lancement du programme
        #Lancement des étapes suivant les cases cochées
        #Initialisation des noms des tables créées
        self.pb_start.setEnabled(False)

        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.username, dbname=self.database, password=self.pwd )
        cur = self.conn.cursor()

        if self.rb_geom.isChecked():
            self.geom = 'geom'
        else:
            self.geom = 'the_geom'

        temp = QTimer
        if self.cbx_etape1.isChecked() and self.cbx_etape2.isChecked() and self.cbx_etape3.isChecked():
            #Premier cas, les 3 étapes sont lancée
            self.cas_etape = 1

            self.socle_geom = 'socle_temp_geom'
            self.yearCode = self.le_annee.text()
            self.schema_desti = self.cb_schema.currentText()
            self.couche_desti = self.le_destination.text()

            self.lbl_etape.setText(u'Etape 1/3 :Création du socle géométrique')
            self.pb_avancement.setValue(0)
            temp.singleShot(100, self.createSocle)

        elif self.cbx_etape1.isChecked() and self.cbx_etape2.isChecked():
            #deuxième cas, seules les deux premières étapes sont lancées
            self.cas_etape = 2

            self.socle_geom = 'socle_temp_geom'


            self.lbl_etape.setText(u'Etape 1/2 : Création du socle géométrique')
            self.pb_avancement.setValue(0)
            temp.singleShot(100, self.createSocle)


        elif self.cbx_etape1.isChecked() and not self.cbx_etape3.isChecked():
            #Troisième cas, seule la première étape est lancée
            self.cas_etape = 3

            self.socle_geom = 'socle_temp_geom'

            self.lbl_etape.setText(u'Etape 1/1 : Création du socle géométrique')
            self.pb_avancement.setValue(0)

            temp.singleShot(100, self.createSocle)


        elif self.cbx_etape2.isChecked() and self.cbx_etape3.isChecked():
            #Quatrième cas, l'étape deux et trois sont lancées
            self.cas_etape = 4

            self.socle_geom = 'socle_temp_geom'
            self.yearCode = self.le_annee.text()

            self.schema_desti = self.cb_schema.currentText()
            self.couche_desti = self.le_destination.text()

            self.lbl_etape.setText(u'Etape 1/2 : Analyse du taux de recouvrement')
            self.pb_avancement.setValue(0)
            try:
                temp.singleShot(100, self.getTauxInfo)
            except Exception as exc:
                QMessageBox.critical(self, "Erreur", u"Un problème est survenu : %s"%exc,
                                     QMessageBox.Ok)

        elif self.cbx_etape2.isChecked():
            #Cinquièeme cas, l'étape deux est lancée
            self.cas_etape = 5

            self.socle_geom = 'socle_temp_geom'

            self.lbl_etape.setText(u'Etape 1/1 : Analyse du taux de recouvrement')
            self.pb_avancement.setValue(0)
            temp.singleShot(100, self.getTauxInfo)


            self.lbl_etape.setText(u'Terminé')
            self.pb_avancement.setValue(100)

        elif self.cbx_etape3.isChecked() and not self.cbx_etape1.isChecked():
            #Sixième cas, l'étape troi est lancée
            self.cas_etape = 6
            self.schema_desti = self.cb_schema_geom.currentText()
            self.couche_desti = self.cb_couche_geom.currentText()

                #Récupération de l'année à d'insertion
            cur.execute(u"""Select right(column_name,4) 
                from information_schema.columns 
                where table_schema||'.'||table_name  = '{0}.{1}'  
                and column_name like 'code4%' 
                order by column_name desc

            """.format(self.schema_desti,
                        self.couche_desti
                        )
            )
            self.yearCode = cur.fetchone()
            self.yearCode = self.yearCode[0]
            cur.close();

            self.lbl_etape.setText(u'Etape 1/1 : Calcul des code4 à attribuer')
            self.pb_avancement.setValue(0)
            temp.singleShot(100, self.getCode4)

        else:
            QMessageBox.critical(self, "Erreur", u"Problème lors de la sélection de phase de calcul",
                                 QMessageBox.Ok)

            #Appel de la fonction pour le début du socle 
        #self.createSocle()

    def createSocle(self):
        #Fonction de création du socle première étape
        #Réalise la géométrie du socle
            #Connexion à la base de données
        print ('OKAY')

        self.addFunctionSafe()

        cur = self.conn.cursor()
            #Execution de la suite de requête de création du socle
        cur.execute(u""" 
                        --Récupération des subdivisions de l'emprise avec leur numéro de section          
                    drop table if exists vm_subdfisc;
                    create temporary table vm_subdfisc as
                    Select row_number() over() as gid, *
                    From (
                        Select s.geo_subdfisc, s.annee, s.object_rid, s.tex, s.creat_date, s.update_dat, s.lot, (st_dump(st_collectionextract(st_safe_intersection(s.geom, p.geom),3))).geom::geometry(Polygon, 2154), sec.tex as section
                        From {1} s
                        Join {2} c29 on St_within(St_PointOnSurface(s.geom), c29.geom)
                        Join {0} p on St_Within(St_PointOnSurface(s.geom), p.geom)
                        Join {11} sec on sec.geo_section = p.geo_section
                    )tt;
                        
                        --Création de subdivisions supplémentaire (découpage des geo_parcelle par les geo_subdfisc)
                    drop table if exists vm_parc_h_subd cascade;
                    create temporary table vm_parc_h_subd as 
                    Select row_number() over() as gid, * From (
                    Select (st_dump(st_collectionextract(st_safe_difference(parc.geom, st_union(sp.geom)),3))).geom::geometry(Polygon, 2154) as geom, parc.idu, 'zzz'::character varying as tex  , s.tex as section 
                    From {0} parc
                    Join vm_subdfisc sp on St_Within(St_PointOnSurface(sp.geom), parc.geom)
                    Join {11} s on s.geo_section = parc.geo_section
                    Group by parc.geom, parc.idu, s.tex)tt;

                        --Récupération des parcelles + subdivisions
                    drop table if exists v_temp_parc_subparc cascade;
                    create temporary table v_temp_parc_subparc As 
                    Select ROW_NUMBER() OVER() as unique_id, *
                    From(
                        (Select (st_dump(st_collectionextract(gs.geom,3))).geom::geometry(Polygon,2154) as geom, 
                                pi.idu as idu, 
                                c29.code_insee as code_insee, 
                                pi.idu || coalesce(gs.tex, 'zzz') as num_parc, 
                                coalesce(gs.tex, 'zzz') as tex,
                                s.tex as section
                            From vm_subdfisc gs
                            Join {2} c29 on St_within(St_PointOnSurface(gs.geom), c29.geom)
                            Join {0} pi on St_Within(St_PointOnSurface(gs.geom), pi.geom)
                            Join {11} s on s.geo_section = pi.geo_section
                        )
                    UNION
                        (Select (st_dump(st_collectionextract(pi2.geom, 3))).geom::geometry(Polygon,2154) as geom, 
                                pi2.idu as idu, 
                                c292.code_insee as code_insee, 
                                pi2.idu as num_parc, 
                                null as tex ,
                                s.tex as section 
                        From {0} pi2
                        Join {2} c292 on St_within(St_PointOnSurface(pi2.geom), c292.geom) 
                        Join {11} s on s.geo_section = pi2.geo_section
                        Where pi2.ogc_fid not in (Select distinct pi3.ogc_fid 
                                                From {0} pi3
                                                Join vm_subdfisc gs2 on St_Within(St_PointOnSurface(gs2.geom), pi3.geom))
                        )
                    UNION
                        (Select (st_dump(st_collectionextract(vmhs.geom,3))).geom::geometry(Polygon,2154) as geom, 
                                vmhs.idu as idu, 
                                c292.code_insee as code_insee, 
                                vmhs.idu || vmhs.tex as num_parc, 
                                vmhs.tex,
                                section  
                        From vm_parc_h_subd vmhs
                        Join {2} c292 on St_within(St_PointOnSurface(vmhs.geom), c292.geom)) 
                    ) tt;
            create index idx_parc_subparc_2 on v_temp_parc_subparc using gist(geom);
                        
                        --Attribution des lettres 'zzz' pour les subdivisions créées par requête
                    update v_temp_parc_subparc 
                        set tex = 'zzz',
                            num_parc = idu || 'zzz'
                        Where tex = '';
                        
                        --Découpage des parcelles par l'emprise BD Parcellaire en ne récupérant que les entités découpées
                    drop table if exists vm_cut_on_com;
                    create temporary table vm_cut_on_com as 
                        Select * From (
                            Select ROW_NUMBER() OVER() as uq_gid, 
                                                                geom, 
                                                                tt.unique_id,
                                                                code_insee
                            From (
                                Select (ST_Dump(ST_CollectionExtract(ST_Safe_Intersection(vm.geom, bdpc.geom),3))).geom::geometry(Polygon, 2154) as geom, 
                                                                                                                            vm.unique_id,
                                                                                                                            vm.code_insee
                                From v_temp_parc_subparc vm
                                Join {2} bdpc on St_intersects(vm.geom, bdpc.geom)
                            )tt
                        )tt2 
                        Where unique_id not in 
                            (Select unique_id 
                                From (Select ROW_NUMBER() OVER() as uq_gid, 
                                                                    geom, 
                                                                    unique_id
                                    From (
                                        Select (ST_Dump(ST_CollectionExtract(ST_Safe_Intersection(vm.geom, bdpc.geom),3))).geom::geometry(Polygon, 2154) as geom, 
                                            vm.unique_id
                                        From v_temp_parc_subparc vm
                                        Join {2} bdpc on St_intersects(vm.geom, bdpc.geom)
                                    )tt
                                )tt2
                                Group By unique_id Having count(unique_id) = 1);
                     create index idx_cut_com_2 on vm_cut_on_com using gist(geom);
                                
                        --Récupération des nouvelles géométries 
                    drop table if exists vm_temp_exclusion;
                    create temporary table vm_temp_exclusion as 
                    Select vmt2.uq_gid, vmt2.unique_id, vmt2.code_insee, vmps.idu, vmps.num_parc, vmps.tex, (st_dump(st_collectionextract(vmt2.geom,3))).geom::geometry(polygon, 2154), section
                    From vm_cut_on_com vmt2
                    Join v_temp_parc_subparc vmps on vmps.unique_id = vmt2.unique_id  
                    Where uq_gid in (Select uq_gid 
                                        From vm_cut_on_com vm, 
                                            {2} bdpc
                                        Where st_within(st_pointonsurface(vm.geom), bdpc.geom)
                                        AND vm.code_insee = bdpc.code_insee );

                        --Récupération des géométries exclues à fusionner avec les parcelles de la commune voisine
                    drop table if exists vm_temp_exclus;
                    create temporary table vm_temp_exclus as 
                    Select  vmcoc.uq_gid, vmcoc.unique_id, vmcoc.code_insee, vmps.idu, vmps.num_parc, vmps.tex, (st_dump(st_collectionextract(vmcoc.geom,3))).geom::geometry(Polygon, 2154), st_area(vmcoc.geom) as surf_area, dd.code_insee as new_insee, section
                    From vm_cut_on_com vmcoc
                    Join v_temp_parc_subparc vmps on vmps.unique_id = vmcoc.unique_id
                    Join {2} dd on St_within(st_pointonsurface(vmcoc.geom), dd.geom )
                    Where vmcoc.uq_gid not in (Select uq_gid From vm_temp_exclusion);
                        
                        --Récupération de toutes les parcelles avec les géométries modifiées
                    drop table if exists vm_temp_parc;
                    create temporary table vm_temp_parc as 
                    Select ROW_NUMBER() over() as un_idd, * FROM( 
                    (Select unique_id, code_insee, idu, num_parc, tex, geom, section
                    From  vm_temp_exclusion
                    )
                    UNION 
                    (
                    Select unique_id, code_insee, idu, num_parc, tex, geom, section
                    From v_temp_parc_subparc
                    Where unique_id not in (Select unique_id From vm_temp_exclusion)
                    ))tt;

                    create index idx_temp_parc_2 on vm_temp_parc using gist(geom);

                        --Fonction de fusion des entités qui ont été découpées par le contour commune
                    Create or replace function public.fun_fusion(i_origine text, i_fuse text) 
                        Returns void AS
                    $BODY$
                        DECLARE
                            v_geomO geometry;
                            v_geomF geometry;
                            
                            v_surfF float;
                            v_idF integer;
                            v_inseeF character varying;
                            v_inseeO character varying;
                            
                            v_iduO character varying;
                            v_numpO character varying;
                            v_texO character varying;
                            v_section character varying;
                            
                            v_surfO float;
                            v_idO integer;
                            
                            v_geomFusion geometry;
                            v_idFusion integer;
                            

                            v_eliOld integer;
                            v_eliId integer;
                            v_eliIdu character varying;
                            v_eliInsee character varying;
                            v_eliNp character varying;
                            v_eliTex character varying;

                            
                            v_lastGeom geometry;
                            cpt integer;
                            cpt2 integer = 0;
                            
                        BEGIN
                        Execute format ('
                                        DROP table if exists tt_fuse;
                                        drop table if exists tt_origine;
                        Create temporary table tt_fuse as
                            Select * from %1$s;
                        Create temporary table tt_origine as
                            Select * from %2$s;',i_fuse, i_origine );
                            drop table if exists t_eliminated cascade;
                            Create temporary table t_eliminated(
                                gid serial,                                                                 
                                old_id integer, 
                                geom geometry(Polygon, 2154),
                                idu character varying,                                                                      
                                code_insee character varying,
                                num_parc character varying,
                                tex character varying,
                                geom_check boolean,
                                section character varying,
                                Constraint pk_t_elimin PRIMARY KEY (gid)
                            );
                            Drop table if exists tt_to_fuse;
                                Create Temporary Table tt_to_fuse(
                                    unique_id integer,                                                                                                      
                                    geom geometry,
                                    surf float,
                                    inseeO character varying,
                                    inseeF character varying,
                                    slow_surf float,
                                    idu character varying,
                                    num_parc character varying,
                                    section character varying,
                                    tex character varying                                                                                                   
                                );

                            For v_geomF, v_inseeF, v_surfF, v_idF in Select geom, new_insee, surf_area, uq_gid from tt_fuse LOOP
                                truncate tt_to_fuse;
                                IF v_surfF < 10 THEN
                                    For v_geomO, v_inseeO, v_idO, v_iduO, v_numpO, v_texO, v_section in Select geom, code_insee, unique_id, idu, num_parc, tex , section
                                                                                                From tt_origine 
                                                                                                Where code_insee = v_inseeF AND st_intersects(v_geomF, geom) LOOP
                                        IF v_inseeO = v_inseeF Then
                                            IF St_intersects(v_geomF, v_geomO) THEN
                                                Select st_area(st_intersection(st_buffer(v_geomF,1), v_geomO )) INTO v_surfO;
                                                Insert into tt_to_fuse values (v_idO, v_geomO, v_surfO, v_inseeO, v_inseeF, v_surfF,v_iduO, v_numpO, v_texO, v_section);
                                                --RAISE NOTICE '%, %, %', v_inseeO, v_inseeF, v_surfF;
                                            END IF;
                                        END IF;
                                    END LOOP;
                                    Select count(*) From tt_to_fuse into cpt;
                                    IF cpt > 0 THEN
                                        Select (st_dump(st_collectionextract(st_union(tt.geom, v_geomF),3))).geom::geometry(Polygon, 2154) as geom, tt.unique_id, tt.inseeO, tt.inseeF , tt.idu, tt.num_parc, tt.tex, tt.section
                                            From tt_to_fuse tt
                                            Where v_inseeF = tt.inseeO 
                                            AND tt.surf in (Select max(surf) From tt_to_fuse LIMIT 1) 
                                        INTO v_geomFusion, v_idFusion, v_inseeO, v_inseeF, v_iduO, v_numpO, v_texO, v_section;
                                        INSERT INTO t_eliminated (geom, code_insee, idu, num_parc, tex, geom_check, old_id, section) values
                                            (v_geomFusion, v_inseeO, v_iduO, v_numpO, v_texO, FALSE, v_idfusion, v_section);
                                    END IF;
                                END IF;
                            End Loop;
                            Select count(*) From t_eliminated INTO cpt;
                            While cpt2 < cpt LOOP
                                Select gid, idu, code_insee, num_parc, tex, old_id, section From t_eliminated Where geom_check = False
                                    INTO v_eliId, v_eliIdu, v_eliInsee, v_eliNp, v_eliTex, v_eliOld, v_section;
                                Select (st_dump(st_collectionextract(st_union(geom),3))).geom::geometry(Polygon, 2154) as geom
                                From t_eliminated
                                Where idu = v_eliIdu INTO v_lastGeom;
                                INSERT INTO t_eliminated (geom, code_insee, idu, num_parc, tex, geom_check, old_id, section) values
                                            (v_lastGeom, v_eliInsee, v_eliIdu, v_eliNp, v_eliTex, TRUE, v_eliOld, v_section);
                                Delete From t_eliminated 
                                    Where idu = v_eliIdu AND geom_check = FALSE;
                                cpt2 = cpt2 +1;
                                Select count(*) From t_eliminated INTO cpt;
                            END LOOP;
                            Return;
                        END;
                    $BODY$
                        LANGUAGE 'plpgsql';

                    select public.fun_fusion('vm_temp_parc', 'vm_temp_exclus');
                        
                        --Création d'une première partie socle cadastré
                    drop table if exists vm_socle_c;
                    create temporary table vm_socle_c as 
                    Select ROW_NUMBER() over() as gid, * FROM( 
                    (Select gid as old_gid, code_insee, idu, num_parc, tex, (st_dump(st_collectionextract(geom,3))).geom::geometry(polygon,2154), section
                    From  t_eliminated
                    )
                    UNION 
                    (
                    Select unique_id as old_gid, code_insee, idu, num_parc, tex, geom, section
                    From vm_temp_parc
                    Where unique_id not in (Select old_id From t_eliminated)
                    ))tt;

                    create index idx_socle_c_2 on vm_socle_c using gist(geom);
                
                        --Création d'une première partie socle non cadastré
                    drop table if exists vm_socle_nc;
                    Create temporary table vm_socle_nc as
                    with tmp as (
                        select b.gid, st_union(st_buffer(a.geom, 0.001)) as geom
                        from {2} b 
                        join vm_socle_c a on st_intersects(a.geom, b.geom)
                        group by b.gid
                        ), tmp2 as (
                        select b.code_insee, (st_dump(st_collectionextract(st_safe_difference(b.geom,coalesce(t.geom, 'GEOMETRYCOLLECTION EMPTY'::geometry)),3))).geom::geometry(Polygon,2154) as geom
                        from {2} b 
                        left join tmp t on b.gid = t.gid
                        )
                    Select row_number() over() as gid, *
                    From tmp2;
                    
                    create index idx_vm_socle_nc on vm_socle_nc using gist(geom);
                

                        --Découpage du socle cadastré par le contour commune de la BD Topo
                    drop table if exists vm_nc_lito cascade;
                    create temporary table vm_nc_lito as
                    Select ROW_NUMBER() OVEr() as gid, *
                    From (
                        Select (st_dump(
                                    st_collectionextract(
                                        st_intersection(st_union(vmtt.geom),vmnc.geom),3))).geom::geometry(polygon,2154) as geom, vmnc.code_insee
                        From vm_socle_nc vmnc, {8} vmtt
                        Where st_intersects(vmtt.geom, vmnc.geom)
                        Group By vmnc.geom, vmnc.code_insee
                    )tt;
                    create index idx_lito_2 on vm_nc_lito using gist(geom);
                    
                        --Récupération du buffer des routes primaires contenue dans l'meprise BD Parcellaire
                    drop table if exists vm_primaire;
                    create temporary table vm_primaire as
                    Select ROW_NUMBER() OVEr() as gid, st_union(geom) as geom, nature
                    From (
                        Select st_buffer(rp.{10}, rp.largeur/2, 'endcap=square join=round')::geometry(Polygon,2154) as geom, 'primaire'::character varying as nature
                        From {3} rp, {2} com
                        Where rp.importance in ('1', '2') 
                        AND st_intersects(rp.{10}, com.geom)   
                    )tt
                    Where st_area(tt.geom) > 10
                    Group By nature;

                    create index idx_primaire_2 on vm_primaire using gist(geom);
                        
                        --Récupération du buffer des routes secondaires contenue dans l'emprise BD Parcellaire
                    drop table if exists vm_secondaire;
                    create temporary table vm_secondaire as
                    Select ROW_NUMBER() OVEr() as gid,  geom, nature
                    From (select st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
                        From (
                            Select st_buffer(rs.{10}, largeur/2, 'endcap=square join=round')::geometry(Polygon,2154) as geom, 'secondaire'::character varying as nature
                            From {3} rs, {2} com
                            Where rs.importance in ('3', '4', '5', 'NC') AND rs.nature not in ('Chemin', 'Escalier', 'Piste cyclable', 'Sentier') 
                            AND st_intersects(rs.{10}, com.geom) 
                            Group by rs.largeur/2, rs.{10}
                        )tt
                    Where st_area(tt.geom) > 10
                    Group by nature) tt2;

                    create index idx_secondaire_2 on vm_secondaire using gist(geom);
                    
                        --Récupération du buffer des chemins contenue dans l'meprise BD Parcellaire
                    drop table if exists vm_chemin;
                    create temporary table vm_chemin as
                    Select ROW_NUMBER() OVEr() as gid,  geom, nature
                    From (select st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
                        From (
                            Select st_buffer(c.{10}, 5.0/2)::geometry(Polygon,2154) as geom, 'Chemin'::character varying as nature
                            From {3} c, {2} com
                            Where c.nature in ('Chemin', 'Escalier' , 'Piste cyclable', 'Sentier')
                            AND st_intersects(c.{10}, com.geom)
                        )tt
                    Where st_area(tt.geom) > 10
                    group By nature)tt2 ;

                    create index idx_chemin_2 on vm_chemin using gist(geom);
                        
                        --Récupération des zones végétation contenue dans l'meprise BD Parcellaire
                    drop table if exists vm_veget;
                    create temporary table vm_veget as
                    with tmp as (
                        Select b.gid, st_union(st_buffer(a.{10},0.001)) as geom
                        From vm_nc_lito b
                        Join {4} a on st_intersects(a.{10}, b.geom)
                        group by b.gid
                    ), tmp2 as (
                        Select (st_dump(st_collectionextract(st_safe_intersection(t.geom, b.geom),3))).geom::geometry(polygon,2154) as geom, 'veget'::character varying as nature
                        From vm_nc_lito b 
                        LEFT join tmp t on b.gid = t.gid
                        )
                    Select row_number() over() as gid, (st_dump(st_collectionextract(st_union(st_buffer(geom,0.001)),3))).geom as geom, nature
                        From tmp2
                        Where st_area(geom) > 400
                        group by nature
                    ;
                    create index idx_veget_2 on vm_veget using gist(geom);
                        
                        --Récupération des surface en eau contenue dans l'meprise BD Parcellaire
                    drop table if exists vm_hydro;
                    create temporary table vm_hydro as
                    Select ROW_NUMBER() OVEr() as gid, st_union(st_buffer(geom,0.001))::geometry(MultiPolygon,2154) as geom, nature
                    From (
                            Select (st_dump(st_collectionextract(st_safe_intersection(st_force2D(se.{10}), vmnc.geom),3))).geom::geometry(Polygon, 2154), 'hydro'::character varying as nature
                            From {5} se
                            Join vm_nc_lito vmnc on st_intersects(se.{10}, vmnc.geom)
                        ) tt2
                    Where st_area(tt2.geom) > 10
                    Group by nature;

                    create index idx_hyro_2 on vm_hydro using gist(geom);
                        
                        --Récupération des parcelles agricoles contenue dans l'meprise BD Parcellaire
                    drop table if exists vm_rpga;
                    create temporary table vm_rpga as
                    with tmp as (
                        Select b.gid, st_union(st_buffer(a.geom,0.001)) as geom
                        From vm_nc_lito b
                        Join {6} a on st_intersects(a.geom, b.geom)
                        group by b.gid
                    ), tmp2 as (
                        Select (st_dump(st_collectionextract(st_safe_intersection(t.geom, b.geom),3))).geom::geometry(polygon,2154) as geom, 'agricole'::character varying as nature
                        From vm_nc_lito b 
                        LEFT join tmp t on b.gid = t.gid
                    )
                    Select row_number() over() as gid, (st_dump(st_collectionextract(st_union(st_buffer(geom,0.001)),3))).geom as geom, nature
                        From tmp2
                        Where st_area(geom) >= 200
                        group by nature
                    ;

                    create index idx_rpga_2 on vm_rpga using gist(geom);
                        
                        --Création du socle non cadastré connu par intersection avec les données précédentes
                    drop table if exists t_socle_nc;
                    create temporary table t_socle_nc (
                        gid serial,
                        geom geometry(Polygon,2154),
                        nature character varying,
                        type_ajout character varying,
                        code_insee character varying,
                        Constraint pk_socle_nc primary key (gid)
                    );
                    create index idx_socle_nc_geom on t_socle_nc using gist(geom);
                        
                    insert into t_socle_nc (geom, nature, type_ajout, code_insee) 
                        select (st_dump(st_collectionextract(st_safe_intersection(vmnc.geom, ipli.geom),3))).geom::geometry(Polygon, 2154), 
                                    ipli.ocsol,
                                    'plage',
                                    vmnc.code_insee
                                From {7} ipli
                                Join vm_nc_lito vmnc on st_intersects(ipli.geom, vmnc.geom)
                                Where usage in (30, 32);


                    insert into t_socle_nc (geom, nature, type_ajout, code_insee)
                    With tmp as(
                        Select b.gid, st_union(st_buffer(a.geom,0.001)) as geom
                        From vm_primaire b
                        Join t_socle_nc a on st_intersects(b.geom, a.geom)
                        group by b.gid
                    ), tmp2 as (
                            Select b.gid, b.nature, a.code_insee, st_safe_intersection(a.geom, b.geom) as geom
                            From vm_primaire b
                            Join vm_nc_lito a on st_intersects(a.geom, b.geom)
                    )
                    Select (st_dump(st_collectionextract(st_safe_difference(b.geom,coalesce(a.geom, 'GEOMETRYCOLLECTION EMPTY'::geometry)),3))).geom::geometry(Polygon,2154), 
                        b.nature, 
                        'route1', 
                        b.code_insee
                        From tmp2 b
                        left join tmp a on b.gid = a.gid
                    ;


                    insert into t_socle_nc(geom, nature, type_ajout, code_insee)
                    With tmp as(
                        Select b.gid, st_union(st_buffer(a.geom,0.001)) as geom
                        From vm_secondaire b
                        Join t_socle_nc a on st_intersects(b.geom, a.geom)
                        group by b.gid
                    ), tmp2 as (
                        Select b.gid, b.nature, a.code_insee, st_safe_intersection(a.geom, b.geom) as geom
                        From vm_secondaire b
                        Join vm_nc_lito a on st_intersects(a.geom, b.geom)
                    )
                    Select (st_dump(st_collectionextract(st_safe_difference(b.geom,coalesce(a.geom, 'GEOMETRYCOLLECTION EMPTY'::geometry)),3))).geom::geometry(Polygon,2154), 
                        b.nature, 
                        'secondaire', 
                        b.code_insee
                        From tmp2 b
                        left join tmp a on b.gid = a.gid
                    ;

                    delete from t_socle_nc where st_area(geom) < 150;


                    insert into t_socle_nc (geom, nature, type_ajout, code_insee) 
                    With tmp as(
                        Select b.gid, st_union(st_buffer(a.geom,0.001)) as geom
                        From vm_chemin b
                        Join t_socle_nc a on st_intersects(b.geom, a.geom)
                        group by b.gid
                    ), tmp2 as (
                        Select b.gid, b.nature, a.code_insee, st_safe_intersection(a.geom, b.geom) as geom
                        From vm_chemin b
                        Join vm_nc_lito a on st_intersects(a.geom, b.geom)
                    )
                    Select (st_dump(st_collectionextract(st_safe_difference(b.geom,coalesce(a.geom, 'GEOMETRYCOLLECTION EMPTY'::geometry)),3))).geom::geometry(Polygon,2154), 
                        b.nature, 
                        'chemin', 
                        b.code_insee
                        From tmp2 b
                        left join tmp a on b.gid = a.gid
                    ;


                    delete from t_socle_nc where st_area(geom) < 150;

                    insert into t_socle_nc (geom, nature, type_ajout, code_insee)
                    With tmp as(
                        Select b.gid, st_union(st_buffer(a.geom,0.001)) as geom
                        From vm_hydro b
                        Join t_socle_nc a on st_intersects(b.geom, a.geom)
                        group by b.gid
                    ), tmp2 as (
                        Select b.gid, b.nature, a.code_insee, st_safe_intersection(a.geom, b.geom) as geom
                        From vm_hydro b
                        Join vm_nc_lito a on st_intersects(a.geom, b.geom)
                    )
                    Select (st_dump(st_collectionextract(st_safe_difference(b.geom,coalesce(a.geom, 'GEOMETRYCOLLECTION EMPTY'::geometry)),3))).geom::geometry(Polygon,2154), 
                        b.nature, 
                        'hydro', 
                        b.code_insee
                        From tmp2 b
                        left join tmp a on b.gid = a.gid
                    ;

                    delete from t_socle_nc where st_area(geom) < 150;

                    insert into t_socle_nc (geom, nature, type_ajout, code_insee)
                    With tmp as(
                        Select b.gid, st_union(st_buffer(a.geom,0.001)) as geom
                        From vm_rpga b
                        Join t_socle_nc a on st_intersects(b.geom, a.geom)
                        group by b.gid
                    ), tmp2 as (
                        Select b.gid, b.nature, a.code_insee, st_safe_intersection(a.geom, b.geom) as geom
                        From vm_rpga b
                        Join vm_nc_lito a on st_intersects(a.geom, b.geom)
                    )
                    Select (st_dump(st_collectionextract(st_safe_difference(b.geom,coalesce(a.geom, 'GEOMETRYCOLLECTION EMPTY'::geometry)),3))).geom::geometry(Polygon,2154), 
                        b.nature, 
                        'rpga', 
                        b.code_insee
                        From tmp2 b
                        left join tmp a on b.gid = a.gid
                    ;


                    delete from t_socle_nc where st_area(geom) < 150;


                    drop table if exists vm_temp_veget;
                    create temporary table vm_temp_veget as
                    with tmp as (
                        Select b.gid, st_union(st_buffer(a.geom,0.001)) as geom
                            From vm_veget b
                            Join t_socle_nc a on st_area(st_intersection(b.geom, a.geom)) > 1
                            group by b.gid
                    ), tmp2 as(
                        Select st_safe_difference(b.geom, t.geom) as geom, b.nature
                            From vm_veget b
                            left Join tmp t on b.gid = t.gid
                    )
                    Select ROW_number() over() as gid, (st_dump(st_collectionextract(st_union(st_buffer(geom,0.001)),3))).geom::geometry(polygon,2154), 
                        nature
                        From tmp2 tt
                        group by tt.geom, tt.nature
                    ;

                    delete from vm_temp_veget where st_area(geom) < 150;


                    insert into t_socle_nc (geom, nature, type_ajout, code_insee) 
                        select ipli.geom::geometry(Polygon, 2154), 
                                    ipli.nature,
                                    'veget', 
                                    a.code_insee
                                From vm_temp_veget ipli
                                Join vm_nc_lito a on st_intersects(a.geom, ipli.geom)
                                Group by ipli.geom, ipli.nature, a.code_insee;

                    delete from t_socle_nc where st_area(geom) < 150;
                        
                        --Création du cadastre connu : parcelles, subdivision et routes, rpga, végétation
                    drop table if exists vm_scv1;
                    Create  temporary table vm_scv1 as
                        Select ROW_NUMBER() OVER() as gid, *
                        FROM (
                            (Select code_insee, idu, num_parc, tex, geom, section
                            From vm_socle_c)
                            UNION
                            (Select code_insee,'NC', 'NC', nature, geom, 'NC'
                            From t_socle_nc)
                            )tt;
                     create index idx_sdb_scv1_2 on vm_scv1 using gist(geom);

                        --Création du cadastre non connu (parties réstantes dans l'emprise n'étant pas concerné par les données précédentes)
                    drop table if exists vm_nc_v2;
                    Create temporary table vm_nc_v2 as
                    with tmp as (
                        select b.gid, st_union(st_buffer(a.geom,0.001)) as geom
                        from {2} b 
                        join vm_scv1 a on st_intersects(a.geom, b.geom)
                        group by b.gid
                        ), tmp2 as (
                        select b.code_insee, (st_dump(st_collectionextract(st_safe_difference(b.geom,coalesce(t.geom, 'GEOMETRYCOLLECTION EMPTY'::geometry)),3))).geom::geometry(Polygon,2154) as geom
                        from {2} b 
                        left join tmp t on b.gid = t.gid
                        )
                    Select row_number() over() as gid, *
                    From tmp2;
    

                    create index idx_ncv2_2 on vm_nc_v2 using gist(geom);
                        --Création du socle géométrique final
                    drop table if exists {12} cascade;
                    Create table {12} as 
                        Select ROW_NUMBER() OVER() as gid, *
                        FROM (
                            (Select code_insee, idu, num_parc, tex, geom, section
                            From vm_scv1)
                            UNION
                            (Select vmnc.code_insee,'NC', 'NC', 'NC', (st_dump(st_collectionextract(st_intersection(st_union(st_buffer(vmtt.geom,0.001)), vmnc.geom), 3))).geom::geometry(polygon,2154) as geom, 'NC'
                            From vm_nc_v2 vmnc, {8} vmtt
                            Group by vmnc.code_insee, vmnc.geom,vmtt.code_insee)
                            )tt;
                    create index idx_{12}_geom on {12} using gist(geom);
                   """.format(self.cb_parcelle.currentText(), #0
                                self.cb_subparc.currentText(), #1
                                self.cb_parcellaire.currentText(),#2
                                self.cb_route.currentText(),#3
                                self.cb_zoneveget.currentText(),#4
                                self.cb_surf_eau.currentText(),#5
                                self.cb_rpga.currentText(),#6
                                self.cb_ipli.currentText(),#7
                                self.cb_parcelle_bdtopo.currentText(),#8
                                self.schema_geom,#9 inutile
                                self.geom,#10
                                self.cb_section.currentText(),#11
                                self.socle_geom#12
                            ))
        cur.close()
        self.conn.commit()
        temp = QTimer 
            #Choix du lancement des étapes selon les cas rencontrés
        if self.cas_etape == 1:
            #Cas 1, on passe à l'étape 2, puis 3
            self.lbl_etape.setText(u'Etape 2/3 : Analyse du taux de recouvrement')
            self.pb_avancement.setValue(20)
            temp.singleShot(100, self.getTauxInfo)

        elif self.cas_etape == 2:
            #Cas 2 on passe à l'étape 2 avant de terminer
            self.lbl_etape.setText(u'Etape 2/2 : Analyse du taux de recouvrement')
            self.pb_avancement.setValue(30)
            temp.singleShot(100, self.getTauxInfo)
        elif self.cas_etape == 3:
            #Cas 3 on a terminé
            self.lbl_etape.setText(u'Terminé')
            self.pb_avancement.setValue(100)

        #Úself.pb_avancement.setValue(20)
              
        #temp.singleShot(100, self.getTauxInfo)
            #Lancement de la deuxième partie de la création du socle
        #self.getTauxInfo()
        
    def getTauxInfo(self):
        #Fonction de création du socle deuxième étape
        #Calcul des taux de présence
        cur2 = self.conn.cursor()
            #Execution de la suite de requêtes
<<<<<<< HEAD
        try:    
            cur2.execute(u"""
                Create or replace function public.fun_typage(i_socle_c text, 
                                                i_pai_milit text, 
                                                i_bati text, 
                                                i_bati_rem text, 
                                                i_bati_indus text, 
                                                i_surf_acti text, 
                                                i_aire_tri text, 
                                                i_voie_ferre text,
                                                i_pai_indus_com text,
                                                i_cime text,
                                                i_terrain_sport text,
                                                i_pai_cul_lois text,
                                                i_rpga text,
                                                i_surf_eau text,
                                                i_pai_scens text,
                                                i_pai_sante text,
                                                i_pai_rel text,
                                                i_point_eau text,
                                                i_post_transf text,
                                                i_pai_transp text,
                                                i_pai_sport text,
                                                i_finess text,
                                                i_zveget text,
                                                i_res text,
                                                i_tronfluv text,
                                                i_tsurf text,
                                                i_route_sec text,
                                                i_tronroute text,
                                                i_emprise text,
                                                i_foncier text,
                                                i_bati_indif text
                                                )
                    Returns void AS
                    --Fonction de calcul des aménagements présents sur les parcelles
                    --Met en correlation de nombreuses données recouvrant ou non une parcelle en indiquant la surface de recouvrement, ou si une présence est constaté
                $BODY$
                    DECLARE
                        v_geom geometry(polygon,2154); -- Géométrie du socle
                        v_insee character varying; --code insee du socle
                        v_idu character varying; -- code idu du socle
                        v_num_parc character varying;-- num_parc du socle
                        v_tex character varying; -- tex du socle
                        v_gid integer; -- identifiant du socle
                        v_section character varying; --Section du socle
                        v_surf_mos double precision;
                        v_peri_mos double precision;
                        v_cpt_mos integer = 0;
                        v_id_mos character varying;
                        
                        v_tomilit integer;--Taux debâtiments militaire sur la parcelle
                        v_tobati integer;-- Taux de bâtiment sur la parcelle
                        v_tobatire integer; --Taux de bâtiment remarquable sur la parcelle
                        v_tobatagri integer; -- Taux de bâtiment agricole sur la parcelle
                        v_toserre integer; --Taux de serre sur la parcelle
                        v_toindust integer; --Taux de bâtiment industriel sur la parcelle
                        v_tocomer integer; -- Taux de bâtiment commercial sur la parcelle
                        v_tozic integer; -- Taux de de bâtiment industriel ou commercial sur la parcelle
                        v_totransp integer; -- Taux de transport sur la parcelle
                        v_tovoiefer integer; -- Taux de voies férrées sur la parcelle
                        v_tocarrier integer; -- Taux de carrière sur la parcelle
                        v_tocime integer; -- Taux de cimetière sur la parcelle
                        v_tosport integer; -- Taux terrain sport sur la parcelle
                        v_toloisir integer; -- Taux de loisir sur la parcelle
                        v_toagri integer; -- Taux de parcelles agricoles sur la parcelle
                        v_toeau integer; -- Taux d'eau dans la parcelle
                        v_toveget integer; -- Taux de végétation hors agriculture dans la parcelle
                        v_toroute integer; -- Taux de route secondaire dans la parcelle
                        v_tobatimaison integer; -- Taux de batiment maison (bati indiferencie)

                        v_temp_toeau integer; -- Taux temporaire pour comparer plusieurs taux d'eau sur la parcelle
                        v_temp_route integer; -- taux temporaire pour comparer plusieurs taux de route sur la parcelle
                        
                        v_prescol integer; --Présence d'équipement d'enseignement sur la parcelle
                        v_presante integer; -- Présence d'équipement de santé sur la parcelle
                        v_preqadmi integer; -- présence d'équipement local, administration sur la parcelle
                        v_preonrj integer; -- Présence d'équipement eau assainissement énergie sur la parcelle
                        v_pretransp integer; -- Présence d'infrastructure de transport sur la parcelle
                        v_presploi integer; -- Présence sport et loisir

                        v_mfonction character varying;-- Type de bâtiment sur la parcelle
                        v_probjardin integer; --Probabilité de présence de jardin 0|1|2
                    BEGIN
                            --Récupération des données à corréler sur l'emprise
                            execute format ('
                                    drop table if exists vm_i_bati;
                                    create temporary table vm_i_bati as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geom, emp.geom);
                                    Create index idx_vm_i_bati on vm_i_bati using gist(geom);
                                    ', i_bati, i_emprise);


                            execute format ('
                                    drop table if exists vm_i_pai_milit;
                                    create temporary table vm_i_pai_milit as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_pai_milit on vm_i_pai_milit using gist({33});
                                    ', i_pai_milit, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_bati_rem;
                                    create temporary table vm_i_bati_rem as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_bati_rem on vm_i_bati_rem using gist({33});
                                    ', i_bati_rem, i_emprise);


                            execute format ('
                                    drop table if exists vm_i_bati_indus;
                                    create temporary table vm_i_bati_indus as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_bati_indus on vm_i_bati_indus using gist({33});
                                    ', i_bati_indus, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_surf_acti;
                                    create temporary table vm_i_surf_acti as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_surf_acti on vm_i_surf_acti using gist({33});
                                    ', i_surf_acti, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_aire_tri;
                                    create temporary table vm_i_aire_tri as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_aire_tri on vm_i_aire_tri using gist({33});
                                    ', i_aire_tri, i_emprise);

                                    
                            execute format ('
                                    drop table if exists vm_i_voie_ferre;
                                    create temporary table vm_i_voie_ferre as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_voie_fette on vm_i_voie_ferre using gist({33});
                                    ', i_voie_ferre, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_pai_indus_com;
                                    create temporary table vm_i_pai_indus_com as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_pai_indus_com on vm_i_pai_indus_com using gist({33});
                                    ', i_pai_indus_com, i_emprise);

                                    
                            execute format ('
                                    drop table if exists vm_i_cime;
                                    create temporary table vm_i_cime as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_cime on vm_i_cime using gist({33});
                                    ', i_cime, i_emprise);

                                    
                            execute format ('
                                    drop table if exists vm_i_terrain_sport;
                                    create temporary table vm_i_terrain_sport as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_terrain_sport on vm_i_terrain_sport using gist({33});
                                    ', i_terrain_sport, i_emprise);

                                    
                            execute format ('
                                    drop table if exists vm_i_pai_cul_lois;
                                    create temporary table vm_i_pai_cul_lois as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_pai_cul_lois on vm_i_pai_cul_lois using gist({33});
                                    ', i_pai_cul_lois, i_emprise);
                                    

                            execute format ('
                                    drop table if exists vm_i_rpga;
                                    create temporary table vm_i_rpga as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geom, emp.geom);
                                    Create index idx_vm_i_rpga on vm_i_rpga using gist(geom);
                                    ', i_rpga, i_emprise);
                                    

                            execute format ('
                                    drop table if exists vm_i_surf_eau;
                                    create temporary table vm_i_surf_eau as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_surf_eau on vm_i_surf_eau using gist({33});
                                    ', i_surf_eau, i_emprise);


                            execute format ('
                                    drop table if exists vm_i_pai_scens;
                                    create temporary table vm_i_pai_scens as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_pai_scens on vm_i_pai_scens using gist({33});
                                    ', i_pai_scens, i_emprise);
                                    

                            execute format ('
                                    drop table if exists vm_i_pai_sante;
                                    create temporary table vm_i_pai_sante as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_pai_sante on vm_i_pai_sante using gist({33});
                                    ', i_pai_sante, i_emprise);

                                    
                            execute format ('
                                    drop table if exists vm_i_pai_rel;
                                    create temporary table vm_i_pai_rel as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_pai_rel on vm_i_pai_rel using gist({33});
                                    ', i_pai_rel, i_emprise);

                                    
                            execute format ('
                                    drop table if exists vm_i_point_eau;
                                    create temporary table vm_i_point_eau as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_point_eau on vm_i_point_eau using gist({33});
                                    ', i_point_eau, i_emprise);
                                    

                            execute format ('
                                    drop table if exists vm_i_post_transf;
                                    create temporary table vm_i_post_transf as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_post_transf on vm_i_post_transf using gist({33});
                                    ', i_post_transf, i_emprise);
                                    

                            execute format ('
                                    drop table if exists vm_i_pai_transp;
                                    create temporary table vm_i_pai_transp as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_pai_transp on vm_i_pai_transp using gist({33});
                                    ', i_pai_transp, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_pai_sport;
                                    create temporary table vm_i_pai_sport as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_pai_sport on vm_i_pai_sport using gist({33});
                                    ', i_pai_sport, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_finess;
                                    create temporary table vm_i_finess as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geom, emp.geom);
                                    Create index idx_vm_i_finess on vm_i_finess using gist(geom);
                                    ', i_finess, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_zveget;
                                    create temporary table vm_i_zveget as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_zveget on vm_i_zveget using gist({33});
                                    ', i_zveget, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_res;
                                    create temporary table vm_i_res as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geom, emp.geom);
                                    Create index idx_vm_i_res on vm_i_res using gist(geom);
                                    ', i_res, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_tronfluv;
                                    create temporary table vm_i_tronfluv as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geom, emp.geom);
                                    Create index idx_vm_i_tronfluv on vm_i_tronfluv using gist(geom);
                                    ', i_tronfluv, i_emprise);


                            execute format ('
                                    drop table if exists vm_i_tsurf;
                                    create temporary table vm_i_tsurf as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geom, emp.geom);
                                    Create index idx_vm_i_tsurf on vm_i_tsurf using gist(geom);
                                    ', i_tsurf, i_emprise);

                            execute format ('
                                    drop table if exists vm_i_tronroute;
                                    create temporary table vm_i_tronroute as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geom, emp.geom);
                                    Create index idx_vm_i_tronroute on vm_i_tronroute using gist(geom);
                                    ', i_tronroute, i_emprise);

                                    
                            execute format ('
                                    drop table if exists vm_i_foncier;
                                    create temporary table vm_i_foncier as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geomloc, emp.geom);
                                    Create index idx_vm_i_foncier on vm_i_foncier using gist(geomloc);
                                    ', i_foncier, i_emprise);

                                    
                            execute format ('
                                    drop table if exists vm_i_bati_indif;
                                    create temporary table vm_i_bati_indif as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.{33}, emp.geom);
                                    Create index idx_vm_i_bati_indif on vm_i_bati_indif using gist({33});
                                    ', i_bati_indif, i_emprise);



                            --Récupération des routes secondaires qui seront corrélées dans nos calculs
                        Execute format('Create temporary table tt_secondaire as
                            Select ROW_NUMBER() OVEr() as gid, *
                                From (select (st_dump(st_collectionextract(st_union(geom),3))).geom::geometry(polygon,2154) as geom, nature
                                    From (
                                        Select st_buffer(rs.{33}, largeur/2, ''endcap=square join=round'')::geometry(Polygon,2154) as geom, nature
                                        From %1$s rs, %2$s com
                                        Where rs.importance in (''3'', ''4'', ''5'', ''NC'') AND rs.nature not in (''Chemin'', ''Escalier'', ''Piste cyclable'', ''Sentier'')   
                                        AND st_intersects(rs.{33}, com.geom) 
                                        Group by rs.largeur/2, rs.{33}, nature
                                    )tt
                                Group by nature) tt2;
                                Create index idx_tt_secondaire on tt_secondaire using gist(geom);', i_route_sec, i_emprise);
                        
                            --Création de la table qui sera le socle MOS final
                        Drop table if exists {30}.{31};
                        Create table {30}.{31} (
                            to_milit integer,
                            to_bati integer,
                            to_batire integer,
                            to_batagri integer, 
                            to_serre integer, 
                            to_indust integer,
                            to_comer integer,
                            to_zic integer,
                            to_transp integer,
                            to_voiefer integer,
                            to_carrier integer,
                            to_cime integer,
                            to_sport integer,
                            to_loisir integer,
                            to_agri integer,
                            to_veget integer,
                            to_eau integer,
                            to_route integer,
                            to_batimaison integer,
                            pre_scol integer,
                            pre_sante integer,
                            pre_eqadmi integer,
                            pre_o_nrj integer,
                            pre_transp integer,
                            pre_sploi integer,
                            prob_jardin integer,
                            m_fonction character varying,
                            idu character varying,
                            num_parc character varying,
                            tex character varying,
                            section character varying,
                            code_insee character varying,
                            nom_commune character varying,
                            gid serial,
                            geom geometry(Polygon,2154),
                            id_mos character varying,
                            subdi_sirs character varying,                                           
                            code4_{32} integer,
                            lib4_{32} character varying,
                            remarque_{32} character varying,
                            surface_m2 double precision,
                            perimetre double precision,
                            constraint pk_{31} PRIMARY KEY (gid)
                                                                                                
                        );
                        Create index idx_{31}_geom on {30}.{31} using gist(geom);

                            --Parcours de toutes les parcelles pour affecter les calcul de présence qui lui sont propre
                            -- Les calculs sont stockés dans des variables puis insérés en fin de boucle dans la table
                        For v_geom, v_insee, v_idu, v_num_parc, v_tex, v_gid, v_section, v_surf_mos, v_peri_mos IN execute format('Select geom, code_insee, idu, num_parc, tex, gid, section, st_area(geom), st_perimeter(geom) From %1$s sc;', i_socle_c) LOOP
                            if v_idu != 'NC' then
                                --Seul les données cadastrés sont calculés pour cette étape
                        --Ajout des colonnes taux
                            --Calcul du taux de bâtiment militaire
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%3$s''))*100)/st_area(''%3$s''))::integer
                                                From %1$s pm
                                                Where st_intersects(''%3$s'', pm.{33}) 
                                                AND pm.id in (Select pm.id
                                                                From %1$s pm
                                                                Join %2$s p2 on st_intersects(p2.{33}, pm.{33}) 
                                                                Where p2.nature = ''Enceinte militaire'')
                                            ', 'vm_i_surf_acti', 'vm_i_pai_milit', v_geom)
                        into v_tomilit;
                                --Calcul du taux de bâtiment présent sur la parcelle
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where st_intersects(''%2$s'', pm.geom) 
                                            ', 'vm_i_bati', v_geom)
                        into v_tobati;
                                --Calcul du taux de maison présentes sur la parcelles (bati indiferencie)
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_bati_indif', v_geom)
                        into v_tobatimaison;
                                --Calcul du taux de présence de bâtiment remarquable
=======
        cur2.execute(u"""
            Create or replace function public.fun_typage(i_socle_c text, 
                                            i_pai_milit text, 
                                            i_bati text, 
                                            i_bati_rem text, 
                                            i_bati_indus text, 
                                            i_surf_acti text, 
                                            i_aire_tri text, 
                                            i_voie_ferre text,
                                            i_pai_indus_com text,
                                            i_cime text,
                                            i_terrain_sport text,
                                            i_pai_cul_lois text,
                                            i_rpga text,
                                            i_surf_eau text,
                                            i_pai_scens text,
                                            i_pai_sante text,
                                            i_pai_rel text,
                                            i_point_eau text,
                                            i_post_transf text,
                                            i_pai_transp text,
                                            i_pai_sport text,
                                            i_finess text,
                                            i_zveget text,
                                            i_res text,
                                            i_tronfluv text,
                                            i_tsurf text,
                                            i_route_sec text,
                                            i_tronroute text,
                                            i_emprise text,
                                            i_foncier text,
                                            i_bati_indif text
                                            )
                Returns void AS
                --Fonction de calcul des aménagements présents sur les parcelles
                --Met en correlation de nombreuses données recouvrant ou non une parcelle en indiquant la surface de recouvrement, ou si une présence est constaté
            $BODY$
                DECLARE
                    v_geom geometry(polygon,2154); -- Géométrie du socle
                    v_insee character varying; --code insee du socle
                    v_idu character varying; -- code idu du socle
                    v_num_parc character varying;-- num_parc du socle
                    v_tex character varying; -- tex du socle
                    v_gid integer; -- identifiant du socle
                    v_section character varying; --Section du socle
                    v_surf_mos double precision;
                    v_peri_mos double precision;
                    v_cpt_mos integer = 0;
                    v_id_mos character varying;
                    
                    v_tomilit integer;--Taux debâtiments militaire sur la parcelle
                    v_tobati integer;-- Taux de bâtiment sur la parcelle
                    v_tobatire integer; --Taux de bâtiment remarquable sur la parcelle
                    v_tobatagri integer; -- Taux de bâtiment agricole sur la parcelle
                    v_toserre integer; --Taux de serre sur la parcelle
                    v_toindust integer; --Taux de bâtiment industriel sur la parcelle
                    v_tocomer integer; -- Taux de bâtiment commercial sur la parcelle
                    v_tozic integer; -- Taux de de bâtiment industriel ou commercial sur la parcelle
                    v_totransp integer; -- Taux de transport sur la parcelle
                    v_tovoiefer integer; -- Taux de voies férrées sur la parcelle
                    v_tocarrier integer; -- Taux de carrière sur la parcelle
                    v_tocime integer; -- Taux de cimetière sur la parcelle
                    v_tosport integer; -- Taux terrain sport sur la parcelle
                    v_toloisir integer; -- Taux de loisir sur la parcelle
                    v_toagri integer; -- Taux de parcelles agricoles sur la parcelle
                    v_toeau integer; -- Taux d'eau dans la parcelle
                    v_toveget integer; -- Taux de végétation hors agriculture dans la parcelle
                    v_toroute integer; -- Taux de route secondaire dans la parcelle
                    v_tobatimaison integer; -- Taux de batiment maison (bati indiferencie)

                    v_temp_toeau integer; -- Taux temporaire pour comparer plusieurs taux d'eau sur la parcelle
                    v_temp_route integer; -- taux temporaire pour comparer plusieurs taux de route sur la parcelle
                    
                    v_prescol integer; --Présence d'équipement d'enseignement sur la parcelle
                    v_presante integer; -- Présence d'équipement de santé sur la parcelle
                    v_preqadmi integer; -- présence d'équipement local, administration sur la parcelle
                    v_preonrj integer; -- Présence d'équipement eau assainissement énergie sur la parcelle
                    v_pretransp integer; -- Présence d'infrastructure de transport sur la parcelle
                    v_presploi integer; -- Présence sport et loisir

                    v_mfonction character varying;-- Type de bâtiment sur la parcelle
                    v_probjardin integer; --Probabilité de présence de jardin 0|1|2
                BEGIN
                        --Récupération des routes secondaires qui seront corrélées dans nos calculs
                    Execute format('Create temporary table tt_secondaire as
                        Select ROW_NUMBER() OVEr() as gid, *
                            From (select (st_dump(st_collectionextract(st_union(geom),3))).geom::geometry(polygon,2154) as geom, nature
                                From (
                                    Select st_buffer(rs.{33}, largeur/2, ''endcap=square join=round'')::geometry(Polygon,2154) as geom, nature
                                    From %1$s rs, %2$s com
                                    Where rs.importance in (''3'', ''4'', ''5'', ''NC'') AND rs.nature not in (''Chemin'', ''Escalier'', ''Piste cyclable'', ''Sentier'')   
                                    AND st_intersects(rs.{33}, com.geom) 
                                    Group by rs.largeur/2, rs.{33}, nature
                                )tt
                            Group by nature) tt2;
                            Create index idx_tt_secondaire on tt_secondaire using gist(geom);', i_route_sec, i_emprise);
                    
                        --Création de la table qui sera le socle MOS final
                    Drop table if exists {30}.{31};
                    Create table {30}.{31} (
                        to_milit integer,
                        to_bati integer,
                        to_batire integer,
                        to_batagri integer, 
                        to_serre integer, 
                        to_indust integer,
                        to_comer integer,
                        to_zic integer,
                        to_transp integer,
                        to_voiefer integer,
                        to_carrier integer,
                        to_cime integer,
                        to_sport integer,
                        to_loisir integer,
                        to_agri integer,
                        to_veget integer,
                        to_eau integer,
                        to_route integer,
                        to_batimaison integer,
                        pre_scol integer,
                        pre_sante integer,
                        pre_eqadmi integer,
                        pre_o_nrj integer,
                        pre_transp integer,
                        pre_sploi integer,
                        prob_jardin integer,
                        m_fonction character varying,
                        idu character varying,
                        num_parc character varying,
                        tex character varying,
                        section character varying,
                        code_insee character varying,
                        nom_commune character varying,
                        gid serial,
                        geom geometry(Polygon,2154),
                        id_mos character varying,
                        subdi_sirs character varying,                                           
                        code4_{32} integer,
                        lib4_{32} character varying,
                        remarque_{32} character varying,
                        surface_m2 double precision,
                        perimetre double precision,
                        constraint pk_{31} PRIMARY KEY (gid)
                                                                                            
                    );
                    Create index idx_{31}_geom on {30}.{31} using gist(geom);

                        --Parcours de toutes les parcelles pour affecter les calcul de présence qui lui sont propre
                        -- Les calculs sont stockés dans des variables puis insérés en fin de boucle dans la table
                    For v_geom, v_insee, v_idu, v_num_parc, v_tex, v_gid, v_section, v_surf_mos, v_peri_mos IN execute format('Select geom, code_insee, idu, num_parc, tex, gid, section, st_area(geom), st_perimeter(geom) From %1$s sc;', i_socle_c) LOOP
                        if v_idu != 'NC' then
                            --Seul les données cadastrés sont calculés pour cette étape
                    --Ajout des colonnes taux
                        --Calcul du taux de bâtiment militaire
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%3$s''))*100)/st_area(''%3$s''))::integer
                                            From %2$s pm
                                            Where st_intersects(''%3$s'', pm.{33}) 
                                            AND pm.id in (Select pm.id
                                                            From %1$s pm
                                                            Join %2$s p2 on st_intersects(p2.{33}, pm.{33}) 
                                                            Where p2.nature = ''Enceinte militaire'')
                                        ', i_surf_acti, i_pai_milit, v_geom)
                    into v_tomilit;
                            --Calcul du taux de bâtiment présent sur la parcelle
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_bati, v_geom)
                    into v_tobati;
                            --Calcul du taux de maison présentes sur la parcelles (bati indiferencie)
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.{33}) 
                                        ', i_bati_indif, v_geom)
                    into v_tobatimaison;
                            --Calcul du taux de présence de bâtiment remarquable
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Chapelle'', ''Château'', ''Fort, blockhaus, casemate'', ''Monument'', ''Tour, donjon, moulin'', ''Arène ou théàtre antique'') 
                                            AND st_intersects(''%2$s'', pm.{33}) 
                                        ', i_bati_rem, v_geom)
                    into v_tobatire;
                            --Calcul du taux de présence de bâtiments agricole
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Bâtiment agricole'') 
                                            AND st_intersects(''%2$s'', pm.{33}) 
                                        ', i_bati_indus, v_geom)
                    into v_tobatagri;
                            --Calcul du taux de présence de serres
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Serre'') 
                                            AND st_intersects(''%2$s'', pm.{33}) 
                                        ', i_bati_indus, v_geom)
                    into v_toserre;
                            --Calcul du taux de présence de bâtiments industriel
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Bâtiment industriel'') 
                                            AND st_intersects(''%2$s'', pm.{33}) 
                                        ', i_bati_indus, v_geom)
                    into v_toindust;
                            --Calcul du taux de présence de bâtiments commerciaux
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Bâtiment commercial'') 
                                            AND st_intersects(''%2$s'', pm.{33}) 
                                        ', i_bati_indus, v_geom)
                    into v_tocomer;
                            --Calcul du taux de présence de bâtiments industriels ou commerciaux
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.categorie in (''Industriel ou commercial'') 
                                            AND st_intersects(''%2$s'', pm.{33}) 
                                        ', i_surf_acti, v_geom)
                    into v_tozic;
                            --Calcul du taux de présence d'équipement de transport
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.categorie in (''Transport'') 
                                            AND st_intersects(''%2$s'', pm.{33}) 
                                        ', i_surf_acti, v_geom)
                    into v_totransp;
                            --Calcul du taux de présence de voies férrées
                        execute format ('Select ((st_area(st_safe_intersection(st_union(st_buffer(pm.{33}, 3 * pm.nb_voies,''endcap=flat join=round'')), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.{33}) 
                                        ', i_voie_ferre, v_geom)
                    into v_tovoiefer;
                    if v_tovoiefer in (null) or v_tovoiefer <1 THEN
                            --Si pas de voie férrées détéctées, recherche avec les aires de triage
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.{33}) 
                                        ', i_aire_tri, v_geom)
                    into v_tovoiefer;
                    END IF;
                            --Calcul du taux de présence de carrières
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%3$s''))*100)/st_area(''%3$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%3$s'', pm.{33}) 
                                            AND pm.id in (Select pm.id
                                                            From %1$s pm
                                                            Join %2$s p2 on st_intersects(p2.{33}, pm.{33}) 
                                                            Where p2.nature = ''Carrière'' )
                                        ',i_surf_acti,  i_pai_indus_com, v_geom)
                    into v_tocarrier;
                            --Calcul du taux de présence de cimetières
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.{33}) 
                                        ', i_cime, v_geom)
                    into v_tocime;
                            --Calcul du taux de présence d'équipement sportif
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where categorie = ''Sport''
                                            AND st_intersects(''%2$s'', pm.{33}) 
                                        ', i_surf_acti, v_geom)
                    into v_tosport;
                    IF v_tosport in (null) or v_tosport < 1 THEN
                                --Si pas d'équipement trouvés, on recherche avec les données IGN terrain de sport
                                    execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.{33}) 
                                        ', i_terrain_sport, v_geom)
                    into v_tosport;
                    END IF;
                            --Calcul du taux de présence d'aménagement loisir
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%3$s''))*100)/st_area(''%3$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%3$s'', pm.{33})
                                            AND pm.id in (Select pm.id 
                                                            From %1$s pm
                                                            Join %2$s p2 on st_intersects(p2.{33}, pm.{33})
                                                            Where p2.nature in (''Village de vacances'', ''Camping'', ''Parc de loisirs'', ''Parc zoologique'', ''parc des expositions'' ))
                                        ', i_surf_acti, i_pai_cul_lois, v_geom)
                    into v_toloisir;
                            --Calcul du taux de présence des parcelles agricoles
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_rpga, v_geom)
                    into v_toagri;
                        If v_toagri in (null) or v_toagri < 1 Then
                                --Si pas de correspondance, on recherche aussi avec les zone de végétation peupleraies et verger
>>>>>>> master
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where pm.nature in (''Chapelle'', ''Château'', ''Fort, blockhaus, casemate'', ''Monument'', ''Tour, donjon, moulin'', ''Arène ou théàtre antique'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_bati_rem', v_geom)
                        into v_tobatire;
                                --Calcul du taux de présence de bâtiments agricole
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where pm.nature in (''Bâtiment agricole'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_bati_indus', v_geom)
                        into v_tobatagri;
                                --Calcul du taux de présence de serres
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where pm.nature in (''Serre'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_bati_indus', v_geom)
                        into v_toserre;
                                --Calcul du taux de présence de bâtiments industriel
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where pm.nature in (''Bâtiment industriel'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_bati_indus', v_geom)
                        into v_toindust;
                                --Calcul du taux de présence de bâtiments commerciaux
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where pm.nature in (''Bâtiment commercial'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_bati_indus', v_geom)
                        into v_tocomer;
                                --Calcul du taux de présence de bâtiments industriels ou commerciaux
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where pm.categorie in (''Industriel ou commercial'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_surf_acti', v_geom)
                        into v_tozic;
                                --Calcul du taux de présence d'équipement de transport
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where pm.categorie in (''Transport'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_surf_acti', v_geom)
                        into v_totransp;
                                --Calcul du taux de présence de voies férrées
                            execute format ('Select coalesce(((st_area(st_safe_intersection(st_union(st_buffer(pm.{33}, 3 * pm.nb_voies,''endcap=flat join=round'')), ''%2$s''))*100)/st_area(''%2$s''))::integer, 0)
                                                From %1$s pm
                                                Where st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_voie_ferre', v_geom)
                        into v_tovoiefer;
                        if v_tovoiefer = 0 THEN
                                --Si pas de voie férrées détéctées, recherche avec les aires de triage
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_aire_tri', v_geom)
                        into v_tovoiefer;
                        END IF;
                                --Calcul du taux de présence de carrières
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%3$s''))*100)/st_area(''%3$s''))::integer
                                                From %1$s pm
                                                Where st_intersects(''%3$s'', pm.{33}) 
                                                AND pm.id in (Select pm.id
                                                                From %1$s pm
                                                                Join %2$s p2 on st_intersects(p2.{33}, pm.{33}) 
                                                                Where p2.nature = ''Carrière'' )
                                            ','vm_i_surf_acti',  'vm_i_pai_indus_com', v_geom)
                        into v_tocarrier;
                                --Calcul du taux de présence de cimetières
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_cime', v_geom)
                        into v_tocime;
                                --Calcul du taux de présence d'équipement sportif
                            execute format ('Select coalesce(((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer,0)
                                                From %1$s pm
                                                Where st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_terrain_sport', v_geom)
                        into v_tosport;
                            
                        IF v_tosport = 0 THEN
                                    --Si pas d'équipement trouvés, on recherche avec les données IGN terrain de sport
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where categorie = ''Sport''
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_surf_acti', v_geom)
                        into v_tosport;
                        END IF;
                                --Calcul du taux de présence d'aménagement loisir
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%3$s''))*100)/st_area(''%3$s''))::integer
                                                From %1$s pm
                                                Where st_intersects(''%3$s'', pm.{33})
                                                AND pm.id in (Select pm.id 
                                                                From %1$s pm
                                                                Join %2$s p2 on st_intersects(p2.{33}, pm.{33})
                                                                Where p2.nature in (''Village de vacances'', ''Camping'', ''Parc de loisirs'', ''Parc zoologique'', ''parc des expositions'' ))
                                            ', 'vm_i_surf_acti', 'vm_i_pai_cul_lois', v_geom)
                        into v_toloisir;
                                --Calcul du taux de présence des parcelles agricoles
                            execute format ('Select coalesce(((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer,0)
                                                From %1$s pm
                                                Where st_intersects(''%2$s'', pm.geom) 
                                            ', 'vm_i_rpga', v_geom)
                        into v_toagri;
                            If v_toagri = 0 Then
                                    --Si pas de correspondance, on recherche aussi avec les zone de végétation peupleraies et verger
                                execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where nature in (''Verger'', ''Peupleraie'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_zveget', v_geom)
                        into v_toagri;
                            END IF;

                                --Calcul du taux de présence de végétation qui ne sont pas verger ou peupleraie
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where nature not in (''Verger'', ''Peupleraie'') 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_zveget', v_geom)
                        into v_toveget;
                                --Calcul de présence des surface en eau permanentes
                            execute format ('Select coalesce(((st_area(st_safe_intersection(st_union(pm.{33}), ''%2$s''))*100)/st_area(''%2$s''))::integer, 0)
                                                From %1$s pm
                                                Where regime = ''Permanent'' 
                                                AND st_intersects(''%2$s'', pm.{33}) 
                                            ', 'vm_i_surf_eau', v_geom)
                        into v_toeau;
                                --Calcul du taux de présence de l'eau des données edigeoo geo_tronfluv
                            execute format ('Select coalesce(((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer,0)
                                                From %1$s pm
                                                Where  st_intersects(''%2$s'', pm.geom) 
                                            ', 'vm_i_tronfluv', v_geom)
                        into v_temp_toeau;
                        if v_temp_toeau > v_toeau Then
                                --Si les données édigéos apportent plus de valeur, on garde cette données qui écrase les surface en eau IGN
                            v_toeau = v_temp_toeau;
                        End if;
                                --Calcul du taux de présence de l'eau des données edigeo geo_tsurf
                            execute format ('Select coalesce(((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer,0)
                                                From %1$s pm
                                                Where  st_intersects(''%2$s'', pm.geom) 
                                            ', 'vm_i_tsurf', v_geom)
                        into v_temp_toeau;
                        if v_temp_toeau > v_toeau Then
                            --Si les données tsurf sont plus importantes que les autres, on écrases les gardes
                            v_toeau = v_temp_toeau;
                        End if;
                            --Calcul du taux de présence des routes secondaire
                        Select ((st_area(st_safe_intersection(st_union(pm.geom), v_geom))*100)/st_area(v_geom))::integer
                                                From tt_secondaire pm
                                                Where  st_intersects(v_geom, pm.geom)       
                        into v_toroute;
                                --Calcul du taux de présence des routes edigeo geo_tronroute
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                From %1$s pm
                                                Where  st_intersects(''%2$s'', pm.geom) 
                                            ', 'vm_i_tronroute', v_geom)
                        into v_temp_route;
                        if v_toroute < v_temp_route Then
                            --Si les données edigeo sont plus impotantes, on les gardes
                            v_toroute = v_temp_route;
                        end if;
                        
                                --Ajout des colonnes bool
                            --Enseignement
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where pm.nature like ''Enseignement%%''
                                                AND st_intersects(st_buffer(pm.{33}, 5), ''%2$s'') 
                                            ', 'vm_i_pai_scens', v_geom)
                        into v_prescol;
                        if v_prescol < 1 Then 
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where categorie = ''Enseignement'' 
                                                AND ((st_area(st_safe_intersection(pm.{33}, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 40 
                                            ', 'vm_i_surf_acti', v_geom)
                        into v_prescol;
                    
                            if v_prescol < 1 Then 
                                v_prescol = 0;
                            end if;
                        end if;

                            --Sante
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where st_intersects(st_buffer(pm.{33}, 5), ''%2$s'') 
                                            ', 'vm_i_pai_sante', v_geom)
                        into v_presante;
            
                        if v_presante = 0 Then 
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where categorie = ''Santé'' 
                                                AND ((st_area(st_safe_intersection(pm.{33}, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 50 
                                            ', 'vm_i_surf_acti', v_geom)
                        into v_presante;
                            if v_presante = 0 THEN
                                execute format ('Select count(*)
                                                    From %1$s pm
                                                    Where libcateget not like ''Pharmacie'' and libcateget not like ''Service%%''
                                                    AND st_intersects(''%2$s'', pm.geom)
                                            ', 'vm_i_finess', v_geom)
                            into v_presante;
                                if v_presante < 1 Then 
                                    v_presante = 0;
                                end if;
                            end if;
                        end if;

                            --Administration
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where nature in (''Eglise'', ''Bâtiment religieux divers'', ''Gare'', ''Mairie'', ''Préfecture'', ''Sous-préfecture'', ''Divers public ou administratif'')
                                                AND st_intersects(st_buffer(pm.{33}, 5), ''%2$s'') 
                                            ', 'vm_i_pai_milit', v_geom)
                        into v_preqadmi;
                        if v_preqadmi < 1 Then 
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where nature in (''Culte catholique ou orthodoxe'', ''Culte protestant'') 
                                                AND st_intersects(st_buffer(pm.{33}, 5), ''%2$s'') 
                                            ', 'vm_i_pai_rel', v_geom)
                        into v_preqadmi;
                    
                            if v_preqadmi < 1 Then 
                                execute format ('Select count(*)
                                                    From %1$s pm
                                                    Where nature in (''Eglise'', ''Mairie'', ''Préfecture'', ''Sous-préfecture'') 
                                                    AND ((st_area(st_safe_intersection(pm.{33}, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 50 
                                                ', 'vm_i_bati_rem', v_geom)
                            into v_preqadmi;
                    
                                IF v_preqadmi < 1 Then
                                    v_preqadmi = 0;
                                end if;
                            end if;
                        end if;

                            --Eau, énergie
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where nature = (''Station de pompage'')
                                                AND st_intersects(st_buffer(pm.{33}, 5), ''%2$s'') 
                                            ', 'vm_i_point_eau', v_geom)
                        into v_preonrj;
                        if v_preonrj < 1 Then 
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where categorie in (''Gestion des eaux'')
                                                AND ((st_area(st_safe_intersection(pm.{33}, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 40
                                            ', 'vm_i_surf_acti', v_geom)
                        into v_preonrj;

                            if v_preonrj < 1 Then 
                                execute format ('Select count(*)
                                                    From %1$s pm
                                                    Where  ((st_area(st_safe_intersection(pm.{33}, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 40 
                                                ', 'vm_i_post_transf', v_geom)
                            into v_preonrj;

                                If v_preonrj < 1 Then 
                                    v_preonrj = 0;
                                end if;
                            end if;
                        end if;

                            --Transport
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where nature in (''Gare routière'',''Gare voyageurs et fret'', ''Gare voyageurs uniquement'', ''Parking'')
                                                AND st_intersects(pm.{33}, ''%2$s'') 
                                            ', 'vm_i_pai_transp', v_geom)
                        into v_pretransp;
                        If v_pretransp != 1 Then 
                            v_pretransp = 0;
                        end if;

                            --Sport, loisir
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where st_intersects(st_buffer(pm.{33}, 5), ''%2$s'') 
                                            ', 'vm_i_pai_sport', v_geom)
                        into v_presploi;
                        If v_presploi < 1 Then
                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where naturelibe != ''Intérieur''
                                                AND st_intersects(pm.geom, ''%2$s'') 
                                            ', 'vm_i_res', v_geom)
                        into v_presploi;
                            IF v_presploi < 1 Then
                                execute format ('Select 2
                                                From %1$s pm
                                                Where naturelibe = ''Intérieur''
                                                AND st_intersects(pm.geom, ''%2$s'') 
                                            ', 'vm_i_res', v_geom)
                            into v_presploi;
                                If v_presploi != 1 Then
                                    v_presploi = 0;
                                end if;
                            end if;
                        end if; 

                        --Traitement fichiers foncier
                            execute format ('Select tlocdomin
                                                From %1$s pm
                                                Where st_intersects(pm.geomloc, ''%2$s'')
                                                order by tlocdomin desc
                                            ', 'vm_i_foncier', v_geom)
                        into v_mfonction;

                            execute format ('Select count(*)
                                                From %1$s pm
                                                Where st_intersects(pm.geomloc, ''%2$s'')
                                                and (pm.dcnt09 > 1 or pm.dcnt11 > 1)
                                            ', 'vm_i_foncier',  v_geom)
                        into v_probjardin;
                        --Récupération de l'identifiant unique
                        v_id_mos = left(v_insee,2) || v_num_parc;

                            else
                                v_cpt_mos = v_cpt_mos +1;
                                v_tomilit = null;
                                v_tobati = null;
                                v_tobatire = null; 
                                v_tobatagri = null;
                                v_toserre = null ;
                                v_toindust = null ;
                                v_tocomer = null ;
                                v_tozic = null ;
                                v_totransp= null; 
                                v_tovoiefer = null;
                                v_tocarrier = null ;
                                v_tocime = null;
                                v_tosport = null; 
                                v_toloisir = null;
                                v_toagri = null;
                                v_toveget = null;
                                v_toeau = null ;
                                v_toroute = null;
                                v_prescol = null;
                                v_presante = null;
                                v_preqadmi = null;
                                v_preonrj = null;
                                v_pretransp = null;
                                v_presploi = null;
                                v_mfonction = null;
                                v_probjardin = null;
                                v_id_mos = v_insee || 'NC' ||  v_cpt_mos;
                            end if;

                        
                        
                            INSERT INTO {30}.{31}(code_insee, idu, num_parc, tex, section, geom, 
                                                            to_milit, 
                                                            to_bati, 
                                                            to_batire, 
                                                            to_batagri, 
                                                            to_serre, 
                                                            to_indust, 
                                                            to_comer, 
                                                            to_zic, 
                                                            to_transp, 
                                                            to_voiefer, 
                                                            to_carrier, 
                                                            to_cime, 
                                                            to_sport,
                                                            to_loisir,
                                                            to_agri,
                                                            to_veget,
                                                            to_eau,
                                                            to_route,
                                                            to_batimaison,
                                                            pre_scol,
                                                            pre_sante,
                                                            pre_eqadmi,
                                                            pre_o_nrj,
                                                            pre_transp,
                                                            pre_sploi,
                                                            m_fonction,
                                                            prob_jardin,
                                                            id_mos,
                                                            surface_m2,
                                                            perimetre) values
                            (v_insee, v_idu, v_num_parc, v_tex,v_section, v_geom, 
                                v_tomilit, 
                                v_tobati, 
                                v_tobatire, 
                                v_tobatagri, 
                                v_toserre, 
                                v_toindust, 
                                v_tocomer, 
                                v_tozic, 
                                v_totransp, 
                                v_tovoiefer, 
                                v_tocarrier, 
                                v_tocime, 
                                v_tosport,
                                v_toloisir,
                                v_toagri,
                                v_toveget,
                                v_toeau,
                                v_toroute,
                                v_tobatimaison,
                                v_prescol,
                                v_presante,
                                v_preqadmi,
                                v_preonrj,
                                v_pretransp,
                                v_presploi,
                                v_mfonction,
                                v_probjardin,
                                v_id_mos,
                                v_surf_mos,
                                v_peri_mos
                            );
                            
                            
                        END LOOP;

                    RETURN;
                    END;
                $BODY$
                    LANGUAGE 'plpgsql';



                select public.fun_typage('{35}', 
                            '{0}', 
                            '{1}', 
                            '{2}', 
                            '{3}', 
                            '{4}', 
                            '{5}',
                            '{6}',
                            '{7}',
                            '{8}',
                            '{9}',
                            '{10}',
                            '{11}',
                            '{12}',
                            '{13}',
                            '{14}',
                            '{15}',
                            '{16}',
                            '{17}',
                            '{18}',
                            '{19}',
                            '{20}',
                            '{21}',
                            '{22}',
                            '{23}',
                            '{24}',
                            '{25}',
                            '{26}',
                            '{27}',
                            '{28}',
                            '{29}'
                            );
                        update {30}.{31} x 
                        set nom_commune = nom_com
                        From {27} y where x.code_insee = y.code_insee

                """.format(self.cb_paimilit.currentText(),#0
                            self.cb_geobati.currentText(),#1
                            self.cb_remarquable.currentText(),#2
                            self.cb_indust.currentText(),#3
                            self.cb_surf_acti.currentText(),#4
                            self.cb_triage.currentText(),#5
                            self.cb_voiefer.currentText(),#6
                            self.cb_paicom.currentText(),#7
                            self.cb_cime.currentText(),#8
                            self.cb_terrainsport.currentText(),#9
                            self.cb_pai_cult.currentText(),#10
                            self.cb_rpga.currentText(),#11
                            self.cb_surf_eau.currentText(),#12
                            self.cb_paiens.currentText(),#13
                            self.cb_paisante.currentText(),#14
                            self.cb_pairel.currentText(),#15
                            self.cb_pt_eau.currentText(),#16
                            self.cb_paitransfo.currentText(),#17
                            self.cb_paitransp.currentText(),#18
                            self.cb_paisport.currentText(),#19
                            self.cb_finess.currentText(),#20
                            self.cb_zoneveget.currentText(),#21
                            self.cb_res_sport.currentText(),#22
                            self.cb_tronfluv.currentText(),#23
                            self.cb_tsurf.currentText(),#24
                            self.cb_route.currentText(),#25
                            self.cb_tronroute.currentText(),#26
                            self.cb_parcellaire.currentText(),#27
                            self.cb_ff_parcelle.currentText(),#28
                            self.cb_indif.currentText(),#29
                            self.cb_schema.currentText(),#30
                            self.le_destination.text(),#31
                            self.le_annee.text(),#32
                            self.geom,#33
                            self.schema_geom,#34
                            self.socle_geom,#35
                        )
                )
            #Récupération du message d'erreur dans un message box critical
        except Exception as exc:
            exc = str(exc).decode('utf-8')
            QMessageBox.critical(self, 'Erreur', u'Un problème est survenu : {0}'.format(exc),
                         QMessageBox.Ok)
        cur2.close()
        self.conn.commit()
        temp = QTimer 
            #Choix des étapes à suivre
        if self.cas_etape == 1:
            #Cas 1 : on passe à l'étape 3 avant de finir
            self.lbl_etape.setText(u'Etape 3/3 : Calcul des code4 à attribuer')
            self.pb_avancement.setValue(70)
            temp.singleShot(100, self.getCode4)
        elif self.cas_etape == 2 or self.cas_etape == 5:
            #Cas 5 : on termine
            self.lbl_etape.setText(u'Terminé')
            self.pb_avancement.setValue(100)
        elif self.cas_etape == 4:
            #Cas 4 on passe à l'étape 3 avant de finir 
            self.lbl_etape.setText(u'2/2 : Calcul des code4 à attribuer')
            self.pb_avancement.setValue(100)
            temp.singleShot(100, self.getCode4)
    
        #temp.singleShot(100, self.getCode4)
 #       time.sleep(15)
            #Lancement de la troisième et dernière étape
        #self.getCode4()

    def getCode4(self):
        #Fonction de création du socle troisième étape
        #Génération du code en fonction des taux de présence
        cur3 = self.conn.cursor()
        cur3.execute(u"""
                DO 
                LANGUAGE plpgsql
                $BODY$
                    DECLARE
                        v_socle record;-- Variable récupérant les données du socle  partie C à comparer

                        v_socle_nc record; -- Variable récupérant les données du socle partie NC à comparer

                        v_hab_act record; -- Variable récupérant les données des code 1112, 121, 1211, 1212, 1225

                        v_vacant record; --Variable récupérant les données du socle pour définir les terrains vacants

                        v_secondaire_nc record; -- Variable récupérant les données du socle pour définir les routes selon desserte

                        v_code4 integer; --Variable récupérant le code de la nomenclature à insérer
                        v_lib4 character varying; -- Variable récupérant le libelle de la nomenclature correspondant

                        v_hab_act_geom1 geometry;--Code 1112
                        v_hab_act_geom2 geometry;--Code 121, 1211, 1212, et 1217

                        v_vac_geom1 geometry;--Code 1112, 1113 et 1114
                        v_vac_geom2 geometry;--Code 121, 1211, 1212, 1217

                        v_sec_geom1 geometry;--Code 1114
                        v_sec_geom2 geometry;--Code 1211,1212,1217
                        v_sec_geom3 geometry;--Code 1112,1113

                        v_is_maison integer;
                        v_is_jardin integer;
                    BEGIN
                        For v_socle in Select * from {0}.{1} where idu != 'NC' LOOP
                            v_code4 = 0;

                            if v_socle.to_milit >= 20 then
                                v_code4 = 1110;
                                v_lib4 = 'Défense (Espace naturel)';

                            elsif v_socle.m_fonction = 'MAISON' or v_socle.m_fonction = 'DEPENDANCE' then
                                if v_socle.to_voiefer > 5 then
                                    v_code4 = 1221;
                                    v_lib4 = 'Infrastructure de transport';
                                elsif v_socle.to_agri > 50 Then 
                                    v_code4 = 2511;
                                    v_lib4 = 'Terre agricole';
                                else
                                    v_code4 = 1112;
                                    v_lib4 = 'Habitat individuel';
                                end if;
   
                            elsif v_socle.m_fonction = 'APPARTEMENT' then
                                v_code4 = 1113;
                                v_lib4 = 'Habitat collectif';

                            elsif v_socle.m_fonction = 'MIXTE' then
                                v_code4 = 1114;
                                v_lib4 = 'Urbain mixte (habitat/activité tertiaire)';

                            elsif v_socle.to_carrier > 40 then
                                v_code4 = 1311;
                                v_lib4 = 'Carrière';

                            elsif v_socle.to_cime > 40 then
                                v_code4 = 1411;
                                v_lib4 = 'Cimetière';

                            elsif v_socle.to_batimaison > 30 then
                                if v_socle.pre_scol > 0  then
                                    v_code4 = 1213;
                                    v_lib4 = 'Equipement d''enseignement';
                                elsif v_socle.pre_sante > 0 then
                                    v_code4 = 1214;
                                    v_lib4 = 'Equipement de santé';
                                elsif v_socle.to_voiefer > 5 then
                                    v_code4 = 1221;
                                    v_lib4 = 'Infrastructure de transport';
                                elsif v_socle.to_agri > 50 Then 
                                    v_code4 = 2511;
                                    v_lib4 = 'Terre agricole';
                                else
                                    v_code4 = 1112;
                                    v_lib4 = 'Habitat individuel';
                                end if;

                            elsif v_socle.to_batire > 50 then
                                v_code4 = 1122;
                                v_lib4 = 'Bâtiment remarquable';

                            elsif v_socle.to_batagri >= 20 then
                                v_code4 = 1131;
                                v_lib4 = 'Bâtiment agricole';

                            elsif v_socle.to_serre >= 20 then
                                v_code4 = 2121;
                                v_lib4 = 'Serre';

                            elsif v_socle.pre_scol > 0 then
                                v_code4 = 1213;
                                v_lib4 = 'Equipement d''enseignement';

                            elsif v_socle.pre_sante > 0 then
                                v_code4 = 1214;
                                v_lib4 = 'Equipement de santé';

                            elsif v_socle.pre_eqadmi > 0 then
                                v_code4 = 1215;
                                v_lib4 = 'Autre équipement local, administration';

                            elsif v_socle.pre_o_nrj > 0 then
                                v_code4 = 1216;
                                v_lib4 = 'Equipement pour eau, assainissement, énergie';

                            elsif v_socle.to_sport > 50 or v_socle.to_loisir > 50 or v_socle.pre_sploi = 1 then
                                if v_socle.to_bati > 50 then
                                    v_code4 = 1422;
                                    v_lib4 = 'Equipement sportif (construit)';
                                else
                                    v_code4 = 1421;
                                    v_lib4 = 'Sport et loisir';
                                end if;
                            
                            elsif v_socle.pre_sploi = 2 then
                                v_code4 = 1422;
                                v_lib4 = 'Equipement sportif (construit)';

                            elsif v_socle.prob_jardin > 0 then
                                if v_socle.to_agri > 50 then
                                    v_code4 = 2511;
                                    v_lib4 = 'Terre agricole';
                                elsif v_socle.to_veget > 50 then
                                    v_code4 = 3261;
                                    v_lib4 = 'Espace boisé';
                                else
                                    v_code4 = 1412;
                                    v_lib4 = 'Parc et jardin';
                                end if;
                            elsif v_socle.to_agri > 50 then
                                v_code4 = 2511;
                                v_lib4 = 'Terre agricole';
                            elsif v_socle.to_veget > 50 then
                                    v_code4 = 3261;
                                    v_lib4 = 'Espace boisé';                               
                            elsif v_socle.m_fonction = '' and v_socle.to_bati > 50  then
                                v_code4 = 1115;
                                v_lib4 = 'Bâti divers';



                            elsif v_socle.m_fonction = 'ACTIVITE' or v_socle.to_zic >= 20 or v_socle.to_comer >= 20 or v_socle.to_indust >= 20 or v_socle.to_bati > 50 then
                                if v_socle.to_indust >= 20 then
                                    v_code4 = 1212;
                                    v_lib4 = 'Activité autre que tertiaire';
                                elsif v_socle.to_comer >= 20 then
                                    v_code4 = 1217;
                                    v_lib4 = 'Surface commerciale';
                                elseif v_socle.to_zic >= 20 then
                                    v_code4 = 121;
                                    v_lib4 = '';
                                else 
                                    v_code4 = 1115;
                                    v_lib4 = 'Bâti divers';
                                end if;

                            elsif v_socle.to_voiefer > 5 or v_socle.pre_transp = 1 then
                                v_code4 = 1221;
                                v_lib4 = 'Infrastructure de transport';

                            elsif v_socle.to_route > 50 then
                                v_code4 = 1222;
                                v_lib4 = 'Voie desserte habitat';
                            elsif v_socle.to_eau > 50 then
                                v_code4 = 5121;
                                v_lib4 = 'Plan d''eau';

                            else 
                                v_code4 = 3251;
                                v_lib4 = 'Espace naturel';

                            end if;

                            if v_code4 = 3251 and v_socle.to_batimaison > 10 then
                                  Select count(*)
                                            From {0}.{1} pm
                                            Where idu = v_socle.idu
                                            and m_fonction = 'MAISON'
                                into v_is_maison;
                                if v_is_maison > 0 then
                                    v_code4 = 1112;
                                    v_lib4 = 'Habitat individuel';
                                end if;
                            elsif v_code4 = 3251 and  v_socle.to_batimaison > 1 then
                                  Select count(*)
                                            From {0}.{1} pm
                                            Where idu = v_socle.idu
                                            and m_fonction = 'MAISON'
                                into v_is_maison;
                                if v_is_maison > 0 then
                                    v_code4 = 1412;
                                    v_lib4 = 'Parc et jardin';
                                end if;
                            end if;

                            if v_code4 = 3251 then
                                 Select count(*)
                                            From {0}.{1} pm
                                            Where idu = v_socle.idu
                                            and prob_jardin > 0
                                into v_is_jardin;
                                if v_is_jardin > 0 then
                                  v_code4 = 1412;
                                    v_lib4 = 'Parc et jardin';
                                elsif v_socle.to_bati > 30 Then
                                    v_code4 = 1115;
                                    v_lib4 = 'Bâti divers';
                                end if;
                            end if;  

                            update  {0}.{1}
                                Set code4_{2} = v_code4,
                                    lib4_{2} = v_lib4
                                Where gid = v_socle.gid;
                        END LOOP;
                        For v_socle in Select * From {0}.{1} where idu != 'NC' and code4_{2} = 3251 LOOP

                            if (st_perimeter(v_socle.geom)/(2 * sqrt(3.14* st_area(v_socle.geom)))) > 3 then

                                select st_union(geom) as geom From {0}.{1} where code4_{2} = 1112 and  st_intersects(st_buffer(v_socle.geom, 2),geom)
                                into v_hab_act_geom1;

                                if v_hab_act_geom1 not in (null) then
                                    v_code4 = 1222;
                                    v_lib4 = 'Voie desserte habitat';
                                else
                                    select st_union(geom) as geom From {0}.{1} where code4_{2} in (121, 1211, 1212, 1217) and  st_intersects(st_buffer(v_socle.geom, 2),geom)
                                    into v_hab_act_geom2;

                                    if v_hab_act_geom2 not in (null) then
                                        v_code4 = 1223;
                                        v_lib4 = 'Voie desserte activité';
                                    else
                                        v_code4 = 1225;
                                        v_lib4 = 'Chemin-sentier';
                                    end if;
                                end if;
                    
                            else

                                select st_union(geom) as geom From {0}.{1} where code4_{2} in (1112, 1113, 1114) and  st_intersects(st_buffer(v_socle.geom, 5),geom)
                                into v_vac_geom1;

                                if v_vac_geom1  not in (null) then
                                    if st_area(st_intersection(st_buffer(v_socle.geom, 5), v_vac_geom1)) > 33 then
                                        if v_socle.to_batimaison > 50 Then
                                            v_code4 = 1112;
                                            v_lib4 = 'Habitat individuel';
                                        else
                                            v_code4 = 1331;
                                            v_lib4 = 'Terrain vacant - habitat';
                                        end if;
                                    end if;
                                else
                                select st_union(geom) as geom From {0}.{1} where code4_{2} in (121, 1211, 1212, 1217) and  st_intersects(st_buffer(v_socle.geom, 5),geom)
                                    into v_vac_geom2;

                                    if v_vac_geom2 not in (null) then
                                        if st_area(st_intersection(st_buffer(v_socle.geom, 5), v_vac_geom1)) > 33 then
                                            v_code4 = 1332;
                                            v_lib4 = 'Terrain vacant - activité';
                                        end if;
                                    end if;
                                end if;
                            end if;

                            update  {0}.{1}
                                Set code4_{2} = v_code4,
                                lib4_{2} = v_lib4
                                Where gid = v_socle.gid;

                        End loop;
                        For v_socle in Select * From {0}.{1} where idu != 'NC' and code4_2018 = 1225 order by gid LOOP
                            if (st_perimeter(v_socle.geom)/(2 * sqrt(3.14* st_area(v_socle.geom)))) > 3 then

                                else 
                                    update {0}.{1} 
                                    set code4_{2} = 3251,
                                        lib4_{2} = 'Espace naturel'
                                        where gid = v_socle.gid;
                                end if;
                        end loop ;

                        For v_socle_nc in Select * from {0}.{1} where idu = 'NC' LOOP

                            if v_socle_nc.tex like 'Plage' then
                                v_code4 = 3311;
                                v_lib4 = 'Plage, dune et sable';

                            elsif v_socle_nc.tex like 'Rochers, falaise' then
                                v_code4 = 3321;
                                v_lib4 = 'Rocher et falaise';

                            elsif v_socle_nc.tex = 'primaire' then
                                v_code4 = 1221;
                                v_lib4 = 'Infrastructure de transport';

                            elsif v_socle_nc.tex = 'secondaire' then
                                For v_secondaire_nc in Select st_union(st_buffer(geom,5)) as geom, code4_{2} From {0}.{1} 
                                                                                                            Where code4_{2} in (1114, 1211, 1212, 1217, 1112, 1113) 
                                                                                                            and st_intersects(v_socle_nc.geom, st_buffer(geom, 5))
                                                                                                            Group by code4_{2} Loop
                                    if v_secondaire_nc.code4_{2} = 1114 then
                                        v_code4 = 1224;
                                        v_lib4 = 'Voie desserte mixte';
                                    elsif v_secondaire_nc.code4_{2} in (1211, 1212, 1217) then
                                        v_code4 = 1223;
                                        v_lib4 = 'Voie desserte activité';
                                    else
                                        v_code4 = 1222;
                                        v_lib4 = 'Voie desserte habitat';
                                    end if;
                                end loop;
                                if v_code4 is null then
                                    v_code4 = 1221;
                                    v_lib4 = 'Infrastructure de transport';
                                end if;

                            elsif v_socle_nc.tex = 'chemin' then
                                v_code4 = 1225;
                                v_lib4 = 'Chemin-sentier';

                            elsif v_socle_nc.tex = 'hydro' then
                                v_code4 = 5131;
                                v_lib4 = 'Réseau hydrographique';

                            elsif v_socle_nc.tex = 'agricole' then
                                v_code4 = 2511;
                                v_lib4 = 'Terre agricole';

                            elsif v_socle_nc.tex = 'veget' then
                                v_code4 = 3261;
                                v_lib4 = 'Espace boisé';

                            else 
                                v_code4 = 1226;
                                v_lib4 = 'Autre infrastructure';

                            end if;

                            update  {0}.{1}
                                Set code4_{2} = v_code4,
                                    lib4_{2} = v_lib4
                                Where gid = v_socle_nc.gid;

                        END LOOP;

                    END;
                $BODY$;

<<<<<<< HEAD
=======
                Drop table if exists socle_temp;
>>>>>>> master
                """.format(
                        self.schema_desti,
                        self.couche_desti,
                        self.yearCode
                            )
                )    
                 
        cur3.close()
        self.conn.commit()

        self.pb_start.setEnabled(True) 
        self.lbl_etape.setText(u'Terminé')
        self.pb_avancement.setValue(100)       
        print 'Finally'


    def addFunctionSafe(self):
        #Fonction de création du socle deuxième étape
        #Calcul des taux de présence
        cur = self.conn.cursor()
            #Execution de la suite de requêtes
        cur.execute(u"""
                    create or replace function ST_Safe_Intersection(
                        geom_a           geometry,
                        geom_b           geometry default null,
                        message          text default '[unspecified]',
                        grid_granularity double precision default 1
                    )
                        returns geometry as
                    $$
                    begin
                        if geom_b is null
                        then
                            raise notice 'ST_Safe_Intersection: second geometry is NULL (%)', message;
                            return geom_b;
                        end if;
                        return
                        ST_Safe_Repair(
                            ST_Intersection(
                                geom_a,
                                geom_b
                            )
                        );
                        exception
                        when others
                            then
                                begin
                                    raise notice 'ST_Safe_Intersection: making everything valid (%)', message;
                                    return
                                    ST_Translate(
                                        ST_Safe_Repair(
                                            ST_Intersection(
                                                ST_Safe_Repair(ST_Translate(geom_a, -ST_XMin(geom_a), -ST_YMin(geom_a))),
                                                ST_Safe_Repair(ST_Translate(geom_b, -ST_XMin(geom_a), -ST_YMin(geom_a)))
                                            )
                                        ),
                                        ST_XMin(geom_a),
                                        ST_YMin(geom_a)
                                    );
                                    exception
                                    when others
                                        then
                                            begin
                                                raise notice 'ST_Safe_Intersection: buffering everything (%)', message;
                                                return
                                                ST_Safe_Repair(
                                                    ST_Intersection(
                                                        ST_Buffer(
                                                            geom_a,
                                                            0.4 * grid_granularity
                                                        ),
                                                        ST_Buffer(
                                                            geom_b,
                                                            -0.4 * grid_granularity
                                                        )
                                                    )
                                                );
                                                exception
                                                when others
                                                    then
                                                        raise exception 'ST_Safe_Intersection: everything failed (%)', message;
                                            end;
                                end;
                    end
                    $$
                    language 'plpgsql' immutable strict parallel safe;

                    create or replace function ST_Safe_Repair(
                        geom    geometry,
                        message text default '[unspecified]'
                    ) returns geometry as
                    $$
                    begin
                        if ST_IsEmpty(geom)
                        then
                            raise debug 'ST_Safe_Repair: geometry is empty (%)', message;
                    -- empty POLYGON makes ST_Segmentize fail, replace it with empty GEOMETRYCOLLECTION
                            return ST_SetSRID('GEOMETRYCOLLECTION EMPTY' :: geometry, ST_SRID(geom));
                        end if;
                        if ST_IsValid(geom)
                        then
                            return ST_ForceRHR(ST_CollectionExtract(geom, ST_Dimension(geom) + 1));
                        end if;
                        return
                        ST_ForceRHR(
                            ST_CollectionExtract(
                                ST_MakeValid(
                                    geom
                                ),
                                ST_Dimension(geom) + 1
                            )
                        );
                    end
                    $$
                    language 'plpgsql' immutable strict parallel safe;

                    create or replace function ST_Safe_Difference(
                        geom_a           geometry,
                        geom_b           geometry default null,
                        message          text default '[unspecified]',
                        grid_granularity double precision default 1
                    )
                        returns geometry as
                    $$
                    begin
                        if geom_b is null or ST_IsEmpty(geom_b)
                        then
                            return geom_a;
                        end if;
                        return
                        ST_Safe_Repair(
                            ST_Translate(
                                ST_Difference(
                                    ST_Translate(geom_a, -ST_XMin(geom_a), -ST_YMin(geom_a)),
                                    ST_Translate(geom_b, -ST_XMin(geom_a), -ST_YMin(geom_a))
                                ),
                                ST_XMin(geom_a),
                                ST_YMin(geom_a)
                            )
                        );
                        exception
                        when others
                            then
                                begin
                                    raise notice 'ST_Safe_Difference: making everything valid (%)', message;
                                    return
                                    ST_Translate(
                                        ST_Safe_Repair(
                                            ST_Difference(
                                                ST_Translate(ST_Safe_Repair(geom_a), -ST_XMin(geom_a), -ST_YMin(geom_a)),
                                                ST_Buffer(ST_Translate(geom_b, -ST_XMin(geom_a), -ST_YMin(geom_a)), 0.4 * grid_granularity)
                                            )
                                        ),
                                        ST_XMin(geom_a),
                                        ST_YMin(geom_a)
                                    );
                                    exception
                                    when others
                                        then
                                            raise warning 'ST_Safe_Difference: everything failed (%)', message;
                                            return ST_Safe_Repair(geom_a);
                                end;
                    end
                    $$
                    language 'plpgsql' immutable strict parallel safe;""")
        cur.close()
        self.conn.commit()



