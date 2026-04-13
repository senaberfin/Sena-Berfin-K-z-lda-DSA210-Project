import pandas as pd

df = pd.read_csv("ViewingActivity.csv")

df = df[df["Profile Name"] == "Berfin"].copy() #since account has diff. profiles-> only taking my own data
print(f"Rows after profile filter : {len(df)}")

non_content = ["HOOK", "TRAILER", "TEASER", "TEASER_TRAILER","PROMOTIONAL", "PREVIEW", "BIG_ROW", "BUMPER", "CINEMAGRAPH"] #data contains non-contents like this

df = df[~df["Supplemental Video Type"].isin(non_content)].copy()
print(f"Rows after removing non-content: {len(df)}")

df["Start Time"] = pd.to_datetime(df["Start Time"])
df["Duration"] = pd.to_timedelta(df["Duration"])

df["duration_minutes"] = df["Duration"].dt.total_seconds() /60

df = df[df["duration_minutes"] >= 1].copy() # droping rows with duration less than 1( not real viewing)

df["date"] = df["Start Time"].dt.date

daily_df = (df.groupby("date").agg(watch_minutes = ("duration_minutes", "sum"), num_sessions = ("duration_minutes", "count")).reset_index())
daily_df["date"] = pd.to_datetime(daily_df["date"])

print(f"\nDays with Netflix viewing: {len(daily_df)}")
print(f"Date range: {daily_df["date"].min().date()} -> {daily_df["date"].max().date()}")
print(f"\nSample output:")
print(daily_df.head(10).to_string(index=False))

daily_df.to_csv("netflix_daily.csv", index=False)
print("\n Saved: netflix_daily.csv")