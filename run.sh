#python3 census.py \
#    --vars H001001:house_units,P001001:population \
#    --geo state:06,'zip code tabulation area (or part)' \
#    --tiger ./data/census/tl_2010_06_zcta510.shp \
#    --out pop_shp/zcta2010.shp

python3 census.py \
    --db acs \
    --vars DP03_0052E \
    --geo state:06,'zip code tabulation area' \
    --out zcta2010.csv
