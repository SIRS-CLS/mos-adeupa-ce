	--1/ Récupérartion des parcelles hors subdivision
Drop table if exists vm_parc_h_subd cascade;
Create temporary table vm_parc_h_subd as 
Select row_number() over() as gid, * From (
Select (st_dump(st_difference(parc.geom, st_union(sp.geom)))).geom::geometry(Polygon, 2154) as geom, idu, 'zzz'::character varying as tex   
From cadastre_edigeo.parcelle_info parc
Join cadastre_edigeo.geo_subdfisc sp on St_Within(St_PointOnSurface(sp.geom), parc.geom)
Group by parc.geom, idu)tt;



	--3/ Union de toutes les parcelles
Drop table if exists v_temp_parc_subparc cascade;
Create temporary table v_temp_parc_subparc As 
	Select ROW_NUMBER() OVER() as unique_id, *
	From(
		(Select (st_dump(st_collectionextract(gs.geom,3))).geom::geometry(Polygon,2154) as geom, 
				pi.idu as idu, 
				c29.code_insee as code_insee, 
				pi.idu || coalesce(gs.tex, 'zzz') as num_parc, 
				coalesce(gs.tex, 'zzz') as tex
			From cadastre_edigeo.geo_subdfisc gs
			Join sandbox.emprise_d29 c29 on St_within(St_PointOnSurface(gs.geom), c29.geom)
			Join cadastre_edigeo.parcelle_info pi on St_Within(St_PointOnSurface(gs.geom), pi.geom)
		)
	UNION
		(Select (st_dump(st_collectionextract(pi2.geom, 3))).geom::geometry(Polygon,2154) as geom, 
				pi2.idu as idu, 
				c292.code_insee as code_insee, 
				pi2.idu as num_parc, 
				null as tex  
		From cadastre_edigeo.parcelle_info pi2
		Join sandbox.emprise_d29 c292 on St_within(St_PointOnSurface(pi2.geom), c292.geom) 
		Where ogc_fid not in (Select distinct pi3.ogc_fid 
								From cadastre_edigeo.parcelle_info pi3
								Join cadastre_edigeo.geo_subdfisc gs2 on St_Within(St_PointOnSurface(gs2.geom), pi3.geom))
		)
	UNION
		(Select (st_dump(st_collectionextract(vmhs.geom,3))).geom::geometry(Polygon,2154) as geom, 
				vmhs.idu as idu, 
				c292.code_insee as code_insee, 
				vmhs.idu || vmhs.tex as num_parc, 
				vmhs.tex  
		From vm_parc_h_subd vmhs
		Join sandbox.emprise_d29 c292 on St_within(St_PointOnSurface(vmhs.geom), c292.geom)) 
	) tt;

	--4/ Découpage des parcelles empiétant sur plusieurs communes
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
			Join sandbox.emprise_d29 bdpc on St_intersects(vm.geom, bdpc.geom)
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
					Join sandbox.emprise_d29 bdpc on St_intersects(vm.geom, bdpc.geom)
				)tt
			)tt2
			Group By unique_id Having count(unique_id) = 1);


		--4.1/ Récupération des données coupées à remplacer dans le socle sans autre modification
Drop table if exists vm_temp_exclusion;
Create temporary table vm_temp_exclusion as 
Select vmt2.uq_gid, vmt2.unique_id, vmt2.code_insee, vmps.idu, vmps.num_parc, vmps.tex, vmt2.geom::geometry(polygon, 2154)
From vm_cut_on_com vmt2
Join v_temp_parc_subparc vmps on vmps.unique_id = vmt2.unique_id  
Where uq_gid in (Select uq_gid 
					From vm_cut_on_com vm, 
						sandbox.emprise_d29 bdpc
					Where st_within(st_pointonsurface(vm.geom), bdpc.geom)
					AND vm.code_insee = bdpc.code_insee );


	--4.2/Récupération des données coupées à fusionner ou éliminer de la couche
Drop table if exists vm_temp_exclus;
Create temporary table vm_temp_exclus as 
Select  vmcoc.uq_gid, vmcoc.unique_id, vmcoc.code_insee, vmps.idu, vmps.num_parc, vmps.tex, vmcoc.geom::geometry(Polygon, 2154), st_area(vmcoc.geom) as surf_area, dd.code_insee as new_insee
From vm_cut_on_com vmcoc
Join v_temp_parc_subparc vmps on vmps.unique_id = vmcoc.unique_id
Join sandbox.emprise_d29 dd on St_within(st_pointonsurface(vmcoc.geom), dd.geom )
Where vmcoc.uq_gid not in (Select uq_gid From vm_temp_exclusion);


	--4.3/ Nouvelle couche de parcelles avec première correction
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

	--5/ Fusion des entités micro 
Create or replace function sandbox.fun_fusion(i_origine text, i_fuse text) 
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
		drop table if exists sandbox.t_eliminated cascade;
		Create table sandbox.t_eliminated(
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
					INSERT INTO sandbox.t_eliminated (geom, code_insee, idu, num_parc, tex, geom_check, old_id) values
						(v_geomFusion, v_inseeO, v_iduO, v_numpO, v_texO, FALSE, v_idfusion);
				END IF;
			END IF;
		End Loop;
		Select count(*) From sandbox.t_eliminated INTO cpt;
		While cpt2 < cpt LOOP
			Select gid, idu, code_insee, num_parc, tex, old_id From sandbox.t_eliminated Where geom_check = False
				INTO v_eliId, v_eliIdu, v_eliInsee, v_eliNp, v_eliTex, v_eliOld;
			Select (st_dump(st_collectionextract(st_union(geom),3))).geom::geometry(Polygon, 2154) as geom
			From sandbox.t_eliminated
			Where idu = v_eliIdu INTO v_lastGeom;
			INSERT INTO sandbox.t_eliminated (geom, code_insee, idu, num_parc, tex, geom_check, old_id) values
						(v_lastGeom, v_eliInsee, v_eliIdu, v_eliNp, v_eliTex, TRUE, v_eliOld);
			Delete From sandbox.t_eliminated 
				Where idu = v_eliIdu AND geom_check = FALSE;
			cpt2 = cpt2 +1;
			Select count(*) From sandbox.t_eliminated INTO cpt;
		END LOOP;
		Return;
	END;
$BODY$
	LANGUAGE 'plpgsql';

select sandbox.fun_fusion('vm_temp_parc', 'vm_temp_exclus');



	--5.1/ Création du socle cadastré v1 : parcelles mises à jours avec les éliminations
Drop table if exists vm_socle_c;
Create temporary table vm_socle_c as 
Select ROW_NUMBER() over() as gid, * FROM( 
(Select gid as old_gid, code_insee, idu, num_parc, tex, geom::geometry(polygon,2154)
From  sandbox.t_eliminated
)
UNION 
(
Select unique_id as old_gid, code_insee, idu, num_parc, tex, geom
From vm_temp_parc
Where unique_id not in (Select old_id From sandbox.t_eliminated)
))tt;




	-- 6/ Création du socle non cadastré
Drop table if exists vm_socle_nc cascade;
Create temporary table vm_socle_nc as 
Select ROW_NUMBER() over() as gid, * FROM( 
	Select (st_dump(st_collectionextract(st_difference(com.geom, st_union(so.geom)),3))).geom::geometry(Polygon, 2154) as geom, com.code_insee
	From vm_socle_c so, sandbox.emprise_d29 com
	group by com.geom, com.code_insee
) tt;

	--6.0/ Récupération du contour BD_TOPO , création d'un nouveau socle non cadastré
Drop table if exists vm_nc_lito cascade;
Create temporary table vm_nc_lito as
Select ROW_NUMBER() OVEr() as gid, *
From (
	Select (st_dump(
				st_collectionextract(
					st_intersection(st_union(vmtt.geom),vmnc.geom),3))).geom::geometry(polygon,2154) as geom, vmnc.code_insee
	From vm_socle_nc vmnc, sandbox.emprise_d29_bdtopo vmtt
	Group By vmnc.geom, vmnc.code_insee
)tt;


--Routes primaire	
Drop table if exists vm_primaire;
Create temporary table vm_primaire as
Select ROW_NUMBER() OVEr() as gid, st_union(geom)::geometry(Polygon,2154) as geom, nature
From (
(Select st_buffer(rp.geom, rp.largeur/2, 'endcap=square join=round')::geometry(Polygon,2154) as geom, 'primaire'::character varying as nature
From ref_ign.route_primaire rp, sandbox.emprise_d29 com
Where st_intersects(rp.geom, com.geom)
)
)tt
Where st_area(tt.geom) > 10
Group By nature;
	
--Routes secondaires
Drop table if exists vm_secondaire;
Create temporary table vm_secondaire as
Select ROW_NUMBER() OVEr() as gid,  geom, nature
From (select st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
	From (
		Select st_buffer(rs.geom, largeur/2, 'endcap=square join=round')::geometry(Polygon,2154) as geom, 'secondaire'::character varying as nature
		From ref_ign.route_secondaire rs, sandbox.emprise_d29 com
		Where st_intersects(rs.geom, com.geom) 
		Group by rs.largeur/2, rs.geom
	)tt
Where st_area(tt.geom) > 10
Group by nature) tt2;

--Chemins
Drop table if exists vm_chemin;
Create temporary table vm_chemin as
Select ROW_NUMBER() OVEr() as gid,  geom, nature
From (select st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
	From (
		Select st_buffer(c.geom, 5.0/2)::geometry(Polygon,2154) as geom, 'chemin'::character varying as nature
		From ref_ign.chemin c, sandbox.emprise_d29 com
		Where st_intersects(c.geom, com.geom)
	)tt
Where st_area(tt.geom) > 10
group By nature)tt2 ;

Drop table if exists vm_veget;
Create temporary table vm_veget as
Select ROW_NUMBER() OVEr() as gid, st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
From (
		Select (st_dump(st_collectionextract(st_safe_intersection(vz.geom, vmnc.geom),3))).geom::geometry(Polygon, 2154) as geom, 'veget'::character varying as nature
  		From ref_ign.zone_vegetation vz
  		Join vm_nc_lito vmnc on st_intersects(vz.geom, vmnc.geom)
	) tt2
Where st_area(tt2.geom) > 400
Group by nature;


Drop table if exists vm_hydro;
Create temporary table vm_hydro as
Select ROW_NUMBER() OVEr() as gid, st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
From (
		Select (st_dump(st_collectionextract(st_safe_intersection(st_force2D(se.geom), vmnc.geom),3))).geom::geometry(Polygon, 2154), 'hydro'::character varying as nature
 		From ref_ign.surface_eau se
 		Join vm_nc_lito vmnc on st_intersects(se.geom, vmnc.geom)
	) tt2
Where st_area(tt2.geom) > 10
Group by nature;


Drop table if exists vm_rpga;
Create temporary table vm_rpga as
Select ROW_NUMBER() OVER() as gid, st_union(geom)::geometry(MultiPolygon,2154) as geom, nature
From (
	Select (st_dump(st_collectionextract(st_safe_intersection(rpga.geom, vmnc.geom),3))).geom::geometry(Polygon, 2154), 'agricole'::character varying as nature
	 From data_exo.rpga_29_2015 rpga
	 Join vm_nc_lito vmnc on st_intersects(rpga.geom, vmnc.geom)
)tt
Where st_area(tt.geom) > 200
Group by nature;



drop table if exists sandbox.t_socle_nc;
Create table sandbox.t_socle_nc (
	gid serial,
	geom geometry(Polygon,2154),
	nature character varying,
	type_ajout character varying,
	Constraint pk_socle_nc primary key (gid)
);
create index idx_socle_nc_geom on sandbox.t_socle_nc using gist(geom);
	

insert into sandbox.t_socle_nc (geom, nature, type_ajout) 
	select (st_dump(st_collectionextract(st_safe_intersection(vmnc.geom, ipli.geom),3))).geom::geometry(Polygon, 2154), 
				ipli.libelle,
				'plage'
			From data_exo.ipli_n_occ_sol_lit_region ipli
			Join vm_nc_lito vmnc on st_intersects(ipli.geom, vmnc.geom)
			Where libelle in ('Plage', 'Rochers, falaise');


insert into sandbox.t_socle_nc (geom, nature, type_ajout) 
	select (st_dump(st_collectionextract(st_safe_difference(st_safe_intersection(vmnc.geom, ipli.geom), st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
				ipli.nature,
				'route1'
			From vm_primaire ipli, sandbox.t_socle_nc vsocle, vm_nc_lito vmnc
			Where st_intersects(ipli.geom, vmnc.geom)
			Group by vmnc.geom, ipli.geom, ipli.nature;


insert into sandbox.t_socle_nc (geom, nature, type_ajout) 
	select (st_dump(st_collectionextract(st_safe_difference(st_safe_intersection(vmnc.geom, ipli.geom), st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
				ipli.nature,
				'secondaire'
			From vm_secondaire ipli, sandbox.t_socle_nc vsocle, vm_nc_lito vmnc
	 		Where st_intersects(ipli.geom, vmnc.geom)
			Group by vmnc.geom, ipli.geom, ipli.nature;

delete from sandbox.t_socle_nc where st_area(geom) < 10;

insert into sandbox.t_socle_nc (geom, nature, type_ajout) 
	select (st_dump(st_collectionextract(st_safe_difference(st_safe_intersection(vmnc.geom, ipli.geom), st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
				ipli.nature,
				'chemin'
			From vm_chemin ipli, sandbox.t_socle_nc vsocle, vm_nc_lito vmnc
	 		Where st_intersects(ipli.geom, vmnc.geom)
			Group by vmnc.geom, ipli.geom, ipli.nature;


delete from sandbox.t_socle_nc where st_area(geom) < 10;

insert into sandbox.t_socle_nc (geom, nature, type_ajout) 
	select (st_dump(st_collectionextract(st_safe_difference(st_safe_intersection(vmnc.geom, ipli.geom), st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
				ipli.nature,
				'hydro'
			From vm_hydro ipli, sandbox.t_socle_nc vsocle, vm_nc_lito vmnc
	 		Where st_intersects(ipli.geom, vmnc.geom)
			Group by vmnc.geom, ipli.geom, ipli.nature;


delete from sandbox.t_socle_nc where st_area(geom) < 10;

insert into sandbox.t_socle_nc (geom, nature, type_ajout) 
	select (st_dump(st_collectionextract(st_safe_difference(ipli.geom, st_union(vsocle.geom)),3))).geom::geometry(Polygon, 2154), 
				ipli.nature,
				'rpga'
			From vm_rpga ipli, sandbox.t_socle_nc vsocle, vm_nc_lito vmnc
	 		Where st_intersects(ipli.geom, vmnc.geom)
			Group by vmnc.geom, ipli.geom, ipli.nature;


delete from sandbox.t_socle_nc where st_area(geom) < 10;


delete from sandbox.t_socle_nc where st_area(geom) < 10;

Drop table if exists vm_temp_veget;
Create temporary table vm_temp_veget as
Select ROW_number() over() as gid, st_union(geom), * 
From (
	Select st_safe_difference(ipli.geom, st_union(vsocle.geom)) as geom, ipli.nature
	From vm_veget ipli, sandbox.t_socle_nc vsocle
	Where st_area(st_intersection(ipli.geom, vsocle.geom)) > 150
	Group by ipli.geom, ipli.nature
	)tt
group by tt.geom, tt.nature ;



insert into sandbox.t_socle_nc (geom, nature, type_ajout) 
	select (st_dump(st_collectionextract(ipli.geom,3))).geom::geometry(Polygon, 2154), 
				ipli.nature,
				'veget'
			From vm_temp_veget ipli, sandbox.t_socle_nc vsocle
			Group by ipli.geom, ipli.nature;

delete from sandbox.t_socle_nc where st_area(geom) < 10;

--Création de l'union du cadastre et de la partie connue du non cadastré
Drop table if exists vm_scv1;
Create temporary table vm_scv1 as
	Select ROW_NUMBER() OVER() as gid, *
	FROM (
		(Select code_insee, idu, num_parc, tex, geom
		From vm_socle_c)
		UNION
		(Select 'NC','NC', 'NC', nature, geom
		From sandbox.t_socle_nc)
		)tt;



	--Création de la partie non cadastré
Drop table if exists vm_nc_v2 cascade;
Create temporary table vm_nc_v2 as 
Select ROW_NUMBER() over() as gid, * FROM( 
	Select (st_dump(st_collectionextract(st_difference(com.geom, st_union(st_buffer(so.geom, 0.0001))),3))).geom::geometry(Polygon, 2154) as geom, com.code_insee
	From vm_scv1 so, sandbox.emprise_d29 com
	Where st_intersects(com.geom, so.geom)
	group by com.geom, com.code_insee
) tt;




	--7/ Création du socle final
Drop table if exists sandbox.socle;
Create table sandbox.socle as 
	Select ROW_NUMBER() OVER() as gid, *
	FROM (
		(Select code_insee, idu, num_parc, tex, geom
		From vm_scv1)
		UNION
		(Select vmnc.code_insee,'NC', 'NC', 'NC', (st_dump(st_collectionextract(st_intersection(st_union(vmtt.geom), vmnc.geom), 3))).geom::geometry(polygon,2154) as geom
		From vm_nc_v2 vmnc, sandbox.emprise_d29_bdtopo vmtt
		Group by vmnc.code_insee, vmnc.geom)
		)tt;
create index idx_socleF_geom on sandbox.socle using gist(geom);



/*Drop table if exists sandbox.vm_nc_sub; 
Create temporary table sandbox.vm_nc_sub as
Select ROW_NUMBER() OVER() gid, *
FROM (
	Select st_subdivide(geom, 100)::geometry(polygon,2154) geom, code_insee
	From vm_nc_v2
)tt

*/








