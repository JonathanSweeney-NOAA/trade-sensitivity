# Prepare data for Bayesian demand analysis by cleaning import data and filtering dealer data

import pandas as pd
import numpy as np

# Read in raw data
i_data = pd.read_csv('data/monthly_trade-no_aggregation.csv', low_memory = False, thousands = ',')
d_data = pd.read_csv('data/dealer_dat.csv', low_memory = False)

# Aggregate import districts to regions
i_data['district_state'] = i_data['US Customs District Name'].str.split(pat=", ", expand = True)[1]

regions = {
    'MA': 'New England',
    'NY': 'Mideast',
    'VA': 'Southeast',
    'GA': 'Southeast',
    'CA': 'Far West',
    'IL': 'Great Lakes',
    'MO': 'Plains',
    'ME': 'New England',
    'ND': 'Plains',
    'FL': 'Southeast',
    'WA': 'Far West',
    'MI': 'Great Lakes',
    'TX': 'Southwest',
    'HI': 'Hawaii',
    'MT': 'Rocky Mountain',
    'DC': 'Mideast',
    'AZ': 'Southwest',
    'PR': None,
    'MD': 'Mideast',
    'LA': 'Southeast',
    'PA': 'Mideast',
    'MN': 'Plains',
    'SC': 'Southeast',
    'OR': 'Far West',
    'VT': 'New England',
    'AL': 'Southeast',
    'OH': 'Great Lakes',
    'AK': 'Far West',
    'NC': 'Southeast',
    'WI': 'Great Lakes',
    'RI': 'New England',
    None: None
}

i_data['region'] = i_data['district_state'].map(regions)
i_data = i_data[i_data['region'].notnull()]

# Aggregate products for focal species Bigeye, Yellowfin, Swordfish, Mahi-mahi
# Contains
i_data = i_data[i_data['Product Name'].str.contains('|'.join(['TUNA BIGEYE', 'TUNA YELLOWFIN', 'SALMON', 'FLATFISH', 'SWORDFISH', 'DOLPHINFISH']))]

# Does not contain
i_data = i_data[~i_data['Product Name'].str.contains('|'.join(['ROE', 'HERRING', 'CANNED', 'SALTED', 'SMOKED', 'NSPF']))]

# Add product group column
i_data.loc[i_data['Product Name'].str.contains("TUNA BIGEYE"),'product_group'] = 'Bigeye Tuna'
i_data.loc[i_data['Product Name'].str.contains("TUNA YELLOWFIN"),'product_group'] = 'Yellowfin Tuna'
i_data.loc[i_data['Product Name'].str.contains("SWORDFISH"),'product_group'] = 'Swordfish'
i_data.loc[i_data['Product Name'].str.contains("DOLPHINFISH"),'product_group'] = 'Mahi-mahi'
i_data.loc[i_data['Product Name'].str.contains("SALMON"),'product_group'] = 'Salmon'
i_data.loc[i_data['Product Name'].str.contains("FLATFISH"),'product_group'] = 'Flatfish'

i_data['Volume (kg)'] = i_data['Volume (kg)']
i_kg = i_data.groupby(['Year', 'Month number', 'region', 'product_group'], as_index=False).agg(imp_kg=('Volume (kg)', 'sum'))

# Replace NaN with 0s
i_kg_no_nan = i_kg.pivot(index = ['Month number', 'Year'], columns = ['region', 'product_group'], values = ['imp_kg'])
i_kg_no_nan = i_kg_no_nan.fillna(0)
i_kg_long = i_kg_no_nan.stack().stack().reset_index()

# Generate date
i_kg_long['day'] = 1
i_kg_long['date'] = pd.to_datetime(i_kg_long['Year'].astype(str) + '/' + i_kg_long['Month number'].astype(str) + '/' + i_kg_long['day'].astype(str))

# Scale import quantities by dividing by 2 SD
i_kg_sd = i_kg_long.groupby(['region', 'product_group'], as_index = False).agg(kg_sd = ('imp_kg', 'std'))
i_kg_long = i_kg_long.merge(i_kg_sd, how = 'left', on = ['region', 'product_group'])
i_kg_long['imp_kg_scaled'] = i_kg_long['imp_kg'] / (2 * i_kg_long['kg_sd'])

i_kg_long.to_csv('data/import_kg.csv')

# Join with dealer prices and weights (bigeye, mahi-mahi, swordfish, yellowfin)
d_focal = d_data[d_data['SPECIES_FK'].isin([6, 13, 11, 3])]
d_focal = d_focal.groupby(['REPORT_DATE', 'SPECIES_FK'], as_index = False).agg(LBS_SOLD = ('LBS_SOLD', 'sum'),
                                                                              PRICE = ('PRICE_PER_LB', 'mean'))

species = {
    6: 'Bigeye Tuna',
    13: 'Mahi-mahi',
    11: 'Swordfish',
    3: 'Yellowfin Tuna'
}

d_focal['species'] = d_focal['SPECIES_FK'].map(species)
d_focal['month'] = pd.DatetimeIndex(d_focal['REPORT_DATE']).month
d_focal['year'] = pd.DatetimeIndex(d_focal['REPORT_DATE']).year
d_focal = d_focal.query('year >= 2010 & year <= 2019')

# Save long merged data for figure
d_i_long = d_focal.merge(i_kg_long, how = 'left', left_on = ['month', 'year'], right_on = ['Month number', 'Year'])
d_i_long.to_csv('data/dealer_import_long.csv')

# Transform i_kg to wide to match with dealer data
i_kg_wide = i_kg_long.pivot(index = ['Month number', 'Year'], columns = ['region', 'product_group'], values = ['imp_kg', 'imp_kg_scaled']).reset_index()
i_kg_wide.columns = i_kg_wide.columns.map('_'.join).str.strip('_')

d_i = d_focal.merge(i_kg_wide, how = 'left', left_on = ['month', 'year'], right_on = ['Month number', 'Year'])
d_i = d_i.drop(columns=['Year', 'Month number'])
d_i['year_num'] = d_i['year'] - 2009

d_i.to_csv('data/dealer_import.csv')