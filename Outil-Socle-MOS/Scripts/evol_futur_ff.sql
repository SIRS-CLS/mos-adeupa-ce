Create or replace function public.fun_evol_t0_t1(i_socle_c text,
                                                i_foncier text
                                                )
                    Returns void AS
                    --Fonction de calcul des aménagements présents sur les parcelles
                    --Met en correlation de nombreuses données recouvrant ou non une parcelle en indiquant la surface de recouvrement, ou si une présence est constaté
                $BODY$
                    DECLARE                      
                        v_socle_total record; --Données du socle parcourues
                        v_mfonction character varying; --Type de bâtiment sur la parcelle
                        v_gravelius integer; -- Identification de la forme de la parcelle
                    BEGIN
                            --Récupération des données à corréler sur l'emprise
                           
                            execute format ('
                                    drop table if exists vm_i_foncier;
                                    create temporary table vm_i_foncier as 
                                    select cegb.* 
                                    from %1$s cegb 
                                    join %2$s emp on st_intersects(cegb.geomloc, emp.geom)
                                    Where tlocdomin != ''AUCUN LOCAL'';
                                    Create index idx_vm_i_foncier on vm_i_foncier using gist(geomloc);
                                    ', i_foncier, i_socle_c);

                                                                                          
                            --Parcours de toutes les parcelles pour affecter les calcul de présence qui lui sont propre
                            -- Les calculs sont stockés dans des variables puis insérés en fin de boucle dans la table
                        For v_socle_total IN execute format('Select * From %1$s sc;', i_socle_c) LOOP
                            execute format ('Select tlocdomin
                                                        From %1$s pm
                                                        Where st_intersects(pm.geomloc, ''%2$s'')
                                                        order by tlocdomin desc
                                                    ', 'vm_i_foncier', v_socle_total.geom)
                                into v_mfonction;

                            if (st_perimeter(v_socle_total.geom)/(2 * sqrt(3.14* st_area(v_socle_total.geom)))) > 3 then
                                execute format('
                                    update %1$s 
                                        set code4_2018 = code4_2012,
                                            lib4_2018 =  lib4_2012
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);

                            elsif v_mfonction = 'MAISON' or v_mfonction = 'DEPENDANCE' then
                                if v_socle_total.code4_2012 = 1412 then
                                    execute format('
                                        update %1$s 
                                            set code4_2018 = code4_2012,
                                                lib4_2018 =  lib4_2012
                                                where gid = %2$s
                                    ',i_socle_c, v_socle_total.gid);
                                else
                                    execute format('
                                        update %1$s 
                                            set code4_2018 = 1112,
                                                lib4_2018 =  ''Habitat individuel''
                                                where gid = %2$s
                                    ',i_socle_c, v_socle_total.gid);
                                end if;

                            elsif v_mfonction = 'APPARTEMENT' then
                                execute format('
                                    update %1$s 
                                        set code4_2018 = 1113,
                                            lib4_2018 =  ''Habitat collectif''
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);

                            elsif v_mfonction = 'MIXTE' then 
                                execute format('
                                    update %1$s 
                                        set code4_2018 = 1114,
                                            lib4_2018 =  ''Urbain mixte (habitat/activité tertiaire)''
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);

                            else 
                                execute format('
                                    update %1$s 
                                        set code4_2018 = code4_2012,
                                            lib4_2018 =  lib4_2012
                                            where gid = %2$s
                                ',i_socle_c, v_socle_total.gid);
                            end if;
                            
                        END LOOP;

                    RETURN;
                    END;
                $BODY$
                    LANGUAGE 'plpgsql';



                select public.fun_evol_t0_t1('sandbox.mos_morlaix_2005_2012_2018_prod2', 'data_exo.communes_morlaix_communaute_bd_parcellaire_2017' ,'ff_d29_2017.d29_2017_pnb10_parcelle');



                        update sandbox.mos_morlaix_2005_2012_2018 x 
                        set nom_commune = nom_com
                        From data_exo.communes_morlaix_communaute_bd_parcellaire_2017 y where x.code_insee = y.code_insee