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

from interface_repair import *

class RepairSocle(QDialog, Ui_interface_repair):
    def __init__(self, interface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.host = None
        self.port = None
        self.database = None
        self.username = None
        self.pwd = None

        self.lbl_etat.setText(None)


        self.connect(self.pb_connect, SIGNAL("clicked()"), self.chargeSchema)
        self.connect(self.cb_schema, SIGNAL("activated(int)"), self.chargeTable)
        self.connect(self.pb_repair, SIGNAL("clicked()"), self.repairGeom)
      
            #Lancement de la liste des connexions QGIS au lancement de la fenêtre
        self.updateConnectionList()

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

    def chargeSchema(self):
        #Fonction de chargement des données de la base dans les combo box
        #initialise les combo box avec la liste des schema + table de la base

            #Initialisation vide des combobox
        self.cb_schema.clear()
        self.cb_table.clear()
        self.cb_schema.setCurrentIndex(self.cb_schema.findText(None))
        db = self.connexion()

            #Connexion à la base de données
        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

                #Attribution des text schema + table aux combo box des tables
           
                    #Initialisation de la combo box schema avec la liste des schemas de la base
            querySchema = QSqlQuery(db)
            querySchema.prepare("Select distinct table_schema from information_schema.tables where table_schema not in ('pg_catalog', 'information_schema') order by table_schema;")
            if querySchema.exec_():
                while querySchema.next():
                    self.cb_schema.setCurrentIndex(self.cb_schema.findText(None))
                    self.cb_schema.addItem(querySchema.value(0))
                    

    def chargeTable(self):
        self.cb_table.clear()


        db = self.connexion()
            #Connexion à la base de données
        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

                    #Initialisation de la combo box schema avec la liste des schemas de la base
            queryTable = QSqlQuery(db)
            wschema = self.cb_schema.currentText()
            queryTable.prepare("Select distinct table_name from information_schema.tables where table_schema = '" + wschema + "' order by table_name;")
            if queryTable.exec_():
                print (self.cb_schema.currentText())
                while queryTable.next():
                    self.cb_table.addItem(queryTable.value(0))

    def repairGeom(self):
        db = self.connexion()
            #Connexion à la base de données
        wschema_table = self.cb_schema.currentText() +'.' + self.cb_table.currentText()
        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.username, dbname=self.database, password=self.pwd )
        cur = self.conn.cursor()
        self.addFunctionSafe()
            #Execution de la suite de requête de création du socle
        cur.execute(u"""
                    update {0} 
                    SET geom=ST_Safe_Repair(geom)::geometry(Polygon,2154)  
                    WHERE ST_ISValid(geom) is FALSE;""".format(wschema_table))
        self.lbl_etat.setText(u'Terminé')
        cur.close()    
        self.conn.commit()

                     
    def addFunctionSafe(self):
        #Fonction de création du socle deuxième étape
        #Calcul des taux de présence
        cur = self.conn.cursor()
            #Execution de la suite de requêtes
        cur.execute(u"""
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
                    """)
        cur.close()
        self.conn.commit()