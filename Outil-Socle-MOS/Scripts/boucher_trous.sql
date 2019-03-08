drop materialized view sandbox.vm_paybrest_temp;																
create materialized view sandbox.vm_paybrest_temp as 																			
with tmp as (
	Select to_milit, to_bati, to_batire, to_batagri, to_serre, to_indust, to_comer, to_zic, to_transp, to_voiefer, 
	to_carrier, to_cime, to_sport, to_loisir, to_agri, to_veget, to_eau, to_route, to_batimaison, pre_scol, pre_sante, pre_eqadmi,
	pre_o_nrj, pre_transp, pre_sploi, prob_jardin, m_fonction, idu, num_parc, tex, section, code_insee, nom_commune, gid, id_mos, 
	subdi_sirs, code4_2005, lib4_2005, remarque_2005, code4_2012, lib4_2012, remarque_2012, code4_2018, lib4_2018, remarque_2018, surface_m2, perimetre, geom
	From production.mos_pays_brest_2005_2012_2018_prod2
	
	UNION
	
	Select to_milit, to_bati, to_batire, to_batagri, to_serre, to_indust, to_comer, to_zic, to_transp, to_voiefer, 
	to_carrier, to_cime, to_sport, to_loisir, to_agri, to_veget, to_eau, to_route, to_batimai as to_batimaison, pre_scol, pre_sante, pre_eqadmi,
	pre_o_nrj, pre_transp, pre_sploi, prob_jardi as prob_jardin, m_fonction, idu, num_parc, tex, section, code_insee, nom_commun as nom_commune, gid, id_mos, 
	subdi_sirs, code4_2005, lib4_2005, remarque_2 as remarque_2005, code4_2012, lib4_2012, remarque_1 as remarque_2012, code4_2018, lib4_2018, remarque_3 as remarque_2018, 
	surface_m2, perimetre, geom
	From sandbox.polygone
	
)
Select row_number() over() as fid, * from tmp;
																			


drop materialized view sandbox.vm_test_diff_paybrest;
Create materialized view sandbox.vm_test_diff_paybrest as
with tmp as (
  select b.gid, st_union(a.geom) as geom
  from sandbox.communes_pays_brest_bd_topo_2017_temp b 
  join production.mos_pays_brest_2005_2012_2018_prod2 a on st_intersects(a.geom, b.geom)
  group by b.gid
) select b.gid, (st_dump(st_collectionextract(st_difference(b.geom,coalesce(t.geom, 'GEOMETRYCOLLECTION EMPTY'::geometry)), 3))).geom::geometry(Polygon, 2154) as newgeom
from sandbox.communes_pays_brest_bd_topo_2017_temp b left join tmp t on b.gid = t.gid;
																	


drop materialized view if exists sandbox.vm_paybrest_final_temp;																
create materialized view sandbox.vm_paybrest_final_temp as 																			
with tmp as (
	Select to_milit, to_bati, to_batire, to_batagri, to_serre, to_indust, to_comer, to_zic, to_transp, to_voiefer, 
	to_carrier, to_cime, to_sport, to_loisir, to_agri, to_veget, to_eau, to_route, to_batimaison, pre_scol, pre_sante, pre_eqadmi,
	pre_o_nrj, pre_transp, pre_sploi, prob_jardin, m_fonction, idu, num_parc, tex, section, code_insee, nom_commune, gid, id_mos, 
	subdi_sirs, code4_2005, lib4_2005, remarque_2005, code4_2012, lib4_2012, remarque_2012, code4_2018, lib4_2018, remarque_2018, surface_m2, perimetre, geom
	From sandbox.vm_paybrest_temp
	
	UNION
	
	Select null as to_milit, null as to_bati, null as to_batire, null as to_batagri, null as to_serre, null as to_indust, null as to_comer, to_zic, to_transp, to_voiefer, 
	null as to_carrier, null as to_cime, null as to_sport, null as to_loisir, null as to_agri, null as to_veget, null as to_eau, null as to_route, null as to_batimaison, null as pre_scol, null as pre_sante, null as pre_eqadmi,
	null as pre_o_nrj, null as pre_transp, null as pre_sploi, null as prob_jardi as prob_jardin, null as m_fonction, 'NC' as idu, 'NC' as num_parc, 'NC' as tex, section, code_insee, nom_commun as nom_commune, gid, id_mos, 
	subdi_sirs, 3251 as code4_2005, lib4_2005, remarque_2 as remarque_2005, 3251 as code4_2012, lib4_2012, remarque_1 as remarque_2012, 3251 as code4_2018, lib4_2018, remarque_3 as remarque_2018, 
	surface_m2, perimetre, geom
	From sandbox.vm_test_diff_paybrest
	
)
Select row_number() over() as fid, * from tmp;
																										


