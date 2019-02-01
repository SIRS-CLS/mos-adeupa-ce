drop table sandbox.mos_lannion_2005_2015_livrable2;
create table sandbox.mos_lannion_2005_2015_livrable2 as 
(Select to_defense as to_milit ,
                            to_bati,
                            to_batirem as to_batire ,
                            to_batagri , 
                            to_serre , 
                            to_indust ,
                            to_comer ,
                            to_zic ,
                            t_trans as to_transp ,
                            to_vferree as to_voiefer ,
                            to_carrier ,
                            to_cime ,
                            to_tsport as to_sport ,
                            to_loisirs as to_loisir ,
                            r_rpga as to_agri ,
                            ratio_ve_r as to_veget ,
                            to_eau ,
                            null::double precision as to_route ,
                            null::double precision as to_batimaison ,
                            id_scol as pre_scol ,
                            id_sante as pre_sante ,
                            id_eqadmin as pre_eqadmi ,
                            id_eau_nrj as pre_o_nrj ,
                            null::integer as pre_transp ,
                            id_splo as pre_sploi ,
                            null::integer as prob_jardin ,
                            null::character varying as m_fonction  ,
                            idu  ,
                            idpar_subd as num_parc  ,
                            tex  ,
                            section  ,
                            dc as code_insee  ,
                            null::character varying as nom_commune  ,
                            gid ,
                            geom ,
                            id_mos_ltc as id_mos  ,
                            subdi_sirs  ,                                           
                            to_number(code4_2008, '9999') as code4_2008 ,
                            lib4_2008  ,
                            remarque08 as remarque_2008,
 				to_number(code4_2015, '9999') as code4_2015 ,
                            lib4_2015  ,
                            remarque15 as remarque_2015,
 				null::integer as code4_2018 ,
                            null::character varying as lib4_2018  ,
                            null::character varying as remarque_2018,
                            surface_m2 ,
                            perimetre
 From livrables.mos_morlaix_communaute_2005_2015
)
alter table sandbox.mos_morlaix_2005_2015_2018 add constraint pk_mos_morlaix_2005_2015_2018_1 primary key (gid);

create index idx_mos_morlaix_2005_2015_2018_1 on sandbox.mos_morlaix_2005_2015_2018 using gist(geom)
create index idx_mos_morlaix_2005_2015_2018_pk on sandbox.mos_morlaix_2005_2015_2018 using gist(geom)


       PG:dbname=adeupa host=192.168.1.88 port=5432 user=adeupa_user password=sirs59


       SPATIAL_INDEX=YES,SRID=2154