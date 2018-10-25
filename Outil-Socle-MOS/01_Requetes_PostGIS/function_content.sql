Create or replace function sandbox.fun_typage(i_socle_c text, 
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

		Drop table if exists sandbox.socle_c_mos;
		Create table sandbox.socle_c_mos (
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
			code4_2018 integer,
			constraint pk_socle_mos PRIMARY KEY (gid)
																				
		);
		Create index idx_socle_geom on sandbox.socle_c_mos using gist(geom);
		
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

		
		
			INSERT INTO sandbox.socle_c_mos(code_insee, idu, num_parc, tex, geom, 
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



select sandbox.fun_typage('sandbox.socle2_clean', 
						'ref_ign.pai_administratif_militaire', 
						'cadastre_edigeo.geo_batiment', 
						'ref_ign.bati_remarquable', 
						'ref_ign.bati_industirel', 
						'ref_ign.surface_activite', 
						'ref_ign.aire_triage',
						'ref_ign.troncon_voie_ferree',
						'ref_ign.pai_industirel_commercial',
						'ref_ign.cimetiere',
						'ref_ign.terrain_sport',
						'ref_ign.pai_culture_loisirs',
						'data_exo.rpga_29_2015',
						'ref_ign.surface_eau',
						'ref_ign.pai_science_enseignement',
						'ref_ign.pai_sante',
						'ref_ign.pai_religieux',
						'ref_ign.point_eau',
						'ref_ign.poste_transformation',
						'ref_ign.pai_transport',
						'ref_ign.pai_sport',
						'data_exo.extraction_finess_dp29',
						'ref_ign.zone_vegetation',
						'data_exo.equipements_sportifs_res_dep_29',
						'cadastre_edigeo.geo_tronfluv',
						'cadastre_edigeo.geo_tsurf',
						'ref_ign.route_secondaire',
						'cadastre_edigeo.geo_tronroute',
						'sandbox.emprise_d29',
						'ff_d29_2015.d29_2015_pnb10_parcelle',
						'ref_ign.bati_indifferencie'
						);

