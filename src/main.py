import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.extract import Extract
from src.transform import Transform
from src.load import Load

def main():
    extractor = Extract(data_dir="data")
    all_data = None
    transformed_data = None

    while True:
        print("\n" + "=" * 40)
        print("|   APLIKASI GREEN TAXI PIPELINE DATA  |")
        print("|               FOR MR FIN             |")
        print("=" * 40)
        print("|  1. Extract Data                     |")
        print("|  2. Transform Data                   |")
        print("|  3. Load Data                        |")
        print("|  4. Exit                             |")
        print("=" * 40)

        pilihan = input("Masukkan pilihan: ")

        if pilihan == "1":
            print("\n--- Extract Data ---")
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

            print("\n--- Transform Data ---")
            transformer = Transform(all_data)
            transformed_data = transformer.transform()

        elif pilihan == "3":
            if transformed_data is None:
                print("Harap lakukan transform terlebih dahulu!")
                continue

            print("\n--- Load Data ---")
            loader = Load(transformed_data)
            loader.save_to_csv("final_combined_data.csv")
            loader.save_to_excel("final_combined_data.xlsx")

        elif pilihan == "4":
            print("Keluar dari program...")
            break

if __name__ == "__main__":
    main()
