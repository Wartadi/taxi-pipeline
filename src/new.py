import os
import pandas as pd
import json
import re
from datetime import datetime

class Extract:
    """Kelas untuk mengekstrak data dari banyak file CSV dan JSON dengan validasi regex."""
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def extract_csv(self):
        csv_dir = os.path.join(self.data_dir, "csv")
        all_dfs = []
        pattern = re.compile(r"^[\w,\s-]+\.csv$")  # Validasi nama file CSV

        if os.path.exists(csv_dir):
            for file_name in os.listdir(csv_dir):
                if pattern.match(file_name):  
                    file_path = os.path.join(csv_dir, file_name)
                    df = pd.read_csv(file_path)
                    print(f"Extracted {file_name}, shape: {df.shape}")
                    all_dfs.append(df)

        if not all_dfs:
            print(f"Tidak ada file CSV di {csv_dir}")
            return None
        
        combined_df = pd.concat(all_dfs, ignore_index=True)
        print(f"Total combined CSV data shape: {combined_df.shape}")
        return combined_df

    def extract_json(self):
        json_dir = os.path.join(self.data_dir, "json")
        all_dfs = []
        pattern = re.compile(r"^[\w,\s-]+\.json$")  # Validasi nama file JSON

        if os.path.exists(json_dir):
            for file_name in os.listdir(json_dir):
                if pattern.match(file_name):
                    file_path = os.path.join(json_dir, file_name)
                    with open(file_path, "r") as f:
                        data = json.load(f)
                    df = pd.DataFrame(data)
                    print(f"Extracted {file_name}, shape: {df.shape}")
                    all_dfs.append(df)

        if not all_dfs:
            print(f"Tidak ada file JSON di {json_dir}")
            return None
        
        combined_df = pd.concat(all_dfs, ignore_index=True)
        print(f"Total combined JSON data shape: {combined_df.shape}")
        return combined_df
    
    def save_to_staging(self, df, file_name):
        staging_dir = "staging"
        staging_path = os.path.join(staging_dir, file_name)

        if not os.path.exists(staging_dir):
            os.makedirs(staging_dir)

        df.to_csv(staging_path, index=False)
        print(f"Saved to staging: {staging_path}")


class Transform:
    """Kelas untuk transformasi data dengan validasi dan regex"""
    def __init__(self, df):
        self.df = df.copy()
    
    def normalize_columns(self):
        """Normalisasi nama kolom agar menjadi format yang lebih rapi."""
        self.df.columns = [re.sub(r"\W+", "_", col.lower().strip()) for col in self.df.columns]
    
    def clean_phone_numbers(self):
        """Membersihkan nomor telepon dan memastikan format yang benar."""
        if "phone_number" in self.df.columns:
            self.df["phone_number"] = self.df["phone_number"].astype(str).apply(
                lambda x: re.sub(r"[^\d+]", "", x) if re.match(r"^\+?\d{10,15}$", x) else None
            )
    
    def validate_emails(self):
        """Memvalidasi email menggunakan regex."""
        if "email" in self.df.columns:
            email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            self.df["email_valid"] = self.df["email"].apply(lambda x: bool(email_pattern.match(str(x))) if pd.notna(x) else False)
    
    def add_trip_duration(self):
        pickup_col = "lpep_pickup_datetime" if "lpep_pickup_datetime" in self.df.columns else "pickup_datetime"
        dropoff_col = "lpep_dropoff_datetime" if "lpep_dropoff_datetime" in self.df.columns else "dropoff_datetime"

        if pickup_col in self.df.columns and dropoff_col in self.df.columns:
            self.df["trip_duration"] = (pd.to_datetime(self.df[dropoff_col]) - 
                                        pd.to_datetime(self.df[pickup_col])).dt.total_seconds() / 60
    
    def convert_distance(self):
        if "trip_distance" in self.df.columns:
            self.df["trip_distance_km"] = self.df["trip_distance"] * 1.60934
    
    def map_payment_type(self):
        if "payment_type" in self.df.columns:
            payment_mapping = {1: "Credit Card", 2: "Cash", 3: "No Charge", 4: "Dispute", 5: "Unknown", 6: "Voided Trip"}
            self.df["payment_type"] = self.df["payment_type"].map(payment_mapping)
    
    def transform(self):
        print("Starting transformation...")
        self.normalize_columns()
        self.clean_phone_numbers()
        self.validate_emails()
        self.add_trip_duration()
        self.convert_distance()
        self.map_payment_type()
        print("Transformation completed.")
        return self.df


class Load:
    """Kelas untuk menyimpan hasil akhir data"""
    def __init__(self, df, output_dir="result"):
        self.df = df
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def save_to_csv(self, file_name):
        output_path = os.path.join(self.output_dir, file_name)
        self.df.to_csv(output_path, index=False)
        print(f"Saved to CSV: {output_path}")
    
    def save_to_excel(self, file_name):
        output_path = os.path.join(self.output_dir, file_name)
        self.df.to_excel(output_path, index=False)
        print(f"Saved to Excel: {output_path}")


def main():
    extractor = Extract(data_dir="/Users/wartadi/purwadhika/module_01/taxi-pipeline/data")
    all_data = None
    transformed_data = None

    while True:
        print("\n=== MENU ===")
        print("1. Extract Data")
        print("2. Transform Data")
        print("3. Load Data")
        print("0. Kembali ke Menu")
        print("4. Exit")
        pilihan = input("Masukkan pilihan: ")

        if pilihan == "1":
            print("\n--- Extracting Data ---")
            csv_data = extractor.extract_csv()
            json_data = extractor.extract_json()

            if csv_data is not None and json_data is not None:
                all_data = pd.concat([csv_data, json_data], ignore_index=True)
            elif csv_data is not None:
                all_data = csv_data
            elif json_data is not None:
                all_data = json_data
            else:
                print("Tidak ada data yang ditemukan!")

            if all_data is not None:
                extractor.save_to_staging(all_data, "staging_combined_data.csv")

        elif pilihan == "2":
            if all_data is None:
                print("Harap lakukan extract terlebih dahulu!")
                continue

            print("\n--- Transforming Data ---")
            transformer = Transform(all_data)
            transformed_data = transformer.transform()

        elif pilihan == "3":
            if transformed_data is None:
                print("Harap lakukan transform terlebih dahulu!")
                continue

            print("\n--- Loading Data ---")
            loader = Load(transformed_data)
            loader.save_to_csv("final_combined_data.csv")
            loader.save_to_excel("final_combined_data.xlsx")

        elif pilihan == "4":
            print("Keluar dari program...")
            break

if __name__ == "__main__":
    main()
