# Plot fit parameters

import pickle
import pandas as pd
import arviz as az
import matplotlib.pyplot as plt

# Unpickle models
with open("pars/swordfish_fit.pkl", "rb") as f:
    swordfish_fit = pickle.load(f)
    
with open("pars/bigeye_fit.pkl", "rb") as f:
    bigeye_fit = pickle.load(f)
    
with open("pars/yellowfin_fit.pkl", "rb") as f:
    yellowfin_fit = pickle.load(f)
    
with open("pars/mahi_fit.pkl", "rb") as f:
    mahi_fit = pickle.load(f)


# Grab column names from data
data = pd.read_csv('data/dealer_import.csv')
data_sub = data[data.columns.drop(list(data.filter(regex='Plains|Rocky Mountain')))]
imp_col_names = data_sub.filter(regex='imp_kg_scaled_', axis=1).columns
imp_col_names = imp_col_names.str.lstrip('imp_kg_scaled_')

product_map = dict(zip(range(0, 48), imp_col_names))
year_map = dict(zip(range(0, 11), [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]))
month_map = dict(zip(range(0,23), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']))
labeller = az.labels.MapLabeller(coord_map= {'alpha_dim_0': month_map,
                                             'delta_dim_0': year_map,
                                             'beta_dim_0': month_map,
                                             'gamma_dim_0': product_map})

# Plot pars
az.plot_forest(swordfish_fit, combined=True, rope = (0,0), labeller = labeller, var_names = ['^alpha', '^beta', '^gamma', '^delta'], filter_vars = 'regex')
plt.gcf().set_size_inches(27, 20)
plt.savefig('figures/pars_swordfish.jpg')
plt.close()

az.plot_forest(bigeye_fit, combined=True, rope = (0,0), labeller = labeller, var_names = ['^alpha', '^beta', '^gamma', '^delta'], filter_vars = 'regex') 
plt.gcf().set_size_inches(27, 20)
plt.savefig('figures/pars_bigeye.jpg')
plt.close()

az.plot_forest(yellowfin_fit, combined=True, rope = (0,0), labeller = labeller, var_names = ['^alpha', '^beta', '^gamma', '^delta'], filter_vars = 'regex') 
plt.gcf().set_size_inches(27, 20)
plt.savefig('figures/pars_yellowfin.jpg')
plt.close()

az.plot_forest(mahi_fit, combined=True, rope = (0,0), labeller = labeller, var_names = ['^alpha', '^beta', '^gamma', '^delta'], filter_vars = 'regex') 
plt.gcf().set_size_inches(27, 20)
plt.savefig('figures/pars_mahi.jpg')
plt.close()



