# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.PyQt.QtWidgets import *
from PyQt5.QtSql import *
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

from .interface_evolgeom import *

class EvolGeom_mos(QDialog, Ui_interface_evolgeom):
    def __init__(self, parent=None):
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
        self.pb_start.clicked.connect(self.start)

            #initialisation du bouton de commencement en inclickable
        self.pb_start.setEnabled(False)

            #Déclenchement du chargement des données de la base dans les combobox
        self.pb_dbConnect.clicked.connect(self.chargeSchema)

            #Lancement de la liste des connexions QGIS au lancement de la fenêtre
        self.updateConnectionList()

        self.cb_schema_origin.activated.connect(self.chargeTableOrigin)
        self.cb_schema_new.activated.connect(self.chargeTableNew)
            #Déclenchement de la vérification de la totalité des champs rentrés pour lancer le programme
        self.cb_schema_desti.activated.connect(self.canStart)
        self.cb_schema_origin.activated.connect(self.canStart)
        self.cb_table_origin.activated.connect(self.canStart)
        self.cb_schema_new.activated.connect(self.canStart)
        self.cb_table_new.activated.connect(self.canStart)
        self.le_table_desti.textChanged.connect(self.canStart)

    def updateConnectionList(self):
        #Récupère les informations des connexion aux bases POSTGRES de QGIS
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
        #Récupère les données de connexion à la base
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

    def connexion(self):
        #Renvois les informations de connexion à la base sélectionnée
        s = QSettings()
        self.getConInfo()
        db = QSqlDatabase.addDatabase("QPSQL", "adeupa1")
        db.setHostName(self.host)
        db.setPort(int(self.port))
        db.setDatabaseName(self.database)
        db.setUserName(self.username)
        db.setPassword(self.pwd)
        return db

    def chargeSchema(self):
        #Fonction de chargement des données de la base dans les combo box
        #initialise les combo box avec la liste des schema + table de la base
            #Initialisation vide des combobox
        self.cb_schema_origin.clear()
        self.cb_schema_desti.clear()
        self.cb_schema_new.clear()
        self.cb_table_origin.clear()
        self.cb_table_new.clear()
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
                    #self.cb_schema.setCurrentIndex(self.cb_schema.findText(None))
                    self.cb_schema_origin.addItem(querySchema.value(0))
                    self.cb_schema_desti.addItem(querySchema.value(0))
                    self.cb_schema_new.addItem(querySchema.value(0))
                    
    def chargeTableOrigin(self):
        #Chargement des couches contenues dans le schéma sélectionné par la box ORIGIN
        self.cb_table_origin.clear()
        db = self.connexion()
            #Connexion à la base de données
        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

                    #Initialisation de la combo box schema avec la liste des schemas de la base
            queryTable = QSqlQuery(db)
            wschema = self.cb_schema_origin.currentText()
            queryTable.prepare("Select distinct table_name from information_schema.tables where table_schema = '" + wschema + "' order by table_name;")
            if queryTable.exec_():
                while queryTable.next():
                    self.cb_table_origin.addItem(queryTable.value(0))

    def chargeTableNew(self):
        #Chargement des couches contenues dans le schéma sélectionné par la box NEW
        self.cb_table_new.clear()
        db = self.connexion()
            #Connexion à la base de données
        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

                    #Initialisation de la combo box schema avec la liste des schemas de la base
            queryTable = QSqlQuery(db)
            wschema = self.cb_schema_new.currentText()
            queryTable.prepare("Select distinct table_name from information_schema.tables where table_schema = '" + wschema + "' order by table_name;")
            if queryTable.exec_():
                while queryTable.next():
                    self.cb_table_new.addItem(queryTable.value(0))

    def canStart(self):
        #Fonction analysant si le programme peu être exécuté (tous les champs sont remplis) ou non
        if  self.cb_schema_new.currentText() == '' or self.cb_schema_origin.currentText() == '' or self.cb_table_new.currentText() == '' or self.cb_table_origin.currentText() == '' or self.cb_schema_desti.currentText() == '' or self.le_table_desti.text() == '':
            self.pb_start.setEnabled(False)
        else:
            self.pb_start.setEnabled(True)
            print ('ok')

    def start(self):
        #Fonction de lancement du programme
        self.lbl_etape.setText(u'Calcul en cours')
        self.pb_start.setEnabled(False)
        self.pb_avancement.setValue(0)
        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.username, dbname=self.database, password=self.pwd )
        temp = QTimer
            #Lancement de la fonction de détection des champs      
        temp.singleShot(100, self.evolGeom)
            #Appel de la fonction pour le début du socle 
        #self.createSocle()

    def evolGeom(self):
        #Recalcul les géométries d'un ancien livrable en fonction d'un nouveau socle géométrique
        #Récupère les nouvelles géométries lorsque les surfaces ne recouvrent pas entièrement la géométrie d'origine
        #récupère les nouvelles géométries qui ont une surface supèreieure à 25 m²
        #Récupère lles nouvelles géométries qui ne sont pas filaires
        cur5 = self.conn.cursor()
        cur5.execute(u"""
                    --Récupération des données d'intersection entre les anciennes et les nouvelles géométries
                    -- La nouvelle géométrie est gardé
                drop table if exists tt_temp_new_geom;
                create temp table tt_temp_new_geom as 
                select row_number() over() as gid , * from (
                Select a.geom, a.idu, 
                                a.code_insee, 
                                a.tex, 
                                a.section, 
                                a.num_parc, 
                    (st_area(st_safe_intersection(a.geom,b.geom))*100 )/st_area(b.geom)  as surf_perc, 
                    (st_area(st_safe_intersection(a.geom,b.geom))*100 )/st_area(a.geom)  as surf_perc_new, 
                    st_area(a.geom) as surf_geom, b.gid as old_gid, 
                    st_perimeter(a.geom)/(2 * sqrt(3.14* st_area(a.geom))) as indic_con 
                from {4}.{5} a 
                join {2}.{3} b on st_intersects(a.geom, b.geom)
                where a.idu != 'NC'and b.idu != 'NC' 
                ) tt;

                    --Récupération des nouvelles géométries qui remplaceront les anciennes
                drop table if exists vm_temp_insert_new_geom;
                create temp table vm_temp_insert_new_geom as
                    select * from tt_temp_new_geom where surf_perc_new > 1.5 and surf_perc > 1.5 and indic_con < 4 
                                                   and ( surf_perc < 99) 
                                                    and (old_subdi_sirs is null);

                    -- Récupération des anciennes données avec les nouvelles géométries                        
                drop table if exists tt_old_to_new_geom;
                create temp table tt_old_to_new_geom as              
                Select b.*, a.geom as new_geom, 
                            a.idu as new_idu, 
                            a.tex as new_tex, 
                            a.code_insee as new_code_insee, 
                            a.section as new_section, 
                            a.num_parc as new_num_parc 
                from {2}.{3} b
                Join vm_temp_insert_new_geom a on b.gid = a.old_gid;

                   --Mise à jour des nouvelles anciennes données avec les nouvelles informations correspondantes
                update tt_old_to_new_geom 
                    set geom = st_multi(new_geom), 
                            idu = new_idu, 
                            tex = new_tex, 
                            code_insee = new_code_insee, 
                            section = new_section,
                            num_parc = new_num_parc ;

                    --Suppression des colonnes inutiles à la table
                alter table tt_old_to_new_geom drop column gid;
                alter table tt_old_to_new_geom drop column new_idu;
                alter table tt_old_to_new_geom drop column new_section;
                alter table tt_old_to_new_geom drop column new_tex;
                alter table tt_old_to_new_geom drop column new_code_insee;
                alter table tt_old_to_new_geom drop column new_num_parc;
                alter table tt_old_to_new_geom drop column new_geom;

                    -- Récupération des anciennes données qui ne changeront pas
                drop table if exists tt_test;                                      
                create temp table tt_test as select * from {2}.{3};
                delete from  tt_test where gid in (Select old_gid from vm_temp_insert_new_geom);
                alter table tt_test drop column gid;
                    
                    -- Regroupement de toutes les données en une couche                               
                drop table if exists {0}.{1} ;
                create table {0}.{1} as 
                   (Select row_number() over() as gid, *
                        From ((Select * from tt_test) UNION (Select * from tt_old_to_new_geom))tt
                   );
                   -- Création des index de clé primaire et géométrie
                create index idx_gid_{1} on {0}.{1} using btree(gid);
                create index idx_geom_{1} on {0}.{1} using gist(geom);

                    """.format(
                        self.cb_schema_desti.currentText(),#0
                        self.le_table_desti.text(),#1
                        self.cb_schema_origin.currentText(),#2
                        self.cb_table_origin.currentText(),#3
                        self.cb_schema_new.currentText(),#4
                        self.cb_table_new.currentText()#5
                        )
                    )
        cur5.close()
        self.conn.commit()
        self.pb_avancement.setValue(100)
        self.lbl_etape.setText(u"La couche a été généré : " + self.cb_schema_desti.currentText() + "." + self.le_table_desti.text())

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



