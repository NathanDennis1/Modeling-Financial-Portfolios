import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn

df_starlog = pd.read_csv("../data/df_starlog.csv")

print(df_starlog.head())

scaler = StandardScaler()