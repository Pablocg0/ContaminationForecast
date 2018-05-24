SELECT gt.fecha as date_gt,  gt.id_est as id_est, gt.val as gt, fo.val as fo
FROM cont_otres as gt, forecast_otres as fo
WHERE 
    date_part('year', gt.fecha)  = YEAR
    AND date_part('year', fo.fecha)  = YEAR
    AND gt.id_est IN (STATIONS)
    AND fo.val = TYPEFOR
    AND date_part('year',  fo.fecha) =  date_part('year',  gt.fecha)
    AND date_part('month', fo.fecha) =  date_part('month', gt.fecha) 
    AND date_part('day',   fo.fecha) =  date_part('day',   gt.fecha) 
    AND date_part('hour',   fo.fecha) =  date_part('hour',   gt.fecha) 
    AND gt.id_est = fo.id_est
