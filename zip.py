import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import threading

class ZipArchiver:
    def __init__(self, root):
        self.root = root
        self.root.title("Dosya Arşivleme ve Çıkarma Aracı")
        
        # Arayüz elemanları
        self.create_widgets()

    def create_widgets(self):
        # Ayıklamayı Başlat Butonu
        self.extract_button = tk.Button(self.root, text="Ayıklamayı Başlat", command=self.extract_file)
        self.extract_button.grid(row=0, column=0, padx=10, pady=10)

        # Arşivlemeyi Başlat Butonu
        self.archive_button = tk.Button(self.root, text="Arşivlemeyi Başlat", command=self.archive_file)
        self.archive_button.grid(row=1, column=0, padx=10, pady=10)
        
        # Çıkarılacak dosya seçme butonu
        self.select_extract_file_button = tk.Button(self.root, text="Çıkarılacak Dosya Seç", command=self.select_extract_file)
        self.select_extract_file_button.grid(row=0, column=1, padx=10, pady=10)

        # Çıkarılacak yol seçme butonu
        self.select_extract_path_button = tk.Button(self.root, text="Çıkarılacak Yol Seç", command=self.select_extract_path)
        self.select_extract_path_button.grid(row=1, column=1, padx=10, pady=10)

        # Arşivlenecek klasörü seçme butonu
        self.select_folder_button = tk.Button(self.root, text="Arşivlenecek Klasörü Seç", command=self.select_folder)
        self.select_folder_button.grid(row=2, column=0, padx=10, pady=10)

        # İlerleme çubuğu
        self.progress = Progressbar(self.root, length=200, mode='determinate', maximum=100)
        self.progress.grid(row=3, column=0, columnspan=2, pady=20)

        # İlerleme çubuğunu güncelleyecek olan değişkenler
        self.extract_file_path = ""
        self.extract_to_path = ""
        self.folder_to_archive = ""
    
    def select_extract_file(self):
        """Çıkarılacak dosyayı seçme."""
        self.extract_file_path = filedialog.askopenfilename(title="Çıkarılacak Dosyayı Seç", filetypes=[("Zip Dosyaları", "*.zip")])
    
    def select_extract_path(self):
        """Çıkarılacak yolu seçme."""
        self.extract_to_path = filedialog.askdirectory(title="Çıkarılacak Yolu Seç")

    def select_folder(self):
        """Arşivlenecek klasörü seçme."""
        self.folder_to_archive = filedialog.askdirectory(title="Arşivlenecek Klasörü Seç")

    def extract_file(self):
        """Zip dosyasını çıkarma işlemi."""
        if not self.extract_file_path or not self.extract_to_path:
            messagebox.showerror("Hata", "Çıkarılacak dosya veya yol seçilmedi!")
            return

        # İlerleme çubuğunu sıfırla
        self.progress['value'] = 0
        self.root.update()

        # Zip dosyasını çıkar
        def extract_zip():
            try:
                with zipfile.ZipFile(self.extract_file_path, 'r') as zip_ref:
                    total_files = len(zip_ref.infolist())
                    for i, file in enumerate(zip_ref.infolist()):
                        zip_ref.extract(file, self.extract_to_path)
                        progress = (i + 1) / total_files * 100
                        self.progress['value'] = progress
                        self.root.update_idletasks()
                messagebox.showinfo("Başarılı", "Dosya başarıyla çıkarıldı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        
        # İşlemi ayrı bir thread'de çalıştır
        threading.Thread(target=extract_zip).start()

    def archive_file(self):
        """Klasörü zip'e arşivleme işlemi."""
        if not self.folder_to_archive:
            messagebox.showerror("Hata", "Arşivlenecek klasör seçilmedi!")
            return

        # İlerleme çubuğunu sıfırla
        self.progress['value'] = 0
        self.root.update()

        # Klasörü zip'e arşivle
        def create_zip():
            try:
                zip_name = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Zip Dosyası", "*.zip")])
                if zip_name:
                    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                        # Klasördeki tüm dosyaları zip dosyasına ekle
                        for foldername, subfolders, filenames in os.walk(self.folder_to_archive):
                            for filename in filenames:
                                file_path = os.path.join(foldername, filename)
                                zip_ref.write(file_path, os.path.relpath(file_path, self.folder_to_archive))
                    self.progress['value'] = 100
                    self.root.update_idletasks()
                    messagebox.showinfo("Başarılı", "Klasör başarıyla arşivlendi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {e}")
        
        # İşlemi ayrı bir thread'de çalıştır
        threading.Thread(target=create_zip).start()

# Tkinter GUI'sini başlat
root = tk.Tk()
app = ZipArchiver(root)
root.mainloop()
