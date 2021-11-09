# Load parameter data and summarize key districts and products for each species

import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load paramter data
bigeye_fit = pd.read_csv('pars/bigeye_fit.csv')
yellowfin_fit = pd.read_csv('pars/yellowfin_fit.csv')
mahi_fit = pd.read_csv('pars/mahi_fit.csv')
swordfish_fit = pd.read_csv('pars/swordfish_fit.csv')

# Keep just the relevant parameters
bigeye_main = bigeye_fit.filter(regex = ('^alpha|^beta|^gamma|^delta'))
yellowfin_main = yellowfin_fit.filter(regex = ('^alpha|^beta|^gamma|^delta'))
mahi_main = mahi_fit.filter(regex = ('^alpha|^beta|^gamma|^delta'))
swordfish_main = swordfish_fit.filter(regex = ('^alpha|^beta|^gamma|^delta'))

# Parse districts and products
data = pd.read_csv('data/dealer_import.csv')
data_sub = data[data.columns.drop(list(data.filter(regex='Plains|Rocky Mountain')))]
imp_col_names = data_sub.filter(regex='imp_kg_scaled_', axis=1).columns
imp_col_names = imp_col_names.str.lstrip('imp_kg_scaled_')

names_index = pd.DataFrame(list(zip(range(1, 42), imp_col_names)), columns = ['index', 'names'])
names_index['district'] = names_index['names'].str.split(pat='_', expand = True)[0]
names_index['product'] = names_index['names'].str.split(pat='_', expand = True)[1]

names_index['par'] = 'gamma.' + names_index['index'].astype(str)
names_index = names_index.drop(['index', 'names'], axis=1)

# Calculate expected parameter values
bigeye_mean = pd.DataFrame(bigeye_main.mean(axis = 0), columns = ['exp']).reset_index().rename(columns = {'index':'par'})
bigeye_mean['species'] = 'bigeye'
yellowfin_mean = pd.DataFrame(yellowfin_main.mean(axis = 0), columns = ['exp']).reset_index().rename(columns = {'index':'par'})
yellowfin_mean['species'] = 'yellowfin'
mahi_mean = pd.DataFrame(mahi_main.mean(axis = 0), columns = ['exp']).reset_index().rename(columns = {'index':'par'})
mahi_mean['species'] = 'mahi'
swordfish_mean = pd.DataFrame(swordfish_main.mean(axis = 0), columns = ['exp']).reset_index().rename(columns = {'index':'par'})
swordfish_mean['species'] = 'swordfish'

par_data = pd.concat([bigeye_mean, yellowfin_mean, mahi_mean, swordfish_mean])

# Calculate absolute value of exp
par_data['abs_exp'] = np.absolute(par_data['exp'])

# Join district and products to pars
par_data = par_data.merge(names_index, how = 'left', on = 'par')

# Summarize district pars
district_summary = par_data.groupby(['species', 'district'], as_index = False).agg({'abs_exp':'mean'})

# Summarize product pars
product_summary = par_data.groupby(['species', 'product'], as_index = False).agg({'abs_exp':'mean'})

# Plot product and district summaries as radar plots

# Product
categories = list(product_summary['product'].unique())
categories = [*categories, categories[0]]

bigeye = list(product_summary.query('species == "bigeye"')['abs_exp'])
yellowfin = list(product_summary.query('species == "yellowfin"')['abs_exp'])
mahi = list(product_summary.query('species == "mahi"')['abs_exp'])
swordfish = list(product_summary.query('species == "swordfish"')['abs_exp'])
bigeye = [*bigeye, bigeye[0]]
yellowfin = [*yellowfin, yellowfin[0]]
mahi = [*mahi, mahi[0]]
swordfish = [*swordfish, swordfish[0]]

fig = go.Figure(
    data=[
        go.Scatterpolar(r=bigeye, theta=categories, name='Bigeye Tuna'),
        go.Scatterpolar(r=yellowfin, theta=categories, name='Yellowfin Tuna'),
        go.Scatterpolar(r=mahi, theta=categories, name='Mahi-mahi'),
        go.Scatterpolar(r=swordfish, theta=categories, name='Swordfish')
    ],
    layout=go.Layout(
        title=go.layout.Title(text='Product comparison'),
        polar={'radialaxis': {'visible': True}},
        showlegend=True
    )
)

fig.write_image("figures/radar_product.jpg")

# District
categories = list(district_summary['district'].unique())
categories = [*categories, categories[0]]

bigeye = list(district_summary.query('species == "bigeye"')['abs_exp'])
yellowfin = list(district_summary.query('species == "yellowfin"')['abs_exp'])
mahi = list(district_summary.query('species == "mahi"')['abs_exp'])
swordfish = list(district_summary.query('species == "swordfish"')['abs_exp'])
bigeye = [*bigeye, bigeye[0]]
yellowfin = [*yellowfin, yellowfin[0]]
mahi = [*mahi, mahi[0]]
swordfish = [*swordfish, swordfish[0]]

fig = go.Figure(
    data=[
        go.Scatterpolar(r=bigeye, theta=categories, name='Bigeye Tuna'),
        go.Scatterpolar(r=yellowfin, theta=categories, name='Yellowfin Tuna'),
        go.Scatterpolar(r=mahi, theta=categories, name='Mahi-mahi'),
        go.Scatterpolar(r=swordfish, theta=categories, name='Swordfish')
    ],
    layout=go.Layout(
        title=go.layout.Title(text='District comparison'),
        polar={'radialaxis': {'visible': True}},
        showlegend=True
    )
)

fig.write_image("figures/radar_district.jpg")