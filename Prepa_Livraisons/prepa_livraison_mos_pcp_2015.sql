--- Recalcul de l'identifiant id_mos_pcp pour inclure la subivision SIRS
UPDATE production.mos_pcp_2015 SET id_mos_pcp = id_mos_pcp + subdi_sirs WHERE type = 'CADASTRE' AND subdi_sirs <> '';
UPDATE production.mos_pcp_2015 SET id_mos_pcp = id_mos_pcp + subdi_sirs WHERE type = 'HORS_CADASTRE' AND subdi_sirs <> '';

-- Reqête ToDo : pour les enregistrements dont le champs revise = 1, ajouter dans remarque la mention "Attribution révisée par PIAO". Attention aux infos déjà exsitantes (ie. Sous divisions zzz ajoutée)

---------- Génération du livrable 2015 pour le MOS PCP--------------
-- Il s'agit simplement d'une récupération des champs existants dans la table de production, mais en les renommant correctement et en les placant dans un ordre "plus naturel"



DROP MATERIALIZED VIEW IF EXISTS sandbox.livr_mos_pcp_2015;

CREATE MATERIALIZED VIEW sandbox.livr_mos_pcp_2015 AS

SELECT
  ocs.gid AS gid,
  ocs.geom::geometry(MultiPolygon,2154) AS geom,
  
  ocs.idu AS idu,
  ocs.id_subdi AS subdi,
  ocs.parcelle_i AS id_parsubd,
  ocs.insee AS code_insee,
  ocs.insee_nom AS nom_insee,
  ocs.type AS type_parc,
  ocs.ind_comp AS ind_comp,
  
  ocs.ap AS m_ap,
  ocs.at AS m_at,
  ocs.ca AS m_ca,
  ocs.cb AS m_cb,
  ocs.cd AS m_cd,
  ocs.ch AS m_ch,
  ocs.cm AS m_cm,
  ocs.dc AS m_dc,
  ocs.de AS m_de,
  ocs.lc AS m_lc,
  ocs.ma AS m_ma,
  ocs.me AS m_me,
  ocs.mp AS m_mp,
  ocs.pp AS m_pp,
  ocs.u AS m_u,
  ocs.ue AS m_ue,
  ocs.ug AS m_ug,
  ocs.us AS m_us,
  ocs.l_fonction AS m_fonction,
 
  ocs.to_agri AS to_agri,
  ocs.to_veg AS to_veg,
  ocs.to_eau AS to_eau,
  ocs.to_bati AS to_bati,
  ocs.prob_jardi AS prob_jardin,
  ocs.to_milit AS to_milit,
  ocs.to_batre AS to_batire,
  ocs.id_eqadmin AS pre_eqadmin,
  ocs.to_batagri AS to_batagri,
  ocs.to_serre AS to_serre,
  ocs.to_zic AS to_zic,
  ocs.to_indust AS to_indust,
  ocs.to_comer AS to_comer,
  ocs.to_carrier AS to_carrier,
  ocs.to_cime AS to_cime,
  ocs.id_scol AS pre_scol,
  ocs.id_sante AS pre_sante,
  ocs.to_sport AS to_sport,
  ocs.to_loisirs AS to_loisirs,
  ocs.id_splo AS pre_sploi,
  ocs.id_eau_nrj AS pre_o_nrj,
  --ocs.to_trans AS to_transp,
  ocs.prob_trans AS pre_transp,
  ocs.to_voifer AS to_voiefer,
  ocs.to_routelo AS to_routelo,
  ocs.r_habitat AS r_habitat,
  ocs.r_activite AS r_activite,
  ocs.t_major AS t_major,  

  ocs.id_mos_pcp AS id_mos_pcp,
  ocs.subdi_sirs AS subdi_sirs,  
  ocs.code4_2015 AS code4_2015,
  nomenclature.libelle_n4 AS lib4_2015,
  ocs.remark_sir AS remarque15,
  
  ST_Area(ocs.geom) AS surface_m2,
  ST_Perimeter(ocs.geom) AS perimetre

FROM
  production.mos_pcp_2015 AS ocs
LEFT JOIN production.nomenclature_niv4 nomenclature ON ocs.code4_2015 = nomenclature.code_n4;


COMMENT ON MATERIALIZED VIEW sandbox.livr_mos_pcp_2015
    IS 'Version livrable pour le millésime 2015';
