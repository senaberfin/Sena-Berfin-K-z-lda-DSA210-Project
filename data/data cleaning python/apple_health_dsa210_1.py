import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from collections import defaultdict

XML_FILE = "export.xml"

SUM_TYPES = {"HKQuantityTypeIdentifierStepCount": "step_count","HKQuantityTypeIdentifierActiveEnergyBurned":"active_energy_kcal","HKQuantityTypeIdentifierAppleExerciseTime": "exercise_minutes"}

AVG_TYPES = {"HKQuantityTypeIdentifierRestingHeartRate": "resting_hr_bpm", "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "hrv_ms"}

SLEEP_STAGES = {"HKCategoryValueSleepAnalysisAsleepCore", "HKCategoryValueSleepAnalysisAsleepDeep", "HKCategoryValueSleepAnalysisAsleepREM", "HKCategoryValueSleepAnalysisAsleepUnspecified"}

sum_data = {col: defaultdict(float) for col in SUM_TYPES.values()}
avg_data = {col: defaultdict(list) for col in AVG_TYPES.values()}
sleep_data = defaultdict(float)

print("Parsing export.xml")
context = ET.iterparse(XML_FILE, events=("start",))

for event, elem in context:
    if elem.tag != "Record":
        continue

    rtype = elem.get("type", "")
    start = elem.get("startDate", "")[:10]


    if rtype in SUM_TYPES:
        try:
            val = float(elem.get("value", ""))
            sum_data[SUM_TYPES[rtype]][start] += val
        except ValueError:
            pass

    elif rtype in AVG_TYPES:
        try:
            val = float(elem.get("value", ""))
            avg_data[AVG_TYPES[rtype]][start].append(val)
        except ValueError:
            pass
    
    elif rtype == "HKCategoryTypeIdentifierSleepAnalysis":
        if elem.get("value", "") in SLEEP_STAGES:
            s_str = elem.get("startDate", "")[:19]
            e_str = elem.get("endDate", "")[:19]
            try:
                s = datetime.strptime(s_str, "%Y-%m-%d %H:%M:%S")
                e = datetime.strptime(s_str, "%Y-%m-%d %H:%M:%S")
                dur_min = (e - s).total_seconds() / 60
                if dur_min > 0:
                    sleep_data[e.date().isoformat()] += dur_min
            except ValueError:
                pass
    
    elem.clear()


print("Parsing complete")


frames = []

for col, daily_dict in sum_data.items():
    df = pd.DataFrame(list(daily_dict.items()), columns=["date", col])
    frames.append(df.set_index("date"))

for col, daily_dict in avg_data.items():
    rows = {date: sum(vals)/len(vals) for date, vals in daily_dict.items()}
    df = pd.DataFrame(list(rows.items()), columns=["date", col])
    frames.append(df.set_index("date"))



sleep_df = pd.DataFrame(list(sleep_data.items()), columns=["date", "sleep_minutes"])
sleep_df["sleep_hours"] = (sleep_df["sleep_minutes"] / 60).round(2)
sleep_df = sleep_df.drop(columns = "sleep_minutes").set_index("date")
frames.append(sleep_df)

health = pd.concat(frames, axis=1, join="outer")
health.index = pd.to_datetime(health.index)
health = health.sort_index()
health = health.reset_index().rename(columns={"index": "date"})

health["step_count"] = health["step_count"].round(0)
health["active_energy_kcal"] = health["active_energy_kcal"].round(1)
health["exercise_minutes"] = health["exercise_minutes"].round(1)
health["resting_hr_bpm"] = health["resting_hr_bpm"].round(1)
health["hrv_ms"] = health["hrv_ms"].round(2)

print(f"\nDate range : {health["date"].min().date} -> {health["date"].max().date}")
print(f"\nTotal days : {len(health)}")
print(f"\nMissing values per column: {health.isnull().sum().to_string()}")
print(f"\nSample (first5 rows) {health.head().to_string(index=False)}")

health.to_csv("apple_health.csv", index=False)
print("\n Saved: apple_health.csv")