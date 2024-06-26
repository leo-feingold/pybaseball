import pandas as pd
season = 2024
min_IP = 10
name = "Aaron Nola"


LHH_path = "/Users/leofeingold/Desktop/pybaseball/Lefty_Righty_Splits_CSV/21Through23LHHAdvanced.csv"
LHH_df = pd.read_csv(LHH_path)
#LHH_df = LHH_df[LHH_df["Season"] == season]

RHH_path = "/Users/leofeingold/Desktop/pybaseball/Lefty_Righty_Splits_CSV/21Through23RHHAdvanced.csv"
RHH_df = pd.read_csv(RHH_path)
#RHH_df = RHH_df[RHH_df["Season"] == season]

merged_df = pd.merge(LHH_df, RHH_df, on=["Name", "Season", "Tm"], suffixes=["_LHH", "_RHH"])

merged_df = merged_df[(merged_df["IP_LHH"] >= min_IP) & (merged_df["IP_RHH"] >= min_IP)]
merged_df = merged_df[merged_df["Name"] == name]


merged_df["xFIP_Difference"] = abs(merged_df["xFIP_LHH"] - merged_df["xFIP_RHH"])
merged_df = merged_df.sort_values("xFIP_Difference", ascending=False)

print(merged_df[["Season", "Tm", "Name", "xFIP_LHH", "IP_LHH", "xFIP_RHH", "IP_RHH", "xFIP_Difference"]].head(30))