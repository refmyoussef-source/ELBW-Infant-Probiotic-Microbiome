import pandas as pd
import subprocess
import os

# التأكد من وجود فولدر raw_data
os.makedirs("raw_data", exist_ok=True)

# 1. قراءة الـ metadata
metadata_path = "raw_data/master_metadata_final.tsv"
df = pd.read_csv(metadata_path, sep="\t")

# 2. البحث عن عمود الـ RUN واختيار أول 3 عينات للتجربة
# (كنتاكدوا واش سميت العمود RUN كبيراً ولا صغيراً لتفادي الأخطاء)
run_col = None
for col in df.columns:
    if col.upper() == "RUN":
        run_col = col
        break

if run_col:
    sample_runs = df[run_col].dropna().head(3).tolist()
    print(f"Test Run IDs to download: {sample_runs}")

    # 3. تحميل العينات باستخدام fasterq-dump
    for run_id in sample_runs:
        print(f"Downloading {run_id}...")
        cmd = f"fasterq-dump {run_id} -O raw_data/"
        result = subprocess.run(cmd, shell=True)

        if result.returncode == 0:
            print(f"Successfully downloaded {run_id}")
        else:
            print(f"Error downloading {run_id}")
else:
    print("Error: 'RUN' column not found in metadata! Check column names.")
