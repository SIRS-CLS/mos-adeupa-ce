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

		v_hab_act_geom1 geometry;--Code 1112
		v_hab_act_geom2 geometry;--Code 121, 1211, 1212, et 1217

		v_vac_geom1 geometry;--Code 1112, 1113 et 1114
		v_vac_geom2 geometry;--Code 121, 1211, 1212, 1217

		v_sec_geom1 geometry;--Code 1114
		v_sec_geom2 geometry;--Code 1211,1212,1217
		v_sec_geom3 geometry;--Code 1112,1113
	BEGIN

		For v_socle in Select * from sandbox.socle_c_mos where idu != 'NC' LOOP

			if v_socle.to_milit > 20 then
				v_code4 = 1110;

			elsif v_socle.m_fonction = 'MAISON' or v_socle.m_fonction = 'DEPENDANCE' then
				if v_socle.to_voiefer > 5 then
					v_code4 = 1221;
				elsif v_socle.to_agri > 50 Then 
					v_code4 = 2511;
				else
					v_code4 = 1112;
				end if;

			elsif v_socle.m_fonction = 'APPARTEMENT' then
				v_code4 = 1113;

			elsif v_socle.m_fonction = 'MIXTE' then
				v_code4 = 1114;

			elsif v_socle.to_carrier > 40 then
				v_code4 = 1311;

			elsif v_socle.to_cime > 40 then
				v_code4 = 1411;

			elsif v_socle.to_batire > 50 then
				v_code4 = 1122;

			elsif v_socle.to_batagri > 20 then
				v_code4 = 1131;

			elsif v_socle.to_serre > 20 then
				v_code4 = 2121;

			elsif v_socle.pre_scol = 1 then
				v_code4 = 1213;

			elsif v_socle.pre_sante = 1 then
				v_code4 = 1214;

			elsif v_socle.pre_eqadmi = 1 then
				v_code4 = 1215;

			elsif v_socle.pre_o_nrj = 1 then
				v_code4 = 1216;

			elsif v_socle.to_sport > 50 or v_socle.to_loisir > 50 then
				if v_socle.to_bati > 50 then
					v_code4 = 1422;
				else
					v_code4 = 1421;
				end if;
			
			elsif v_socle.pre_sploi = 2 then
				v_code4 = 1422;

			elsif v_socle.prob_jardin in (1,2) then
				if v_socle.to_agri > 50 then
					v_code4 = 2511;
				elsif v_socle.to_veget > 50 then
					v_code4 = 3261;
				else
					v_code4 = 1412;
				end if;
			elsif v_socle.to_agri > 50 then
				v_code4 = 2511;
			elsif v_socle.m_fonction = '' and v_socle.to_bati > 50  then
				v_code4 = 1115;



			elsif v_socle.m_fonction = 'ACTIVITE' or v_socle.to_zic > 20 or v_socle.to_comer > 20 or v_socle.to_indust > 20 then
				if v_socle.to_indust > 20 then
					v_code4 = 1212;
				elsif v_socle.to_comer > 20 then
					v_code4 = 1217;
				elseif v_socle.to_zic > 20 then
					v_code4 = 121;
				else 
					v_code4 = 1115;
				end if;

			elsif v_socle.to_voiefer > 5 or v_socle.pre_transp = 1 then
				v_code4 = 1221;

			elsif v_socle.to_route > 50 then
				v_code4 = 1222;

			elsif v_socle.to_eau > 50 then
				v_code4	= 5121;


			else 
				v_code4 = 3251;

			end if; 

			update  sandbox.socle_c_mos
				Set code4_2018 = v_code4
				Where gid = v_socle.gid;
		END LOOP;
		v_code4 = null;
		For v_socle in Select * From sandbox.socle_c_mos where idu != 'NC' and code4_2018 = 3251 LOOP
			if (st_perimeter(v_socle.geom)/(2 * sqrt(3.14* st_area(v_socle.geom)))) > 2.5 then


					select st_union(geom) as geom From sandbox.socle_c_mos where code4_2018 = 1112 and  st_intersects(st_buffer(v_socle.geom, 2),geom)
				into v_hab_act_geom1;

				if v_hab_act_geom1 is not null and v_hab_act_geom1 != '' then
					v_code4 = 1222;
				else
						select st_union(geom) as geom From sandbox.socle_c_mos where code4_2018 = 1112 and  st_intersects(st_buffer(v_socle.geom, 2),geom)
					into v_hab_act_geom2;

					if v_hab_act_geom2 is not null and v_hab_act_geom2 != '' then
						v_code4 = 1223;
					elsif v_socle.to_batimaison > 50 then
						v_code4 = 1112;
					else
						v_code4 = 1225;
					end if;
				end if;
	
			else

				select st_union(geom) as geom From sandbox.socle_c_mos where code4_2018 in (1112, 1113, 1114) and  st_intersects(st_buffer(v_socle.geom, 5),geom)
				into v_vac_geom1;

				if v_vac_geom1 is not null and v_vac_geom1 != '' then
					if st_area(st_intersection(st_buffer(v_socle.geom, 5), v_vac_geom1)) > 33 then
						if v_socle.to_batimaison > 50 Then
							v_code4 = 1112;
						else
							v_code4 = 1331;
						end if;
					end if;
				else
						select st_union(geom) as geom From sandbox.socle_c_mos where code4_2018 in (121, 1211, 1212, 1217) and  st_intersects(st_buffer(v_socle.geom, 5),geom)
					into v_vac_geom2;

					if v_vac_geom2 is not null and v_vac_geom2 != '' then
						if st_area(st_intersection(st_buffer(v_socle.geom, 5), v_vac_geom1)) > 33 then
							v_code4 = 1332;
						end if;
					end if;
				end if;
			end if;

			update  sandbox.socle_c_mos
				Set code4_2018 = v_code4
				Where gid = v_socle.gid;

		End loop;
		v_code4 = null;
		For v_socle_nc in Select * from sandbox.socle_c_mos where idu = 'NC' LOOP

			if v_socle_nc.tex like 'Plage' then
				v_code4 = 3311;

			elsif v_socle_nc.tex like 'Rochers, falaise' then
				v_code4 = 3321;

			elsif v_socle_nc.tex = 'primaire' then
				v_code4 = 1221;

			elsif v_socle_nc.tex = 'secondaire' then
				For v_secondaire_nc in Select st_union(st_buffer(geom,5)) as geom, code4_2018 From sandbox.socle_c_mos 
																							Where code4_2018 in (1114, 1211, 1212, 1217, 1112, 1113) 
																							and st_intersects(v_socle_nc.geom, st_buffer(geom, 5))
																							Group by code4_2018 Loop
					if v_secondaire_nc.code4_2018 = 1114 then
						v_code4 = 1224;
					elsif v_secondaire_nc.code4_2018 in (1211, 1212, 1217) then
						v_code4 = 1223;
					else
						v_code4 = 1222;
					end if;
				end loop;
				if v_code4 is null then
					v_code4 = 1221;
				end if;

			elsif v_socle_nc.tex = 'chemin' then
				v_code4 = 1225;

			elsif v_socle_nc.tex = 'hydro' then
				v_code4 = 5131;

			elsif v_socle_nc.tex = 'agricole' then
				v_code4 = 2511;

			elsif v_socle_nc.tex = 'veget' then
				v_code4 = 3261;

			else 
				v_code4 = 1226;

			end if;

			update  sandbox.socle_c_mos
				Set code4_2018 = v_code4
				Where gid = v_socle_nc.gid;

		END LOOP;

	END;
$BODY$;
