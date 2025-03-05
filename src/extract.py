import os
import pandas as pd
import json
import re

class Extract:
    """Kelas untuk mengekstrak data dari banyak file CSV dan JSON dengan validasi regex."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.extracted_files = {"csv": [], "json": []}

    def extract_csv(self):
        """Mengekstrak semua file CSV dalam folder data/csv"""
        csv_dir = os.path.join(self.data_dir, "csv")
        all_dfs = []
        pattern = re.compile(r"^[\w,\s-]+\.csv$")  

        if os.path.exists(csv_dir):
            for file_name in os.listdir(csv_dir):
                if pattern.match(file_name):  
                    file_path = os.path.join(csv_dir, file_name)
                    df = pd.read_csv(file_path)
                    self.extracted_files["csv"].append(file_name)
                    print(f"\n📂 Extracted {file_name}, shape: {df.shape}")
                    all_dfs.append(df)

        total_files = len(self.extracted_files["csv"])
        print(f"\n✅ Total CSV Extracted: {total_files}")

        merged_df = pd.concat(all_dfs, ignore_index=True) if all_dfs else None
        if merged_df is not None:
            print("\n🔍 Ringkasan data null dari CSV:")
            self.show_null_summary(merged_df)

        return merged_df

    def extract_json(self):
        """Mengekstrak semua file JSON dalam folder data/json"""
        json_dir = os.path.join(self.data_dir, "json")
        all_dfs = []
        pattern = re.compile(r"^[\w,\s-]+\.json$")  

        if os.path.exists(json_dir):
            for file_name in os.listdir(json_dir):
                if pattern.match(file_name):
                    file_path = os.path.join(json_dir, file_name)
                    with open(file_path, "r") as f:
                        data = json.load(f)
                    df = pd.DataFrame(data)
                    self.extracted_files["json"].append(file_name)
                    print(f"\n📂 Extracted {file_name}, shape: {df.shape}")
                    all_dfs.append(df)

        total_files = len(self.extracted_files["json"])
        print(f"\n✅ Total JSON Extracted: {total_files}")

        merged_df = pd.concat(all_dfs, ignore_index=True) if all_dfs else None
        if merged_df is not None:
            print("\n🔍 Ringkasan data null dari JSON:")
            self.show_null_summary(merged_df)

        return merged_df
    
    def show_null_summary(self, df):
        """Menampilkan jumlah data null dari setiap kolom dan total keseluruhan."""
        null_counts = df.isnull().sum()
        null_summary = null_counts[null_counts > 0]
        total_nulls = null_counts.sum()
        
        if null_summary.empty:
            print("\n✅ Tidak ada data null dalam dataset.")
        else:
            print("\n⚠️ Data mengandung nilai null:")
            print(null_summary.to_string())
            print(f"\n🔢 Total nilai null di seluruh dataset: {total_nulls}")
    
    def save_to_staging(self, df, file_name):
        """Menyimpan hasil ekstraksi ke folder staging"""
        staging_dir = "staging"
        os.makedirs(staging_dir, exist_ok=True)
        output_path = os.path.join(staging_dir, file_name)
        
        df.to_csv(output_path, index=False)
        file_size = os.path.getsize(output_path) / 1024  # KB
        
        print(f"\n✅ Saved to staging: {file_name}")
        print(f"📊 Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        print(f"💾 File Size: {file_size:.2f} KB\n")
        
        print("\n🔍 Ringkasan data null setelah digabungkan dan disimpan:")
        self.show_null_summary(df)
