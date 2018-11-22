# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.PyQt.QtWidgets import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *
import os, sys
import psycopg2
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

class MainDialog(QDialog, Ui_interface_socle):
    def __init__(self, interface):
        QDialog.__init__(self)
        self.setupUi(self)
    	self.host = None
        self.port = None
        self.database = None
        self.username = None
        self.pwd = None

        self.pb_avancement.setValue(0)
        self.lbl_etape.setText(None)
        

        self.connect(self.pb_start, SIGNAL("clicked()"), self.createSocle)

        self.pb_start.setEnabled(0)

        self.connect(self.pb_dbConnect, SIGNAL("clicked()"), self.charge)

        self.updateConnectionList()



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

    def connexion(self):
        #Fonction de connexion à la base de données
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
        '''
        Update the combo box containing the database connection list
        '''
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
        '''
        Update the combo box containing the schema list if relevant
        '''
        self.cb_parcelle_bdtopo.clear()


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
        db = self.connexion()

        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:
            self.relation_district = QSqlTableModel(self, db)

            queryTable = QSqlQuery(db)
            queryTable.prepare("Select table_schema || '.' || table_name as tname from information_schema.tables where table_schema not in ('pg_catalog', 'information_schema') order by table_schema;")
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

                    #self.pb_start.setEnabled(1)


            querySchema = QSqlQuery(db)
            querySchema.prepare("Select distinct table_schema from information_schema.tables where table_schema not in ('pg_catalog', 'information_schema') order by table_schema;")
            if querySchema.exec_():
                while querySchema.next():
                    self.cb_schema.addItem(querySchema.value(0))


            self.cb_parcelle.setCurrentIndex(self.cb_parcelle.findText('cadastre_edigeo.parcelle_info'))
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
            self.cb_route.setCurrentIndex(self.cb_route.findText('ref_ign.route_primaire'))
            self.cb_ipli.setCurrentIndex(self.cb_ipli.findText('data_exo.ipli_n_occ_sol_lit_region'))
            self.cb_remarquable.setCurrentIndex(self.cb_remarquable.findText('ref_ign.bati_remarquable'))
            self.cb_indust.setCurrentIndex(self.cb_indust.findText('ref_ign.bati_industirel'))
            self.cb_indif.setCurrentIndex(self.cb_indif.findText('ref_ign.bati_indifferencie'))
            self.cb_surf_eau.setCurrentIndex(self.cb_surf_eau.findText('ref_ign.surface_eau'))
            self.cb_pt_eau.setCurrentIndex(self.cb_pt_eau.findText('ref_ign.point_eau'))
            self.cb_surf_acti.setCurrentIndex(self.cb_surf_acti.findText('ref_ign.surface_activite'))
            self.cb_triage.setCurrentIndex(self.cb_triage.findText('ref_ign.aire_triage'))
            self.cb_voiefer.setCurrentIndex(self.cb_voiefer.findText('ref_ign.troncon_voie_ferree'))

            self.cb_schema.setCurrentIndex(self.cb_schema.findText('sandbox'))
            self.le_destination.setText('socle_c_mos2')

            """self.cb_parcelle.setCurrentIndex(self.cb_subparc.findText(None))
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

            self.cb_schema.setCurrentIndex(self.cb_schema.findText(None))"""

    def canStart(self):
        if self.cb_parcelle.currentText() == '' or self.cb_subparc.currentText() == '' or self.cb_tronroute.currentText() == '' or self.cb_tronfluv.currentText() == '' or self.cb_tsurf.currentText() == '' or self.cb_rpga.currentText() == '' or self.cb_finess.currentText() == '' or self.cb_res_sport.currentText() == '' or self.cb_ff_parcelle.currentText() == '' or self.cb_parcellaire.currentText() == '' or self.cb_pai_cult.currentText() == '' or self.cb_paitransp.currentText() == '' or self.cb_paisante.currentText() == '' or self.cb_pairel.currentText() == '' or self.cb_paimilit.currentText() == '' or self.cb_paiens.currentText() == '' or self.cb_paicom.currentText() == '' or self.cb_paitransfo.currentText() == '' or self.cb_terrainsport.currentText() == '' or self.cb_cime.currentText() == '' or self.cb_zoneveget.currentText() == '' or self.cb_parcelle_bdtopo.currentText() == '' or self.cb_route.currentText() == '' or self.cb_remarquable.currentText() == '' or self.cb_indust.currentText() == '' or self.cb_indif.currentText() == '' or self.cb_surf_eau.currentText() == '' or self.cb_pt_eau.currentText() == '' or  self.cb_surf_acti.currentText() == '' or self.cb_triage.currentText() == '' or self.cb_voiefer.currentText() == '' or self.cb_paisport.currentText() == '' or self.cb_paisport.currentText() == '' or self.cb_schema.currentText() == '' or self.le_destination.text() == '':
            self.pb_start.setEnabled(0)
        else:
            self.pb_start.setEnabled(1)


    def createSocle(self):

        
        self.pb_start.setEnabled(0)
        self.lbl_etape.setText(u'Etape 1/4')
        print 'starting'
        conn = psycopg2.connect(host=self.host, port=self.port, user=self.username, dbname=self.database, password=self.pwd )
        cur = conn.cursor()
        
        cur.execute(u"""
                    Drop table if exists vm_parc_h_subd cascade;
                    Create temporary table vm_parc_h_subd as 
                    Select row_number() over() as gid, * From (
                    Select (st_dump(st_difference(parc.geom, st_union(sp.geom)))).geom::geometry(Polygon, 2154) as geom, parc.idu, 'zzz'::character varying as tex   
                    From {0} parc
                    Join {1} sp on St_Within(St_PointOnSurface(sp.geom), parc.geom)
                    Group by parc.geom, idu)tt;


                    Drop table if exists v_temp_parc_subparc cascade;
                    Create temporary table v_temp_parc_subparc As 
                    Select ROW_NUMBER() OVER() as unique_id, *
                    From(
                        (Select (st_dump(st_collectionextract(gs.geom,3))).geom::geometry(Polygon,2154) as geom, 
                                pi.idu as idu, 
                                c29.code_insee as code_insee, 
                                pi.idu || coalesce(gs.tex, 'zzz') as num_parc, 
                                coalesce(gs.tex, 'zzz') as tex
                            From {1} gs
                            Join {2} c29 on St_within(St_PointOnSurface(gs.geom), c29.geom)
                            Join {0} pi on St_Within(St_PointOnSurface(gs.geom), pi.geom)
                        )
                    UNION
                        (Select (st_dump(st_collectionextract(pi2.geom, 3))).geom::geometry(Polygon,2154) as geom, 
                                pi2.idu as idu, 
                                c292.code_insee as code_insee, 
                                pi2.idu as num_parc, 
                                null as tex  
                        From {0} pi2
                        Join {2} c292 on St_within(St_PointOnSurface(pi2.geom), c292.geom) 
                        Where ogc_fid not in (Select distinct pi3.ogc_fid 
                                                From {0} pi3
                                                Join {1} gs2 on St_Within(St_PointOnSurface(gs2.geom), pi3.geom))
                        )
                    UNION
                        (Select (st_dump(st_collectionextract(vmhs.geom,3))).geom::geometry(Polygon,2154) as geom, 
                                vmhs.idu as idu, 
                                c292.code_insee as code_insee, 
                                vmhs.idu || vmhs.tex as num_parc, 
                                vmhs.tex  
                        From vm_parc_h_subd vmhs
                        Join {2} c292 on St_within(St_PointOnSurface(vmhs.geom), c292.geom)) 
                    ) tt;

                    update v_temp_parc_subparc 
                        set tex = 'zzz',
                            num_parc = idu || 'zzz'
                        Where tex = '';

                    Drop table if exists vm_cut_on_com;
                    Create temporary table vm_cut_on_com as 
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
                    Drop table if exists vm_temp_exclusion;
                    Create temporary table vm_temp_exclusion as 
                    Select vmt2.uq_gid, vmt2.unique_id, vmt2.code_insee, vmps.idu, vmps.num_parc, vmps.tex, vmt2.geom::geometry(polygon, 2154)
                    From vm_cut_on_com vmt2
                    Join v_temp_parc_subparc vmps on vmps.unique_id = vmt2.unique_id  
                    Where uq_gid in (Select uq_gid 
                                        From vm_cut_on_com vm, 
                                            {2} bdpc
                                        Where st_within(st_pointonsurface(vm.geom), bdpc.geom)
                                        AND vm.code_insee = bdpc.code_insee );
                    Drop table if exists vm_temp_exclus;
                    Create temporary table vm_temp_exclus as 
                    Select  vmcoc.uq_gid, vmcoc.unique_id, vmcoc.code_insee, vmps.idu, vmps.num_parc, vmps.tex, vmcoc.geom::geometry(Polygon, 2154), st_area(vmcoc.geom) as surf_area, dd.code_insee as new_insee
                    From vm_cut_on_com vmcoc
                    Join v_temp_parc_subparc vmps on vmps.unique_id = vmcoc.unique_id
                    Join {2} dd on St_within(st_pointonsurface(vmcoc.geom), dd.geom )
                    Where vmcoc.uq_gid not in (Select uq_gid From vm_temp_exclusion);

                    Drop table if exists vm_temp_parc;
                    Create temporary table vm_temp_parc as 
                    Select ROW_NUMBER() over() as un_idd, * FROM( 
                    (Select unique_id, code_insee, idu, num_parc, tex, geom
                    From  vm_temp_exclusion
                    )
                    UNION 
                    (
                    Select unique_id, code_insee, idu, num_parc, tex, geom
                    From v_temp_parc_subparc
                    Where unique_id not in (Select unique_id From vm_temp_exclusion)
                    ))tt;

                    Create or replace function {10}.fun_fusion(i_origine text, i_fuse text) 
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
                                Constraint pk_t_elimin PRIMARY KEY (gid)
                            );

                            For v_geomF, v_inseeF, v_surfF, v_idF in Select geom, new_insee, surf_area, uq_gid from tt_fuse LOOP
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
                                    tex character varying                                                                                                   
                                );
                                IF v_surfF < 10 THEN
                                    For v_geomO, v_inseeO, v_idO, v_iduO, v_numpO, v_texO in Select geom, code_insee, unique_id, idu, num_parc, tex 
                                                                                                From tt_origine 
                                                                                                Where code_insee = v_inseeF AND st_intersects(v_geomF, geom) LOOP
                                        IF v_inseeO = v_inseeF Then
                                            IF St_intersects(v_geomF, v_geomO) THEN
                                                Select st_area(st_intersection(st_buffer(v_geomF,1), v_geomO )) INTO v_surfO;
                                                Insert into tt_to_fuse values (v_idO, v_geomO, v_surfO, v_inseeO, v_inseeF, v_surfF,v_iduO, v_numpO, v_texO);
                                                --RAISE NOTICE '%, %, %', v_inseeO, v_inseeF, v_surfF;
                                            END IF;
                                        END IF;
                                    END LOOP;
                                    Select count(*) From tt_to_fuse into cpt;
                                    IF cpt > 0 THEN
                                        Select (st_dump(st_collectionextract(st_union(tt.geom, v_geomF),3))).geom::geometry(Polygon, 2154) as geom, tt.unique_id, tt.inseeO, tt.inseeF , tt.idu, tt.num_parc, tt.tex
                                            From tt_to_fuse tt
                                            Where v_inseeF = tt.inseeO 
                                            AND tt.surf in (Select max(surf) From tt_to_fuse LIMIT 1) 
                                        INTO v_geomFusion, v_idFusion, v_inseeO, v_inseeF, v_iduO, v_numpO, v_texO;
                                        INSERT INTO t_eliminated (geom, code_insee, idu, num_parc, tex, geom_check, old_id) values
                                            (v_geomFusion, v_inseeO, v_iduO, v_numpO, v_texO, FALSE, v_idfusion);
                                    END IF;
                                END IF;
                            End Loop;
                            Select count(*) From t_eliminated INTO cpt;
                            While cpt2 < cpt LOOP
                                Select gid, idu, code_insee, num_parc, tex, old_id From t_eliminated Where geom_check = False
                                    INTO v_eliId, v_eliIdu, v_eliInsee, v_eliNp, v_eliTex, v_eliOld;
                                Select (st_dump(st_collectionextract(st_union(geom),3))).geom::geometry(Polygon, 2154) as geom
                                From t_eliminated
                                Where idu = v_eliIdu INTO v_lastGeom;
                                INSERT INTO t_eliminated (geom, code_insee, idu, num_parc, tex, geom_check, old_id) values
                                            (v_lastGeom, v_eliInsee, v_eliIdu, v_eliNp, v_eliTex, TRUE, v_eliOld);
                                Delete From t_eliminated 
                                    Where idu = v_eliIdu AND geom_check = FALSE;
                                cpt2 = cpt2 +1;
                                Select count(*) From t_eliminated INTO cpt;
                            END LOOP;
                            Return;
                        END;
                    $BODY$
                        LANGUAGE 'plpgsql';

                    select {10}.fun_fusion('vm_temp_parc', 'vm_temp_exclus');

                    Drop table if exists vm_socle_c;
                    Create temporary table vm_socle_c as 
                    Select ROW_NUMBER() over() as gid, * FROM( 
                    (Select gid as old_gid, code_insee, idu, num_parc, tex, geom::geometry(polygon,2154)
                    From  t_eliminated
                    )
                    UNION 
                    (
                    Select unique_id as old_gid, code_insee, idu, num_parc, tex, geom
                    From vm_temp_parc
                    Where unique_id not in (Select old_id From t_eliminated)
                    ))tt;

                    Drop table if exists vm_socle_nc cascade;
                    Create temporary table vm_socle_nc as 
                    Select ROW_NUMBER() over() as gid, * FROM( 
                        Select (st_dump(st_collectionextract(st_difference(com.geom, st_union(so.geom)),3))).geom::geometry(Polygon, 2154) as geom, com.code_insee
                        From vm_socle_c so, {2} com
                        group by com.geom, com.code_insee
                    ) tt;

                    Drop table if exists vm_nc_lito cascade;
                    Create temporary table vm_nc_lito as
                    Select ROW_NUMBER() OVEr() as gid, *
                    From (
                        Select (st_dump(
                                    st_collectionextract(
                                        st_intersection(st_union(vmtt.geom),vmnc.geom),3))).geom::geometry(polygon,2154) as geom, vmnc.code_insee
                        From vm_socle_nc vmnc, {9} vmtt
                        Group By vmnc.geom, vmnc.code_insee
                    )tt;

                    Drop table if exists vm_primaire;
                    Create temporary table vm_primaire as
                    Select ROW_NUMBER() OVEr() as gid, st_union(geom)::geometry(Polygon,2154) as geom, nature
                    From (
                    (Select st_buffer(rp.geom, rp.largeur/2, 'endcap=square join=round')::geometry(Polygon,2154) as geom, 'primaire'::character varying as nature
                    From {3} rp, {2} com
                    Where rp.importance in ('1', '2') 
                    AND st_intersects(rp.geom, com.geom)
                    )
                    )tt
                    Where st_area(tt.geom) > 10
                    Group By nature;
                    
                    Drop table if exists vm_secondaire;
                    Create temporary table vm_secondaire as
                    Select ROW_NUMBER() OVEr() as gid,  geom, nature
                    From (select st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
                        From (
                            Select st_buffer(rs.geom, largeur/2, 'endcap=square join=round')::geometry(Polygon,2154) as geom, 'secondaire'::character varying as nature
                            From {3} rs, {2} com
                            Where rs.importance in ('3', '4', '5', 'NC') AND rs.nature not in ('Chemin', 'Escalier', 'Piste cyclable', 'Sentier') 
                            AND st_intersects(rs.geom, com.geom) 
                            Group by rs.largeur/2, rs.geom
                        )tt
                    Where st_area(tt.geom) > 10
                    Group by nature) tt2;

                    Drop table if exists vm_chemin;
                    Create temporary table vm_chemin as
                    Select ROW_NUMBER() OVEr() as gid,  geom, nature
                    From (select st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
                        From (
                            Select st_buffer(c.geom, 5.0/2)::geometry(Polygon,2154) as geom, 'Chemin'::character varying as nature
                            From {3} c, {2} com
                            Where c.nature in ('Chemin', 'Escalier' , 'Piste cyclable', 'Sentier'
                            AND st_intersects(c.geom, com.geom)
                        )tt
                    Where st_area(tt.geom) > 10
                    group By nature)tt2 ;

                    Drop table if exists vm_veget;
                    Create temporary table vm_veget as
                    Select ROW_NUMBER() OVEr() as gid, st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
                    From (
                            Select (st_dump(st_collectionextract(st_safe_intersection(vz.geom, vmnc.geom),3))).geom::geometry(Polygon, 2154) as geom, 'veget'::character varying as nature
                            From {4} vz
                            Join vm_nc_lito vmnc on st_intersects(vz.geom, vmnc.geom)
                        ) tt2
                    Where st_area(tt2.geom) > 400
                    Group by nature;

                    Drop table if exists vm_hydro;
                    Create temporary table vm_hydro as
                    Select ROW_NUMBER() OVEr() as gid, st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
                    From (
                            Select (st_dump(st_collectionextract(st_safe_intersection(st_force2D(se.geom), vmnc.geom),3))).geom::geometry(Polygon, 2154), 'hydro'::character varying as nature
                            From {5} se
                            Join vm_nc_lito vmnc on st_intersects(se.geom, vmnc.geom)
                        ) tt2
                    Where st_area(tt2.geom) > 10
                    Group by nature;

                    Drop table if exists vm_rpga;
                    Create temporary table vm_rpga as
                    Select ROW_NUMBER() OVER() as gid, st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
                    From (
                        Select (st_dump(st_collectionextract(st_safe_intersection(rpga.geom, vmnc.geom),3))).geom::geometry(Polygon, 2154), 'agricole'::character varying as nature
                         From {6} rpga
                         Join vm_nc_lito vmnc on st_intersects(rpga.geom, vmnc.geom)
                    )tt
                    Where st_area(tt.geom) > 200
                    Group by nature;

                    drop table if exists t_socle_nc;
                    Create temporary table t_socle_nc (
                        gid serial,
                        geom geometry(Polygon,2154),
                        nature character varying,
                        type_ajout character varying,
                        Constraint pk_socle_nc primary key (gid)
                    );
                    create index idx_socle_nc_geom on t_socle_nc using gist(geom);
                        
                    insert into t_socle_nc (geom, nature, type_ajout) 
                        select (st_dump(st_collectionextract(st_safe_intersection(vmnc.geom, ipli.geom),3))).geom::geometry(Polygon, 2154), 
                                    ipli.libelle,
                                    'plage'
                                From {7} ipli
                                Join vm_nc_lito vmnc on st_intersects(ipli.geom, vmnc.geom)
                                Where libelle in ('Plage', 'Rochers, falaise');


                    insert into t_socle_nc (geom, nature, type_ajout) 
                        select (st_dump(st_collectionextract(st_safe_difference(st_safe_intersection(vmnc.geom, ipli.geom), st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
                                    ipli.nature,
                                    'route1'
                                From vm_primaire ipli, t_socle_nc vsocle, vm_nc_lito vmnc
                                Where st_intersects(ipli.geom, vmnc.geom)
                                Group by vmnc.geom, ipli.geom, ipli.nature;


                    insert into t_socle_nc (geom, nature, type_ajout) 
                        select (st_dump(st_collectionextract(st_safe_difference(st_safe_intersection(vmnc.geom, ipli.geom), st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
                                    ipli.nature,
                                    'secondaire'
                                From vm_secondaire ipli, t_socle_nc vsocle, vm_nc_lito vmnc
                                Where st_intersects(ipli.geom, vmnc.geom)
                                Group by vmnc.geom, ipli.geom, ipli.nature;

                    delete from t_socle_nc where st_area(geom) < 10;

                    insert into t_socle_nc (geom, nature, type_ajout) 
                        select (st_dump(st_collectionextract(st_safe_difference(st_safe_intersection(vmnc.geom, ipli.geom), st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
                                    ipli.nature,
                                    'chemin'
                                From vm_chemin ipli, t_socle_nc vsocle, vm_nc_lito vmnc
                                Where st_intersects(ipli.geom, vmnc.geom)
                                Group by vmnc.geom, ipli.geom, ipli.nature;


                    delete from t_socle_nc where st_area(geom) < 10;

                    insert into t_socle_nc (geom, nature, type_ajout) 
                        select (st_dump(st_collectionextract(st_safe_difference(st_safe_intersection(vmnc.geom, ipli.geom), st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
                                    ipli.nature,
                                    'hydro'
                                From vm_hydro ipli, t_socle_nc vsocle, vm_nc_lito vmnc
                                Where st_intersects(ipli.geom, vmnc.geom)
                                Group by vmnc.geom, ipli.geom, ipli.nature;


                    delete from t_socle_nc where st_area(geom) < 10;

                    insert into t_socle_nc (geom, nature, type_ajout) 
                        select (st_dump(st_collectionextract(st_safe_difference(ipli.geom, st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
                                    ipli.nature,
                                    'rpga'
                                From vm_rpga ipli, t_socle_nc vsocle, vm_nc_lito vmnc
                                Where st_intersects(ipli.geom, vmnc.geom)
                                Group by vmnc.geom, ipli.geom, ipli.nature;


                    delete from t_socle_nc where st_area(geom) < 10;

                    Drop table if exists vm_temp_veget;
                    Create temporary table vm_temp_veget as
                    Select ROW_number() over() as gid, st_union(geom), * 
                    From (
                        Select st_safe_difference(ipli.geom, st_union(vsocle.geom)) as geom, ipli.nature
                        From vm_veget ipli, t_socle_nc vsocle
                        Where st_area(st_intersection(ipli.geom, vsocle.geom)) > 150
                        Group by ipli.geom, ipli.nature
                        )tt
                    group by tt.geom, tt.nature ;

                    insert into t_socle_nc (geom, nature, type_ajout) 
                        select (st_dump(st_collectionextract(ipli.geom,3))).geom::geometry(Polygon, 2154), 
                                    ipli.nature,
                                    'veget'
                                From vm_temp_veget ipli, t_socle_nc vsocle
                                Group by ipli.geom, ipli.nature;

                    delete from t_socle_nc where st_area(geom) < 10;

                    Drop table if exists vm_scv1;
                    Create temporary table vm_scv1 as
                        Select ROW_NUMBER() OVER() as gid, *
                        FROM (
                            (Select code_insee, idu, num_parc, tex, geom
                            From vm_socle_c)
                            UNION
                            (Select 'NC','NC', 'NC', nature, geom
                            From t_socle_nc)
                            )tt;

                    Drop table if exists vm_nc_v2 cascade;
                    Create temporary table vm_nc_v2 as 
                    Select ROW_NUMBER() over() as gid, * FROM( 
                        Select (st_dump(st_collectionextract(st_difference(com.geom, st_union(st_buffer(so.geom, 0.0001))),3))).geom::geometry(Polygon, 2154) as geom, com.code_insee
                        From vm_scv1 so, {2} com
                        Where st_intersects(com.geom, so.geom)
                        group by com.geom, com.code_insee
                    ) tt;

                    Drop table if exists socle_temp;
                    Create temporary table socle_temp as 
                        Select ROW_NUMBER() OVER() as gid, *
                        FROM (
                            (Select code_insee, idu, num_parc, tex, geom
                            From vm_scv1)
                            UNION
                            (Select vmnc.code_insee,'NC', 'NC', 'NC', (st_dump(st_collectionextract(st_intersection(st_union(vmtt.geom), vmnc.geom), 3))).geom::geometry(polygon,2154) as geom
                            From vm_nc_v2 vmnc, {8} vmtt
                            Group by vmnc.code_insee, vmnc.geom)
                            )tt;
                    create index idx_socleF_geom on socle_temp using gist(geom);
                   """.format(self.cb_parcelle.currentText(), 
                                self.cb_subparc.currentText(), 
                                 self.cb_parcellaire.currentText(),
                                 self.cb_route.currentText(),
                                 self.cb_zoneveget.currentText(),
                                 self.cb_surf_eau.currentText(),
                                 self.cb_rpga.currentText(),
                                 self.cb_ipli.currentText(),
                                 self.cb_parcelle_bdtopo.currentText(),
                                 self.cb_schema.currentText()
                                 ))
        cur.close()
        conn.commit()
        self.lbl_etape.setText(u'Etape 2/4')
        self.pb_avancement.setValue(20)
        print 'Then'
        cur2 = conn.cursor()

        cur2.execute(u"""
            Create or replace function {30}.fun_typage(i_socle_c text, 
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
            $BODY$
                DECLARE
                    v_geom geometry(polygon,2154); -- Géométrie du socle
                    v_insee character varying; --code insee du socle
                    v_idu character varying; -- code idu du socle
                    v_num_parc character varying;-- num_parc du socle
                    v_tex character varying; -- tex du socle
                    v_gid integer; -- identifiant du socle
                    
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

                    Execute format('Create temporary table tt_secondaire as
                        Select ROW_NUMBER() OVEr() as gid, *
                            From (select (st_dump(st_collectionextract(st_union(geom),3))).geom::geometry(polygon,2154) as geom, nature
                                From (
                                    Select st_buffer(rs.geom, largeur/2, ''endcap=square join=round'')::geometry(Polygon,2154) as geom, nature
                                    From %1$s rs, %2$s com
                                    Where st_intersects(rs.geom, com.geom) 
                                    Group by rs.largeur/2, rs.geom, nature
                                )tt
                            Group by nature) tt2;', i_route_sec, i_emprise);
                    

                    Drop table if exists {30}.{31};
                    Create table {30}.{31} (
                        gid serial,
                        code_insee character varying,
                        idu character varying,
                        num_parc character varying,
                        tex character varying,
                        geom geometry(Polygon,2154),
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
                        m_fonction character varying,
                        prob_jardin integer,
                        code4_{32} integer,
                        constraint pk_{31} PRIMARY KEY (gid)
                                                                                            
                    );
                    Create index idx_{31}_geom on {30}.{31} using gist(geom);
                    
                    For v_geom, v_insee, v_idu, v_num_parc, v_tex, v_gid IN execute format('Select geom, code_insee, idu, num_parc, tex, gid From %1$s sc;', i_socle_c) LOOP
                        if v_idu != 'NC' then
                    --Ajout des colonnes taux
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_pai_milit, v_geom)
                    into v_tomilit;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_bati, v_geom)
                    into v_tobati;

                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_bati_indif, v_geom)
                    into v_tobati;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Chapelle'', ''Château'', ''Fort, blockhaus, casemate'', ''Monument'', ''Tour, donjon, moulin'', ''Arène ou théàtre antique'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_bati_rem, v_geom)
                    into v_tobatire;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Bâtiment agricole'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_bati_indus, v_geom)
                    into v_tobatagri;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Serre'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_bati_indus, v_geom)
                    into v_toserre;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Bâtiment industriel'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_bati_indus, v_geom)
                    into v_toindust;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.nature in (''Bâtiment commercial'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_bati_indus, v_geom)
                    into v_tocomer;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.categorie in (''Industriel ou commercial'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_surf_acti, v_geom)
                    into v_tozic;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where pm.categorie in (''Transport'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_surf_acti, v_geom)
                    into v_totransp;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(st_buffer(pm.geom, 3 * pm.nb_voies,''endcap=flat join=round'')), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_voie_ferre, v_geom)
                    into v_tovoiefer;
                    if v_tovoiefer is null or v_tovoiefer <1 THEN
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_aire_tri, v_geom)
                    into v_tovoiefer;
                    END IF;

                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%3$s''))*100)/st_area(''%3$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%3$s'', pm.geom) 
                                            AND pm.id in (Select pm.id
                                                            From %1$s pm
                                                            Join %2$s p2 on st_intersects(p2.geom, pm.geom) 
                                                            Where p2.nature = ''Carričre'' )
                                        ',i_surf_acti,  i_pai_indus_com, v_geom)
                    into v_tocarrier;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_cime, v_geom)
                    into v_tocime;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where categorie = ''Sport''
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_surf_acti, v_geom)
                    into v_tosport;
                    IF v_tosport is null or v_tosport < 1 THEN
                                    execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_terrain_sport, v_geom)
                    into v_tosport;
                    END IF;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%3$s''))*100)/st_area(''%3$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%3$s'', pm.geom)
                                            AND pm.id in (Select pm.id 
                                                            From %1$s pm
                                                            Join %2$s p2 on st_intersects(p2.geom, pm.geom)
                                                            Where p2.nature in (''Village de vacances'', ''Camping'', ''Parc de loisirs'', ''Parc zoologique'', ''parc des expositions'' ))
                                        ', i_surf_acti, i_pai_cul_lois, v_geom)
                    into v_toloisir;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where st_intersects(''%2$s'', pm.geom) 
                                        ', i_rpga, v_geom)
                    into v_toagri;
                        If v_toagri is null or v_toagri < 1 Then
                            execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where nature in (''Verger'', ''Peupleraie'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_zveget, v_geom)
                    into v_toagri;
                        END IF;

                        
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where nature not in (''Verger'', ''Peupleraie'') 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_zveget, v_geom)
                    into v_toveget;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where regime = ''Permanent'' 
                                            AND st_intersects(''%2$s'', pm.geom) 
                                        ', i_surf_eau, v_geom)
                    into v_toeau;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where  st_intersects(''%2$s'', pm.geom) 
                                        ', i_tronfluv, v_geom)
                    into v_temp_toeau;
                    if v_temp_toeau > v_toeau Then
                        v_toeau = v_temp_toeau;
                    End if;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where  st_intersects(''%2$s'', pm.geom) 
                                        ', i_tsurf, v_geom)
                    into v_temp_toeau;
                    if v_temp_toeau > v_toeau Then
                        v_toeau = v_temp_toeau;
                    End if;

                    Select ((st_area(st_safe_intersection(st_union(pm.geom), v_geom))*100)/st_area(v_geom))::integer
                                            From tt_secondaire pm
                                            Where  st_intersects(v_geom, pm.geom)       
                    into v_toroute;
                        execute format ('Select ((st_area(st_safe_intersection(st_union(pm.geom), ''%2$s''))*100)/st_area(''%2$s''))::integer
                                            From %1$s pm
                                            Where  st_intersects(''%2$s'', pm.geom) 
                                        ', i_tronroute, v_geom)
                    into v_temp_route;
                    if v_toroute < v_temp_route Then
                        v_toroute = v_temp_route;
                    end if;
                    
                            --Ajout des colonnes bool
                        --Enseignement
                        execute format ('Select 1
                                            From %1$s pm
                                            Where pm.nature = ''Enseignement''
                                            AND st_intersects(st_buffer(pm.geom, 5), ''%2$s'') 
                                        ', i_pai_scens, v_geom)
                    into v_prescol;
                    if v_prescol != 1 Then 
                        execute format ('Select 1
                                            From %1$s pm
                                            Where categorie = ''Enseignement'' 
                                            AND ((st_area(st_safe_intersection(pm.geom, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 40 
                                        ', i_surf_acti, v_geom)
                    into v_prescol;
                
                        if v_prescol != 1 Then 
                            v_prescol = 0;
                        end if;
                    end if;
                        --Sante
                        execute format ('Select 1
                                            From %1$s pm
                                            Where st_intersects(st_buffer(pm.geom, 5), ''%2$s'') 
                                        ', i_pai_sante, v_geom)
                    into v_presante;

                    if v_presante != 1 Then 
                        execute format ('Select 1
                                            From %1$s pm
                                            Where categorie = ''Santé'' 
                                            AND ((st_area(st_safe_intersection(pm.geom, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 50 
                                        ', i_surf_acti, v_geom)
                    into v_presante;
                        if v_presante != 1 THEN
                            execute format ('Select 1
                                                From %1$s pm
                                                Where lib_catego not like (''Pharmacie d''Officine'') and lib_catego not like ''Service %''
                                                AND ((st_area(st_safe_intersection(pm.geom, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 50 
                                        ', i_finess, v_geom)
                        into v_presante;
                            if v_presante != 1 Then 
                                v_presante = 0;
                            end if;
                        end if;
                    end if;
                        --Administration
                        execute format ('Select 1
                                            From %1$s pm
                                            Where nature in (''Eglise'', ''Bâtiment religieux divers'', ''Gare'', ''Mairie'', ''Préfecture'', ''Sous-préfecture'')
                                            AND st_intersects(st_buffer(pm.geom, 5), ''%2$s'') 
                                        ', i_pai_milit, v_geom)
                    into v_preqadmi;
                    if v_preqadmi != 1 Then 
                        execute format ('Select 1
                                            From %1$s pm
                                            Where nature in (''Culte catholique ou orthodoxe'', ''Culte protestant'') 
                                            AND st_intersects(st_buffer(pm.geom, 5), ''%2$s'') 
                                        ', i_pai_rel, v_geom)
                    into v_preqadmi;
                
                        if v_preqadmi != 1 Then 
                            execute format ('Select 1
                                                From %1$s pm
                                                Where nanture in (''Eglise'', ''Mairie'', ''Préfecture'', ''Sous-préfecture'') 
                                                AND ((st_area(st_safe_intersection(pm.geom, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 50 
                                            ', i_bati_rem, v_geom)
                        into v_preqadmi;
                
                            IF v_preqadmi != 1 Then
                                v_preqadmi = 0;
                            end if;
                        end if;
                    end if;
                        --Eau, énergie
                        execute format ('Select 1
                                            From %1$s pm
                                            Where nature = (''Station de pompage'')
                                            AND st_intersects(st_buffer(pm.geom, 5), ''%2$s'') 
                                        ', i_point_eau, v_geom)
                    into v_preonrj;
                    if v_preonrj != 1 Then 
                        execute format ('Select 1
                                            From %1$s pm
                                            Where categorie in = ''Gestion des eaux''
                                            AND ((st_area(st_safe_intersection(pm.geom, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 40
                                        ', i_surf_acti, v_geom)
                    into v_preonrj;

                        if v_preonrj != 1 Then 
                            execute format ('Select 1
                                                From %1$s pm
                                                Where  ((st_area(st_safe_intersection(pm.geom, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 40 
                                            ', i_post_transf, v_geom)
                        into v_preonrj;

                            If v_preonrj != 1 Then 
                                v_preonrj = 0;
                            end if;
                        end if;
                    end if;
                        --Transport
                        execute format ('Select 1
                                            From %1$s pm
                                            Where nature in (''Gare (routière, fre, ou voyageur)'', ''Parking'')
                                            AND ((st_area(st_safe_intersection(pm.geom, ''%2$s''))*100)/st_area(''%2$s''))::integer >= 40 
                                        ', i_pai_transp, v_geom)
                    into v_pretransp;
                    If v_pretransp != 1 Then 
                        v_pretransp = 0;
                    end if;
                        --Sport, loisir
                        execute format ('Select 1
                                            From %1$s pm
                                            Where st_intersects(st_buffer(pm.geom, 5), ''%2$s'') 
                                        ', i_pai_sport, v_geom)
                    into v_presploi;
                    If v_presploi != 1 Then
                        execute format ('Select 1
                                            From %1$s pm
                                            Where naturelibe != ''Intérieur''
                                            AND st_intersects(pm.geom, ''%2$s'') 
                                        ', i_res, v_geom)
                    into v_presploi;
                        IF v_presploi != 1 Then
                            execute format ('Select 2
                                            From %1$s pm
                                            Where naturelibe = ''Intérieur''
                                            AND st_intersects(pm.geom, ''%2$s'') 
                                        ', i_res, v_geom)
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
                                        ', i_foncier, v_geom)
                    into v_mfonction;

                    if v_tex is not null then
                        execute format ('Select 1
                                            From %1$s pm
                                            Where pm.dcnt09 > 1
                                            AND st_intersects(pm.geomloc, ''%2$s'') 
                                        ', i_foncier, v_geom)
                    into v_probjardin;
                    if v_probjardin != 1 Then
                        v_probjardin = 0;
                    end if;
                    end if;

                        else
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
                        end if;

                    
                    
                        INSERT INTO {30}.{31}(code_insee, idu, num_parc, tex, geom, 
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
                                                        prob_jardin) values
                        (v_insee, v_idu, v_num_parc, v_tex, v_geom, 
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
                            v_probjardin
                        );
                        
                        
                    END LOOP;

                RETURN;
                END;
            $BODY$
                LANGUAGE 'plpgsql';



            select {30}.fun_typage('sandbox.socle_temp', 
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

            """.format(self.cb_paimilit.currentText(),
                        self.cb_geobati.currentText(),
                        self.cb_remarquable.currentText(),
                        self.cb_indust.currentText(),
                        self.cb_surf_acti.currentText(),
                        self.cb_triage.currentText(),
                        self.cb_voiefer.currentText(),
                        self.cb_paicom.currentText(),
                        self.cb_cime.currentText(),
                        self.cb_terrainsport.currentText(),
                        self.cb_pai_cult.currentText(),
                        self.cb_rpga.currentText(),
                        self.cb_surf_eau.currentText(),
                        self.cb_paiens.currentText(),
                        self.cb_paisante.currentText(),
                        self.cb_pairel.currentText(),
                        self.cb_pt_eau.currentText(),
                        self.cb_paitransfo.currentText(),
                        self.cb_paitransp.currentText(),
                        self.cb_paisport.currentText(),
                        self.cb_finess.currentText(),
                        self.cb_zoneveget.currentText(),
                        self.cb_res_sport.currentText(),
                        self.cb_tronfluv.currentText(),
                        self.cb_tsurf.currentText(),
                        self.cb_tronroute.currentText(),
                        self.cb_parcellaire.currentText(),
                        self.cb_ff_parcelle.currentText(),
                        self.cb_indif.currentText(),
                        self.cb_schema.currentText(),
                        self.le_destination,
                        self.le_annee
                    )
            )
        cur2.close()
        conn.commit()

        self.lbl_etape.setText(u'Etape 3/4')
        self.pb_avancement.setValue(70)
        print 'Then again'
        cur3 = conn.cursor()

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
                    BEGIN
                        alter table {0}.{1} add column lib4_{2} character varying;
                        For v_socle in Select * from {0}.{1} where idu != 'NC' LOOP

                            if v_socle.to_milit > 20 then
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
                                v_lib4 = 'urbain mixte (habitat/activité tertiaire)';

                            elsif v_socle.to_carrier > 40 then
                                v_code4 = 1311;
                                v_lib4 = 'Carrière';

                            elsif v_socle.to_cime > 40 then
                                v_code4 = 1411;
                                v_lib4 = 'Cimetière';

                            elsif v_socle.to_batire > 50 then
                                v_code4 = 1122;
                                v_lib4 = 'Bâtiment remarquable';

                            elsif v_socle.to_batagri > 20 then
                                v_code4 = 1131;
                                v_lib4 = 'Bâtiment agricole';

                            elsif v_socle.to_serre > 20 then
                                v_code4 = 2121;
                                v_lib4 = 'Serre';

                            elsif v_socle.pre_scol = 1 then
                                v_code4 = 1213;
                                v_lib4 = 'Equipement d''enseignement';

                            elsif v_socle.pre_sante = 1 then
                                v_code4 = 1214;
                                v_lib4 = 'Bâtiment de santé';

                            elsif v_socle.pre_eqadmi = 1 then
                                v_code4 = 1215;
                                v_lib4 = 'Autre équipement local, administration';

                            elsif v_socle.pre_o_nrj = 1 then
                                v_code4 = 1216;
                                v_lib4 = 'Equipement pour eau, assainissement, énergie';

                            elsif v_socle.to_sport > 50 or v_socle.to_loisir > 50 then
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

                            elsif v_socle.prob_jardin in (1,2) then
                                if v_socle.to_agri > 50 then
                                    v_code4 = 2511;
                                    v_lib4 = 'Terre agricole';
                                elsif v_socle.to_veget > 50 then
                                    v_code4 = 3261;
                                    v_lib4 = 'Espace boisé';
                                else
                                    v_code4 = 1412;
                                    v_lib4 = 'parc et jardin';
                                end if;
                            elsif v_socle.to_agri > 50 then
                                v_code4 = 2511;
                                v_lib4 = 'Terre agricole';
                            elsif v_socle.m_fonction = '' and v_socle.to_bati > 50  then
                                v_code4 = 1115;
                                v_lib4 = 'Bâti divers';



                            elsif v_socle.m_fonction = 'ACTIVITE' or v_socle.to_zic > 20 or v_socle.to_comer > 20 or v_socle.to_indust > 20 then
                                if v_socle.to_indust > 20 then
                                    v_code4 = 1212;
                                    v_lib4 = 'Activité autre que tertiaire';
                                elsif v_socle.to_comer > 20 then
                                    v_code4 = 1217;
                                    v_lib4 = 'Surface commerciale';
                                elseif v_socle.to_zic > 20 then
                                    v_code4 = 121;
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

                            update  {0}.{1}
                                Set code4_{2} = v_code4
                                Where gid = v_socle.gid;
                        END LOOP;
                        v_code4 = null;
                        For v_socle in Select * From {0}.{1} where idu != 'NC' and code4_{2} = 3251 LOOP
                            if (st_perimeter(v_socle.geom)/(2 * sqrt(3.14* st_area(v_socle.geom)))) > 2.5 then


                                    select st_union(geom) as geom From {0}.{1} where code4_{2} = 1112 and  st_intersects(st_buffer(v_socle.geom, 2),geom)
                                into v_hab_act_geom1;

                                if v_hab_act_geom1 is not null and v_hab_act_geom1 != '' then
                                    v_code4 = 1222;
                                    v_lib4 = 'Voie desserte habitat';
                                else
                                        select st_union(geom) as geom From {0}.{1} where code4_{2} = 1112 and  st_intersects(st_buffer(v_socle.geom, 2),geom)
                                    into v_hab_act_geom2;

                                    if v_hab_act_geom2 is not null and v_hab_act_geom2 != '' then
                                        v_code4 = 1223;
                                        v_lib4 = 'Voie desserte activité';
                                    elsif v_socle.to_batimaison > 50 then
                                        v_code4 = 1112;
                                        v_lib4 = 'Habitat individuel';
                                    else
                                        v_code4 = 1225;
                                        v_lib4 = 'Chemin-sentier';
                                    end if;
                                end if;
                    
                            else

                                select st_union(geom) as geom From {0}.{1} where code4_{2} in (1112, 1113, 1114) and  st_intersects(st_buffer(v_socle.geom, 5),geom)
                                into v_vac_geom1;

                                if v_vac_geom1 is not null and v_vac_geom1 != '' then
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

                                    if v_vac_geom2 is not null and v_vac_geom2 != '' then
                                        if st_area(st_intersection(st_buffer(v_socle.geom, 5), v_vac_geom1)) > 33 then
                                            v_code4 = 1332;
                                            v_lib4 = 'Terrain vacant - activité';
                                        end if;
                                    end if;
                                end if;
                            end if;

                            update  {0}.{1}
                                Set code4_{2} = v_code4
                                Where gid = v_socle.gid;

                        End loop;
                        v_code4 = null;
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
                """.format(
                        self.cb_schema.currentText(),
                        self.le_destination.text(),
                        self.le_annee.text()
                            )
                )
                
        cur3.close()
        conn.commit()
        self.lbl_etape.setText('Etape 4/4')
        self.pb_avancement.setValue(85)
        print 'Then last'
        self.pb_start.setEnabled(1) 
        self.lbl_etape.setText('Terminé')
        self.pb_avancement.setValue(100)       
        print 'Finally'
