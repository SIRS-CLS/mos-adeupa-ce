-- pour créer des couches par millésimes, il suffit de faire une copie de la couche générées et
-- de supprimer les champs code4_xxxx, liv4_xxxx, et remarque_xxxx des années xxxx inutiles


---------------------------------------------------------------------
--
--                            GUINGAMP
--
---------------------------------------------------------------------


--correction du champ tex
UPDATE production.mos_guimgamp_2008_2018_prod
Set section = tex, tex = section where tex in (Select distinct tex from cadastre_edigeo_22.geo_section);


--- Recalcul de l'identifiant id_mos pour les polygones hors cadastre
UPDATE production.mos_guimgamp_2008_2018_prod SET id_mos = CONCAT(code_insee , 'NC', gid::varchar) WHERE num_parc = 'NC' ;
-- Recalcul de l'identifiant id_mos pour inclure la subivision SIRS
UPDATE production.mos_guimgamp_2008_2018_prod SET id_mos = CONCAT(LEFT(code_insee,2), idu, subdi_sirs) WHERE num_parc <> 'NC' AND subdi_sirs <> '' ;


DROP TABLE IF EXISTS livrables.livr_mos_guimgamp_2008_2018_ca_guingamp_paimpol;

CREATE TABLE  livrables.livr_mos_guimgamp_2008_2018_ca_guingamp_paimpol AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comeromer,
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  ocs.remarque_2008, 
  ocs.code4_2018,
  ocs.remarque_2018
 
 
FROM production.mos_guimgamp_2008_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'CA Guingamp-Paimpol Armor-Argoat Agglomération'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comeromer,
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  ocs.remarque_2008, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comeromer as to_comer,
  NULL::integer as to_zic, 
  NULL::integer as to_transp, 
  NULL::integer as to_voiefer, 
  NULL::integer as to_carrier, 
  NULL::integer as to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc22.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  nomenclature08.libelle_n4 as lib4_2008,
  ocs.remarque_2008, 
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature08 ON ocs.code4_2008 = nomenclature08.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d22_2017 bdparc22 ON ocs.code_insee = bdparc22.code_insee


;



DROP TABLE IF EXISTS livrables.livr_mos_guimgamp_2008_2018_cc_leff_armor;

CREATE TABLE  livrables.livr_mos_guimgamp_2008_2018_cc_leff_armor AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comeromer,
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  ocs.remarque_2008, 
  ocs.code4_2018,
  ocs.remarque_2018
 
 
FROM production.mos_guimgamp_2008_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'CC Leff Armor Communauté'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comeromer,
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  ocs.remarque_2008, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comeromer as to_comer,
  NULL::integer as to_zic, 
  NULL::integer as to_transp, 
  NULL::integer as to_voiefer, 
  NULL::integer as to_carrier, 
  NULL::integer as to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc22.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  nomenclature08.libelle_n4 as lib4_2008,
  ocs.remarque_2008, 
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature08 ON ocs.code4_2008 = nomenclature08.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d22_2017 bdparc22 ON ocs.code_insee = bdparc22.code_insee


;



---------------------------------------------------------------------
--
--                            LANNION
--
--
---------------------------------------------------------------------

--correction du champ tex
UPDATE production.mos_lannion_2008_2015_2018_prod
Set section = tex, tex = section where tex in (Select distinct tex from cadastre_edigeo_22.geo_section);


--- Recalcul de l'identifiant id_mos pour les polygones hors cadastre
UPDATE production.mos_lannion_2008_2015_2018_prod SET id_mos = CONCAT(code_insee , 'NC', gid::varchar) WHERE num_parc = 'NC' ;
-- Recalcul de l'identifiant id_mos pour inclure la subivision SIRS
UPDATE production.mos_lannion_2008_2015_2018_prod SET id_mos = CONCAT(LEFT(code_insee,2), idu, subdi_sirs) WHERE num_parc <> 'NC' AND subdi_sirs <> '' ;


DROP TABLE IF EXISTS livrables.livr_mos_lannion_2008_2015_2018;

CREATE TABLE  livrables.livr_mos_lannion_2008_2015_2018 AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  ocs.remarque_2008,
  ocs.code4_2015,
  ocs.remarque_2015, 
  ocs.code4_2018,
  ocs.remarque_2018
 
 
FROM production.mos_lannion_2008_2015_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  ocs.remarque_2008, 
  ocs.code4_2015,
  ocs.remarque_2015,
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire::integer,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  NULL::integer as to_zic, 
  NULL::integer as to_transp, 
  NULL::integer as to_voiefer, 
  NULL::integer as to_carrier, 
  NULL::integer as to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc22.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2008,
  nomenclature08.libelle_n4 as lib4_2008,
  ocs.remarque_2008,
  ocs.code4_2015,
  nomenclature15.libelle_n4 as lib4_2015,
  ocs.remarque_2015,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature08 ON ocs.code4_2008 = nomenclature08.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature15 ON ocs.code4_2015 = nomenclature15.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d22_2017 bdparc22 ON ocs.code_insee = bdparc22.code_insee


;




---------------------------------------------------------------------
--
--                            MORLAIX
--
--
---------------------------------------------------------------------



--correction du champ tex
UPDATE production.mos_morlaix_2005_2015_2018_prod
Set section = tex, tex = section where tex in (Select distinct tex from cadastre_edigeo_29.geo_section);

ALTER TABLE production.mos_morlaix_2005_2015_2018_prod ALTER COLUMN code_insee SET DATA TYPE VARCHAR(255);
ALTER TABLE production.mos_morlaix_2005_2015_2018_prod ALTER COLUMN subdi_sirs SET DATA TYPE VARCHAR(255);
ALTER TABLE production.mos_morlaix_2005_2015_2018_prod ALTER COLUMN idu SET DATA TYPE VARCHAR(255);
ALTER TABLE production.mos_morlaix_2005_2015_2018_prod ALTER COLUMN id_mos SET DATA TYPE VARCHAR(255);


--- Recalcul de l'identifiant id_mos pour les polygones hors cadastre
UPDATE production.mos_morlaix_2005_2015_2018_prod SET id_mos = CONCAT(LEFT(code_insee,5) , 'NC', gid::varchar) WHERE num_parc = 'NC' ;
-- Recalcul de l'identifiant id_mos pour inclure la subivision SIRS
UPDATE production.mos_morlaix_2005_2015_2018_prod SET id_mos = CONCAT(LEFT(code_insee,2), idu, subdi_sirs) WHERE num_parc <> 'NC' AND subdi_sirs <> '' ;







DROP TABLE IF EXISTS livrables.livr_mos_morlaix_2005_2015_2018;

CREATE TABLE  livrables.livr_mos_morlaix_2005_2015_2018 AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005, 
  ocs.code4_2015,
  ocs.remarque_2015, 
  ocs.code4_2018,
  ocs.remarque_2018


 
 
FROM production.mos_morlaix_2005_2015_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005,
  ocs.code4_2015,
  ocs.remarque_2015, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc29.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  nomenclature05.libelle_n4 as lib4_2005,
  ocs.remarque_2005,
  ocs.code4_2015,
  nomenclature15.libelle_n4 as lib4_2015,
  ocs.remarque_2015,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature05 ON ocs.code4_2005 = nomenclature05.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature15 ON ocs.code4_2015 = nomenclature15.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d29_2017 bdparc29 ON ocs.code_insee = bdparc29.code_insee


;




---------------------------------------------------------------------
--
--                            BREST
--
--
---------------------------------------------------------------------


--correction du champ tex
UPDATE production.mos_pays_brest_2005_2012_2018_prod
Set section = tex, tex = section where tex in (Select distinct tex from cadastre_edigeo_29.geo_section);

ALTER TABLE production.mos_pays_brest_2005_2012_2018_prod ALTER COLUMN code_insee SET DATA TYPE VARCHAR(255);
ALTER TABLE production.mos_pays_brest_2005_2012_2018_prod ALTER COLUMN subdi_sirs SET DATA TYPE VARCHAR(255);
ALTER TABLE production.mos_pays_brest_2005_2012_2018_prod ALTER COLUMN idu SET DATA TYPE VARCHAR(255);
ALTER TABLE production.mos_pays_brest_2005_2012_2018_prod ALTER COLUMN id_mos SET DATA TYPE VARCHAR(255);


--- Recalcul de l'identifiant id_mos pour les polygones hors cadastre
UPDATE production.mos_pays_brest_2005_2012_2018_prod SET id_mos = CONCAT(LEFT(code_insee,5) , 'NC', gid::varchar) WHERE num_parc = 'NC' ;
-- Recalcul de l'identifiant id_mos pour inclure la subivision SIRS
UPDATE production.mos_pays_brest_2005_2012_2018_prod SET id_mos = CONCAT(LEFT(code_insee,2), idu, subdi_sirs) WHERE num_parc <> 'NC' AND subdi_sirs <> '' ;







DROP TABLE IF EXISTS livrables.livr_mos_pays_brest_2005_2012_2018_cc_presquile_crozon;

CREATE TABLE  livrables.livr_mos_pays_brest_2005_2012_2018_cc_presquile_crozon AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005, 
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018


 
 
FROM production.mos_pays_brest_2005_2012_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'CC Presqu''île de Crozon - Aulne Maritime'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc29.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  nomenclature05.libelle_n4 as lib4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  nomenclature12.libelle_n4 as lib4_2012,
  ocs.remarque_2012,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature05 ON ocs.code4_2005 = nomenclature05.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature12 ON ocs.code4_2012 = nomenclature12.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d29_2017 bdparc29 ON ocs.code_insee = bdparc29.code_insee


;




DROP TABLE IF EXISTS livrables.livr_mos_pays_brest_2005_2012_2018_cc_pays_landerneau;

CREATE TABLE  livrables.livr_mos_pays_brest_2005_2012_2018_cc_pays_landerneau AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005, 
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018


 
 
FROM production.mos_pays_brest_2005_2012_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'CC du Pays de Landerneau-Daoulas'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc29.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  nomenclature05.libelle_n4 as lib4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  nomenclature12.libelle_n4 as lib4_2012,
  ocs.remarque_2012,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature05 ON ocs.code4_2005 = nomenclature05.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature12 ON ocs.code4_2012 = nomenclature12.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d29_2017 bdparc29 ON ocs.code_insee = bdparc29.code_insee


;



DROP TABLE IF EXISTS livrables.livr_mos_pays_brest_2005_2012_2018_cc_pays_abers;

CREATE TABLE  livrables.livr_mos_pays_brest_2005_2012_2018_cc_pays_abers AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005, 
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018


 
 
FROM production.mos_pays_brest_2005_2012_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'CC du Pays des Abers'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc29.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  nomenclature05.libelle_n4 as lib4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  nomenclature12.libelle_n4 as lib4_2012,
  ocs.remarque_2012,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature05 ON ocs.code4_2005 = nomenclature05.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature12 ON ocs.code4_2012 = nomenclature12.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d29_2017 bdparc29 ON ocs.code_insee = bdparc29.code_insee


;



DROP TABLE IF EXISTS livrables.livr_mos_pays_brest_2005_2012_2018_cc_pays_iroise;

CREATE TABLE  livrables.livr_mos_pays_brest_2005_2012_2018_cc_pays_iroise AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005, 
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018


 
 
FROM production.mos_pays_brest_2005_2012_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'CC du Pays d''Iroise'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc29.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  nomenclature05.libelle_n4 as lib4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  nomenclature12.libelle_n4 as lib4_2012,
  ocs.remarque_2012,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature05 ON ocs.code4_2005 = nomenclature05.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature12 ON ocs.code4_2012 = nomenclature12.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d29_2017 bdparc29 ON ocs.code_insee = bdparc29.code_insee


;



DROP TABLE IF EXISTS livrables.livr_mos_pays_brest_2005_2012_2018_cc_communaute_lesneven;

CREATE TABLE  livrables.livr_mos_pays_brest_2005_2012_2018_cc_communaute_lesneven AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005, 
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018


 
 
FROM production.mos_pays_brest_2005_2012_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'CC Communauté Lesneven Côte des Légendes'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc29.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  nomenclature05.libelle_n4 as lib4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  nomenclature12.libelle_n4 as lib4_2012,
  ocs.remarque_2012,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature05 ON ocs.code4_2005 = nomenclature05.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature12 ON ocs.code4_2012 = nomenclature12.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d29_2017 bdparc29 ON ocs.code_insee = bdparc29.code_insee


;



DROP TABLE IF EXISTS livrables.livr_mos_pays_brest_2005_2012_2018_brest_metropole;

CREATE TABLE  livrables.livr_mos_pays_brest_2005_2012_2018_brest_metropole AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005, 
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018


 
 
FROM production.mos_pays_brest_2005_2012_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'Brest Métropole'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc29.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  nomenclature05.libelle_n4 as lib4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  nomenclature12.libelle_n4 as lib4_2012,
  ocs.remarque_2012,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature05 ON ocs.code4_2005 = nomenclature05.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature12 ON ocs.code4_2012 = nomenclature12.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d29_2017 bdparc29 ON ocs.code_insee = bdparc29.code_insee


;



DROP TABLE IF EXISTS livrables.livr_mos_pays_brest_2005_2012_2018_cc_pleyben;

CREATE TABLE  livrables.livr_mos_pays_brest_2005_2012_2018_cc_pleyben AS

WITH 
 sel AS(

SELECT 
   
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005, 
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018


 
 
FROM production.mos_pays_brest_2005_2012_2018_prod ocs, data_exo.ccca_communes_adeupa com
WHERE com.code_insee = ocs.code_insee and com.ccca = 'CC Pleyben-Châteaulin-Porzay'
GROUP BY
  ocs.geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  ocs.remarque_2012, 
  ocs.code4_2018,
  ocs.remarque_2018
)
SELECT
  ROW_NUMBER() OVER()::integer as gid,
  ocs.geom::geometry(Polygon,2154) AS geom,
  ocs.to_milit,
  ocs.to_bati,
  ocs.to_batire,
  ocs.to_batagri,
  ocs.to_serre, 
  ocs.to_indust,
  ocs.to_comer,
  ocs.to_zic, 
  ocs.to_transp, 
  ocs.to_voiefer, 
  ocs.to_carrier, 
  ocs.to_cime, 
  ocs.to_sport,
  ocs.to_loisir,
  ocs.to_agri,
  ocs.to_veget, 
  ocs.to_eau,
  ocs.to_route,
  ocs.to_batimaison,
  ocs.pre_scol,
  ocs.pre_sante,
  ocs.pre_eqadmi, 
  ocs.pre_o_nrj,
  ocs.pre_transp,
  ocs.pre_sploi,
  ocs.prob_jardin,
  ocs.m_fonction,
  ocs.idu,
  ocs.num_parc,
  ocs.tex,
  ocs.section,
  ocs.code_insee, 
  bdparc29.nom_com as nom_commune,
  ocs.id_mos,
  ocs.subdi_sirs,
  ocs.code4_2005,
  nomenclature05.libelle_n4 as lib4_2005,
  ocs.remarque_2005,
  ocs.code4_2012,
  nomenclature12.libelle_n4 as lib4_2012,
  ocs.remarque_2012,
  ocs.code4_2018,
  nomenclature18.libelle_n4 as lib4_2018,
  ocs.remarque_2018,
  ST_Area(ocs.geom) as surface_m2,
  ST_Perimeter(ocs.geom) as perimetre
FROM
  sel as ocs
 
LEFT JOIN production.nomenclature_niv4 nomenclature05 ON ocs.code4_2005 = nomenclature05.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature12 ON ocs.code4_2012 = nomenclature12.code_n4
LEFT JOIN production.nomenclature_niv4 nomenclature18 ON ocs.code4_2018 = nomenclature18.code_n4
LEFT JOIN data_exo.communes_bd_parcellaire_d29_2017 bdparc29 ON ocs.code_insee = bdparc29.code_insee


;


