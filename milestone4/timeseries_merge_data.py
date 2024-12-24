import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

years = np.arange(2016,2025)
print(years)
base_subdir = "../../data"

infotable_list = []
coverpage_list = []
summarypg_list = []
submissio_list = []
for year in years:
    for i in [1,2,3,4]:
        if not(year == 2024 and i == 4):
            foldername = f"{year}q{i}"
            dir_ = f"{base_subdir}/{foldername}"
            infotable_list.append(pd.read_csv(f"{dir_}/INFOTABLE.tsv", sep="\t"))
            coverpage_list.append(pd.read_csv(f"{dir_}/COVERPAGE.tsv", sep="\t"))
            summarypg_list.append(pd.read_csv(f"{dir_}/SUMMARYPAGE.tsv", sep="\t"))
            submissio_list.append(pd.read_csv(f"{dir_}/SUBMISSION.tsv", sep="\t"))
            print(foldername)

print("Concatenating...")
df_infotable_ts = pd.concat(infotable_list, axis = 0, ignore_index = True)
df_coverpage_ts = pd.concat(coverpage_list, axis = 0, ignore_index = True)
df_summarypg_ts = pd.concat(summarypg_list, axis = 0, ignore_index = True)
df_submissio_ts = pd.concat(submissio_list, axis = 0, ignore_index = True)

print("Saving infotable...")
df_infotable_ts.to_csv(f"{base_subdir}/timeseries_INFOTABLE.csv", index=False)
print("Saving coverpage...")
df_coverpage_ts.to_csv(f"{base_subdir}/timeseries_COVERPAGE.csv", index=False)
print("Saving summarypage...")
df_summarypg_ts.to_csv(f"{base_subdir}/timeseries_SUMMARYPAGE.csv", index=False)
print("Saving submission...")
df_submissio_ts.to_csv(f"{base_subdir}/timeseries_SUBMISSION.csv", index=False)
print("Done!")