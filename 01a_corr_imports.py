# Examine the correlation between import districts for different species

import pandas as pd

data = pd.read_csv('data/dealer_import.csv')

# Remove plains and rocky mountain areas
data = data[data.columns.drop(list(data.filter(regex='Plains|Rocky Mountain')))]

data_imp = data.filter(regex='imp_kg_scaled_|month|year', axis=1).drop_duplicates().reset_index(drop = True)

# Examine correlations
# Bigeye Tuna
data_imp_bigeye = data_imp.filter(regex='Bigeye Tuna', axis = 1)
data_imp_bigeye.corr()

# Salmon
data_imp_salmon = data_imp.filter(regex='Salmon', axis = 1)
data_imp_salmon.corr()

# Swordfish
data_imp_swordfish = data_imp.filter(regex='Swordfish', axis = 1)
data_imp_swordfish.corr()

# Flatfish
data_imp_flatfish = data_imp.filter(regex='Flatfish', axis = 1)
data_imp_flatfish.corr()

# Mahi-mahi
data_imp_mahi = data_imp.filter(regex='Mahi-mahi', axis = 1)
data_imp_mahi.corr()

# Yellowfin
data_imp_yellowfin = data_imp.filter(regex='Yellowfin Tuna', axis = 1)
data_imp_yellowfin.corr()