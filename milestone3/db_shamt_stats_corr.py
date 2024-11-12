import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df_star = pd.read_csv("../data/df_star.csv")
# fig, ax = plt.subplots(1,1,figsize=(6,3))
fig, ax = plt.subplots(3,3,figsize=(30,15))
a1 = ax[0,0]
a2 = ax[0,1]
a3 = ax[0,2]

a4 = ax[1,0]
a5 = ax[1,1]
a6 = ax[1,2]

a7 = ax[2,0]
a8 = ax[2,1]
a9 = ax[2,2]

sns.scatterplot(data = df_star, y = 'TABLEVALUETOTAL', x = '01% SHAMT', ax = a1)
a1.set_xscale("log"), a1.set_yscale("log")

sns.scatterplot(data = df_star, y = 'TABLEVALUETOTAL', x = '10% SHAMT', ax = a2)
a2.set_xscale("log"), a2.set_yscale("log")

sns.scatterplot(data = df_star, y = 'TABLEVALUETOTAL', x = '90% SHAMT', ax = a3)
a3.set_xscale("log"), a3.set_yscale("log")

sns.scatterplot(data = df_star, y = 'TABLEVALUETOTAL', x = '99% SHAMT', ax = a4)
a4.set_xscale("log"), a4.set_yscale("log")

sns.scatterplot(data = df_star, y = 'TABLEVALUETOTAL', x = '50% SHAMT', ax = a5)
a5.set_xscale("log"), a5.set_yscale("log")

sns.scatterplot(data = df_star, y = 'TABLEVALUETOTAL', x = 'MIN SHAMT', ax = a6)
a6.set_xscale("log"), a6.set_yscale("log")

sns.scatterplot(data = df_star, y = 'TABLEVALUETOTAL', x = 'MAX SHAMT', ax = a7)
a7.set_xscale("log"), a7.set_yscale("log")

sns.scatterplot(data = df_star, y = '25% VALUE', x = '75% SHAMT', ax = a8)
a8.set_xscale("log"), a8.set_yscale("log")

sns.scatterplot(data = df_star, y = 'TABLEVALUETOTAL', x = 'STD SHAMT', ax = a9)
a9.set_xscale("log"), a9.set_yscale("log")

plt.show()