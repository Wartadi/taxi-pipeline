
### Langkah-langkah Menjalankan Proyek

1.  **Buat Virtual Environment**: Dari root proyek, jalankan perintah berikut untuk membuat virtual environment:
    
    
    ```bash
    python3 -m venv venv
    
    ```
    
2.  **Aktifkan Virtual Environment**: Setelah virtual environment dibuat, aktifkan dengan perintah:
        
    ```bash
    source ./venv/bin/activate
    
    ```
    
3.  **Instal Dependensi**: Pastikan Anda memiliki file  `requirements.txt`  yang berisi semua dependensi yang diperlukan. Instal dependensi dengan perintah:
        
    ```bash
    pip install -r requirements.txt
    
    ```
    
4.  **Jalankan Program**: Setelah semua dependensi terinstal, jalankan program utama dengan perintah:
        
    ```bash
    python src/main.py
    
    ```
    
5.  **Menu Interaktif**: Setelah menjalankan program, Anda akan melihat menu interaktif di konsol. Menu ini akan terlihat seperti ini:
    
    `=== MENU === 
    1. Extract Data
    2.  Transform Data
    3. Load Data
    4. Exit` 
    
6.  **Pilih Opsi**:
    -   **Pilih 1**  untuk mengekstrak data. Program akan meminta Anda untuk memilih sumber data (CSV atau JSON) dan mengekstrak data dari folder yang sesuai.
    -   **Pilih 2**  untuk mentransformasi data yang telah diekstrak. Program akan melakukan berbagai transformasi yang telah Anda definisikan.
    -   **Pilih 3**  untuk memuat data yang telah ditransformasi ke dalam format yang diinginkan (CSV atau Excel).
    -   **Pilih 4**  untuk keluar dari program.