# Fit our Stan model to the combined import and dealer data for Swordfish, Bigeye, Yellowfin, and Mahi-mahi

import nest_asyncio
nest_asyncio.apply()
import stan
import pandas as pd
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import pickle

data = pd.read_csv('data/dealer_import.csv')

# Stan model specification
model = """
data {
  int<lower=0> N;
  int mn[N];
  int yr[N];
  vector[N] qu; // scaled quantity
  vector[N] pr; // logged or not logged price
  real imp[N,42];
}

parameters {
  real mu_alpha; // Mean of month distribution
  real mu_beta;
  real mu_delta;
  real<lower=0> sigma_alpha; // sigma of month distribution 
  real<lower = 0> sigma_beta;
  real<lower = 0> sigma_delta;
  vector[12] alpha; // Month random effects
  vector[12] beta;
  vector[10] delta;
  vector[42] gamma;
  real<lower=0> sigma; // sigma of price model
}

transformed parameters{

}

model {
  sigma ~ normal(0, 1);
  mu_alpha ~ normal(0, 1);
  mu_beta ~ normal(0, 1);
  mu_delta ~ normal(0, 1);
  sigma_alpha ~ normal(0, 1);
  sigma_beta ~ normal(0, 1);
  sigma_delta ~ normal(0, 1);
  beta ~ normal(mu_beta, sigma_beta);
  alpha ~ normal(mu_alpha, sigma_alpha);
  delta ~ normal(mu_delta, sigma_delta);
  gamma ~ normal(0, 1);

  
  for (n in 1:N) {
    real gamma_data = 0;
    for (k in 1:42)
      gamma_data += imp[n, k] * gamma[k];
    pr[n] ~ normal(alpha[mn[n]] + beta[mn[n]] * qu[n] + gamma_data + delta[yr[n]], sigma);
  }
}

generated quantities {
  vector[N] pr_hat; // Posterior predictive check
  for (n in 1:N) {
      real gamma_data = 0;
      for (k in 1:42)
        gamma_data += imp[n, k] * gamma[k];
      pr_hat[n] = normal_rng(alpha[mn[n]] + beta[mn[n]] * qu[n] + gamma_data + delta[yr[n]], sigma);
  }
}
"""

def fit_imports_model(species):
    # Fit import model to different species
    data_sub = data[data['species'] == species]

    # Drop Plains region
    data_sub = data_sub[data_sub.columns.drop(list(data_sub.filter(regex='Plains|Rocky Mountain')))]

    # Scale quantity landed in Hawaii
    data_sub['sd2'] = 2 * data_sub['LBS_SOLD'].std()
    data_sub['z_quant'] = data_sub['LBS_SOLD'] / data_sub['sd2']

    imp_data = data_sub.filter(regex='imp_kg_scaled_', axis=1).to_numpy()

    stan_data = {
        'N': data_sub.shape[0], 
        'qu': list(data_sub['z_quant']), 
        'pr': list(np.log(data_sub['PRICE'])),
        #'pr': list(data_sub['PRICE']),
        'imp': imp_data,
        'mn': list(data_sub['month']),
        'yr': list(data_sub['year_num'])
    }

    posterior = stan.build(model, data = stan_data, random_seed = 1)
    fit = posterior.sample(num_chains=4, num_samples=1000)
    
    return(fit, posterior)

swordfish_fit = fit_imports_model('Swordfish')
bigeye_fit = fit_imports_model('Bigeye Tuna')
yellowfin_fit = fit_imports_model('Yellowfin Tuna')
mahi_fit = fit_imports_model('Mahi-mahi')

# Save pars as dataframe
swordfish_fit[0].to_frame().to_csv('pars/swordfish_fit.csv')
bigeye_fit[0].to_frame().to_csv('pars/bigeye_fit.csv')
yellowfin_fit[0].to_frame().to_csv('pars/yellowfin_fit.csv')
mahi_fit[0].to_frame().to_csv('pars/mahi_fit.csv')

# Pickle fit results
with open('pars/swordfish_fit.pkl', 'wb') as pickle_out:
    pickle.dump(swordfish_fit[0], pickle_out)
    
with open('pars/bigeye_fit.pkl', 'wb') as pickle_out:
    pickle.dump(bigeye_fit[0], pickle_out)
    
with open('pars/yellowfin_fit.pkl', 'wb') as pickle_out:
    pickle.dump(yellowfin_fit[0], pickle_out)
    
with open('pars/mahi_fit.pkl', 'wb') as pickle_out:
    pickle.dump(mahi_fit[0], pickle_out)

# Pickle posterior model
with open('pars/swordfish_posterior.pkl', 'wb') as pickle_out:
    pickle.dump(swordfish_fit[1], pickle_out)
    
with open('pars/bigeye_posterior.pkl', 'wb') as pickle_out:
    pickle.dump(bigeye_fit[1], pickle_out)
    
with open('pars/yellowfin_posterior.pkl', 'wb') as pickle_out:
    pickle.dump(yellowfin_fit[1], pickle_out)
    
with open('pars/mahi_posterior.pkl', 'wb') as pickle_out:
    pickle.dump(mahi_fit[1], pickle_out)
