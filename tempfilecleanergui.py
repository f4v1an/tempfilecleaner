import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import psutil  # Sistem bilgisi için kullanılıyor

# Eksik kütüphaneleri otomatik yükleme
def paket_kontrol_ve_yukle(paket_adi):
    try:
        __import__(paket_adi)
    except ImportError:
        print(f"{paket_adi} bulunamadı. Yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", paket_adi])
        print(f"{paket_adi} başarıyla yüklendi.")

# Gerekli kütüphaneleri kontrol et
paket_kontrol_ve_yukle("psutil")

# Dosyaları temizleme fonksiyonu
def temizle(klasor):
    try:
        if os.path.exists(klasor):
            for dosya in os.listdir(klasor):
                dosya_yolu = os.path.join(klasor, dosya)
                try:
                    if os.path.isfile(dosya_yolu) or os.path.islink(dosya_yolu):
                        os.unlink(dosya_yolu)  # Dosyayı sil
                    elif os.path.isdir(dosya_yolu):
                        shutil.rmtree(dosya_yolu)  # Alt klasörleri sil
                except Exception as e:
                    print(f"Dosya atlandı: {dosya_yolu} - {e}")
            print(f"{klasor} temizlendi.")
        else:
            print(f"{klasor} bulunamadı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

# Temizlik işlemi başlatıcı
def temizlik_islemi():
    temp_klasor = os.getenv('TEMP')  # %temp%
    prefetch_klasor = r"C:\Windows\Prefetch"
    local_temp_klasor = os.path.join(os.getenv('USERPROFILE'), "AppData", "Local", "Temp")  # temp

    temizle(temp_klasor)
    temizle(prefetch_klasor)
    temizle(local_temp_klasor)
    messagebox.showinfo("İşlem Tamamlandı", "Geçici dosyalar temizlendi!")

# Anlık sistem bilgisi güncelleme
def sistem_kontrolu_guncelle():
    # Disk kullanımı
    disk_kullanimi = psutil.disk_usage('/')
    toplam_disk = disk_kullanimi.total // (1024 ** 3)  # GB
    kullanilan_disk = disk_kullanimi.used // (1024 ** 3)  # GB
    bos_disk = disk_kullanimi.free // (1024 ** 3)  # GB
    disk_yuzde = disk_kullanimi.percent

    # RAM kullanımı
    ram_kullanimi = psutil.virtual_memory()
    toplam_ram = ram_kullanimi.total // (1024 ** 3)  # GB
    kullanilan_ram = ram_kullanimi.used // (1024 ** 3)  # GB
    bos_ram = ram_kullanimi.available // (1024 ** 3)  # GB
    ram_yuzde = ram_kullanimi.percent

    # Bilgileri arayüzde göster
    sistem_bilgisi.set(
        f"Disk Kullanımı: {kullanilan_disk}GB/{toplam_disk}GB ({disk_yuzde}%) boş: {bos_disk}GB\n"
        f"RAM Kullanımı: {kullanilan_ram}GB/{toplam_ram}GB ({ram_yuzde}%) boş: {bos_ram}GB"
    )

    # 1 saniye sonra tekrar çalıştır
    pencere.after(1, sistem_kontrolu_guncelle)

# Arayüz
def arayuz_olustur():
    global pencere, sistem_bilgisi
    pencere = tk.Tk()
    pencere.title("Geçici Dosya Temizleyici ve Sistem Kontrolü")
    pencere.geometry("500x300")

    baslik = tk.Label(pencere, text="Geçici Dosya Temizleyici ve Anlık Sistem Kontrolü", font=("Arial", 14))
    baslik.pack(pady=10)

    bilgi = tk.Label(pencere, text="Bu araç, temp, prefetch ve %temp% klasörlerini temizler.\nAyrıca anlık sistem bilgilerini gösterir.", wraplength=450, justify="center")
    bilgi.pack(pady=10)

    temizle_butonu = tk.Button(pencere, text="Temizliği Başlat", command=temizlik_islemi, bg="green", fg="white", font=("Arial", 12))
    temizle_butonu.pack(pady=10)

    # Sistem bilgisi bölümü
    sistem_bilgisi = tk.StringVar()
    sistem_bilgisi.set("Anlık sistem bilgileri alınıyor...")
    sistem_bilgi_etiketi = tk.Label(pencere, textvariable=sistem_bilgisi, font=("Arial", 10), justify="center", wraplength=450)
    sistem_bilgi_etiketi.pack(pady=10)

    pencere.after(1, sistem_kontrolu_guncelle)  # 1 saniye sonra sistem kontrolünü başlat
    pencere.mainloop()

# Programı başlat
if __name__ == "__main__":
    arayuz_olustur()
