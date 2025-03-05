import os
import pandas as pd

class Load:
    """Kelas untuk menyimpan hasil akhir data"""
    def __init__(self, df, output_dir="result"):
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def get_file_info(self, file_path):
        """Menampilkan jumlah baris, kolom, dan ukuran file"""
        num_rows, num_cols = self.df.shape
        file_size = os.path.getsize(file_path) / 1024  # Konversi ke KB
        
        print(f"✅ Data saved successfully!")
        print(f"📂 File: {file_path}")
        print(f"📊 Rows: {num_rows}, Columns: {num_cols}")
        print(f"💾 File Size: {file_size:.2f} KB")
    
    def save_to_csv(self, file_name):
        """Menyimpan data ke CSV"""
        output_path = os.path.join(self.output_dir, file_name)
        self.df.to_csv(output_path, index=False)
        self.get_file_info(output_path)  # Menampilkan info file
        self.show_statistics()
    
    def save_to_excel(self, file_name):
        """Menyimpan data ke Excel"""
        output_path = os.path.join(self.output_dir, file_name)
        self.df.to_excel(output_path, index=False)
        self.get_file_info(output_path)  # Menampilkan info file
        self.show_statistics()
    
    def show_statistics(self):
        """Menampilkan informasi bahwa tidak ada data null serta statistik total_amount dan rentang tanggal"""
        total_nulls = self.df.isnull().sum().sum()
        if total_nulls == 0:
            print("\n✅ Data yang sudah terload tidak mengandung data null!")
            if "total_amount" in self.df.columns:
                print(f"➡️ Total Amount: {self.df['total_amount'].sum():.2f}")
            else:
                print("⚠️ Kolom total_amount tidak ditemukan dalam dataset!")
            
            if "lpep_pickup_datetime" in self.df.columns:
                self.df["lpep_pickup_datetime"] = pd.to_datetime(self.df["lpep_pickup_datetime"], errors='coerce')
                min_date = self.df["lpep_pickup_datetime"].min().date()
                max_date = self.df["lpep_pickup_datetime"].max().date()
                print(f"📅 Data tersedia dari {min_date} sampai {max_date}\n")
            else:
                print("⚠️ Kolom lpep_pickup_datetime tidak ditemukan dalam dataset!")
        else:
            print(f"⚠️ Dataset masih mengandung {total_nulls} nilai null!")
