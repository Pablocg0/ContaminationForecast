SELECT count(aval) as tot, sum(sval), sum(aval)/count(aval) as mae 
FROM 
(	SELECT abs(gt.val - fo.val) as aval, (gt.val - fo.val)^2 as sval
	FROM forecast_otres as fo, cont_otres as gt
	WHERE
	  date_part('year', fo.fecha) = 2017 AND
	  date_part('year', gt.fecha) = 2017 AND
	  fo.id_est = gt.id_est  AND
	  date_part('year', fo.fecha)  = date_part('year', gt.fecha) AND
	  date_part('month', fo.fecha)  = date_part('month', gt.fecha) AND
	  date_part('day', fo.fecha)  = date_part('day', gt.fecha) AND
	  date_part('hour', fo.fecha)  = date_part('hour', gt.fecha) 
	 ) as internal
