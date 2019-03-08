drop table if exists sandbox.mos_haut_leaon_2005_2015_2018_livrable2;
create table sandbox.mos_haut_2005_2015_2018_livrable2 as 
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
                            id_mos_pdm as id_mos  ,
                            subdi_sirs  ,                                           
                            to_number(code4_2005, '9999') as code4_2005 ,
                            lib4_2005  ,
                            remarque05 as remarque_2005,
                            to_number(code4_2015, '9999') as code4_2015 ,
                            lib4_2015  ,
                            remarque15 as remarque_2015,
                            null::integer as code4_2018 ,
                            null::character varying as lib4_2018  ,
                            null::character varying as remarque_2018,
                            surface_m2 ,
                            perimetre
 From livrables.mos_haut_leon_2005_2015_20150314
)
alter table sandbox.mos_haut_2005_2015_2018_livrable2 add constraint pk_mos_haut_leaon_2005_2015_2018_1 primary key (gid);

create index idx_geom_mos_haut_leon_2005_2015_2018_1 on sandbox.mos_haut_2005_2015_2018_livrable2 using gist(geom)

create index idx_gid_mos_haut_leon_2005_2015_2018_pk on sandbox.mos_haut_2005_2015_2018_livrable2 using btree(gid)

