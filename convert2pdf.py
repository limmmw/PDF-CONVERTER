#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║          KONVERTER FILE KE PDF - Linux Terminal      ║
║   Mendukung: Gambar (JPG/PNG/BMP/GIF), DOCX, XLSX   ║
╚══════════════════════════════════════════════════════╝
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path

# ── Warna terminal ──────────────────────────────────────
class Warna:
    MERAH    = "\033[91m"
    HIJAU    = "\033[92m"
    KUNING   = "\033[93m"
    BIRU     = "\033[94m"
    MAGENTA  = "\033[95m"
    CYAN     = "\033[96m"
    BOLD     = "\033[1m"
    RESET    = "\033[0m"

def cetak_header():
    print(f"""
{Warna.CYAN}{Warna.BOLD}╔══════════════════════════════════════════════════════╗
║          KONVERTER FILE KE PDF - Linux Terminal      ║
║   Mendukung: Gambar (JPG/PNG/BMP/GIF), DOCX, XLSX   ║
╚══════════════════════════════════════════════════════╝{Warna.RESET}
""")

def ok(pesan):
    print(f"  {Warna.HIJAU}✔{Warna.RESET}  {pesan}")

def err(pesan):
    print(f"  {Warna.MERAH}✘{Warna.RESET}  {pesan}")

def info(pesan):
    print(f"  {Warna.BIRU}➜{Warna.RESET}  {pesan}")

def warn(pesan):
    print(f"  {Warna.KUNING}⚠{Warna.RESET}  {pesan}")

# ── Deteksi dependencies ─────────────────────────────────
def cek_dependensi():
    """Cek dan pasang dependensi yang dibutuhkan."""
    print(f"\n{Warna.BOLD}[1/3] Mengecek dependensi...{Warna.RESET}")
    
    # Cek sistem tools
    tools_sistem = {
        "libreoffice": "LibreOffice (konversi DOCX/XLSX)",
        "convert"    : "ImageMagick (konversi gambar)",
    }
    
    semua_ok = True
    for tool, nama in tools_sistem.items():
        if shutil.which(tool):
            ok(f"{nama} — ditemukan")
        else:
            warn(f"{nama} — TIDAK ditemukan")
            if tool == "libreoffice":
                info("Install: sudo apt install libreoffice")
            elif tool == "convert":
                info("Install: sudo apt install imagemagick")
            semua_ok = False

    # Cek python packages
    paket_python = ["PIL", "reportlab"]
    for paket in paket_python:
        try:
            __import__(paket if paket != "PIL" else "PIL.Image")
            ok(f"Python: {paket} — ditemukan")
        except ImportError:
            warn(f"Python: {paket} — TIDAK ditemukan")
            nama_install = "Pillow" if paket == "PIL" else paket
            info(f"Install: pip install {nama_install}")
            semua_ok = False

    if not semua_ok:
        print(f"\n{Warna.KUNING}⚠  Beberapa dependensi belum terpasang.{Warna.RESET}")
        print(f"   Jalankan: {Warna.BOLD}bash install_deps.sh{Warna.RESET} untuk instalasi otomatis.\n")
    else:
        ok("Semua dependensi siap!")

    return semua_ok


# ── Konversi Gambar → PDF ─────────────────────────────────
def konversi_gambar(input_path: Path, output_path: Path) -> bool:
    """Konversi file gambar (JPG, PNG, BMP, GIF, WEBP, TIFF) ke PDF."""
    try:
        from PIL import Image
        
        img = Image.open(input_path)
        
        # Konversi ke RGB jika perlu (PDF tidak mendukung RGBA/P)
        if img.mode in ("RGBA", "P", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            if img.mode in ("RGBA", "LA"):
                background.paste(img, mask=img.split()[-1])
            else:
                background.paste(img)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        img.save(str(output_path), "PDF", resolution=150)
        return True

    except Exception as e:
        err(f"Gagal konversi gambar: {e}")
        return False


# ── Konversi DOCX → PDF ───────────────────────────────────
def konversi_docx(input_path: Path, output_path: Path) -> bool:
    """Konversi file Word (.docx/.doc) ke PDF menggunakan LibreOffice."""
    if not shutil.which("libreoffice"):
        err("LibreOffice tidak ditemukan. Install: sudo apt install libreoffice")
        return False
    
    try:
        output_dir = output_path.parent
        hasil = subprocess.run(
            [
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", str(output_dir),
                str(input_path)
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # LibreOffice menghasilkan nama file otomatis, rename jika perlu
        generated = output_dir / (input_path.stem + ".pdf")
        if generated.exists() and generated != output_path:
            generated.rename(output_path)
        
        if hasil.returncode == 0 and output_path.exists():
            return True
        else:
            err(f"LibreOffice error: {hasil.stderr.strip()}")
            return False

    except subprocess.TimeoutExpired:
        err("Konversi DOCX timeout (>60 detik)")
        return False
    except Exception as e:
        err(f"Gagal konversi DOCX: {e}")
        return False


# ── Konversi XLSX → PDF ───────────────────────────────────
def konversi_xlsx(input_path: Path, output_path: Path) -> bool:
    """Konversi file Excel (.xlsx/.xls/.ods) ke PDF menggunakan LibreOffice."""
    if not shutil.which("libreoffice"):
        err("LibreOffice tidak ditemukan. Install: sudo apt install libreoffice")
        return False
    
    try:
        output_dir = output_path.parent
        hasil = subprocess.run(
            [
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", str(output_dir),
                str(input_path)
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        generated = output_dir / (input_path.stem + ".pdf")
        if generated.exists() and generated != output_path:
            generated.rename(output_path)
        
        if hasil.returncode == 0 and output_path.exists():
            return True
        else:
            err(f"LibreOffice error: {hasil.stderr.strip()}")
            return False

    except subprocess.TimeoutExpired:
        err("Konversi XLSX timeout (>60 detik)")
        return False
    except Exception as e:
        err(f"Gagal konversi XLSX: {e}")
        return False


# ── Router format ─────────────────────────────────────────
FORMAT_GAMBAR = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff", ".tif"}
FORMAT_DOCX   = {".docx", ".doc", ".odt", ".rtf"}
FORMAT_XLSX   = {".xlsx", ".xls", ".ods", ".csv"}

def konversi_file(input_path: Path, output_dir: Path) -> bool:
    """Tentukan tipe file dan jalankan konversi yang sesuai."""
    ekstensi = input_path.suffix.lower()
    nama_output = input_path.stem + ".pdf"
    output_path = output_dir / nama_output

    print(f"\n  {Warna.BOLD}{input_path.name}{Warna.RESET}  →  {Warna.CYAN}{nama_output}{Warna.RESET}")

    if ekstensi in FORMAT_GAMBAR:
        info(f"Tipe: Gambar ({ekstensi})")
        berhasil = konversi_gambar(input_path, output_path)
    elif ekstensi in FORMAT_DOCX:
        info(f"Tipe: Word / Dokumen ({ekstensi})")
        berhasil = konversi_docx(input_path, output_path)
    elif ekstensi in FORMAT_XLSX:
        info(f"Tipe: Excel / Spreadsheet ({ekstensi})")
        berhasil = konversi_xlsx(input_path, output_path)
    else:
        err(f"Format '{ekstensi}' tidak didukung.")
        return False

    if berhasil:
        ukuran = output_path.stat().st_size / 1024
        ok(f"Tersimpan → {output_path}  ({ukuran:.1f} KB)")
    return berhasil


# ── Mode batch (folder) ───────────────────────────────────
def konversi_folder(input_dir: Path, output_dir: Path, rekursif: bool = False):
    """Konversi semua file yang didukung dalam sebuah folder."""
    semua_format = FORMAT_GAMBAR | FORMAT_DOCX | FORMAT_XLSX
    
    if rekursif:
        files = [f for f in input_dir.rglob("*") if f.is_file() and f.suffix.lower() in semua_format]
    else:
        files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in semua_format]

    if not files:
        warn(f"Tidak ada file yang didukung di '{input_dir}'")
        return

    print(f"\n{Warna.BOLD}[2/3] Memproses {len(files)} file...{Warna.RESET}")

    berhasil = 0
    gagal    = 0

    for f in sorted(files):
        # Jaga struktur subfolder jika rekursif
        if rekursif:
            rel = f.relative_to(input_dir).parent
            tujuan = output_dir / rel
        else:
            tujuan = output_dir
        tujuan.mkdir(parents=True, exist_ok=True)

        if konversi_file(f, tujuan):
            berhasil += 1
        else:
            gagal += 1

    print(f"\n{Warna.BOLD}[3/3] Selesai{Warna.RESET}")
    print(f"  {Warna.HIJAU}✔  Berhasil : {berhasil}{Warna.RESET}")
    if gagal:
        print(f"  {Warna.MERAH}✘  Gagal    : {gagal}{Warna.RESET}")
    print(f"  {Warna.CYAN}📁 Output  : {output_dir}{Warna.RESET}\n")


# ── CLI ───────────────────────────────────────────────────
def main():
    cetak_header()

    parser = argparse.ArgumentParser(
        description="Konverter file gambar/Word/Excel ke PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python3 convert_to_pdf.py foto.jpg
  python3 convert_to_pdf.py laporan.docx -o ~/Dokumen/PDF
  python3 convert_to_pdf.py data.xlsx neraca.xlsx -o ./output
  python3 convert_to_pdf.py ./folder_input -o ./folder_output --rekursif
  python3 convert_to_pdf.py --cek-deps
        """
    )

    parser.add_argument(
        "input",
        nargs="*",
        help="File atau folder yang akan dikonversi"
    )
    parser.add_argument(
        "-o", "--output",
        default="./pdf_output",
        metavar="FOLDER",
        help="Folder tujuan output PDF (default: ./pdf_output)"
    )
    parser.add_argument(
        "-r", "--rekursif",
        action="store_true",
        help="Proses subfolder secara rekursif (mode folder)"
    )
    parser.add_argument(
        "--cek-deps",
        action="store_true",
        help="Hanya cek dependensi, tidak konversi"
    )

    args = parser.parse_args()

    # Mode cek dependensi saja
    if args.cek_deps:
        cek_dependensi()
        return

    if not args.input:
        parser.print_help()
        sys.exit(1)

    # Cek dependensi sebelum mulai
    cek_dependensi()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{Warna.BOLD}[2/3] Memproses input...{Warna.RESET}")

    berhasil = 0
    gagal    = 0

    for arg in args.input:
        path = Path(arg)

        if not path.exists():
            err(f"Tidak ditemukan: {arg}")
            gagal += 1
            continue

        if path.is_dir():
            # Mode folder
            konversi_folder(path, output_dir, args.rekursif)
            return  # konversi_folder sudah print ringkasan sendiri
        else:
            # Mode file tunggal / beberapa file
            if konversi_file(path, output_dir):
                berhasil += 1
            else:
                gagal += 1

    print(f"\n{Warna.BOLD}[3/3] Selesai{Warna.RESET}")
    print(f"  {Warna.HIJAU}✔  Berhasil : {berhasil}{Warna.RESET}")
    if gagal:
        print(f"  {Warna.MERAH}✘  Gagal    : {gagal}{Warna.RESET}")
    print(f"  {Warna.CYAN}📁 Output  : {output_dir.resolve()}{Warna.RESET}\n")


if __name__ == "__main__":
    main()