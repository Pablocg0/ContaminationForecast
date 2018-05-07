SELECT 	'Buena' as indice, sum(CASE WHEN val_gt = 0 THEN 1 ELSE 0 END) as N,
	sum(CASE WHEN val_gt = 1 THEN 1 ELSE 0 END) as P,
	sum(CASE WHEN val_gt = 1 and val_fo = 1 THEN 1 ELSE 0 END) as TP,
	sum(CASE WHEN val_gt = 0 and val_fo = 0 THEN 1 ELSE 0 END) as TN,
	sum(CASE WHEN val_gt = 1 and val_fo = 0 THEN 1 ELSE 0 END) as FP,
	sum(CASE WHEN val_gt = 0 and val_fo = 1 THEN 1 ELSE 0 END) as FN
FROM 
	(SELECT 	date_part('year', fecha) as y_gt, 
		date_part('month', fecha) as m_gt,
		date_part('day', fecha) as d_gt,		
		CASE WHEN max(val) < 50 THEN 1 ELSE 0 END as val_gt,
		max(val) as ppm_gt
	FROM cont_otres
	WHERE 
		date_part('year', fecha)  = 2017 
		/*AND id_est IN ('ATI', 'BJU','CUA','LPR','MER','PED','TLA','UIZ','XAL') */
		AND id_est IN (EST) 
	GROUP BY
		1,2,3 ) as gt,
	
	(SELECT date_part('year', fecha) as y_fo, 
		date_part('month', fecha) as m_fo,
		date_part('day', fecha) as d_fo,
		CASE WHEN max(val) < 50 THEN 1 ELSE 0 END as val_fo,
		max(val) as ppm_fo
	FROM forecast_otres
	WHERE 
		date_part('year', fecha)  = 2017 		
		AND id_est IN ('ATI', 'BJU','CUA','LPR','MER','PED','TLA','UIZ','XAL') 
		/*AND id_est IN ('ATI', 'BJU','CUA','LPR','MER','PED','TLA','UIZ','XAL') */
		AND id_est IN (EST) 
	GROUP BY
		1,2,3 ) as fo

WHERE 
	y_gt = y_fo AND
	m_gt = m_fo AND
	d_gt = d_fo
