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
        self.subdi_sirs = []

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

        self.connect(self.cb_schema_t1, SIGNAL("activated(int)"), self.chargeTable0)
        self.connect(self.cb_schema_t0, SIGNAL("activated(int)"), self.chargeTable1)
      
            #Déclenchement de la vérification de la totalité des champs rentrés pour lancer le programme
        self.connect(self.cb_schema_t0, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_schema_t1, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_table_t1, SIGNAL("activated(int)"), self.canStart)
        self.connect(self.cb_table_t0, SIGNAL("activated(int)"), self.canStart)


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
        self.cb_schema_t1.clear()
        self.cb_schema_t0.clear()
        self.cb_schema_desti.clear()
        self.cb_table_t1.clear()
        self.cb_table_t0.clear()
        self.cb_schema_t1.setCurrentIndex(self.cb_schema_t1.findText(None))
        self.cb_schema_t0.setCurrentIndex(self.cb_schema_t0.findText(None))
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
                    self.cb_schema_t1.setCurrentIndex(self.cb_schema_t1.findText(None))
                    self.cb_schema_t1.addItem(querySchema.value(0))
                    self.cb_schema_t0.setCurrentIndex(self.cb_schema_t0.findText(None))
                    self.cb_schema_t0.addItem(querySchema.value(0))
                    self.cb_schema_desti.setCurrentIndex(self.cb_schema_desti.findText(None))
                    self.cb_schema_desti.addItem(querySchema.value(0))

            self.cb_schema_desti.setCurrentIndex(self.cb_schema_desti.findText('sandbox'))
            self.le_table_desti.setText('test_comparaison_1')
            self.cb_schema_t0.setCurrentIndex(self.cb_schema_t0.findText('livrables'))
            self.cb_table_t0.setCurrentIndex(self.cb_table_t0.findText('mos_pdm_2015_3com'))
            self.cb_schema_t1.setCurrentIndex(self.cb_schema_t1.findText('sandbox'))
            self.cb_table_t1.setCurrentIndex(self.cb_table_t1.findText('morlaix_2018_clean'))
                    

    def chargeTable0(self):
        #Fonction de chargement des données des tables lorsque le schéma T0 est changé
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
                while queryTable.next():
                    self.cb_table_t1.addItem(queryTable.value(0))

    def chargeTable1(self):
        #Fonction de chargement des données des tables lorsque le schéma T+1 est changé
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
                while queryTable.next():
                    self.cb_table_t0.addItem(queryTable.value(0))



    def canStart(self):
        #Fonction analysant si le programme peu être exécuté (tous les champs sont remplis) ou non
        if self.cb_table_t0.currentText() == '' or self.cb_table_t1.currentText() == ''  or self.cb_schema_desti.currentText() == '' or  self.le_table_desti.text() == '':
            self.pb_start.setEnabled(False)
        else:
            self.pb_start.setEnabled(True)
            print ('ok')


    def start(self):
        #Fonction de lancement du programme
        self.lbl_etape.setText(u'Etape 1/1')
        self.pb_start.setEnabled(False)
        self.pb_avancement.setValue(0)

        self.conn = psycopg2.connect(host=self.host, port=self.port, user=self.username, dbname=self.database, password=self.pwd )

        temp = QTimer
            #Appel de la fonction avec un délai de 100ms pour permettre l'affichage        
        temp.singleShot(100, self.detectionChamps)

    def detectionChamps(self):
        #Fonction de détection des champs à appeler dans la couche t0
        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like '%sub%sirs%'
                        order by column_name 

                    """.format(self.cb_schema_t0.currentText(),
                                self.cb_table_t0.currentText()
                                )
                    )
        if cur.rowcount > 0:
            self.subdi_sirs = cur.fetchone()
        else:
            self.subdi_sirs.append('null')

        cur.close();

        cur = self.conn.cursor()
        cur.execute(u"""Select column_name
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'code4%' 
                        order by column_name desc 

                    """.format(self.cb_schema_t0.currentText(),
                                self.cb_table_t0.currentText()
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

                    """.format(self.cb_schema_t0.currentText(),
                                self.cb_table_t0.currentText()
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

                    """.format(self.cb_schema_t0.currentText(),
                                self.cb_table_t0.currentText()
                                )
                    )
        self.remarque = cur.fetchone()
        cur.close();


        self.conn.commit();
        self.lbl_etape.setText(u'Etape 2/2')
        self.pb_avancement.setValue(5)
        temp = QTimer
            #Appel à la fonction de comparaison de socle       
        temp.singleShot(100, self.compareSocle)


    def compareSocle(self):
        #Fonction de comparaison de socle t0 (multi date) et t+1
        #Création des géométries en fonction des anciennes présentes et des nouvelles
        #Garde les découpe de l'ancienne en ajoutant les découpes nouvelles
        cur = self.conn.cursor()
            #Récupération de l'année t+1
        cur.execute(u"""Select right(column_name,4) 
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'code4%' 
                        order by column_name desc

                    """.format(self.cb_schema_t1.currentText(),
                                self.cb_table_t1.currentText()
                                )
                    )
        yearCode_t1 = cur.fetchone()
        cur.close();

            #Récupération de l'année t0
        cur2 = self.conn.cursor()
        cur2.execute(u"""Select right(column_name,4) 
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'code4%' 
                        order by column_name desc

                    """.format(self.cb_schema_t0.currentText(),
                                self.cb_table_t0.currentText()
                                )
                    )
        yearCode_t0 = cur2.fetchone()
        cur2.close();
            #Récupération du type de données du code t0
        cur = self.conn.cursor()
        cur.execute(u"""Select data_type
                        from information_schema.columns 
                        where table_schema||'.'||table_name  = '{0}.{1}'  
                        and column_name like 'code4_{2}' 
                        order by column_name

                    """.format(self.cb_schema_t0.currentText(),
                                self.cb_table_t0.currentText(),
                                yearCode_t0[0]
                                )
                    )
        dType = cur.fetchone()
        cur.close();
            #Récupération de l'appel à la focntion de conversion de text en integer dans le cas où le code est un varchar
        if dType[0] == 'integer':
            tonumber_debut = ' '
            tonumber_fin = ' '
            tonummfinbis = ' '
        else:
            tonumber_debut = "to_number("
            tonumber_fin = ", '9999')"
            tonummfinbis = ", ''9999'')"


        
            #Lancement du processus de comparaison de socle
        cur5 = self.conn.cursor()
        cur5.execute(u"""
                --Création de la table de comparaison avec les champs nécessaire sans les différentes dates
                drop table if exists {6}.{7};
                Create table {6}.{7} (
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
                        gid_t0 integer,                                         
                        constraint pk_{6}_{7} PRIMARY KEY (gid)
                );
                create index idx_{6}_{7} on {6}.{7} using gist(geom);


                    --Création de la donnée avec les nouvelles géométries fusionnées
                drop table if exists vm_temp_compare cascade;
                Create temporary table vm_temp_compare as 
                Select row_number() over() as gid, * ,
                                case when code4_{1} = {12}code4_{0}{13} Then false::boolean
                                else true::boolean
                                end as evolution_{0}_{1}
                From (
                    Select (st_dump(st_collectionextract(st_safe_intersection(mos.geom, p.geom),3))).geom::geometry(Polygon,2154) as geom,
                        mos.gid as gid_t0,
                        p.to_milit as to_milit,
                        p.to_bati as to_bati,
                        p.to_batire as to_batire,
                        p.to_batagri as to_batagri,
                        p.to_serre as to_serre,
                        p.to_indust as to_indust,
                        p.to_comer as to_comer,
                        p.to_zic as to_zic,
                        p.to_transp as to_transp,
                        p.to_voiefer as to_voiefer,
                        p.to_carrier as to_carrier,
                        p.to_cime as to_cime,
                        p.to_sport as to_sport,
                        p.to_loisir as to_loisir,
                        p.to_agri as to_agri,
                        p.to_veget as to_veget,
                        p.to_eau as to_eau,
                        p.to_route as to_route,
                        p.to_batimaison as to_batimaison,
                        p.pre_scol as pre_scol,
                        p.pre_sante as pre_sante,
                        p.pre_eqadmi as pre_eqadmi,
                        p.pre_o_nrj as pre_o_nrj,
                        p.pre_transp as pre_transp,
                        p.pre_sploi as pre_sploi,
                        p.m_fonction as m_fonction,
                        p.prob_jardin as prob_jardin,
                        p.idu,
                        p.num_parc,
                        p.tex,
                        p.section,
                        p.code_insee,
                        --p.nom_commune as nom_commune,
                        mos.{8} as subdi_sirs,
                        left(p.code_insee,2) || p.num_parc || coalesce(mos.{8}, '')::character varying as id_mos,
                        mos.{9} as code4_{0},
                        mos.{10} as lib4_{0},
                        mos.{11} as remarque_{0},
                        p.code4_{1},
                        p.lib4_{1},
                        p.remarque_{1} as remarque_{1}
                    From {4}.{5} p
                    left Join {2}.{3} mos on st_intersects(p.geom,mos.geom)
                ) tt;

                    --Ajout des colonnes de code pour les différentes année contenues + la nouvelle année
                    --Ajout des colonnes de surface et périmetre 
                DO 
                LANGUAGE plpgsql
                $BODY$
                    DECLARE
                        v_annee character varying;
                        v_datatype character varying;
                    BEGIN
                        For v_annee, v_datatype in Select right(column_name,4), data_type from information_schema.columns where table_schema||'.'||table_name  = '{2}.{3}' and column_name like 'code4%' order by column_name asc LOOP
                            execute format('Alter table {6}.{7} add column code4_%1$s integer;
                                            Alter table {6}.{7} add column lib4_%1$s character varying;
                                            Alter table {6}.{7} add column remarque_%1$s character varying;', v_annee);
                        END LOOP;
                        Alter table {6}.{7} add column code4_{1} integer;
                        Alter table {6}.{7} add column lib4_{1} character varying;
                        Alter table {6}.{7} add column remarque_{1} character varying;

                        Alter table {6}.{7} add column surface_m2 double precision;                        
                        Alter table {6}.{7} add column perimetre double precision;
                    END;
                $BODY$;



                    --Insertion des données dans la table en fusionnant les routes
                insert into {6}.{7} (
                            gid_t0,
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
                            idu,
                            num_parc,
                            tex,
                            section,
                            code_insee,
                            --nom_commune
                            subdi_sirs,
                            id_mos, 
                            code4_{0}, 
                            code4_{1}, 
                            lib4_{0}, 
                            lib4_{1}, 
                            remarque_{0}, 
                            remarque_{1}, 
                            geom                            
                ) 
                with tmp as (
                    Select 
                        left(code_insee,2)||'NC'|| row_number() over() as id_mos,
                        code_insee,
                        --nom_commune, 
                        array_to_string(array_agg(distinct (code4_{0})), ',') as code4_{0},
                        array_to_string(array_agg(distinct (lib4_{0})), ',') as lib4_{0},
                        array_to_string(array_agg(distinct (remarque_{0})), ',') as remarque_{0},
                        code4_{1}, 
                        lib4_{1},
                        remarque_{1},
                        (st_dump(st_collectionextract(st_union(geom),3))).geom::geometry(Polygon,2154) as geom
                    From vm_temp_compare mos
                    where {12}code4_{0}{13} in (1224, 1222, 1221, 1223, 1225, 1226)
                    Group by code4_{1}, code_insee, lib4_{1}, remarque_{1} , subdi_sirs --,nom_commune
                    Having code4_{1} in (1224, 1222, 1221, 1223, 1225, 1226) and subdi_sirs is null 
                ), tmpunion as(
                    Select row_number() over() as gid, *
                        from tmp
                ), tmp1 as (
                    Select gid
                    From vm_temp_compare
                    where {12}code4_{0}{13} in (1224, 1222, 1221, 1223, 1225, 1226)
                    and (code4_{1} in (1224, 1222, 1221, 1223, 1225, 1226) and subdi_sirs is null )
                ), tmp3 as (
                (Select
                    gid_t0, 
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
                    idu,
                    num_parc,
                    tex,
                    section,
                    code_insee,
                    --nom_commune,
                    subdi_sirs,
                    id_mos, 
                    {12}code4_{0}{13}, 
                    code4_{1}, 
                    lib4_{0}, 
                    lib4_{1}, 
                    remarque_{0}, 
                    remarque_{1}, 
                    geom
                From vm_temp_compare mos 
                Where mos.gid not in (Select gid from tmp1)
                )
                UNION
                (Select 
                    null::integer as gid_t0,
                    null as to_milit,
                    null as to_bati,
                    null as to_batire,
                    null as to_batagri,
                    null as to_serre,
                    null as to_indust,
                    null as to_comer,
                    null as to_zic,
                    null as to_transp,
                    null as to_voiefer,
                    null as to_carrier,
                    null as to_cime,
                    null as to_sport,
                    null as to_loisir,
                    null as to_agri,
                    null as to_veget,
                    null as to_eau,
                    null as to_route,
                    null as to_batimaison,
                    null as pre_scol,
                    null as pre_sante,
                    null as pre_eqadmi,
                    null as pre_o_nrj,
                    null as pre_transp,
                    null as pre_sploi,
                    null as m_fonction,
                    null as prob_jardin,
                    'NC' as idu,
                    'NC' as num_parc,
                    'NC' as tex, 
                    'NC' as section, 
                    code_insee as code_insee,
                    --nom_commune as nom_commune,
                    null as subdi_sirs,
                    id_mos as id_mos,  
                    {12}code4_{0}{13} as code4_{0}, 
                    code4_{1} as code4_{1}, 
                    lib4_{0} as lib4_{0}, 
                    lib4_{1} as lib4_{1}, 
                    remarque_{0} as remarque_{0}, 
                    'Unification des routes' as remarque_{1}, 
                    geom
                from tmpunion)
                )
                    Select  *
                    From tmp3;

                    --Mise à jour des codes des années précédentes t-x
                    --Mise à jour des codes t+1 lorsque l'évolution est jugé incorecte
                DO 
                LANGUAGE plpgsql
                $BODY$
                    DECLARE
                        v_gid_t0 integer;
                        v_annee character varying;
                        v_remarque integer;
                    BEGIN
                            --Mise à jour des 
                        For v_annee in Select right(column_name,4) from information_schema.columns where table_schema||'.'||table_name  = '{2}.{3}' and column_name like 'code4%' order by column_name asc LOOP
                            execute format('select count(*) from information_schema.columns where table_schema||''.''||table_name  = ''{2}.{3}'' and column_name like ''remarque_%1$s'' ', v_annee) into v_remarque;
                            if v_remarque > 0 then
                                execute format('Update {6}.{7} x Set 
                                                    code4_%1$s = {12}y.code4_%1$s{14},
                                                    lib4_%1$s = y.lib4_%1$s,
                                                    remarque_%1$s = y.remarque_%1$s,
                                                    surface_m2 = st_area(x.geom),
                                                    perimetre = st_perimeter(x.geom)
                                                    From {2}.{3} y
                                                    Where gid_t0 = y.gid;
                                                ', v_annee);
                            else
                                execute format('Update {6}.{7} x Set 
                                                    code4_%1$s = {12}y.code4_%1$s{14},
                                                    lib4_%1$s = y.lib4_%1$s,
                                                    surface_m2 = st_area(x.geom),
                                                    perimetre = st_perimeter(x.geom)
                                                    From {2}.{3} y
                                                    Where gid_t0 = y.gid;
                                                ', v_annee);

                            end if;
                                execute format('Update {6}.{7} x Set 
                                                    code4_%1$s = code4_{1},
                                                    lib4_%1$s = lib4_{1},
                                                    surface_m2 = st_area(x.geom),
                                                    perimetre = st_perimeter(x.geom)
                                                    Where gid_t0 is null
                                                ', v_annee);
                        END LOOP;
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where subdi_sirs is not null;
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where (code4_{1} = 1412 and  code4_{0} in (1112, 1113, 1114, 1115)) or (code4_{1} = 1112 and  code4_{0} = 1412);
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where code4_{1} = 1226 and  code4_{0} != 1226;

                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where code4_{1} = 2511 and  (code4_{0} = 2121 or code4_{0} = 1412) ;

                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where code4_{0} in (1112, 1113,1114,1115,1122,1131) and  (to_char(code4_{1}, '9999') like ' 5%' 
                                                                                        or to_char(code4_{1}, '9999') like ' 3%'
                                                                                        or to_char(code4_{1}, '9999') like ' 2%'
                                                                                        or to_char(code4_{1}, '9999') like ' 13%'
                                                                                        or to_char(code4_{1}, '9999') like ' 12%');
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where (code4_{0} = 1421 and code4_{1} != 1421) or (code4_{0} = 1422 and code4_{1} != 1422) or (code4_{0} != 1412 and code4_{1} = 1412);


                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where (code4_{0} != 121 and code4_{1} = 121) ;

                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where to_char(code4_{1}, '9999') in (' 3251', ' 3261')  and to_char(code4_{0}, '9999') not in (' 3251', ' 3261') ;

                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where to_char(code4_{0}, '9999') like ' 13%'  and code4_{1} = 3251;

                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where code4_{1} = 1112 and to_char(code4_{0}, '9999') in (' 1113', ' 1114', ' 1122', ' 1212', ' 1215', ' 1217', ' 1213', ' 1422', ' 1431', ' 1214', ' 1131', ' 2511', ' 1222', ' 2121') ;
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where code4_{1} = 1115 and to_char(code4_{0}, '9999') in (' 1212', ' 1216', ' 1217', ' 1214', ' 1113', ' 1222', ' 1212', ' 1131', ' 2121', ' 1213', ' 1112', ' 1422', ' 1211' ) ;
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where code4_{1} = 1113 and to_char(code4_{0}, '9999') in (' 1222', ' 1213', ' 1131', ' 1112') ;
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}

                                Where code4_{1} = 1212 and to_char(code4_{0}, '9999') in (' 1217', ' 1412') ;
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where code4_{1} = 1114 and to_char(code4_{0}, '9999') in (' 1213') ;
                        update {6}.{7} x
                            Set code4_{1} = code4_{0},
                                lib4_{1} = lib4_{0}
                                Where code4_{1} = 2511 and code4_{0} = 1226
                                And (st_perimeter(geom)/(2 * sqrt(3.14* st_area(geom)))) > 2 ;



                        Alter table {6}.{7} drop column gid_t0;
                    END;
                $BODY$;

                    """.format(
                        yearCode_t0[0],#0
                        yearCode_t1[0],#1
                        self.cb_schema_t0.currentText(),#2
                        self.cb_table_t0.currentText(),#3
                        self.cb_schema_t1.currentText(),#4
                        self.cb_table_t1.currentText(),#5
                        self.cb_schema_desti.currentText(),#6
                        self.le_table_desti.text(),#7
                        self.subdi_sirs[0],#8
                        self.code4[0],#9
                        self.lib4[0],#10
                        self.remarque[0],#11
                        tonumber_debut,#12
                        tonumber_fin,#13
                        tonummfinbis#14
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



