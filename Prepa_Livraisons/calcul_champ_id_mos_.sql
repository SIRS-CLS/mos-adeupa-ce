UPDATE production.mos_pays_brest_2005_2012_2018_prod3
SET num_parc = 'NC'
WHERE (num_parc IS NULL OR num_parc = '') AND (idu IS NULL OR idu = '');

UPDATE production.mos_pays_brest_2005_2012_2018_prod3
Set section = tex, tex = section where tex in (Select distinct tex from cadastre_edigeo_29.geo_section);


UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5) , 'NC', fid::varchar) WHERE num_parc = 'NC' ;

-- UPDATE production.mos_pays_brest_2005_2012_2018_prod3 cf
-- SET (code_insee, nom_commune) = (foo.code_insee, foo.nom_com)
-- FROM ( SELECT couchepiao.fid, couchecom.code_insee, couchecom.nom_com FROM production.mos_pays_brest_2005_2012_2018_prod3 couchepiao, data_exo.communes_bd_parcellaire_d29_2017  couchecom
-- 	   WHERE ST_Intersects(couchecom.geom, couchepiao.geom)  AND (couchepiao.code_insee LIKE '29' || '%' )
-- 	 ) AS foo
-- WHERE  id_mos LIKE '29' || '%' AND cf.fid = foo.fid;


SELECT fid, idu, num_parc, subdi_sirs FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE num_parc <> 'NC' and subdi_sirs <> '' and subdi_sirs <> right(num_parc,1) AND
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;

SELECT fid, idu, num_parc, substring(num_parc from 6 for 2), subdi_sirs FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE num_parc <> 'NC' and subdi_sirs <> '' and subdi_sirs <> right(num_parc,1) AND
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;

SELECT fid, idu, num_parc, substring(num_parc from 6 for 2), subdi_sirs FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE num_parc <> 'NC' and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;

--recalcul du champ section à partir du champ num_parc (184103 parcelles)
UPDATE production.mos_pays_brest_2005_2012_2018_prod3
SET section = substring(num_parc from 6 for 2)
WHERE num_parc <> 'NC' and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;



--sélection des parcelles NC (11798)
SELECT fid, idu, num_parc, subdi_sirs, id_mos FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE num_parc = 'NC' and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;
--recalcul id_mos pour parcelle NC
UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5) , 'NC', fid::varchar) WHERE num_parc = 'NC' and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;


--sélection des parcelles qui ont une subdi_sirs = dernier caractère du champ num_parc et un caractère espace avant la section qui ne fait a priori qu'un seul caractère (1656 parcelles)
SELECT fid, idu, num_parc, subdi_sirs, CONCAT(LEFT(code_insee,5),'0000',substring(num_parc from 7 for 20))  FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE (subdi_sirs <> '' and subdi_sirs is not NULL) and subdi_sirs = right(num_parc,1) and substring(num_parc from 6 for 1) = ' 'and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
; 
--recalcul id_mos pour les 1656 parcelles précédentes
UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5),'0000',substring(num_parc from 7 for 20))WHERE subdi_sirs <> '' and subdi_sirs = right(num_parc,1) and substring(num_parc from 6 for 1) = ' 'and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
; 


--sélection des parcelles qui ont une subdi_sirs = dernier caractère du champ num_parc et pas de caractère espace dans num_parc  fait a priori 2 caractères ( 9076 parcelles)
SELECT fid, idu, num_parc, subdi_sirs, CONCAT(LEFT(code_insee,5),'000',substring(num_parc from 6 for 20))  FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE (subdi_sirs <> '' and subdi_sirs is not NULL) and subdi_sirs = right(num_parc,1) and substring(num_parc from 6 for 1) <> ' 'and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;
--recalcul id_mos pour les 9076 parcelles précédentes
UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5),'000',substring(num_parc from 6 for 20)) WHERE (subdi_sirs <> '' and subdi_sirs is not NULL) and subdi_sirs = right(num_parc,1) and substring(num_parc from 6 for 1) <> ' 'and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;


--sélection des parcelles cadastrées (donc hors NC) qui ont une subdi_sirs et subdi_sirs <> du dernier caractère du champ num_parc et pas de caractère espace dans num_parc qui fait a priori 2 caractères ( 4921 parcelles)
SELECT fid, idu, num_parc, subdi_sirs, CONCAT(LEFT(code_insee,5),'000',substring(num_parc from 6 for 6), subdi_sirs)  FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE num_parc <> 'NC' and (subdi_sirs <> '' and subdi_sirs is not NULL) and subdi_sirs <> right(num_parc,1) and substring(num_parc from 6 for 1) <> ' 'and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;
--recalcul id_mos pour les 4921 parcelles précédentes
UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5),'000',substring(num_parc from 6 for 6), subdi_sirs) WHERE num_parc <> 'NC' and (subdi_sirs <> '' and subdi_sirs is not NULL) and subdi_sirs <> right(num_parc,1) and substring(num_parc from 6 for 1) <> ' 'and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;


--sélection des parcelles cadastrées (donc hors NC) qui ont une subdi_sirs et subdi_sirs <> du dernier caractère du champ num_parc et un caractère espace dans num_parc qui fait a priori 1 caractère ( 1887 parcelles)
SELECT fid, idu, section, num_parc, subdi_sirs, CONCAT(LEFT(code_insee,5),'0000',substring(num_parc from 7 for 5), subdi_sirs)  FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE num_parc <> 'NC' and (subdi_sirs <> '' and subdi_sirs is not NULL) and subdi_sirs <> right(num_parc,1) and substring(num_parc from 6 for 1) = ' 'and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;
--recalcul id_mos pour les 1887 parcelles précédentes
UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5),'0000',substring(num_parc from 7 for 5), subdi_sirs) WHERE num_parc <> 'NC' and (subdi_sirs <> '' and subdi_sirs is not NULL) and subdi_sirs <> right(num_parc,1) and substring(num_parc from 6 for 1) = ' 'and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;


--pas de subdi_sirs

--avec une section d'un seul caractère
--45001 parcelles
SELECT fid, idu, section, num_parc, subdi_sirs, CONCAT(LEFT(code_insee,5),'0000',substring(num_parc from 7 for 10))  FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE num_parc <> 'NC' and (subdi_sirs = '' or subdi_sirs is NULL) and substring(num_parc from 6 for 1) = ' ' and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;
UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5),'0000',substring(num_parc from 7 for 10))WHERE num_parc <> 'NC' and (subdi_sirs = '' or subdi_sirs is NULL) and substring(num_parc from 6 for 1) = ' ' and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;
-- avec une section à 2 caractères
--121562  parcelles
SELECT fid, idu, section, num_parc, subdi_sirs, CONCAT(LEFT(code_insee,5),'000',substring(num_parc from 6 for 10))  FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE num_parc <> 'NC' and (subdi_sirs = '' or subdi_sirs is NULL) and substring(num_parc from 6 for 1) <> ' ' and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;
UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5),'000',substring(num_parc from 6 for 10))  WHERE num_parc <> 'NC' and (subdi_sirs = '' or subdi_sirs is NULL) and substring(num_parc from 6 for 1) <> ' ' and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
;






SELECT fid, idu, section, num_parc, subdi_sirs, code_insee, id_mos FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE substring(id_mos from 1 for 5) <> code_insee and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
 and num_parc <> 'NC';

UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5),substring(id_mos from 6 for 20))  WHERE substring(id_mos from 1 for 5) <> code_insee and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
 and num_parc <> 'NC';


SELECT fid, idu, section, num_parc, subdi_sirs, code_insee, id_mos FROM production.mos_pays_brest_2005_2012_2018_prod3 WHERE substring(id_mos from 1 for 5) <> code_insee and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
 and num_parc = 'NC';

 UPDATE production.mos_pays_brest_2005_2012_2018_prod3 SET id_mos = CONCAT(LEFT(code_insee,5),substring(id_mos from 6 for 20))  WHERE substring(id_mos from 1 for 5) <> code_insee and
 (code_insee = '29011' OR code_insee = '29019' OR code_insee = '29061' OR code_insee = '29069' OR code_insee = '29189' OR code_insee = '29212' OR code_insee = '29235' OR code_insee = '29017' OR code_insee = '29040' OR code_insee = '29076' OR code_insee ='29098' OR code_insee = '29099' OR code_insee = '29109' OR code_insee = '29112' OR code_insee = '29119' OR code_insee = '29130' OR code_insee = '29149' OR code_insee = '29177' OR code_insee = '29178' OR code_insee = '29190' OR code_insee = '29201' OR code_insee = '29208' OR code_insee = '29221' OR code_insee = '29260' OR code_insee = '29282' OR code_insee = '29299')
 and num_parc = 'NC';


 UPDATE production.mos_pays_brest_2005_2012_2018_prod3 cf
SET (code_insee, nom_commune) = (foo.code_insee, foo.nom_com)
FROM ( SELECT couchepiao.fid, couchecom.code_insee, couchecom.nom_com FROM production.mos_pays_brest_2005_2012_2018_prod3 couchepiao, data_exo.communes_bd_parcellaire_d29_2017  couchecom
	   WHERE ST_Intersects(couchecom.geom, couchepiao.geom)  AND ST_Intersects(couchecom.geom, couchepiao.geom) AND ST_Contains(couchecom.geom, ST_PointOnSurface(couchepiao.geom))
	 ) AS foo
WHERE  (foo.code_insee = '29011' OR foo.code_insee = '29019' OR foo.code_insee = '29061' OR foo.code_insee = '29069' OR foo.code_insee = '29189' OR foo.code_insee = '29212' OR foo.code_insee = '29235' OR foo.code_insee = '29017' OR foo.code_insee = '29040' OR foo.code_insee = '29076' OR foo.code_insee ='29098' OR foo.code_insee = '29099' OR foo.code_insee = '29109' OR foo.code_insee = '29112' OR foo.code_insee = '29119' OR foo.code_insee = '29130' OR foo.code_insee = '29149' OR foo.code_insee = '29177' OR foo.code_insee = '29178' OR foo.code_insee = '29190' OR foo.code_insee = '29201' OR foo.code_insee = '29208' OR foo.code_insee = '29221' OR foo.code_insee = '29260' OR foo.code_insee = '29282' OR foo.code_insee = '29299')
  AND cf.fid = foo.fid;