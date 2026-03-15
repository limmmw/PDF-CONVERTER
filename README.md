# 📄 Konverter File ke PDF — Linux Terminal

Program Python untuk mengonversi file **Gambar**, **Word**, dan **Excel** ke PDF langsung dari terminal Linux.

---

## Format yang Didukung

| Tipe       | Format                                      |
|------------|---------------------------------------------|
| 🖼 Gambar  | `.jpg` `.jpeg` `.png` `.bmp` `.gif` `.webp` `.tiff` |
| 📝 Word    | `.docx` `.doc` `.odt` `.rtf`               |
| 📊 Excel   | `.xlsx` `.xls` `.ods` `.csv`               |

---

## Instalasi Dependensi

```bash
bash install_deps.sh
```

Atau manual:
```bash
sudo apt install libreoffice imagemagick python3-pip
pip3 install Pillow reportlab
```

---

## Cara Penggunaan

### Konversi 1 file
```bash
python3 convert_to_pdf.py foto.jpg
python3 convert_to_pdf.py laporan.docx
python3 convert_to_pdf.py data.xlsx
```

### Tentukan folder output
```bash
python3 convert_to_pdf.py laporan.docx -o ~/Dokumen/PDF
```

### Konversi beberapa file sekaligus
```bash
python3 convert_to_pdf.py foto.jpg laporan.docx data.xlsx -o ./output
```

### Konversi seluruh isi folder
```bash
python3 convert_to_pdf.py ./folder_input -o ./folder_output
```

### Konversi folder + subfolder (rekursif)
```bash
python3 convert_to_pdf.py ./folder_input -o ./folder_output --rekursif
```

### Cek dependensi saja
```bash
python3 convert_to_pdf.py --cek-deps
```

---

## Opsi Lengkap

```
positional arguments:
  input               File atau folder yang akan dikonversi

options:
  -o, --output DIR    Folder tujuan PDF (default: ./pdf_output)
  -r, --rekursif      Proses subfolder secara rekursif
  --cek-deps          Hanya cek dependensi
  -h, --help          Tampilkan bantuan
```

---

## Cara Kerja

| Format   | Engine yang digunakan |
|----------|-----------------------|
| Gambar   | Python **Pillow** (tanpa dependensi eksternal) |
| DOCX/DOC | **LibreOffice** `--headless` |
| XLSX/XLS | **LibreOffice** `--headless` |

---

## Contoh Output Terminal

```
╔══════════════════════════════════════════════════════╗
║          KONVERTER FILE KE PDF - Linux Terminal      ║
╚══════════════════════════════════════════════════════╝

[1/3] Mengecek dependensi...
  ✔  LibreOffice — ditemukan
  ✔  ImageMagick — ditemukan
  ✔  Python: PIL — ditemukan

[2/3] Memproses input...

  foto.png  →  foto.pdf
  ➜  Tipe: Gambar (.png)
  ✔  Tersimpan → ./pdf_output/foto.pdf  (142.3 KB)

  laporan.docx  →  laporan.pdf
  ➜  Tipe: Word / Dokumen (.docx)
  ✔  Tersimpan → ./pdf_output/laporan.pdf  (89.7 KB)

[3/3] Selesai
  ✔  Berhasil : 2
  📁 Output  : /home/user/pdf_output
```