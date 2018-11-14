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

from interface_compare import *

class Compare_mos(QDialog, Ui_interface_compare):
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


            #Lancement de la liste des connexions QGIS au lancement de la fenêtre
        self.updateConnectionList()

        self.connect(self.pb_dbConnect, SIGNAL("clicked()"), self.chargeSchema)

        self.connect(self.cb_schema_t0, SIGNAL("activated(int)"), self.chargeTable0)
        self.connect(self.cb_schema_t1, SIGNAL("activated(int)"), self.chargeTable1)
      
            #Déclenchement de la vérification de la totalité des champs rentrés pour lancer le programme
        self.connect(self.cb_schema_t1, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_schema_t0, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_table_t0, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_table_t1, SIGNAL("activated(int)"), self.canStart)


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
        self.cb_schema_t0.clear()
        self.cb_schema_t1.clear()
        self.cb_schema_desti.clear()
        self.cb_table_t0.clear()
        self.cb_table_t1.clear()
        self.cb_schema_t0.setCurrentIndex(self.cb_schema_t0.findText(None))
        self.cb_schema_t1.setCurrentIndex(self.cb_schema_t1.findText(None))
        self.cb_schema_desti.setCurrentIndex(self.cb_schema_desti.findText(None))
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
                    self.cb_schema_t0.setCurrentIndex(self.cb_schema_t0.findText(None))
                    self.cb_schema_t0.addItem(querySchema.value(0))
                    self.cb_schema_t1.setCurrentIndex(self.cb_schema_t1.findText(None))
                    self.cb_schema_t1.addItem(querySchema.value(0))
                    self.cb_schema_desti.setCurrentIndex(self.cb_schema_desti.findText(None))
                    self.cb_schema_desti.addItem(querySchema.value(0))

            self.cb_schema_desti.setCurrentIndex(self.cb_schema_desti.findText('sandbox'))
            self.le_table_desti.setText('test_comparaison_1')
            self.cb_schema_t1.setCurrentIndex(self.cb_schema_t1.findText('livrables'))
            self.cb_table_t1.setCurrentIndex(self.cb_table_t1.findText('mos_pdm_2015_3com'))
            self.cb_schema_t0.setCurrentIndex(self.cb_schema_t0.findText('sandbox'))
            self.cb_table_t0.setCurrentIndex(self.cb_table_t0.findText('morlaix_2018_clean'))
                    

    def chargeTable0(self):
        self.cb_table_t0.clear()
        db = self.connexion()
            #Connexion à la base de données
        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

                    #Initialisation de la combo box schema avec la liste des schemas de la base
            queryTable = QSqlQuery(db)
            wschema = self.cb_schema_t0.currentText()
            queryTable.prepare("Select distinct table_name from information_schema.tables where table_schema = '" + wschema + "' order by table_name;")
            if queryTable.exec_():
                print (self.cb_schema_t0.currentText())
                while queryTable.next():
                    self.cb_table_t0.addItem(queryTable.value(0))

    def chargeTable1(self):
        self.cb_table_t1.clear()


        db = self.connexion()
            #Connexion à la base de données
        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

                    #Initialisation de la combo box schema avec la liste des schemas de la base
            queryTable = QSqlQuery(db)
            wschema = self.cb_schema_t1.currentText()
            queryTable.prepare("Select distinct table_name from information_schema.tables where table_schema = '" + wschema + "' order by table_name;")
            if queryTable.exec_():
                print (self.cb_schema_t1.currentText())
                while queryTable.next():
                    self.cb_table_t1.addItem(queryTable.value(0))



    def canStart(self):
        #Fonction analysant si le programme peu être exécuté (tous les champs sont remplis) ou non
        if self.cb_table_t1.currentText() == '' or self.cb_table_t0.currentText() == ''  or self.cb_schema_desti.currentText() == '' or  self.le_table_desti.text() == '':
            self.pb_start.setEnabled(False)
        else:
            self.pb_start.setEnabled(True)
            print ('ok')


    def start(self):
        #Fonction de lancement du programme
        self.lbl_etape.setText(u'Etape 1/3')
        self.pb_start.setEnabled(False)
        self.pb_avancement.setValue(0)

        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.username, dbname=self.database, password=self.pwd )

        temp = QTimer
            #Appel de la fonction avec un délai de 100ms pour permettre l'affichage        
        temp.singleShot(100, self.compareSocle)


    def compareSocle(self):
        #Calcul des taux de présence
        cur = self.conn.cursor()
            #Execution de la suite de requêtes
        cur.execute(u"""Select right(column_name,4) 
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'code4%' 
                        order by column_name 

                    """.format(self.cb_schema_t0.currentText(),
                                self.cb_table_t0.currentText()
                                )
                    )
        yearCode_t0 = cur.fetchone()
        cur.close();


        cur2 = self.conn.cursor()
        cur2.execute(u"""Select right(column_name,4) 
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'code4%' 
                        order by column_name 

                    """.format(self.cb_schema_t1.currentText(),
                                self.cb_table_t1.currentText()
                                )
                    )
        yearCode_t1 = cur2.fetchone()
        cur2.close();

        cur3 = self.conn.cursor()
        cur3.execute(u"""Select column_name 
                        from information_schema.columns 
                        where table_schema||'.'||table_name  =  '{0}.{1}'
                        and column_name like 'id_mos%' 
                        order by column_name 

                    """.format(self.cb_schema_t1.currentText(),
                                self.cb_table_t1.currentText()
                            )
                    )
        idmos_t1 = cur3.fetchone()
        cur3.close();

        cur4 = self.conn.cursor()
        cur4.execute(u"""Select column_name 
                        from information_schema.columns 
                        where table_schema||'.'||table_name  =  '{0}.{1}'
                        and column_name like 'id_mos%' 
                        order by column_name 

                    """.format(self.cb_schema_t0.currentText(),
                                self.cb_table_t0.currentText()
                            )
                    )
        idmos_t0 = cur4.fetchone()
        cur4.close();

        cur5 = self.conn.cursor()
        cur5.execute(u"""
                drop table if exists vm_temp_compare cascade;
                Create temporary table vm_temp_compare as 
                Select row_number() over() as gid, * ,
                                case when code4_{1} = to_number(code4_{0}, '9999') Then false::boolean
                                else true::boolean
                                end as evolution_{0}_{1}
                From (
                    Select (st_dump(st_collectionextract(st_safe_intersection(mos.geom, p.geom),3))).geom::geometry(Polygon,2154) as geom,
                        p.to_milit,
                        p.to_bati,
                        p.to_batire,
                        p.to_batagri,
                        p.to_serre,
                        p.to_indust,
                        p.to_comer,
                        p.to_zic,
                        p.to_transp,
                        p.to_voiefer,
                        p.to_carrier,
                        p.to_cime,
                        p.to_sport,
                        p.to_loisir,
                        p.to_agri,
                        p.to_veget,
                        p.to_eau,
                        p.to_route,
                        p.to_batimaison,
                        p.pre_scol,
                        p.pre_sante,
                        p.pre_eqadmi,
                        p.pre_o_nrj,
                        p.pre_transp,
                        p.pre_sploi,
                        p.m_fonction,
                        p.prob_jardin,
                        mos.section as section_{0},
                        p.section as section_{1},
                        mos.idu as idu_{0},
                        p.idu as idu_{1},
                        mos.dc as code_insee_{0},
                        p.code_insee as code_insee_{1},
                        mos.{6} as id_mos_{0},
                        p.{7} as id_mos_{1},
                        mos.perimetre as perimetre_{0},
                        p.perimetre as perimetre_{1},
                        mos.surface_m2 as surface_m2_{0},
                        p.surface_m2 as surface_m2_{1},
                        mos.code4_{0},
                        p.code4_{1},
                        mos.lib4_{0},
                        p.lib4_{1},
                        mos.remarque as remarque_{0},
                        p.remarque_{1}
                    From {4}.{5} p
                    left Join {2}.{3} mos on st_intersects(p.geom,mos.geom)
                ) tt;

                drop table if exists {8}.{9};
                Create table {8}.{9} as
                with tmp as (
                    Select left(code_insee_{1},2)||'NC'|| row_number() over() as id_mos_{1},code_insee_{1}, array_to_string(array_agg(distinct (code4_{0})), ',') as code4_{0}, code_insee_{0} ,code4_{1}, lib4_{1} ,(st_dump(st_collectionextract(st_union(geom),3))).geom::geometry(Polygon,2154) as geom, array_agg(id_mos_{1}) as agg_idmos
                        From vm_temp_compare mos
                        Group by code4_{1}, code_insee_{0}, code_insee_{1}, lib4_{1}
                        Having code4_{1} in (1224, 1222, 1226, 1221, 1223, 1225)
                ), tmpunion as(
                    Select row_number() over() as gid, *
                        from tmp
                ), tmp3 as (
                (Select to_milit, to_bati, to_batire, to_batagri, to_serre, to_indust, to_comer, to_zic, to_transp, to_voiefer, to_carrier, to_cime, to_sport, to_loisir, to_agri, to_veget, to_eau, to_route, to_batimaison, pre_scol, pre_sante, pre_eqadmi, pre_o_nrj, pre_transp, pre_sploi, prob_jardin,
                section_{0}, section_{1}, idu_{0}, idu_{1}, code_insee_{0}, code_insee_{1}, id_mos_{0}, id_mos_{1}, perimetre_{0}, perimetre_{1}, surface_m2_{0}, surface_m2_{1}, code4_{0}, code4_{1}, lib4_{0}, lib4_{1}, remarque_{0}, remarque_{1}, geom
                    From vm_temp_compare mos
                    where code4_{1} not in (1224, 1222, 1226, 1221, 1223, 1225)
                )
                UNION
                (Select null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
                'NC', 'NC', 'NC', 'NC', code_insee_{0}, code_insee_{1}, null, id_mos_{1}, null, st_perimeter(geom), null, st_area(geom), code4_{0}, code4_{1}, null, lib4_{1}, null, 'Unification des routes', geom
                from tmpunion))
                    Select row_number() over() as gid, *
                    From tmp3

                    """.format(
                        yearCode_t1[0],
                        yearCode_t0[0],
                        self.cb_schema_t1.currentText(),
                        self.cb_table_t1.currentText(),
                        self.cb_schema_t0.currentText(),
                        self.cb_table_t0.currentText(),
                        idmos_t1[0],
                        idmos_t0[0],
                        self.cb_schema_desti.currentText(),
                        self.le_table_desti.text()
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



