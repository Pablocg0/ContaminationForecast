

SELECT 	date_part('year', fecha) as year_gt, 
		date_part('month', fecha) as month_gt,
		date_part('day', fecha) as day_gt,
		CASE WHEN max(val) > 155 THEN 1 ELSE 0 END as val_gt,
		max(val) as ppm_gt, id_est
	FROM cont_otres
	WHERE 
		date_part('year', fecha)  = 2017 		                 
	GROUP BY
		1,2,3, id_est
	ORDER BY 1,2,3