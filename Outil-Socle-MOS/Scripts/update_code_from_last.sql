update sandbox.mos_payb_prod3 x 
set code_insee = y.code_insee,
	idu = y.idu,
	num_parc = y.num_parc,
	tex = y.tex,
	section = y.section,
	id_mos = y.id_mos,
	subdi_sirs = y.subdi_sirs,
	code4_2005 = y.code4_2005,
	remarque_2005 = y.remarque_2005,
	code4_2012 = y.code4_2012,
	remarque_2012 = y.remarque_2012,
	code4_2018 = y.code4_2018
From sandbox.pays_brest_prod2_crozon y 
where st_intersects(st_pointonsurface(x.geom), y.geom)
AND x.code4_2005 != y.code4_2005
AND x.code4_2012 != y.code4_2012
AND (to_char(x.code4_2012, '9999') != '11%%' and to_char(y.code4_2012, '9999') != '122%');