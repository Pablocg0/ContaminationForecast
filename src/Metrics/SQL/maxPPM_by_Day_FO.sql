SELECT         date_part('year', fecha) as year_fo, 
                date_part('month', fecha) as month_fo,
                date_part('day', fecha) as day_fo,
                CASE WHEN max(val) > 155 THEN 1 ELSE 0 END as val_fo,
                max(val) as ppm_fo
        FROM forecast_otres
        WHERE 
                date_part('year', fecha)  = 2017                 
        GROUP BY
                1,2,3
        ORDER BY 1,2,3