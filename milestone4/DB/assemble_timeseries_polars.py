import polars as pl
import os
import numpy as np
submissio_list = []
infotable_list = []
coverpage_list = []
summarypg_list = []

base_subdir = "../../data"

infotable_list = []
coverpage_list = []
summarypg_list = []
submissio_list = []
years = np.arange(2016,2025)
for year in years:
    for i in [1,2,3,4]:
        if not(year == 2024 and i == 4):
            foldername = f"{year}q{i}"
            dir_ = f"{base_subdir}/{foldername}"
            infotable_list.append(pl.read_csv(f"{dir_}/INFOTABLE.tsv", separator="\t"))
            coverpage_list.append(pl.read_csv(f"{dir_}/COVERPAGE.tsv", separator="\t"))
            summarypg_list.append(pl.read_csv(f"{dir_}/SUMMARYPAGE.tsv", separator="\t"))
            submissio_list.append(pl.read_csv(f"{dir_}/SUBMISSION.tsv", separator="\t"))
            print(foldername)

print("Concatenating...")
df_infotable_ts = pl.concat(infotable_list)
df_coverpage_ts = pl.concat(coverpage_list)
df_summarypg_ts = pl.concat(summarypg_list)
df_submissio_ts = pl.concat(submissio_list)

print("Saving infotable...")
df_infotable_ts.write_csv(f"{base_subdir}/INFOTABLE_timeseries.tsv", sep="\t")
print("Saving coverpage...")
df_coverpage_ts.write_csv(f"{base_subdir}/COVERPAGE_timeseries.tsv", sep="\t")
print("Saving summarypage...")
df_summarypg_ts.write_csv(f"{base_subdir}/SUMMARYPAGE_timeseries.tsv", sep="\t")
print("Saving submission...")
df_submissio_ts.write_csv(f"{base_subdir}/SUBMISSION_timeseries.tsv", sep="\t")
print("Done!")