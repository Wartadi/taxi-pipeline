import pandas as pd
import re

class Transform:
    """Kelas untuk transformasi data dengan validasi dan regex"""
    
    def __init__(self, df):
        self.df = df.copy()
    
    def normalize_columns(self):
        """Normalisasi nama kolom agar sesuai dengan konvensi penamaan"""
        self.df.columns = [re.sub(r"\W+", "_", col.lower().strip()) for col in self.df.columns]
        rename_mapping = {
            "vendorid": "vendor_id",
            "ratecodeid": "rate_code_id",
            "pulocationid": "pu_location_id",
            "dolocationid": "do_location_id"
        }
        self.df.rename(columns=rename_mapping, inplace=True)
    
    def clean_phone_numbers(self):
        """Membersihkan nomor telepon agar hanya berisi angka dan '+' jika valid"""
        if "phone_number" in self.df.columns:
            self.df["phone_number"] = self.df["phone_number"].astype(str).apply(
                lambda x: re.sub(r"[^\d+]", "", x) if re.match(r"^\+?\d{10,15}$", x) else None
            )
    
    def validate_emails(self):
        """Menambahkan kolom validasi email berdasarkan pola regex"""
        if "email" in self.df.columns:
            email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            self.df["email_valid"] = self.df["email"].apply(lambda x: bool(email_pattern.match(str(x))) if pd.notna(x) else False)
    
    def add_trip_duration(self):
        """Menghitung durasi perjalanan dalam menit"""
        pickup_col = "lpep_pickup_datetime" if "lpep_pickup_datetime" in self.df.columns else "pickup_datetime"
        dropoff_col = "lpep_dropoff_datetime" if "lpep_dropoff_datetime" in self.df.columns else "dropoff_datetime"

        if pickup_col in self.df.columns and dropoff_col in self.df.columns:
            self.df["trip_duration"] = (pd.to_datetime(self.df[dropoff_col]) - 
                                        pd.to_datetime(self.df[pickup_col])).dt.total_seconds() / 60
    
    def convert_distance(self):
        """Mengonversi jarak perjalanan dari mil ke kilometer"""
        if "trip_distance" in self.df.columns:
            self.df["trip_distance_km"] = self.df["trip_distance"] * 1.60934
    
    def map_payment_type(self):
        """Memetakan kode pembayaran menjadi kategori deskriptif"""
        if "payment_type" in self.df.columns:
            payment_mapping = {
                1: "Credit Card",
                2: "Cash",
                3: "No Charge",
                4: "Dispute",
                5: "Unknown",
                6: "Voided Trip"
            }
            self.df["payment_type"] = self.df["payment_type"].map(payment_mapping)

    def fill_missing_values(self):
        """Mengganti nilai null dalam dataset dengan angka 0.0"""
        self.df = self.df.fillna(0.0)  # Semua nilai NaN diganti dengan 0.0
    
    def show_data_info(self, title):
        """Menampilkan info data: nama kolom, 5 data pertama, 5 data terakhir"""
        print(f"\n🔹 {title}")
        print("📌 Nama Kolom:", list(self.df.columns))
        print("\n🖥️ 5 Data Teratas:")
        print(self.df.head())
        print("\n📉 5 Data Terakhir:")
        print(self.df.tail())

    def transform(self):
        """Menjalankan transformasi data dan menampilkan hasil sebelum & sesudah"""
        print("🚀 Starting transformation...")
        
        # Menampilkan data sebelum transformasi
        self.show_data_info(f"Data Sebelum Transformasi")
        
        # Proses transformasi
        self.normalize_columns()
        self.clean_phone_numbers()
        self.validate_emails()
        self.add_trip_duration()
        self.convert_distance()
        self.map_payment_type()
        self.fill_missing_values()  # Mengganti nilai null dengan angka 0.0

        # Menentukan kolom pickup datetime untuk pengurutan
        pickup_col = "lpep_pickup_datetime" if "lpep_pickup_datetime" in self.df.columns else "pickup_datetime"
        if pickup_col in self.df.columns:
            self.df = self.df.sort_values(by=pickup_col, ascending=True)

        print("✅ Transformation completed.")
        
        # Menampilkan data setelah transformasi
        self.show_data_info("Data Setelah Transformasi")

        return self.df
