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

from interface_analyse import *

class Analyse_mos(QDialog, Ui_interface_analyse):
    def __init__(self, interface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.host = None
        self.port = None
        self.database = None
        self.username = None
        self.pwd = None

        self.geom = None

        self.pb_avancement.setValue(False)
        self.lbl_etape.setText(None)
        
            #Déclenchement de la création du socle
        self.connect(self.pb_start, SIGNAL("clicked()"), self.start)

            #initialisation du bouton de commencement en inclickable
        self.pb_start.setEnabled(False)
        self.rb_geom.setChecked(True)

            #Déclenchement du chargement des données de la base dans les combobox
        self.connect(self.pb_dbConnect, SIGNAL("clicked()"), self.chargeSchema)
        self.connect(self.pb_dbConnect, SIGNAL("clicked()"), self.charge)


            #Lancement de la liste des connexions QGIS au lancement de la fenêtre
        self.updateConnectionList()

        self.connect(self.cb_schema, SIGNAL("activated(int)"), self.chargeTable)
      
            #Déclenchement de la vérification de la totalité des champs rentrés pour lancer le programme
        self.connect(self.cb_schema_desti, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_schema, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_table, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_ff_parcelle, SIGNAL("activated(int)"), self.canStart)


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

    def charge(self):
        #Fonction de chargement des données de la base dans les combo box
        #initialise les combo box avec la liste des schema + table de la base

            #Initialisation vide des combobox        
        self.cb_geobati.clear()
        self.cb_ff_parcelle.clear()
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
                    self.cb_geobati.addItem(queryTable.value(0))
                    self.cb_ff_parcelle.addItem(queryTable.value(0))
                    self.cb_indust.addItem(queryTable.value(0))
                    self.cb_batirem.addItem(queryTable.value(0))
                    self.cb_bati_indif.addItem(queryTable.value(0))

        
                #initialisation des combo box avec la valeur nulle, pour pouvoir voir l'avancement de notre saisie
            self.cb_geobati.setCurrentIndex(self.cb_geobati.findText(None))
            self.cb_ff_parcelle.setCurrentIndex(self.cb_ff_parcelle.findText(None))
            self.cb_geobati.setCurrentIndex(self.cb_geobati.findText(None))
            self.cb_ff_parcelle.setCurrentIndex(self.cb_ff_parcelle.findText('ff_d29_2015.d29_2015_pnb10_parcelle'))
            self.cb_schema.setCurrentIndex(self.cb_schema.findText('sandbox'))
            self.cb_table.setCurrentIndex(self.cb_table.findText('morlaix_2018_clean'))

            self.cb_indust.setCurrentIndex(self.cb_indust.findText(None))
            self.cb_batirem.setCurrentIndex(self.cb_batirem.findText(None))
            self.cb_bati_indif.setCurrentIndex(self.cb_bati_indif.findText(None))


    def chargeSchema(self):
        #Fonction de chargement des données de la base dans les combo box
        #initialise les combo box avec la liste des schema + table de la base

            #Initialisation vide des combobox
        self.cb_schema.clear()
        self.cb_schema_desti.clear()
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
                    self.cb_schema_desti.addItem(querySchema.value(0))
                    

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


    def canStart(self):
        #Fonction analysant si le programme peu être exécuté (tous les champs sont remplis) ou non
        if self.cb_ff_parcelle.currentText() == '' or self.le_annee.text() == '' or self.cb_table.currentText() == '' or self.cb_schema_desti.currentText() == '' or self.le_table_desti.text() == '':
            self.pb_start.setEnabled(False)
        else:
            self.pb_start.setEnabled(True)
            print ('ok')


    def start(self):
        #Fonction de lancement du programme
        self.lbl_etape.setText(u'Etape 1/2')
        self.pb_start.setEnabled(False)
        self.pb_avancement.setValue(0)

        if self.rb_geom.isChecked():
            self.geom = 'geom'
        else:
            self.geom = 'the_geom'

        if self.cb_geobati.currentText() == '':
            self.geo_bati = 'none'
        else:
            self.geo_bati = self.cb_geobati.currentText()

        if self.cb_indust.currentText() == '':
            self.indust = 'none'
        else: 
            self.indust = self.cb_indust.currentText()

        if self.cb_batirem.currentText() == '':
            self.bati_rem = 'none'
        else:
            self.bati_rem = self.cb_batirem.currentText()

        if self.cb_bati_indif.currentText() == '':
            self.bati_indif = 'none'
        else:
            self.bati_indif = self.cb_bati_indif.currentText()
        

        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.username, dbname=self.database, password=self.pwd )

        temp = QTimer       
        temp.singleShot(100, self.detectionChamps)
            #Appel de la fonction pour le début du socle 
        #self.createSocle()

    def detectionChamps(self):
        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_milit%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_milit = cur.fetchone()
        cur.close();
        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_bati%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_bati = cur.fetchone()
        cur.close();
        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_batire%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_batire = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_batagri%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_batagri = cur.fetchone()
        cur.close();
        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_serre%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_serre = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_batire%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_indust = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_comer%'
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_comer = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_sport%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_sport = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_loisir%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_loisir = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_agri%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_agri = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_veget%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_veget = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_eau%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_eau = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_route%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_route = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%to_batimaison%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_batimaison = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%pre_scol%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.pre_scol = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%pre_sante%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.pre_sante = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%pre_eqadmi%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.pre_eqadmi = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%pre_o_nrj%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.pre_o_nrj = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%pre_transp%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.pre_transp = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%pre_sploi%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.pre_sploi = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%prob_jardin%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.prob_jardin = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%m_fonction%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.m_fonction = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%idu%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.idu = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%tex%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.tex = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%section%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.section = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%num_parc%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.num_parc = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%tex%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_batire = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%section%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.to_batire = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%code_insee%' or column_name like 'dc' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.code_insee = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'id_mos%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.id_mos = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%sirs%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.subdi_sirs = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'code4%' 
                        order by column_name desc 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.code4 = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'lib4%' 
                        order by column_name desc

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.lib4 = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'remarque%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.remarque = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'surface%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.surface = cur.fetchone()
        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'perimetre%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.perimetre = cur.fetchone()
        cur.close();

        self.conn.commit();
        self.lbl_etape.setText(u'Etape 2/2')
        self.pb_avancement.setValue(20)
        temp = QTimer       
        temp.singleShot(100, self.analyseSocle)

    def analyseSocle(self):
        #Calcul des taux de présence
        print (self.cb_ff_parcelle.currentText())
        yearCode_t1 = int(self.le_annee.text())
        cur = self.conn.cursor()
            #Execution de la suite de requêtes
        cur.execute(u"""Select right(column_name,4) 
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'code4%' 
                        order by column_name desc

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        yearCode_t0 = cur.fetchone()
        cur.close();


        cur3 = self.conn.cursor()
        cur3.execute(u"""Select column_name 
                        from information_schema.columns 
                        where table_schema||'.'||table_name  =  '{0}.{1}'
                        and column_name like 'id_mos%' 
                        order by column_name desc

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                            )
                    )
        idmos_t0 = cur3.fetchone()
        cur3.close();

        cur5 = self.conn.cursor()
        cur5.execute(u"""
                Create or replace function public.fun_bati_evol(i_socle_c text, 
                                                                i_bati_t1 text, 
                                                                i_foncier text,
                                                                i_bati_indus text,
                                                                i_bati_rem text,
                                                                i_bati_indif text
                                                                )
                Returns void AS
                    --Fonction de calcul des évolutions de construction sur le territoire
                    --Met en correlation les fichiers fonciers et bâtiments edigeo
                    --Entrée : - Socle de base année t0 
                    --         - Batiment t-1 edigeo
                    --         - Fichiers fonciers t0
                    --         - Années t0
                    --         - Année t-1 
                    $BODY$
                        DECLARE
                            v_geom geometry(polygon,2154); -- Géométrie du socle
                            v_id_mos character varying; -- code idu du socle
                            v_gid integer; -- identifiant du socle
                            v_code4 integer; -- Code de l'année courante
                            v_lib4 character varying; -- libellé de l'année courante
                            
                            v_tobati integer;-- Taux de présence de bati sur la parcelle à l'année t0

                            v_tobati_old integer;-- Taux de bâtiment sur la parcelle
                            v_evol boolean;--Définit si il y a évolution ou non
                            v_tourbain integer; -- Taux d'urbain sur les parcelles en évolution
                            v_mfonction character varying;-- Type de bâtiment sur la parcelle

                            v_tobatire integer; --Taux de bâtiment remarquable sur la parcelle
                            v_tobatagri integer; -- Taux de bâtiment agricole sur la parcelle
                            v_toindust integer; --Taux de bâtiment industriel sur la parcelle
                            v_tocomer integer; -- Taux de bâtiment commercial sur la parcelle
                            v_tobatimaison integer; -- Taux de batiment maison (bati indiferencie)


                            v_yearMax integer;--Année de construction du dernier bâtiment de la parcelle
                            v_yearMin integer; -- Année de constrauction du premier bâtiment de la parcelle
                            v_newCode4 integer; -- Nouveau code à attributer pour l'ancienne date
                            v_newLib4 character varying;-- Nouveau libellé à attribuer pour l'ancienne date


                        BEGIN            
                                --Parcours de toutes les parcelles pour affecter les calcul de présence qui lui sont propre
                                --Les calculs sont stockés dans des variables puis insérés en fin de boucle dans la table
                             execute format ('
                                    drop table if exists {41}.{42};   
                                    create table {41}.{42} as (
                                        Select {7} as to_milit,
                                                {8} as to_bati,
                                                {9} as to_batire,
                                                {10} as to_batagri,
                                                {11} as to_serre,
                                                {12} as to_indust,
                                                {13} as to_comeromer,
                                                {14} as to_sport,
                                                {15} as to_loisir,
                                                {16} as to_agri,
                                                {17} as to_veget,
                                                {18} as to_eau,
                                                {19} as to_route,
                                                {20} as to_batimaison,
                                                {21} as pre_scol,
                                                {22} as pre_sante,
                                                {23} as pre_eqadmi,
                                                {24} as pre_o_nrj,
                                                {25} as pre_transp,
                                                {26} as pre_sploi,
                                                {27} as prob_jardin,
                                                {28} as m_fonction,
                                                0::integer as to_bati_old,
                                                0::integer as to_urbain, 
                                                False::boolean as est_evol,
                                                {29} as idu,
                                                {30} as num_parc,
                                                {31} as tex,
                                                {32} as section,
                                                {33} as code_insee,
                                                gid,
                                                geom,
                                                {34} as id_mos,
                                                {35} as subdi_sirs,
                                                0::integer as code4_{0},
                                                null::character varying as lib4_{0},
                                                null::character varying as remarque_{0},
                                                {36} as code4_{1},
                                                {37} as lib4_{1},
                                                {38} as remarque_{1},
                                                {39} as surface_m2,
                                                {40} as perimetre
                                            From %1$s   
                                    )
                            ', i_socle_c);

                            For v_geom, v_gid, v_id_mos, v_code4, v_lib4, v_tobati IN execute format('Select geom, gid, {34}, {36}, {37}, {8} From %1$s sc;', i_socle_c) LOOP
                                        --calcul d'évolution par fichiers foncier : Date de première et dernière création de bâtiment sur la parcelle
                                    execute format('Select jannatmin, jannatmax
                                                From %1$s f
                                                Where f.idpar = ''%2$s'';',i_foncier, v_id_mos)
                                into v_yearMin, v_yearMax;
                                v_tobati_old = 0;

                                if v_yearMin > {0} then
                                    --Evolution détecté : date de première création posterieur à t-1
                                    v_evol = TRUE;
                                else 
                                    --Pas d'évolution : aucune date, ou bâtiment déjà existant, ou pas de bâtiment
                                            --Calcul du taux de bâtiment présent sur la parcelle avec les données bati t-1
                                    if i_bati_t1 != 'none' then
                                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                        From %1$s pm
                                                        Where st_intersects(''%2$s'', pm.geom) 
                                                    ', i_bati_t1, v_geom)
                                    into v_tobati_old;
                                    end if;

                                    if i_bati_indif != 'none' then

                                                --Calcul du taux de maison présentes sur la parcelles (bati indiferencie)
                                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{6}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                        From %1$s pm
                                                        Where st_intersects(''%2$s'', pm.{6}) 
                                                    ', i_bati_indif, v_geom)
                                        into v_tobatimaison;
                                        if v_tobati_old < v_tobatimaison then
                                            v_tobati_old = v_tobatimaison;
                                        end if;

                                    end if;

                                    if i_bati_rem != 'none' then
                                                --Calcul du taux de présence de bâtiment remarquable
                                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{6}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                                From %1$s pm
                                                                Where st_intersects(''%2$s'', pm.{6}) 
                                                            ', i_bati_rem, v_geom)
                                        into v_tobatire;
                                        if v_tobati_old < v_tobatire then
                                            v_tobati_old = v_tobatire;
                                        end if;
                                    end if;

                                    if i_bati_indus != 'none' then
                                                --Calcul du taux de présence de bâtiments agricole
                                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.{6}), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                                                From %1$s pm
                                                                Where st_intersects(''%2$s'', pm.{6}) 
                                                            ', i_bati_indus, v_geom)
                                        into v_tobatagri;
                                        if v_tobati_old < v_tobatagri then
                                            v_tobati_old = v_tobatagri;
                                        end if;
                                    end if;

                                    if i_bati_indus != 'none' or i_bati_rem != 'none' or i_bati_indif != 'none' or i_bati_t1 != 'none' then
                                        if v_tobati > 70 and v_tobati_old < 2 then
                                            --Evolution détecté : présence de bâtiment en t0 sans présence de bâtiment en t-1
                                            v_evol = TRUE;
                                        else
                                            v_evol = FALSE;
                                        end if;
                                    end if;

                                end if;

                                if v_evol then
                                    --Pour toutes les évolutions détectés, on cherche à attribuer le code terrain vacant ou terre agricole
                                            --Recherche de taux de présence d'urbanisation dans un rayon de 10m de la parcelle 
                                        execute format('With tmpBuffer as (
                                                            Select (st_dump(st_collectionextract(st_safe_difference(st_buffer(geom,10), geom),3))).geom::geometry(polygon,2154) as geom
                                                            From %1$s
                                                            Where gid = %2$s
                                                        ), tmpUrbain as (
                                                            Select st_union(a.geom) as geom
                                                            FROM %1$s a
                                                            Join tmpBuffer t on st_intersects(a.geom, t.geom)
                                                            Where code4_2018 in (''1112'', ''1113'', ''1114'', ''1213'', ''1214'', ''1215'', ''1211'', ''1212'')
                                                        ) 
                                                            Select ((st_area(st_safe_intersection(a.geom, t.geom))*100)/st_area(t.geom))::integer
                                                            From tmpBuffer t,tmpUrbain a
                                                    ', i_socle_c, v_gid)
                                    into v_tourbain;
                                    

                                    if v_tourbain > 40 then
                                        --Si il y a plus de 50/100  d'urbanisation, alors c'était un terrain vacant
                                        v_newCode4 = 1333;
                                        v_newLib4 = 'Terrain vacant à vocation autre';
                                    else
                                        --Sinon, c'était une terre agricole
                                        v_newCode4 = 2511;
                                        v_newLib4 = 'Terre agricole';
                                    end if;
                                else
                                    --Si il n'y a pas eu d'évolution détécté, alors on récupère les anciens codes 
                                    v_newCode4 = v_code4;
                                    v_newLib4 = v_lib4;
                                    v_tourbain = 0;
                                end if;

                                    update {41}.{42}
                                    Set est_evol = v_evol,
                                        code4_{0} = v_newCode4,
                                        lib4_{0} = v_newLib4 ,
                                        to_urbain = v_tourbain ,
                                        to_bati_old = v_tobati_old
                                    where gid = v_gid;                                    

                            END LOOP;
                        RETURN;
                        END;
                    $BODY$
                        LANGUAGE 'plpgsql';

                    select fun_bati_evol('{2}.{3}', '{4}', '{5}', '{43}', '{44}', '{45}' );

                    """.format(
                        yearCode_t1,
                        yearCode_t0[0],
                        self.cb_schema.currentText(),
                        self.cb_table.currentText(),
                        self.geo_bati,#4
                        self.cb_ff_parcelle.currentText(),
                        self.geom,
                        self.to_milit[0],#7
                        self.to_bati[0],#8
                        self.to_batire[0],#9
                        self.to_batagri[0],#10
                        self.to_serre[0],#11
                        self.to_indust[0],#12
                        self.to_comer[0],#13
                        self.to_sport[0],#14
                        self.to_loisir[0],#15
                        self.to_agri[0],#16
                        self.to_veget[0],#17
                        self.to_eau[0],#18
                        self.to_route[0],#19
                        self.to_batimaison[0],#20
                        self.pre_scol[0],#21
                        self.pre_sante[0],#22
                        self.pre_eqadmi[0],#23
                        self.pre_o_nrj[0],#24
                        self.pre_transp[0],#25
                        self.pre_sploi[0],#26
                        self.prob_jardin[0],#27
                        self.m_fonction[0],#28
                        self.idu[0],#29
                        self.num_parc[0],#30
                        self.tex[0],#31
                        self.section[0],#32
                        self.code_insee[0],#33
                        self.id_mos[0],#34
                        self.subdi_sirs[0],#35
                        self.code4[0],#36
                        self.lib4[0],#37
                        self.remarque[0],#38
                        self.surface[0],#39
                        self.perimetre[0],#40
                        self.cb_schema_desti.currentText(),#41
                        self.le_table_desti.text(),#42
                        self.indust,#43
                        self.bati_rem,#44
                        self.bati_indif#45
                        )
                    )

        cur5.close()
        self.conn.commit()

        self.pb_avancement.setValue(100)
        self.lbl_etape.setText(u"Terminé")


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
                    language 'plpgsql' immutable parallel safe;

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



