import geopandas as gpd
import requests
import io
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--vars', type=str, required=True,
                    help='the requested census variables, seperated by commas')
parser.add_argument('--geo', type=str, required=True,
                    help='the geo hierarchy, seperated by commas')
parser.add_argument('--tiger', type=str, required=True,
                    help='the tiger shapefile')
parser.add_argument('--out', type=str, required=True,
                    help='the output filename')
args = parser.parse_args()

vars_dict = {var[0]:var[-1]
             for var in [x.split(':') for x in args.vars.split(',')]}
geos = [geo.strip() if ':' in geo else f'{geo.strip()}:*'
        for geo in args.geo.split(',')]
geo_spec = '&'.join([f'in={geo}' for geo in geos[:-1]])

query = 'https://api.census.gov/data/2010/dec/sf1?' + \
        f'get={",".join(vars_dict.keys())}&' + \
        f'for={geos[-1]}&{geo_spec}'
response = requests.get(query)
content = response.text.replace('[', '').replace(']', '').replace(',\n','\n')
census_df = pd.read_csv(io.StringIO(content), dtype=str)
del content, response
census_df['GEOID10'] = census_df[[geo.split(':')[0] for geo in geos]]\
                            .agg(''.join, axis=1)
census_df = census_df[['GEOID10'] + list(vars_dict.keys())]
census_df.rename(columns=vars_dict, inplace=True)

shp_df = gpd.read_file(args.tiger)
shp_df = shp_df[['GEOID10', 'geometry']].drop_duplicates('GEOID10')

df = pd.merge(shp_df, census_df, on='GEOID10')
df.to_file(args.out)
