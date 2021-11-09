# Plot posterior predictive checks

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
    
# Unpickle posteriors
with open("pars/swordfish_posterior.pkl", "rb") as f:
    swordfish_posterior = pickle.load(f)
    
with open("pars/bigeye_posterior.pkl", "rb") as f:
    bigeye_posterior = pickle.load(f)
    
with open("pars/yellowfin_posterior.pkl", "rb") as f:
    yellowfin_posterior = pickle.load(f)
    
with open("pars/mahi_posterior.pkl", "rb") as f:
    mahi_posterior = pickle.load(f)

az.plot_ppc(az.from_pystan(posterior = swordfish_fit, posterior_predictive= ['pr_hat'], observed_data = ['pr'], posterior_model = swordfish_posterior), data_pairs = {'pr' : 'pr_hat'})
plt.gcf().set_size_inches(6, 6)
plt.savefig('figures/ppc_swordfish.jpg')
plt.close()

az.plot_ppc(az.from_pystan(posterior = bigeye_fit, posterior_predictive= ['pr_hat'], observed_data = ['pr'], posterior_model = bigeye_posterior), data_pairs = {'pr' : 'pr_hat'})
plt.gcf().set_size_inches(6, 6)
plt.savefig('figures/ppc_bigeye.jpg')
plt.close()

az.plot_ppc(az.from_pystan(posterior = yellowfin_fit, posterior_predictive= ['pr_hat'], observed_data = ['pr'], posterior_model = yellowfin_posterior), data_pairs = {'pr' : 'pr_hat'})
plt.gcf().set_size_inches(6, 6)
plt.savefig('figures/ppc_yellowfin.jpg')
plt.close()

az.plot_ppc(az.from_pystan(posterior = mahi_fit, posterior_predictive= ['pr_hat'], observed_data = ['pr'], posterior_model = mahi_posterior), data_pairs = {'pr' : 'pr_hat'})
plt.gcf().set_size_inches(6, 6)
plt.savefig('figures/ppc_mahi.jpg')
plt.close()