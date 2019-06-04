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

from interface_evolution import *

class Evolution_mos(QDialog, Ui_interface_evolution):
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
        self.connect(self.le_table_desti, SIGNAL("editingFinished()"), self.canStart)
        self.connect(self.le_annee, SIGNAL("editingFinished()"), self.canStart)


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
            queryTable.prepare("Select distinct f_table_schema || '.' || f_table_name as tname from geometry_columns order by tname;")
            if queryTable.exec_():       
                while queryTable.next():
                    self.cb_ff_parcelle.addItem(queryTable.value(0))

        
                #initialisation des combo box avec la valeur nulle, pour pouvoir voir l'avancement de notre saisie
            self.cb_ff_parcelle.setCurrentIndex(self.cb_ff_parcelle.findText(None))
            self.cb_ff_parcelle.setCurrentIndex(self.cb_ff_parcelle.findText('ff_d29_2015.d29_2015_pnb10_parcelle'))
            self.cb_schema.setCurrentIndex(self.cb_schema.findText('sandbox'))
            self.cb_table.setCurrentIndex(self.cb_table.findText('morlaix_{0}_clean'))


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
        #Fonction de chargement des données des tables contenues dans le schémas
        #Fonction lancée lorsque le schéma est modifié
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
        if len(self.le_annee.text()) != 4:
            QMessageBox.critical(self, "Erreur", u"L'année doit se composer de 4 chiffres", QMessageBox.Ok)

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

        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.username, dbname=self.database, password=self.pwd )

        temp = QTimer 
            #Lancement de la fonction de détection des champs      
        temp.singleShot(100, self.detectionChamps)
            #Appel de la fonction pour le début du socle 
        #self.createSocle()

    def detectionChamps(self):
        #Fonction récupérant le nom de chaque champs contenus dans le socle
        #Appliqué pour les cas où le champ n'est pas nommé de la même façon 
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
                        and column_name like '%nom_com%' 
                        order by column_name 

                    """.format(self.cb_schema.currentText(),
                                self.cb_table.currentText()
                                )
                    )
        self.nom_com = cur.fetchone()
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
            #Lancement de la fonction d'analyse      
        temp.singleShot(100, self.evolMos)

    def evolMos(self):
        #Fonction calculant les évolution entre l'année t0 et l'année t-1
        #Prend en compte les données des ficheirs foncier sur les dates de construction des bâtiments
        #Dans le cas où des données bâtiments à la date t-1 sont utilisées on calcul la surface de recouvrant sur la parcelle 
            #Récupération de l'année t-1
        yearCode_t1 = int(self.le_annee.text())
            #Récupération de l'année t0
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

            #Récupération de l'id_mos
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

            #Lancement de l'analyse
        cur5 = self.conn.cursor()
        cur5.execute(u"""
                --Création de la table en sortie sans les dates
                drop table if exists {41}.{42};
                Create table {41}.{42} as  
                    (select 
                        to_milit,
                        to_bati,
                        to_batire,
                        to_batagri,
                        to_serre,
                        to_indust,
                        to_comer,
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
                        prob_jardin,
                        m_fonction,
                        idu,
                        num_parc,
                        tex,
                        section,
                        code_insee,
                        nom_commune,
                        gid,
                        id_mos,
                        subdi_sirs, 
                        geom
                        from {2}.{3}
                );
                alter table  {41}.{42} add constraint pk_{42}_1 primary key (gid);
                create index idx_{42}_1 on {41}.{42} using gist(geom);

                DO 
                    LANGUAGE plpgsql
                $BODY$
                    DECLARE
                        v_annee character varying;
                        v_datatype character varying;
                    BEGIN
                        For v_annee, v_datatype in Select right(column_name,4), data_type from information_schema.columns where table_schema||'.'||table_name  = '{2}.{3}' and column_name like 'code4%' order by column_name asc LOOP
                            execute format('Alter table {41}.{42} add column code4_%1$s integer;
                                            Alter table {41}.{42} add column lib4_%1$s character varying;
                                            Alter table {41}.{42} add column remarque_%1$s character varying;

                                            update {41}.{42} x set 
                                                    code4_%1$s = y.code4_%1$s,
                                                    lib4_%1$s = y.lib4_%1$s,
                                                    remarque_%1$s = y.remarque_%1$s
                                                    from {2}.{3} y
                                                    Where y.gid = x.gid
                                            ', v_annee);
                        END LOOP;
                        Alter table {41}.{42} add column code4_{0} integer;
                        Alter table {41}.{42} add column lib4_{0} character varying;
                        Alter table {41}.{42} add column remarque_{0} character varying;

                        Alter table {41}.{42} add column surface_m2 double precision;                        
                        Alter table {41}.{42} add column perimetre double precision;
                    END;
                $BODY$;

                Create or replace function public.fun_evol_t0_t1(
                                                            i_socle_c text,
                                                            i_foncier text
                                                        )
                    Returns void AS
                    --Fonction de calcul des aménagements présents sur les parcelles
                    --Met en correlation de nombreuses données recouvrant ou non une parcelle en indiquant la surface de recouvrement, ou si une présence est constaté
                $BODY$
                    DECLARE                      
                        v_socle_total record; --Données du socle parcourues
                        v_mfonction character varying; --Type de bâtiment sur la parcelle
                        v_gravelius integer; -- Identification de la forme de la parcelle
                    BEGIN
                            --Récupération des données à corréler sur l'emprise
                           
                            execute format ('
                                    drop table if exists vm_i_foncier;
                                    create temporary table vm_i_foncier as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geomloc, emp.geom)
                                    Where tlocdomin != ''AUCUN LOCAL'';
                                    Create index idx_vm_i_foncier on vm_i_foncier using gist(geomloc);
                                    ', i_foncier, i_socle_c);

                                                                                          
                            --Parcours de toutes les parcelles pour affecter les calcul de présence qui lui sont propre
                            -- Les calculs sont stockés dans des variables puis insérés en fin de boucle dans la table
                        For v_socle_total IN execute format('Select * From %1$s sc;', i_socle_c) LOOP
                            execute format ('Select tlocdomin
                                                        From %1$s pm
                                                        Where st_intersects(pm.geomloc, ''%2$s'')
                                                        order by tlocdomin desc
                                                    ', 'vm_i_foncier', v_socle_total.geom)
                                into v_mfonction;
                            if st_area(v_socle_total.geom) < 25 then
                                execute format('
                                    update %1$s 
                                        set code4_{0} = code4_{1},
                                            lib4_{0} =  lib4_{1}
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);

                            elsif (st_perimeter(v_socle_total.geom)/(2 * sqrt(3.14* st_area(v_socle_total.geom)))) > 3 then
                                execute format('
                                    update %1$s 
                                        set code4_{0} = code4_{1},
                                            lib4_{0} =  lib4_{1}
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);

                            elsif v_mfonction = 'MAISON' or v_mfonction = 'DEPENDANCE' then
                                if v_socle_total.code4_{1} = 1412 then
                                    execute format('
                                        update %1$s 
                                            set code4_{0} = code4_{1},
                                                lib4_{0} =  lib4_{1}
                                                where gid = %2$s
                                    ',i_socle_c, v_socle_total.gid);
                                else
                                    execute format('
                                        update %1$s 
                                            set code4_{0} = 1112,
                                                lib4_{0} =  ''Habitat individuel''
                                                where gid = %2$s
                                    ',i_socle_c, v_socle_total.gid);
                                end if;

                            elsif v_mfonction = 'APPARTEMENT' then
                                execute format('
                                    update %1$s 
                                        set code4_{0} = 1113,
                                            lib4_{0} =  ''Habitat collectif''
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);

                            elsif v_mfonction = 'MIXTE' then 
                                execute format('
                                    update %1$s 
                                        set code4_{0} = 1114,
                                            lib4_{0} =  ''Urbain mixte (habitat/activité tertiaire)''
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);

                            else 
                                execute format('
                                    update %1$s 
                                        set code4_{0} = code4_{1},
                                            lib4_{0} =  lib4_{1}
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);
                            end if;
                        END LOOP;
                    RETURN;
                    END;
                $BODY$
                    LANGUAGE 'plpgsql';

                    select fun_evol_t0_t1('{41}.{42}', '{5}');

                    update {41}.{42} set surface_m2 = st_area(geom), perimetre = st_perimeter(geom);

                    """.format(
                        yearCode_t1,#0
                        yearCode_t0[0],#1
                        self.cb_schema.currentText(),#2
                        self.cb_table.currentText(),#3
                        None,#4
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
                        None,#43
                        None,#44
                        None,#45
                        self.nom_com[0]#46
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



