	--Création des routes à récupérer
	
	drop materialized view if exists sandbox.vm_chemin;
	create materialized view sandbox.vm_chemin as
	Select ROW_NUMBER() OVEr() as gid, *
	From (
	Select st_buffer(c.geom, 5.5/2, 'endcap=flat join=round')::geometry(Polygon,2154) as geom, 'chemin'::character varying as nature
	From ref_ign.chemin c, data_exo.bdparcellaire_communes_d29 com
	Where com.code_insee in ('29259', '29239', '29273') and st_intersects(c.geom, com.geom)
	)tt;
	
	drop materialized view if exists sandbox.vm_primaire;
	create materialized view sandbox.vm_primaire as
	Select ROW_NUMBER() OVEr() as gid, *
	From (
	(Select st_buffer(rp.geom, rp.largeur/2, 'endcap=flat join=round')::geometry(Polygon,2154) as geom, 'primaire'::character varying as nature
	From ref_ign.route_primaire rp, data_exo.bdparcellaire_communes_d29 com
	Where com.code_insee in ('29259', '29239', '29273') and st_intersects(rp.geom, com.geom)
	Group by rp.largeur/2, rp.geom)	
	)tt;
	
	
	drop materialized view if exists sandbox.vm_secondaire;
	create materialized view sandbox.vm_secondaire as
	Select ROW_NUMBER() OVEr() as gid, *
	From (
	Select st_buffer(rs.geom, largeur/2, 'endcap=flat join=round')::geometry(Polygon,2154) as geom, 'secondaire'::character varying as nature
	From ref_ign.route_secondaire rs, data_exo.bdparcellaire_communes_d29 com
	Where com.code_insee in ('29259', '29239', '29273') and st_intersects(rs.geom, com.geom) 
	Group by rs.largeur/2, rs.geom
	)tt;
	
	
	select * from sandbox.vm_secondaire
	
	
	
drop materialized view if exists sandbox.vm_route_temp cascade;
Create materialized view sandbox.vm_route_temp as
Select ROW_NUMBER() OVEr() as gid, *
From (
	(Select geom, nature
	 From sandbox.vm_primaire
	 )
	UNION
	(Select (st_dump(st_collectionextract(st_safe_difference(sec.geom, st_union(prim.geom)),3))).geom::geometry(Polygon,2154) as geom, sec.nature
		From sandbox.vm_secondaire sec, sandbox.vm_primaire prim
		Group By sec.geom, sec.nature)
	) tt;

drop materialized view if exists sandbox.vm_route cascade;
Create materialized view sandbox.vm_route as
Select ROW_NUMBER() OVEr() as gid, *
From (
	(Select geom, nature
	 From sandbox.vm_route_temp
	 )
	UNION
	(Select (st_dump(st_collectionextract(st_safe_difference(sec.geom, st_union(prim.geom)),3))).geom::geometry(Polygon,2154) as geom, sec.nature
		From sandbox.vm_chemin sec, sandbox.vm_route_temp prim
	Group By sec.geom, sec.nature)
	) tt;



drop materialized view if exists sandbox.vm_rpga;
Create materialized view sandbox.vm_rpga as
Select ROW_NUMBER() OVER() as gid, *
From (
	Select (st_dump(st_collectionextract(st_safe_intersection(rpga.geom, vmnc.geom),3))).geom::geometry(Polygon, 2154), 'agricole'::character varying as nature
	 From data_exo.rpga_29_2015 rpga
	 Join sandbox.vm_socle_nc vmnc on st_intersects(rpga.geom, vmnc.geom)
)tt;

drop materialized view if exists sandbox.vm_ipli;
Create materialized view sandbox.vm_ipli as
Select ROW_NUMBER() OVER() as gid, *
From
	(Select (st_dump(st_collectionextract(st_safe_intersection(ipli.geom, vmnc.geom),3))).geom::geometry(Polygon, 2154), libelle as nature
	 From data_exo.ipli_n_occ_sol_lit_region ipli
	 Join sandbox.vm_socle_nc vmnc on st_intersects(ipli.geom, vmnc.geom)
	 Where libelle in ('Plage', 'Rochers, falaise')
	)tt;
	
drop materialized view if exists sandbox.vm_hydro;
Create materialized view sandbox.vm_hydro as
Select ROW_NUMBER() OVER() as gid, *
From
	(Select (st_dump(st_collectionextract(st_safe_intersection(st_force2D(se.geom), vmnc.geom),3))).geom::geometry(Polygon, 2154), 'hydro'::character varying as nature
	 From ref_ign.surface_eau se
	 Join sandbox.vm_socle_nc vmnc on st_intersects(se.geom, vmnc.geom)
	 )tt;

drop materialized view if exists sandbox.vm_veget;
Create materialized view sandbox.vm_veget as
Select ROW_NUMBER() OVER() as gid, *
From
	 (Select (st_dump(st_collectionextract(st_safe_intersection(vz.geom, vmnc.geom),3))).geom::geometry(Polygon, 2154), 'veget'::character varying as nature
	  From ref_ign.zone_vegetation vz
	  Join sandbox.vm_socle_nc vmnc on st_intersects(vz.geom, vmnc.geom)
	 ) tt
	 