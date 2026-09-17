import pandas as pd
import subprocess
import os

# 1. التأكد من وجود فولدر raw_data
os.makedirs("raw_data", exist_ok=True)

# 2. قراءة الـ metadata
metadata_path = "raw_data/master_metadata_final.tsv"
df = pd.read_csv(metadata_path, sep="\t")

# 3. تحديد عمود الـ RUN بدقة
run_col = None
for col in df.columns:
    if col.upper() == "RUN":
        run_col = col
        break

if run_col:
    all_runs = df[run_col].dropna().tolist()
    print(f"Total samples to download: {len(all_runs)}")
    
    # ملف لتسجيل العينات التي فشل تحميلها
    error_log = "failed_downloads.txt"
    
    for i, run_id in enumerate(all_runs, 1):
        print(f"[{i}/{len(all_runs)}] Downloading {run_id}...")
        cmd = f"fasterq-dump {run_id} -O raw_data/"
        
        try:
            # تشغيل الأمر والتحقق من حالة الخروج (Return Code)
            result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
            print(f"Successfully downloaded {run_id}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {run_id}. Skipping to next sample.")
            # تسجيل الخطأ في الملف وعدم توقف السكريبت
            with open(error_log, "a") as f:
                f.write(f"{run_id}\n")
        except Exception as e:
            print(f"Unexpected error with {run_id}: {e}")
            with open(error_log, "a") as f:
                f.write(f"{run_id}\n")
                
    print("Download process completed for all samples!")
else:
    print("Error: 'RUN' column not found in metadata!")
