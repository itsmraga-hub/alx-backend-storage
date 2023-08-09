SELECT band_name, 
       EXTRACT(YEAR FROM DATE '2022-01-01' - split) - EXTRACT(YEAR FROM formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;

